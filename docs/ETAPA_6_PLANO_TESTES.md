# Etapa 6 — Plano de testes e portão

- [x] **T6-01 — Autorização:** início confirmado por Fabrício em 25/10/2026.
- [x] **T6-02 — Escopo:** fluxo, cenários e critérios definidos no blueprint.
- [x] **T6-03 — Pré-condições:** Etapas 0–5 finalizadas e serviços acessíveis.
- [x] **T6-04 — Execução A normal:** telemetria ao vivo chega ao dashboard.
- [x] **T6-05 — Execução A BPM alto:** alerta aparece sem falso negativo.
- [x] **T6-06 — Execução A offline:** nove amostras entraram no FIFO.
- [x] **T6-07 — Execução A sincronização:** FIFO voltou a zero em ordem.
- [x] **T6-08 — Execução B independente:** nova inicialização comprovada por `sequence=1`.
- [x] **T6-09 — Execução B BPM baixo:** alerta apareceu sem falso negativo.
- [x] **T6-10 — Execução B DHT22:** falha e recuperação ocorreram sem reinício.
- [x] **T6-11 — Limites:** 50 BPM, 120 BPM e 38,0 °C permaneceram normais.
- [x] **T6-12 — Estado final:** 110 BPM, 36,5 °C, fila 0 e descartes 0.
- [x] **T6-13 — Correlação:** logs, capturas e sequências são compatíveis.
- [x] **T6-14 — Repetibilidade:** duas execuções terminaram aprovadas.
- [x] **T6-15 — Regressão:** Etapas 1–5 permaneceram aprovadas.
- [x] **T6-16 — Consistência:** nenhuma contradição ou pendência crítica.

## Estado do portão

**FECHADO — T6-01 a T6-16 APROVADOS.** A Etapa 7 está liberada, mas não foi iniciada.
