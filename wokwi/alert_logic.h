#pragma once

#include <stdint.h>

namespace AlertThresholds {
constexpr uint16_t BPM_LOW = 50;
constexpr uint16_t BPM_HIGH = 120;
constexpr float TEMP_HIGH_C = 38.0F;
}  // namespace AlertThresholds

enum AlertCode : uint8_t {
  ALERT_NONE = 0,
  ALERT_BPM_LOW = 1 << 0,
  ALERT_BPM_HIGH = 1 << 1,
  ALERT_TEMP_HIGH = 1 << 2,
  ALERT_SENSOR_ERROR = 1 << 3,
};

inline uint8_t calculateAlert(float temperatureC, uint16_t bpm,
                              bool sensorValid) {
  uint8_t code = ALERT_NONE;
  if (!sensorValid) code |= ALERT_SENSOR_ERROR;
  if (sensorValid && temperatureC > AlertThresholds::TEMP_HIGH_C) {
    code |= ALERT_TEMP_HIGH;
  }
  if (bpm < AlertThresholds::BPM_LOW) code |= ALERT_BPM_LOW;
  if (bpm > AlertThresholds::BPM_HIGH) code |= ALERT_BPM_HIGH;
  return code;
}
