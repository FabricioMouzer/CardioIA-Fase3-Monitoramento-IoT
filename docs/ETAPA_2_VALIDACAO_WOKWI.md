# Etapa 2 — validação funcional no Wokwi

Execução inicial: 23/10/2026  
Complementação das evidências: 24/10/2026  
Conclusão e teste público: 25/10/2026  
Projeto público: <https://wokwi.com/projects/478845707855731713>  
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
| T2-10 | Link público aberto sem sessão | Código, circuito e simulação acessíveis com `SIGN IN / SIGN UP` visível | Aprovado |
| T2-11 | Transições contínuas | `high_bpm → normal` e `sensor_error → normal`, sem segundo `BOOT` | Aprovado |
| T2-12 | Capturas preservadas | Circuito, LED e Serial registrados juntos nos estados normal, alerta e recuperação | Aprovado |

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
| `E2-06-circuito-led-normal-link-publico.jpg` | Link público, circuito completo, LED apagado e log normal | `25827d64c1fdad184c07b0563050e779d21f9f5f436fedc31ebf06404d17d8e2` |
| `E2-07-circuito-led-alerta-link-publico.jpg` | Mesmo circuito, LED aceso e log `high_bpm` | `5c79829a9781389349e1d9ce48111c32bd66a19e1e172d4d7f7a0028bccda102` |
| `E2-08-circuito-led-recuperado-link-publico.jpg` | Mesmo circuito, LED apagado novamente e log normal | `bbebe06f8e7c18a5c9c67edd752b4b3cc49e4e06cd55949d112caf8c53f22a76` |

As três capturas finais mostram o título do projeto público, o botão `SIGN IN / SIGN UP`, o circuito, o LED e o Monitor Serial. A correspondência é direta: `seq=1` normal/LED apagado, `seq=2` `high_bpm`/LED aceso e `seq=3` normal/LED apagado novamente, sem segundo `BOOT`.

## Validação do link público sem sessão

O endereço <https://wokwi.com/projects/478845707855731713> foi aberto em uma nova aba sem autenticação. A página exibiu `SIGN IN / SIGN UP`, permitiu ler todos os arquivos e iniciou a simulação. Não houve solicitação de novas permissões do GitHub.

Antes da execução definitiva, `sketch.ino`, `alert_logic.h` e `diagram.json` foram alinhados com os arquivos documentados no repositório, salvos e recarregados pelo endereço público.

```text
SAMPLE seq=1 uptime_ms=523   bpm=110 alert_code=0 alert=normal
SAMPLE seq=2 uptime_ms=5541  bpm=180 alert_code=2 alert=high_bpm
SAMPLE seq=3 uptime_ms=10549 bpm=110 alert_code=0 alert=normal
```

Além do intervalo de 5.018 ms já justificado, a execução final mediu 5.008 ms entre `seq=2` e `seq=3`, desvio de apenas +8 ms (+0,16%), também dentro da faixa aceita.

## Integridade dos arquivos executados

```text
3ea3d1522fd2de20d88549dd2bbadbd4de8fabf114edbc842bd4a853101afc79  wokwi/sketch.ino
5ed404361508d43b96421faa2fa86a09c2a110d81d5fd2924970ac553e1d1608  wokwi/diagram.json
1de1c36dc36573381f9f334b2c40b5e05d9e1fdc96ed5a5b1e368557d95bf372  wokwi/alert_logic.h
652f92b0e7836bb2bbfdcc28d5e3dd539b952fb991e1343e359ba27700c3fb9f  wokwi/libraries.txt
```

## Portão de conclusão

- [x] Projeto salvo e publicado no Wokwi.
- [x] Link aberto e executado sem sessão (T2-10).
- [x] Logs contínuos preservados (T2-11).
- [x] Circuito, LED e Serial capturados e versionados (T2-12).
- [x] Correspondência visual e textual conferida.
- [x] Tolerância de tempo justificada.

Todos os critérios foram aprovados. A conclusão formal está em `docs/ETAPA_2_CONCLUSAO.md`. A Etapa 3 não foi iniciada.
