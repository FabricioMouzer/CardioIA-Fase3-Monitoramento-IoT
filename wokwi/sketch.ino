#include <Arduino.h>
#include <DHTesp.h>

#include "alert_logic.h"

// CardioIA Fase 3 — Etapa 2.
// Todos os valores são sintéticos e destinados exclusivamente a ensino.
namespace Config {
constexpr uint8_t DHT_PIN = 15;
constexpr uint8_t BPM_PIN = 34;
constexpr uint8_t ALERT_LED_PIN = 2;
constexpr uint32_t SAMPLE_INTERVAL_MS = 5000;

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

DHTesp dht;
uint32_t nextSequence = 1;
uint32_t lastSampleAt = 0;
bool forceDhtFailure = false;

void processTestCommands() {
  while (Serial.available() > 0) {
    const char command = static_cast<char>(Serial.read());
    if (command == 'F' || command == 'f') {
      forceDhtFailure = true;
      Serial.println("TEST dht_fault=on");
    } else if (command == 'R' || command == 'r') {
      forceDhtFailure = false;
      Serial.println("TEST dht_fault=off");
    }
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
}

void setup() {
  Serial.begin(115200);
  pinMode(Config::ALERT_LED_PIN, OUTPUT);
  digitalWrite(Config::ALERT_LED_PIN, LOW);
  analogReadResolution(12);
  dht.setup(Config::DHT_PIN, DHTesp::DHT22);

  Serial.println("BOOT CardioIA Fase 3 Etapa 2 — sensores sintéticos");
  Serial.println("TEST commands: F=falha DHT22, R=recuperacao DHT22");
  sampleAndReport();
  lastSampleAt = millis();
}

void loop() {
  processTestCommands();
  if (millis() - lastSampleAt >= Config::SAMPLE_INTERVAL_MS) {
    lastSampleAt = millis();
    sampleAndReport();
  }
  delay(10);
}
