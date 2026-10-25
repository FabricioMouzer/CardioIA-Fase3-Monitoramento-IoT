# Etapa 4 — Plano de testes e portão

- [x] **T4-01 — Contrato:** três tópicos e JSON versão 1 presentes no código.
- [x] **T4-02 — Segurança:** nenhuma credencial ou dado clínico real versionado.
- [x] **T4-03 — Escopo:** HiveMQ público e porta 1883 documentados como inseguros.
- [x] **T4-04 — Reconexão:** tentativas limitadas a uma a cada cinco segundos.
- [x] **T4-05 — Buffer:** amostra só sai após aceitação local da publicação.
- [x] **T4-06 — Compilação Wokwi:** firmware com WiFi/PubSubClient compila.
- [x] **T4-07 — Conexão:** Wi-Fi e MQTT registram conexão bem-sucedida.
- [x] **T4-08 — Telemetria:** assinante independente recebe JSON válido.
- [x] **T4-09 — Alerta:** assinante recebe mensagem no tópico `alerta`.
- [x] **T4-10 — Status:** assinante recebe status retido.
- [x] **T4-11 — Reconexão:** interrupção acumula e retorno sincroniza o FIFO.
- [x] **T4-12 — Link público:** versão executável abre sem sessão.
- [x] **T4-13 — Regressão e consistência:** etapas anteriores continuam aprovadas.

## Estado do portão

**FECHADO — ETAPA CONFIRMADA E FINALIZADA.** Os treze testes possuem evidência
real e os resultados foram validados por `tests/validate_stage4_evidence.py`.
