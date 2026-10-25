# Etapa 3 — Plano de testes e portão

## Testes planejados

- [x] **T3-01 — Capacidade declarada:** código e documentação usam 2.160 amostras.
- [x] **T3-02 — Retenção calculada:** 2.160 × 5 s = 3 horas nominais.
- [x] **T3-03 — FIFO unitário:** remoção preserva a ordem de inserção.
- [x] **T3-04 — Estouro unitário:** item mais antigo é substituído e o contador sobe.
- [x] **T3-05 — Drenagem unitária:** o buffer termina vazio e sem duplicações.
- [x] **T3-06 — Separação de escopo:** não há MQTT nem conexão Wi-Fi real nesta etapa.
- [ ] **T3-07 — Execução Wokwi online:** leitura ao vivo aparece como `CLOUD_SEND`.
- [ ] **T3-08 — Coleta offline:** três ou mais amostras entram no buffer sem reinício.
- [ ] **T3-09 — Reconexão:** amostras são sincronizadas em ordem e `pending=0`.
- [ ] **T3-10 — Correspondência visual:** botão/circuito e logs contínuos são capturados.
- [ ] **T3-11 — Link público:** projeto abre e executa sem sessão autenticada.
- [ ] **T3-12 — Regressão:** testes das Etapas 1 e 2 continuam aprovados.
- [ ] **T3-13 — Revisão final:** documentação, logs e estado não se contradizem.

## Evidências ainda obrigatórias

- log contínuo online → offline → buffer → online → sincronização;
- captura do circuito com o botão de conectividade;
- captura/log do estado offline com pendências;
- captura/log após reconexão com `SYNC_DONE` e `pending=0`;
- teste automatizado da capacidade e da política de descarte;
- verificação do link público em sessão anônima.

## Estado do portão

**ABERTO — ETAPA EM EXECUÇÃO.** A presença do código e a aprovação de testes
unitários não substituem a execução no Wokwi nem as evidências públicas.
