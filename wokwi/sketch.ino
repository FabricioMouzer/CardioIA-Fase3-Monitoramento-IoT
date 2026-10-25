#include <Arduino.h>
#include <DHTesp.h>

#include "alert_logic.h"
#include "edge_buffer.h"

// CardioIA Fase 3 — Etapa 3.
// Todos os valores são sintéticos e destinados exclusivamente a ensino.
namespace Config {
constexpr uint8_t DHT_PIN = 15;
constexpr uint8_t BPM_PIN = 34;
constexpr uint8_t ALERT_LED_PIN = 2;
constexpr uint8_t CONNECTIVITY_BUTTON_PIN = 4;
constexpr uint32_t SAMPLE_INTERVAL_MS = 5000;
constexpr uint32_t BUTTON_DEBOUNCE_MS = 50;
constexpr size_t OFFLINE_BUFFER_CAPACITY = 2160;

constexpr uint16_t BPM_MIN = 40;
constexpr uint16_t BPM_MAX = 180;
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
EdgeBuffer<Sample, Config::OFFLINE_BUFFER_CAPACITY> offlineBuffer;
uint32_t nextSequence = 1;
uint32_t lastSampleAt = 0;
uint32_t buttonChangedAt = 0;
bool forceDhtFailure = false;
bool connected = true;
bool lastButtonReading = HIGH;
bool stableButtonState = HIGH;

void sendToCloudSimulation(const Sample& sample, const char* source) {
  Serial.printf(
      "CLOUD_SEND seq=%lu source=%s uptime_ms=%lu temp=%.1fC humidity=%.1f%% "
      "bpm=%u alert_code=%u\n",
      static_cast<unsigned long>(sample.sequence), source,
      static_cast<unsigned long>(sample.capturedAtMs), sample.temperatureC,
      sample.humidityPct, sample.bpm, sample.alertCode);
}

void synchronizeBufferedSamples() {
  const size_t pendingBefore = offlineBuffer.size();
  if (pendingBefore == 0) return;

  Serial.printf("SYNC_START pending=%u dropped_samples=%lu\n",
                static_cast<unsigned>(pendingBefore), offlineBuffer.dropped());
  Sample buffered{};
  size_t sent = 0;
  while (offlineBuffer.pop(buffered)) {
    sendToCloudSimulation(buffered, "buffered");
    ++sent;
  }
  Serial.printf("SYNC_DONE sent=%u pending=%u dropped_samples=%lu\n",
                static_cast<unsigned>(sent),
                static_cast<unsigned>(offlineBuffer.size()),
                offlineBuffer.dropped());
}

void setConnectivity(bool newState, const char* source) {
  if (connected == newState) return;
  connected = newState;
  Serial.printf("CONNECTIVITY state=%s source=%s pending=%u\n",
                connected ? "online" : "offline", source,
                static_cast<unsigned>(offlineBuffer.size()));
  if (connected) synchronizeBufferedSamples();
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
      setConnectivity(false, "serial");
    } else if (command == 'N' || command == 'n') {
      setConnectivity(true, "serial");
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
    if (stableButtonState == LOW) setConnectivity(!connected, "button");
  }
}

const char* primaryAlertLabel(uint8_t code) {
  if (code == ALERT_NONE) return "normal";
  if (code & ALERT_SENSOR_ERROR) return "sensor_error";
  if (code & ALERT_TEMP_HIGH) return "high_temperature";
  if (code & ALERT_BPM_HIGH) return "high_bpm";
  if (code & ALERT_BPM_LOW) return "low_bpm";
  return "unknown";
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

void reportSample(const Sample& sample) {
  Serial.printf(
      "SAMPLE seq=%lu uptime_ms=%lu temp=%.1fC humidity=%.1f%% bpm=%u "
      "sensor_valid=%s alert_code=%u alert=%s\n",
      static_cast<unsigned long>(sample.sequence),
      static_cast<unsigned long>(sample.capturedAtMs), sample.temperatureC,
      sample.humidityPct, sample.bpm, sample.sensorValid ? "true" : "false",
      sample.alertCode, primaryAlertLabel(sample.alertCode));
}

void sampleAndReport() {
  const Sample sample = collectSample();
  digitalWrite(Config::ALERT_LED_PIN,
               sample.alertCode == ALERT_NONE ? LOW : HIGH);
  reportSample(sample);
  if (connected) {
    synchronizeBufferedSamples();
    sendToCloudSimulation(sample, "live");
  } else {
    const bool overwritten = offlineBuffer.push(sample);
    Serial.printf(
        "BUFFER_STORE seq=%lu pending=%u capacity=%u dropped_samples=%lu "
        "overwritten=%s\n",
        static_cast<unsigned long>(sample.sequence),
        static_cast<unsigned>(offlineBuffer.size()),
        static_cast<unsigned>(offlineBuffer.capacity()), offlineBuffer.dropped(),
        overwritten ? "true" : "false");
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(Config::ALERT_LED_PIN, OUTPUT);
  pinMode(Config::CONNECTIVITY_BUTTON_PIN, INPUT_PULLUP);
  digitalWrite(Config::ALERT_LED_PIN, LOW);
  analogReadResolution(12);
  dht.setup(Config::DHT_PIN, DHTesp::DHT22);

  Serial.println("BOOT CardioIA Fase 3 Etapa 3 — Edge offline sintético");
  Serial.println(
      "TEST commands: F=falha DHT22, R=recuperacao DHT22, "
      "O=offline, N=online");
  Serial.printf("EDGE_BUFFER capacity=%u interval_ms=%lu retention_hours=3\n",
                static_cast<unsigned>(offlineBuffer.capacity()),
                static_cast<unsigned long>(Config::SAMPLE_INTERVAL_MS));
  sampleAndReport();
  lastSampleAt = millis();
}

void loop() {
  processTestCommands();
  processConnectivityButton();
  if (millis() - lastSampleAt >= Config::SAMPLE_INTERVAL_MS) {
    lastSampleAt = millis();
    sampleAndReport();
  }
  delay(10);
}
