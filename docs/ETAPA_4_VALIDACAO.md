# Etapa 4 — Validação MQTT e broker

## Escopo executado

- ESP32 simulado conectado à rede `Wokwi-GUEST`;
- publicação MQTT em `broker.hivemq.com:1883`, QoS 0;
- telemetria e alertas sem retenção;
- status com retenção e Last Will `offline_unexpected`;
- cliente WebSocket HiveMQ independente conectado a `mqtt-dashboard.com:8884`;
- somente dados sintéticos; nenhuma credencial foi utilizada.

## Tópicos validados

| Tipo | Tópico | Retenção | Recebido externamente |
|---|---|---:|---:|
| Telemetria | `cardioia/fase3/rm566777/cardioia-esp32-01/telemetria` | Não | Sim |
| Alerta | `cardioia/fase3/rm566777/cardioia-esp32-01/alerta` | Não | Sim |
| Status | `cardioia/fase3/rm566777/cardioia-esp32-01/status` | Sim | Sim |

## Resultados observados

1. O firmware compilou no Wokwi com `WiFi.h`, `PubSubClient` e a biblioteca do DHT22.
2. A conexão retornou `MQTT_CONNECT_RESULT connected=true state=0`.
3. O cliente independente recebeu JSON válido com os 13 campos do contrato.
4. BPM sintético de 180 gerou `alert_code=2` e `alert=high_bpm` nos tópicos de telemetria e alerta.
5. A interrupção controlada acumulou as sequências 32–35.
6. A reconexão publicou 32, 33, 34 e 35 em FIFO, com pendências 3, 2, 1 e 0.
7. O ciclo terminou com `SYNC_DONE sent=4 pending=0 dropped_samples=0`.
8. O assinante externo recebeu as quatro amostras com `source=buffered`.
9. O status retido foi comprovado por recebimento imediato de `offline_unexpected` após a assinatura.

## Correção detectada durante a validação

A primeira compilação falhou porque as barras de escape das aspas JSON foram
removidas durante a transferência ao editor. O formatador foi alterado para
literais C++ `R"json(...)json"`. A versão corrigida compilou, foi publicada e
teve os payloads analisados por um assinante independente.

## Evidências

- `E4-02-compilacao-conexao.jpg`: execução do firmware, circuito e JSON aceito;
- `E4-03-assinante-independente.jpg`: cliente HiveMQ conectado e recebendo;
- `E4-04-alerta-resiliencia.jpg`: LED de alerta e publicação `high_bpm`;
- `E4-05-log-wokwi-serial.txt`: log contínuo completo do ESP32;
- `E4-06-log-assinante-hivemq.txt`: mensagens recebidas fora do Wokwi;
- `E4-07-link-publico.txt`: teste sem sessão;
- `E4-08-validacao-automatizada.txt`: saídas dos portões automatizados.

## Limites assumidos

O broker é público, sem autenticação e sem TLS no enlace MQTT do ESP32. Ele é
adequado apenas a demonstrações com dados sintéticos. Produção exigiria TLS,
autenticação, autorização por tópico, rotação de credenciais e monitoramento.
