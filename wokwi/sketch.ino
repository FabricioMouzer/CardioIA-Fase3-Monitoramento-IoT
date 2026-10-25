#include <Arduino.h>
#include <DHTesp.h>
#include <PubSubClient.h>
#include <WiFi.h>

#include "alert_logic.h"
#include "edge_buffer.h"
#include "mqtt_payload.h"

// CardioIA Fase 3 — Etapa 4. Dados exclusivamente sintéticos.
namespace Config {
constexpr uint8_t DHT_PIN = 15;
constexpr uint8_t BPM_PIN = 34;
constexpr uint8_t ALERT_LED_PIN = 2;
constexpr uint8_t CONNECTIVITY_BUTTON_PIN = 4;
constexpr uint32_t SAMPLE_INTERVAL_MS = 5000;
constexpr uint32_t BUTTON_DEBOUNCE_MS = 50;
constexpr uint32_t RECONNECT_INTERVAL_MS = 5000;
constexpr size_t OFFLINE_BUFFER_CAPACITY = 2160;
constexpr uint16_t BPM_MIN = 40;
constexpr uint16_t BPM_MAX = 180;

constexpr char WIFI_SSID[] = "Wokwi-GUEST";
constexpr char MQTT_HOST[] = "broker.hivemq.com";
constexpr uint16_t MQTT_PORT = 1883;
constexpr char MQTT_CLIENT_ID[] = "cardioia-rm566777-esp32-01";
constexpr char TOPIC_TELEMETRY[] =
    "cardioia/fase3/rm566777/cardioia-esp32-01/telemetria";
constexpr char TOPIC_ALERT[] =
    "cardioia/fase3/rm566777/cardioia-esp32-01/alerta";
constexpr char TOPIC_STATUS[] =
    "cardioia/fase3/rm566777/cardioia-esp32-01/status";
}  // namespace Config

struct Sample {
  uint32_t sequence;
  uint32_t capturedAtMs;
  float temperatureC;
  float humidityPct;
  uint16_t bpm;
  bool sensorValid;
  uint8_t alertCode;
};

static_assert(sizeof(Sample) == 20,
              "Revise a capacidade: o tamanho de Sample foi alterado");

DHTesp dht;
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
EdgeBuffer<Sample, Config::OFFLINE_BUFFER_CAPACITY> offlineBuffer;

uint32_t nextSequence = 1;
uint32_t lastSampleAt = 0;
uint32_t lastReconnectAttemptAt = 0;
uint32_t buttonChangedAt = 0;
bool forceDhtFailure = false;
bool networkEnabled = true;
bool lastButtonReading = HIGH;
bool stableButtonState = HIGH;

const char* primaryAlertLabel(uint8_t code) {
  if (code == ALERT_NONE) return "normal";
  if (code & ALERT_SENSOR_ERROR) return "sensor_error";
  if (code & ALERT_TEMP_HIGH) return "high_temperature";
  if (code & ALERT_BPM_HIGH) return "high_bpm";
  if (code & ALERT_BPM_LOW) return "low_bpm";
  return "unknown";
}

void publishStatus(const char* state, bool retained) {
  if (!mqttClient.connected()) return;
  char payload[256];
  const int length = formatStatusJson(
      payload, sizeof(payload), state, offlineBuffer.size(),
      offlineBuffer.dropped(), millis());
  const bool valid = length > 0 && static_cast<size_t>(length) < sizeof(payload);
  const bool accepted = valid &&
                        mqttClient.publish(Config::TOPIC_STATUS, payload, retained);
  Serial.printf("MQTT_STATUS state=%s retained=%s accepted=%s pending=%u\n",
                state, retained ? "true" : "false",
                accepted ? "true" : "false",
                static_cast<unsigned>(offlineBuffer.size()));
}

