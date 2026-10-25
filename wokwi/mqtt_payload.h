#pragma once

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

struct TelemetryPayloadInput {
  uint32_t sequence;
  uint32_t capturedAtMs;
  float temperatureC;
  float humidityPct;
  uint16_t bpm;
  bool sensorValid;
  uint8_t alertCode;
  const char* alert;
  const char* source;
  size_t bufferPending;
  unsigned long droppedSamples;
};

inline int formatTelemetryJson(char* output, size_t capacity,
                               const TelemetryPayloadInput& input) {
  return snprintf(
      output, capacity,
      R"json({"schema_version":1,"device_id":"cardioia-esp32-01","sequence":%lu,"captured_uptime_ms":%lu,"temperature_c":%.1f,"humidity_pct":%.1f,"bpm":%u,"sensor_valid":%s,"alert_code":%u,"alert":"%s","source":"%s","buffer_pending":%u,"dropped_samples":%lu})json",
      static_cast<unsigned long>(input.sequence),
      static_cast<unsigned long>(input.capturedAtMs), input.temperatureC,
      input.humidityPct, input.bpm, input.sensorValid ? "true" : "false",
      input.alertCode, input.alert, input.source,
      static_cast<unsigned>(input.bufferPending), input.droppedSamples);
}

inline int formatStatusJson(char* output, size_t capacity, const char* state,
                            size_t bufferPending,
                            unsigned long droppedSamples,
                            uint32_t uptimeMs) {
  return snprintf(
      output, capacity,
      R"json({"schema_version":1,"device_id":"cardioia-esp32-01","state":"%s","buffer_pending":%u,"dropped_samples":%lu,"uptime_ms":%lu})json",
      state, static_cast<unsigned>(bufferPending), droppedSamples,
      static_cast<unsigned long>(uptimeMs));
}
