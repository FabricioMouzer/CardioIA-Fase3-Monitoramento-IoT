# Etapa 3 — conclusão formal

Data: 25/10/2026  
Projeto público: <https://wokwi.com/projects/478851580032675841>

## ✅ ETAPA 3 CONFIRMADA E FINALIZADA

**Entregáveis:** buffer FIFO circular limitado a 2.160 amostras, retenção
nominal de três horas, coleta offline, sincronização ordenada, política de
estouro, contador de descartes, botão de conectividade e comandos de teste.

**Testes aprovados:** T3-01 a T3-13; compilação Wokwi; ciclo contínuo online →
offline → online; três amostras armazenadas e sincronizadas na ordem; `pending=0`;
10/10 verificações do log; 18/18 verificações FIFO; regressão das Etapas 1 e 2.

**Evidências:** `evidencias/etapa-3/`, principalmente E3-05, E3-06 e E3-07;
`docs/ETAPA_3_VALIDACAO_WOKWI.md`.

**Pendências críticas:** nenhuma.

**Próxima etapa liberada:** Etapa 4 — MQTT e broker, ainda não iniciada.

## Limites declarados

- Dados exclusivamente sintéticos.
- Armazenamento em RAM, portanto volátil no simulador.
- Envio à nuvem representado pelo Monitor Serial nesta etapa.
- MQTT, credenciais e broker não pertencem à Etapa 3.