bool publishSample(const Sample& sample, const char* source,
                   size_t pendingAfterPublish) {
  if (!mqttClient.connected()) return false;
  const TelemetryPayloadInput input{
      sample.sequence,       sample.capturedAtMs, sample.temperatureC,
      sample.humidityPct,    sample.bpm,          sample.sensorValid,
      sample.alertCode,      primaryAlertLabel(sample.alertCode),
      source,                pendingAfterPublish, offlineBuffer.dropped()};
  char payload[512];
  const int length = formatTelemetryJson(payload, sizeof(payload), input);
  if (length <= 0 || static_cast<size_t>(length) >= sizeof(payload)) {
    Serial.printf("MQTT_ERROR seq=%lu reason=payload_overflow\n",
                  static_cast<unsigned long>(sample.sequence));
    return false;
  }
  const bool telemetryAccepted =
      mqttClient.publish(Config::TOPIC_TELEMETRY, payload, false);
  bool alertAccepted = true;
  if (sample.alertCode != ALERT_NONE) {
    alertAccepted = mqttClient.publish(Config::TOPIC_ALERT, payload, false);
  }
  const bool accepted = telemetryAccepted && alertAccepted;
  Serial.printf(
      "MQTT_PUBLISH seq=%lu source=%s telemetry=%s alert=%s accepted=%s "
      "pending_after=%u payload=%s\n",
      static_cast<unsigned long>(sample.sequence), source,
      telemetryAccepted ? "true" : "false",
      alertAccepted ? "true" : "false", accepted ? "true" : "false",
      static_cast<unsigned>(pendingAfterPublish), payload);
  return accepted;
}

void synchronizeBufferedSamples() {
  if (!mqttClient.connected() || offlineBuffer.empty()) return;
  Serial.printf("SYNC_START pending=%u dropped_samples=%lu\n",
                static_cast<unsigned>(offlineBuffer.size()),
                offlineBuffer.dropped());
  publishStatus("online_syncing", true);
  size_t sent = 0;
  Sample sample{};
  while (mqttClient.connected() && offlineBuffer.front(sample)) {
    const size_t pendingAfter = offlineBuffer.size() - 1;
    if (!publishSample(sample, "buffered", pendingAfter)) break;
    offlineBuffer.discardFront();
    ++sent;
    mqttClient.loop();
  }
  Serial.printf("SYNC_DONE sent=%u pending=%u dropped_samples=%lu\n",
                static_cast<unsigned>(sent),
                static_cast<unsigned>(offlineBuffer.size()),
                offlineBuffer.dropped());
  publishStatus(offlineBuffer.empty() ? "online" : "online_syncing", true);
}

void enqueueSample(const Sample& sample, const char* reason) {
  const bool overwritten = offlineBuffer.push(sample);
  Serial.printf(
      "BUFFER_STORE seq=%lu reason=%s pending=%u capacity=%u "
      "dropped_samples=%lu overwritten=%s\n",
      static_cast<unsigned long>(sample.sequence), reason,
      static_cast<unsigned>(offlineBuffer.size()),
      static_cast<unsigned>(offlineBuffer.capacity()), offlineBuffer.dropped(),
      overwritten ? "true" : "false");
}

void serviceNetwork() {
  if (!networkEnabled) return;
  if (WiFi.status() != WL_CONNECTED) {
    if (millis() - lastReconnectAttemptAt >= Config::RECONNECT_INTERVAL_MS) {
      lastReconnectAttemptAt = millis();
      Serial.println("WIFI_RECONNECT attempt=true");
      WiFi.begin(Config::WIFI_SSID, "", 6);
    }
    return;
  }
  if (!mqttClient.connected()) {
    if (millis() - lastReconnectAttemptAt < Config::RECONNECT_INTERVAL_MS) return;
    lastReconnectAttemptAt = millis();
    char willPayload[256];
    formatStatusJson(willPayload, sizeof(willPayload), "offline_unexpected",
                     offlineBuffer.size(), offlineBuffer.dropped(), millis());
    Serial.printf("MQTT_CONNECT host=%s port=%u\n", Config::MQTT_HOST,
                  Config::MQTT_PORT);
    const bool connected = mqttClient.connect(
        Config::MQTT_CLIENT_ID, Config::TOPIC_STATUS, 0, true, willPayload);
    Serial.printf("MQTT_CONNECT_RESULT connected=%s state=%d\n",
                  connected ? "true" : "false", mqttClient.state());
    if (connected) {
      publishStatus(offlineBuffer.empty() ? "online" : "online_syncing", true);
      synchronizeBufferedSamples();
    }
    return;
  }
  mqttClient.loop();
  synchronizeBufferedSamples();
}

void setNetworkEnabled(bool enabled, const char* source) {
  if (networkEnabled == enabled) return;
  networkEnabled = enabled;
  Serial.printf("CONNECTIVITY state=%s source=%s pending=%u\n",
                enabled ? "enabled" : "disabled", source,
                static_cast<unsigned>(offlineBuffer.size()));
  if (!enabled) {
    mqttClient.disconnect();
  } else {
    lastReconnectAttemptAt = millis() - Config::RECONNECT_INTERVAL_MS;
  }
}

