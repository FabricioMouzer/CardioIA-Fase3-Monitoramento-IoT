# Etapa 2 — validação funcional no Wokwi

Execução inicial: 23/10/2026  
Complementação das evidências: 24/10/2026  
Commit inicial executado: `b5b08142d0f3eb94ce184a0b85992f0e8913e580`  
Commit com injeção reproduzível de falha: `66140cd9a89f4447246c2983e565f615e196dcb8`

## Escopo validado

O firmware e o circuito da Etapa 2 foram carregados no Wokwi a partir dos commits públicos e comparados integralmente no editor antes da execução. A biblioteca `DHT sensor library for ESPx` foi instalada após autorização expressa de Fabrício.

| Teste | Entrada observada | Saída observada | Resultado |
|---|---|---|---|
| T2-01 | Boot com os arquivos do commit | `BOOT CardioIA Fase 3 Etapa 2` | Aprovado |
| T2-02 | 36,5 °C, 55%, 110 BPM | `alert_code=0 alert=normal` | Aprovado |
| T2-03 | Potenciômetro em 0 | `bpm=40 alert_code=1 alert=low_bpm` | Aprovado |
| T2-04 | Potenciômetro em 1023 | `bpm=180 alert_code=2 alert=high_bpm` | Aprovado |
| T2-05 | Temperatura em 39,0 °C | `alert_code=4 alert=high_temperature` | Aprovado |
| T2-06 | Sensores restaurados | `bpm=110 alert_code=0 alert=normal` | Aprovado |
| T2-07 | Comandos `F` e `R` na mesma execução | `sensor_error` seguido de `normal`, sem novo `BOOT` | Aprovado |
| T2-08 | Limites exatos no teste C++ | 8/8 cenários aprovados | Aprovado |
| T2-09 | Duas amostras sem reinício | `522 ms` e `5540 ms`; diferença de `5018 ms` | Aprovado |
| T2-10 | Link público aberto sem sessão | Projeto ainda não foi salvo/publicado | Pendente |
| T2-11 | Transições contínuas | `high_bpm → normal` e `sensor_error → normal`, sem segundo `BOOT` | Aprovado |
| T2-12 | Capturas preservadas | Serial dos dois ensaios salvo; circuito/LED ainda não capturados integralmente | Parcial |

## Logs contínuos, sem reinício

Os registros completos estão em `evidencias/etapa-2/E2-03-transicoes-continuas.txt`.

### Alerta de BPM alto e retorno ao normal

```text
BOOT CardioIA Fase 3 Etapa 2 — sensores sintéticos
SAMPLE seq=1 uptime_ms=521 ... bpm=110 ... alert=normal
SAMPLE seq=2 uptime_ms=5529 ... bpm=180 ... alert=high_bpm
SAMPLE seq=3 uptime_ms=10537 ... bpm=110 ... alert=normal
```

A sequência é crescente e existe somente um `BOOT`, comprovando a transição na mesma execução.

### Falha controlada do DHT22 e recuperação

```text
TEST dht_fault=on
SAMPLE seq=4 uptime_ms=15545 temp=-999.0C humidity=-1.0% ... sensor_valid=false alert=sensor_error
TEST dht_fault=off
SAMPLE seq=5 uptime_ms=20553 temp=36.5C humidity=55.0% ... sensor_valid=true alert=normal
```

Não houve novo `BOOT` entre a falha e a recuperação. Os comandos `F` e `R` são um recurso de teste reproduzível, documentado na decisão D-013; não simulam uma falha clínica real.

## Tolerância da cadência de 5.000 ms

| Medida | Valor |
|---|---:|
| Intervalo nominal | 5.000 ms |
| Intervalo observado | 5.018 ms |
| Desvio absoluto | +18 ms |
| Desvio relativo | +0,36% |
| Faixa de aceitação | 5.000 a 5.050 ms |

O firmware verifica `millis() - lastSampleAt >= 5000`, portanto a amostra não deve ser emitida antes do alvo. Um pequeno atraso é esperado porque o laço é cooperativo, possui `delay(10)` e também executa leitura do DHT22 e escrita serial. Foi adotada tolerância unilateral de até 1% de atraso (50 ms). Assim, 5.018 ms está dentro do critério e é aprovado. A medição considerada é `uptime_ms` do ESP32 simulado, não o tempo de parede do navegador.

## Capturas preservadas

| Arquivo | Conteúdo | SHA-256 |
|---|---|---|
| `E2-03-alerta-normal-sem-reinicio.jpg` | Trecho do Serial com `high_bpm` e retorno a `normal` | `f5acb69ba69f060175a091f3e70d969359081ed6a0e85a75db1b73095e1a2e2c` |
| `E2-04-dht-falha-recuperacao-sem-reinicio.jpg` | Trecho do Serial com falha e recuperação do DHT22 | `77575d137daf0d43ef742b69c7efacb09a4a5c3ea01d6f2575759005c9fe0e40` |

As capturas acima comprovam o Serial. Para concluir T2-12 ainda devem ser adicionadas vistas completas do circuito e do LED nos estados de alerta e normal.

## Integridade dos arquivos executados

```text
3ea3d1522fd2de20d88549dd2bbadbd4de8fabf114edbc842bd4a853101afc79  wokwi/sketch.ino
5ed404361508d43b96421faa2fa86a09c2a110d81d5fd2924970ac553e1d1608  wokwi/diagram.json
1de1c36dc36573381f9f334b2c40b5e05d9e1fdc96ed5a5b1e368557d95bf372  wokwi/alert_logic.h
652f92b0e7836bb2bbfdcc28d5e3dd539b952fb991e1343e359ba27700c3fb9f  wokwi/libraries.txt
```

## Portão de conclusão

A Etapa 2 permanece aberta. Para encerrá-la, não basta publicar o link. É obrigatório:

1. salvar e publicar o projeto no Wokwi;
2. abrir o link sem sessão e registrar o resultado (T2-10);
3. manter o log contínuo versionado (T2-11, já aprovado);
4. completar e versionar as capturas do circuito, LED e Serial (T2-12, parcial).

Somente depois dos quatro itens a mensagem formal de conclusão poderá ser emitida e a Etapa 3 será liberada.
