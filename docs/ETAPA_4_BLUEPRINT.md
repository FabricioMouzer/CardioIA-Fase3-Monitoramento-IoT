# Etapa 4 — Blueprint MQTT e broker

## Estado

**Em execução desde 25/10/2026.** A etapa permanecerá aberta até que um
assinante independente receba mensagens reais dos três tópicos.

## Configuração aprovada

| Item | Valor |
|---|---|
| Wi-Fi simulado | `Wokwi-GUEST`, sem senha |
| Broker | `broker.hivemq.com` |
| Porta | `1883`, MQTT sem TLS |
| QoS | 0 |
| Retain | somente status |
| Telemetria | não retida |
| Alerta | não retido |
| Dados | exclusivamente sintéticos |

O broker é público, compartilhado e sem confidencialidade. A configuração é
adequada apenas para demonstração acadêmica, nunca para dados clínicos reais.

## Fluxo

1. O ESP32 conecta ao `Wokwi-GUEST`.
2. O cliente MQTT tenta conectar com intervalo mínimo de cinco segundos.
3. O status retido informa `online`, `online_syncing` ou
   `offline_unexpected` (Last Will).
4. A telemetria é formatada conforme o contrato JSON versão 1.
5. Uma amostra com alerta também é publicada no tópico `alerta`.
6. Se a conexão/publicação falhar, a amostra entra no FIFO da Etapa 3.
7. Após reconexão, o FIFO é sincronizado em ordem; uma posição só é removida
   depois que `PubSubClient.publish()` aceita localmente a mensagem.

## Limite de comprovação

`accepted=true` no firmware comprova apenas aceitação local pela biblioteca.
A prova fim a fim exige que outro cliente, independente do ESP32, assine os
tópicos e preserve as mensagens recebidas.