void processTestCommands() {
  while (Serial.available() > 0) {
    const char command = static_cast<char>(Serial.read());
    if (command == 'F' || command == 'f') {
      forceDhtFailure = true;
      Serial.println("TEST dht_fault=on");
    } else if (command == 'R' || command == 'r') {
      forceDhtFailure = false;
      Serial.println("TEST dht_fault=off");
    } else if (command == 'O' || command == 'o') {
      setNetworkEnabled(false, "serial");
    } else if (command == 'N' || command == 'n') {
      setNetworkEnabled(true, "serial");
    }
  }
}

void processConnectivityButton() {
  const bool reading = digitalRead(Config::CONNECTIVITY_BUTTON_PIN);
  if (reading != lastButtonReading) {
    lastButtonReading = reading;
    buttonChangedAt = millis();
  }
  if (millis() - buttonChangedAt < Config::BUTTON_DEBOUNCE_MS) return;
  if (reading != stableButtonState) {
    stableButtonState = reading;
    if (stableButtonState == LOW) setNetworkEnabled(!networkEnabled, "button");
  }
}

Sample collectSample() {
  const TempAndHumidity reading = dht.getTempAndHumidity();
  const bool sensorValid = !forceDhtFailure && !isnan(reading.temperature) &&
                           !isnan(reading.humidity);
  const int rawBpm = constrain(analogRead(Config::BPM_PIN), 0, 4095);
  const uint16_t bpm = map(rawBpm, 0, 4095, Config::BPM_MIN, Config::BPM_MAX);
  Sample sample{};
  sample.sequence = nextSequence++;
  sample.capturedAtMs = millis();
  sample.temperatureC = sensorValid ? reading.temperature : -999.0F;
  sample.humidityPct = sensorValid ? reading.humidity : -1.0F;
  sample.bpm = bpm;
  sample.sensorValid = sensorValid;
  sample.alertCode = calculateAlert(reading.temperature, bpm, sensorValid);
  return sample;
}

void sampleAndRoute() {
  const Sample sample = collectSample();
  digitalWrite(Config::ALERT_LED_PIN,
               sample.alertCode == ALERT_NONE ? LOW : HIGH);
  Serial.printf(
      "SAMPLE seq=%lu uptime_ms=%lu temp=%.1fC humidity=%.1f%% bpm=%u "
      "sensor_valid=%s alert_code=%u alert=%s\n",
      static_cast<unsigned long>(sample.sequence),
      static_cast<unsigned long>(sample.capturedAtMs), sample.temperatureC,
      sample.humidityPct, sample.bpm, sample.sensorValid ? "true" : "false",
      sample.alertCode, primaryAlertLabel(sample.alertCode));
  if (!networkEnabled || !mqttClient.connected()) {
    enqueueSample(sample, !networkEnabled ? "network_disabled" : "mqtt_offline");
    return;
  }
  synchronizeBufferedSamples();
  if (!offlineBuffer.empty() || !publishSample(sample, "live", 0)) {
    enqueueSample(sample, "publish_failed");
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(Config::ALERT_LED_PIN, OUTPUT);
  pinMode(Config::CONNECTIVITY_BUTTON_PIN, INPUT_PULLUP);
  digitalWrite(Config::ALERT_LED_PIN, LOW);
  analogReadResolution(12);
  dht.setup(Config::DHT_PIN, DHTesp::DHT22);
  mqttClient.setServer(Config::MQTT_HOST, Config::MQTT_PORT);
  mqttClient.setBufferSize(512);
  WiFi.mode(WIFI_STA);
  WiFi.begin(Config::WIFI_SSID, "", 6);
  Serial.println("BOOT CardioIA Fase 3 Etapa 4 — MQTT sintético");
  Serial.printf("MQTT_TOPICS telemetry=%s alert=%s status=%s\n",
                Config::TOPIC_TELEMETRY, Config::TOPIC_ALERT,
                Config::TOPIC_STATUS);
  lastReconnectAttemptAt = millis() - Config::RECONNECT_INTERVAL_MS;
  sampleAndRoute();
  lastSampleAt = millis();
}

void loop() {
  processTestCommands();
  processConnectivityButton();
  serviceNetwork();
  if (millis() - lastSampleAt >= Config::SAMPLE_INTERVAL_MS) {
    lastSampleAt = millis();
    sampleAndRoute();
  }
  delay(10);
}
