# Etapa 3 — Plano de testes e portão

## Testes planejados

- [x] **T3-01 — Capacidade declarada:** código e documentação usam 2.160 amostras.
- [x] **T3-02 — Retenção calculada:** 2.160 × 5 s = 3 horas nominais.
- [x] **T3-03 — FIFO unitário:** remoção preserva a ordem de inserção.
- [x] **T3-04 — Estouro unitário:** item mais antigo é substituído e o contador sobe.
- [x] **T3-05 — Drenagem unitária:** o buffer termina vazio e sem duplicações.
- [x] **T3-06 — Separação de escopo:** não há MQTT nem conexão Wi-Fi real nesta etapa.
- [x] **T3-07 — Execução Wokwi online:** leitura ao vivo aparece como `CLOUD_SEND`.
- [x] **T3-08 — Coleta offline:** três ou mais amostras entram no buffer sem reinício.
- [x] **T3-09 — Reconexão:** amostras são sincronizadas em ordem e `pending=0`.
- [x] **T3-10 — Correspondência visual:** botão/circuito e logs contínuos são capturados.
- [x] **T3-11 — Link público:** HTTP 200 e arquivos acessíveis sem cookies de sessão.
- [x] **T3-12 — Regressão:** testes das Etapas 1 e 2 continuam aprovados.
- [x] **T3-13 — Revisão final:** documentação, logs e estado foram reconciliados.

## Evidências produzidas

- `E3-02`: circuito com botão e buffer offline;
- `E3-04`: log contínuo de uma execução extensa;
- `E3-05` + `E3-06`: captura e log correlacionados da execução final;
- `run_stage3_buffer_logic.py`: capacidade reduzida, ordem e estouro;
- `validate_stage3_runtime.py`: duplicação, perda e esvaziamento;
- `E3-07`: portão final e acesso público sem cookies de sessão.

## Estado do portão

**FECHADO — ETAPA CONFIRMADA.** Todos os testes T3-01 a T3-13 possuem
evidências estáticas, unitárias, visuais ou de execução pública.
