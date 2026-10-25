# Etapa 5 — Validação do dashboard e alertas

## Resultado executivo

O dashboard Node-RED Dashboard 2.0 foi implantado no Render e validado de ponta
a ponta com dados sintéticos publicados pelo ESP32 no Wokwi via HiveMQ.

- [Dashboard público](https://cardioia-fase3-dashboard.onrender.com/dashboard/monitoramento)
- [Projeto público no Wokwi](https://wokwi.com/projects/478851580032675841)

## Ambiente validado

| Componente | Configuração | Resultado |
|---|---|---|
| Node-RED | 5.0.9 | Aprovado |
| Dashboard | FlowFuse Dashboard 2.0 1.34.0 | Aprovado |
| Hospedagem | Render Web Service, plano Free | Live |
| Broker | `broker.hivemq.com:1883` | Conectado |
| Contrato | `schema_version=1`, 13 campos | Aprovado |
| Dashboard | `/dashboard/monitoramento` | HTTP 200 |
| Editor público | Desabilitado por variável de ambiente | HTTP 404 na raiz |

## Critérios funcionais

| Critério | Evidência | Resultado |
|---|---|---|
| MQTT real do Wokwi | sequência e publicações aceitas em E5-06 | Aprovado |
| Gráfico BPM | histórico com 110 → 163 → 110 → 42 → 110 | Aprovado |
| Gauge de temperatura | 36,5 °C, 39,5 °C e limite 38,0 °C | Aprovado |
| Gauge de umidade | 55% na execução normal | Aprovado |
| Estado normal | `alert_code=0` | Aprovado |
| BPM alto | 163 BPM, `alert_code=2` | Aprovado |
| BPM baixo | 42 BPM, `alert_code=1` | Aprovado |
| Temperatura alta | 39,5 °C, `alert_code=4` | Aprovado |
| Falha de sensor | `sensor_valid=false`, `alert_code=8` | Aprovado |
| Recuperação sem reinício | comando `R`, retorno a NORMAL | Aprovado |
| Limites inclusivos | 50 BPM, 120 BPM e 38,0 °C normais | Aprovado |
| Edge no painel | origem, fila e descartes visíveis | Aprovado |

## Evidências

- [`E5-03-dashboard-normal-online.jpg`](../evidencias/etapa-5/E5-03-dashboard-normal-online.jpg)
- [`E5-04-wokwi-mqtt-online.jpg`](../evidencias/etapa-5/E5-04-wokwi-mqtt-online.jpg)
- [`E5-05-implantacao-render.txt`](../evidencias/etapa-5/E5-05-implantacao-render.txt)
- [`E5-06-teste-integrado-mqtt-dashboard.txt`](../evidencias/etapa-5/E5-06-teste-integrado-mqtt-dashboard.txt)
- [`E5-07-cenarios-alerta-limites.txt`](../evidencias/etapa-5/E5-07-cenarios-alerta-limites.txt)
- [`E5-08-regressao-final.txt`](../evidencias/etapa-5/E5-08-regressao-final.txt)

## Riscos conhecidos

O broker público e sem TLS é adequado apenas ao protótipo com dados sintéticos.
O plano gratuito do Render pode suspender a instância após inatividade e causar
demora no primeiro acesso. Os avisos transitivos do `npm audit` foram registrados
sem aplicar atualização forçada; não há credenciais nem dados clínicos reais, e
o editor administrativo permanece desabilitado.

## Parecer

Todos os 16 testes do portão foram atendidos. Não existe pendência crítica para
a Etapa 5. A Etapa 6 está liberada, mas não foi iniciada.
