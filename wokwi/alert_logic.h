#pragma once

#include <stdint.h>

// ============================================================================
// CardioIA Fase 3 — Regras de Classificação de Alertas no Edge (ESP32)
// ============================================================================
// Define os limites didáticos de monitoramento contínuo para triagem local:
// - Faixa normal de batimentos: 50 <= BPM <= 120 (limites inclusivos)
// - Temperatura normal: <= 38.0 °C (limite inclusivo)
// O processamento ocorre integralmente na borda (Edge Computing), permitindo
// acionamento imediato do LED físico e rotulagem mesmo sem conexão Wi-Fi/MQTT.
namespace AlertThresholds {
constexpr uint16_t BPM_LOW = 50;
constexpr uint16_t BPM_HIGH = 120;
constexpr float TEMP_HIGH_C = 38.0F;
}  // namespace AlertThresholds

// Máscara de bits (bitmask) para representar múltiplos alertas simultâneos:
// - Bit 0 (valor 1): Bradicardia sintética (BPM < 50)
// - Bit 1 (valor 2): Taquicardia sintética (BPM > 120)
// - Bit 2 (valor 4): Hipertermia / febre sintética (Temperatura > 38.0 °C)
// - Bit 3 (valor 8): Falha técnica de leitura do sensor DHT22 (NaN / timeout)
enum AlertCode : uint8_t {
  ALERT_NONE = 0,
  ALERT_BPM_LOW = 1 << 0,
  ALERT_BPM_HIGH = 1 << 1,
  ALERT_TEMP_HIGH = 1 << 2,
  ALERT_SENSOR_ERROR = 1 << 3,
};

// Avalia os sinais vitais capturados e retorna a máscara combinada (alert_code).
// Quando o DHT22 falha (!sensorValid), a regra térmica é suprimida para evitar
// falso positivo sobre o valor sentinela (-999.0 °C), sinalizando ALERT_SENSOR_ERROR.
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
