# Etapa 2 — validação funcional no Wokwi

Data da execução: 23/10/2026  
Commit executado: `b5b08142d0f3eb94ce184a0b85992f0e8913e580`

## Escopo validado

O firmware e o circuito da Etapa 2 foram carregados no Wokwi a partir do commit público e comparados integralmente no editor antes da execução. A biblioteca `DHT sensor library for ESPx` foi instalada após autorização expressa de Fabrício.

| Teste | Entrada observada | Saída observada | Resultado |
|---|---|---|---|
| T2-01 | Boot com os arquivos do commit | `BOOT CardioIA Fase 3 Etapa 2` | Aprovado |
| T2-02 | 36,5 °C, 55%, 110 BPM | `alert_code=0 alert=normal` | Aprovado |
| T2-03 | Potenciômetro em 0 | `bpm=40 alert_code=1 alert=low_bpm` | Aprovado |
| T2-04 | Potenciômetro em 1023 | `bpm=180 alert_code=2 alert=high_bpm` | Aprovado |
| T2-05 | Temperatura em 39,0 °C | `alert_code=4 alert=high_temperature` | Aprovado |
| T2-06 | Sensores restaurados | `bpm=110 alert_code=0 alert=normal` | Aprovado |
| T2-07 | Sinal do DHT22 desconectado de forma controlada | `sensor_valid=false alert_code=8 alert=sensor_error` | Aprovado |
| T2-08 | Limites exatos no teste C++ | 8/8 cenários aprovados | Aprovado |
| T2-09 | Duas amostras sem reinício | `522 ms` e `5540 ms`; diferença de `5018 ms` | Aprovado |
| T2-10 | Link público aberto sem sessão | Projeto ainda não foi salvo/publicado | Pendente |

## Restauração após o ensaio de falha

Para T2-07, a ligação do sinal foi temporariamente alterada de `esp:D15` para `esp:D14`. Após observar `sensor_error`, o `diagram.json` original foi restaurado e comparado integralmente. Uma nova execução confirmou novamente o estado normal.

## Integridade dos arquivos executados

```text
edbe08b78355563253e9f256c2b0669d7ad78c2de51ed9af10080eca963d4188  wokwi/sketch.ino
5ed404361508d43b96421faa2fa86a09c2a110d81d5fd2924970ac553e1d1608  wokwi/diagram.json
1de1c36dc36573381f9f334b2c40b5e05d9e1fdc96ed5a5b1e368557d95bf372  wokwi/alert_logic.h
652f92b0e7836bb2bbfdcc28d5e3dd539b952fb991e1343e359ba27700c3fb9f  wokwi/libraries.txt
```

## Conclusão provisória

Os testes técnicos T2-01 a T2-09 foram aprovados. A Etapa 2 permanece aberta até o projeto ser salvo no Wokwi, disponibilizado por link público e testado sem sessão, conforme T2-10.
