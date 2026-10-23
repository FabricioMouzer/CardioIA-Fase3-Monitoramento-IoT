# Etapa 1 — contrato MQTT e JSON

## Namespace definitivo

```text
cardioia/fase3/rm566777/cardioia-esp32-01/telemetria
cardioia/fase3/rm566777/cardioia-esp32-01/alerta
cardioia/fase3/rm566777/cardioia-esp32-01/status
```

Qualquer versão anterior sem `rm566777` fica rejeitada. Firmware, flow, exemplos e testes deverão usar exatamente estes tópicos.

## Contrato de telemetria — versão 1

| Campo | Tipo | Unidade | Regra |
|---|---|---|---|
| `schema_version` | inteiro | — | Deve ser `1` |
| `device_id` | string | — | `cardioia-esp32-01` |
| `sequence` | inteiro | — | Crescente durante a execução |
| `captured_uptime_ms` | inteiro | ms | Momento da coleta desde o boot |
| `temperature_c` | número | °C | `-999.0` se DHT inválido |
| `humidity_pct` | número | % | `-1.0` se DHT inválido |
| `bpm` | inteiro | bpm | Faixa sintética de 40 a 180 |
| `sensor_valid` | booleano | — | Validade do DHT22 |
| `alert_code` | inteiro | máscara | Soma dos bits ativos |
| `alert` | string | — | Rótulo prioritário |
| `source` | string | — | `live` ou `buffered` |
| `buffer_pending` | inteiro | amostras | Fila restante |
| `dropped_samples` | inteiro | amostras | Perdas acumuladas por estouro |

## Máscara de alertas

| Bit | Valor | Significado |
|---:|---:|---|
| 0 | 1 | BPM abaixo de 50 |
| 1 | 2 | BPM acima de 120 |
| 2 | 4 | Temperatura acima de 38,0 °C |
| 3 | 8 | Falha do DHT22 |

O campo `alert_code` preserva combinações. O campo `alert` oferece um rótulo principal com prioridade: falha do sensor, temperatura alta, BPM alto, BPM baixo e normal.

## Status

O tópico `status` publicará `online`, `online_syncing` ou `offline_unexpected`, acompanhado de fila, descartes e uptime. O último estado poderá ser retido para facilitar a visualização.

## Regras de validação

- JSON inválido ou sem campos obrigatórios deve ser descartado pelo Node-RED.
- Valores não numéricos não podem chegar aos widgets.
- `schema_version` diferente de 1 deve gerar aviso explícito.
- O assinante independente deve receber telemetria, alerta e status durante os testes.
- Nenhuma senha, token, e-mail ou dado clínico real pode integrar o payload.
