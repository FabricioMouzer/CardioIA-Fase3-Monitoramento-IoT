#pragma once

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

// ============================================================================
// CardioIA Fase 3 — Serializador do Contrato JSON v1 para MQTT
// ============================================================================
// Estrutura de entrada para formatação determinística do payload de telemetria
// e alerta (13 campos obrigatórios validados na camada Fog pelo Node-RED).
struct TelemetryPayloadInput {
  uint32_t sequence;            // Número sequencial crescente da amostra
  uint32_t capturedAtMs;        // Timestamp relativo (millis() no momento da coleta)
  float temperatureC;           // Temperatura em °C (-999.0 se DHT22 inválido)
  float humidityPct;            // Umidade relativa em % (-1.0 se DHT22 inválido)
  uint16_t bpm;                 // Batimentos por minuto sintéticos (40 a 180 BPM)
  bool sensorValid;             // Indica se a leitura do DHT22 foi válida
  uint8_t alertCode;            // Máscara binária combinada de alertas (0 a 15)
  const char* alert;            // Rótulo textual prioritário do estado/alerta
  const char* source;           // Origem do envio: "live" ou "buffered"
  size_t bufferPending;         // Amostras restantes no buffer FIFO após envio
  unsigned long droppedSamples; // Total acumulado de descartes por buffer cheio
};

// Formata o JSON de telemetria/alerta em buffer estático sem usar String dinâmica.
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

// Formata o JSON de estado operacional publicado no tópico de status (e Last Will).
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
