# Etapa 6 — Validação integrada e repetibilidade

## Resultado executivo

O fluxo completo foi aprovado em duas execuções independentes: sensores
sintéticos no Wokwi, processamento e buffer no ESP32, publicação MQTT no HiveMQ,
validação no Node-RED e visualização no dashboard público.

- [Projeto público no Wokwi](https://wokwi.com/projects/478851580032675841)
- [Dashboard público](https://cardioia-fase3-dashboard.onrender.com/dashboard/monitoramento)

## Execução A — risco elevado e resiliência

| Cenário | Observado | Resultado |
|---|---|---|
| Normal | 110 BPM, 36,5 °C, `alert_code=0` | Aprovado |
| BPM alto | 163 BPM, `alert_code=2`, painel “BPM ALTO” | Aprovado |
| Retorno sem reinício | sequência 10 normal após o alerta | Aprovado |
| Offline | sequências 12–20, nove amostras no FIFO | Aprovado |
| Sincronização | sequências 12–20 publicadas em ordem | Aprovado |
| Estado final | fila 0, descartes 0, origem `live` | Aprovado |

A primeira leitura desta execução registrou falha transitória do DHT22 durante a
inicialização e foi armazenada enquanto o MQTT conectava. A sequência 2 já estava
normal, sem reinício. O evento foi mantido no log por transparência e não afetou
os cenários planejados.

## Execução B — diversidade, falha e fronteiras

| Cenário | Observado | Resultado |
|---|---|---|
| Reinício independente | nova execução começou em `sequence=1` | Aprovado |
| BPM baixo | 42 BPM, `alert_code=1`, painel “BPM BAIXO” | Aprovado |
| Falha do DHT22 | `sensor_valid=false`, `alert_code=8` | Aprovado |
| Recuperação | sequência 14 voltou a normal sem reinício | Aprovado |
| Limite inferior | 50 BPM permaneceu normal | Aprovado |
| Limite superior | 120 BPM permaneceu normal | Aprovado |
| Limite térmico | 38,0 °C permaneceu normal | Aprovado |
| Estado final | 110 BPM, 36,5 °C, fila 0 e descartes 0 | Aprovado |

## Correlação e automação

Os números de sequência, valores, alertas, origem, fila e descartes dos logs são
compatíveis com as capturas do Wokwi e do dashboard. O validador
[`tests/validate_stage6_evidence.py`](../tests/validate_stage6_evidence.py)
confere integridade das imagens, transições, ordem do FIFO, recuperação, limites
e independência das execuções.

## Falhas e correções durante o ensaio

Uma tentativa preliminar apresentou lentidão severa no simulador porque havia
abas técnicas duplicadas consumindo recursos. Ela foi descartada, as abas foram
fechadas e as execuções A e B foram reiniciadas desde o início. Somente as
execuções completas e correlacionadas foram aceitas como evidência.

## Evidências principais

- [`E6-02-execucao-a-bpm-alto.jpg`](../evidencias/etapa-6/E6-02-execucao-a-bpm-alto.jpg)
- [`E6-03-execucao-a-log.txt`](../evidencias/etapa-6/E6-03-execucao-a-log.txt)
- [`E6-04-execucao-a-wokwi.jpg`](../evidencias/etapa-6/E6-04-execucao-a-wokwi.jpg)
- [`E6-05-execucao-a-sincronizada.jpg`](../evidencias/etapa-6/E6-05-execucao-a-sincronizada.jpg)
- [`E6-06-execucao-b-bpm-baixo.jpg`](../evidencias/etapa-6/E6-06-execucao-b-bpm-baixo.jpg)
- [`E6-07-execucao-b-falha-dht.jpg`](../evidencias/etapa-6/E6-07-execucao-b-falha-dht.jpg)
- [`E6-08-execucao-b-log.txt`](../evidencias/etapa-6/E6-08-execucao-b-log.txt)
- [`E6-09-execucao-b-wokwi.jpg`](../evidencias/etapa-6/E6-09-execucao-b-wokwi.jpg)
- [`E6-10-execucao-b-final-normal.jpg`](../evidencias/etapa-6/E6-10-execucao-b-final-normal.jpg)
- [`E6-11-validacao-automatizada.txt`](../evidencias/etapa-6/E6-11-validacao-automatizada.txt)

## Parecer

T6-01 a T6-16 foram aprovados. Não há perda de amostra, falso negativo nos
cenários críticos, fila pendente, contradição documental ou pendência crítica.
