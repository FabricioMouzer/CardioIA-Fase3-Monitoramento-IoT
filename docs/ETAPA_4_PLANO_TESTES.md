# Etapa 4 — Plano de testes e portão

- [x] **T4-01 — Contrato:** três tópicos e JSON versão 1 presentes no código.
- [x] **T4-02 — Segurança:** nenhuma credencial ou dado clínico real versionado.
- [x] **T4-03 — Escopo:** HiveMQ público e porta 1883 documentados como inseguros.
- [x] **T4-04 — Reconexão:** tentativas limitadas a uma a cada cinco segundos.
- [x] **T4-05 — Buffer:** amostra só sai após aceitação local da publicação.
- [ ] **T4-06 — Compilação Wokwi:** firmware com WiFi/PubSubClient compila.
- [ ] **T4-07 — Conexão:** Wi-Fi e MQTT registram conexão bem-sucedida.
- [ ] **T4-08 — Telemetria:** assinante independente recebe JSON válido.
- [ ] **T4-09 — Alerta:** assinante recebe mensagem no tópico `alerta`.
- [ ] **T4-10 — Status:** assinante recebe status retido.
- [ ] **T4-11 — Reconexão:** interrupção acumula e retorno sincroniza o FIFO.
- [ ] **T4-12 — Link público:** versão executável abre sem sessão.
- [ ] **T4-13 — Regressão e consistência:** etapas anteriores continuam aprovadas.

## Estado do portão

**ABERTO — ETAPA EM EXECUÇÃO.** Código preparado não equivale a publicação
recebida. T4-06 a T4-13 dependem das evidências reais.
