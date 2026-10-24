# Registro de decisões

## D-001 — Repositório exclusivo

- **Decisão:** usar `CardioIA-Fase3-Monitoramento-IoT`.
- **Visibilidade:** pública.
- **Motivo:** separar a Fase 3 dos trabalhos anteriores e permitir acesso do grupo e do avaliador.
- **Estado:** concluída em 23/10/2026; repositório criado e validado como público.

## D-002 — Desenvolvimento por portões

- **Decisão:** bloquear a etapa seguinte até a confirmação formal da anterior.
- **Motivo:** impedir acúmulo de pendências e documentação divergente.
- **Estado:** aprovada.

## D-003 — Rascunhos anteriores

- **Decisão:** considerar o código existente em outro repositório apenas como referência não validada.
- **Motivo:** o rascunho contém implementação preparada, mas não possui evidências suficientes de execução no Wokwi, MQTT e Node-RED.
- **Estado:** aprovada.

## D-004 — Node-RED

- **Decisão:** a instalação, escolha do pacote de dashboard e importação do flow serão tratadas somente na etapa correspondente.
- **Motivo:** o computador ainda não possui Node-RED e nenhuma execução deve ser presumida.
- **Estado:** aprovada.

## D-005 — Sensores da solução

- **Decisão:** usar DHT22 como sensor obrigatório e potenciômetro analógico como segundo sensor, simulando BPM entre 40 e 180.
- **Motivo:** permite reproduzir valores normais, limites e alertas de forma controlada no Wokwi.
- **Limitação:** o potenciômetro não mede pulso real; produz apenas um sinal sintético para fins acadêmicos.
- **Estado:** aprovada pelos quatro integrantes em 23/10/2026.

## D-006 — Resiliência offline

- **Decisão:** adotar buffer circular FIFO em RAM com 2.160 amostras, intervalo de cinco segundos e retenção nominal de três horas.
- **Motivo:** atende ao pedido de estratégia limitada na ordem de milhares de amostras e mantém consumo previsível de memória.
- **Política de estouro:** substituir a amostra mais antiga e incrementar `dropped_samples`.
- **Estado:** aprovada pelos quatro integrantes em 23/10/2026.

## D-007 — Contrato e tópicos MQTT

- **Decisão:** padronizar o prefixo `cardioia/fase3/rm566777/cardioia-esp32-01` e os sufixos `telemetria`, `alerta` e `status`.
- **Motivo:** eliminar a divergência localizada na PR nº 10 e separar telemetria, alertas e estado operacional.
- **Estado:** aprovada pelos quatro integrantes em 23/10/2026.

## D-008 — Broker e qualidade de serviço

- **Decisão:** usar inicialmente `broker.hivemq.com:1883`, QoS 0 e somente dados sintéticos; comprovar o recebimento com assinante independente.
- **Motivo:** reduz barreiras de configuração no Wokwi e atende ao protótipo acadêmico.
- **Limitação:** aceite local de publicação não comprova entrega fim a fim; porta 1883 não oferece confidencialidade.
- **Estado:** aprovada pelos quatro integrantes em 23/10/2026.

## D-009 — Dashboard

- **Decisão:** utilizar `@flowfuse/node-red-dashboard` (Dashboard 2.0) na Etapa 5.
- **Motivo:** o pacote clássico `node-red-dashboard` está descontinuado e o FlowFuse Dashboard é seu sucessor oficial.
- **Estado:** aprovada pelos quatro integrantes em 23/10/2026.

## D-010 — Escopo dos desafios opcionais

- **Decisão:** não iniciar REST/e-mail, Grafana nem IA em séries temporais antes da aprovação integral dos cinco critérios obrigatórios.
- **Motivo:** proteger a nota principal e impedir que itens opcionais desviem recursos das evidências obrigatórias.
- **Estado:** aprovada.

## D-011 — Biblioteca do DHT22

- **Decisão:** utilizar `DHT sensor library for ESPx` e o cabeçalho `DHTesp.h`.
- **Motivo:** é a biblioteca indicada pela documentação do Wokwi para DHT22 com ESP32.
- **Estado:** aprovada para validação na Etapa 2.

## D-012 — Circuito incremental

- **Decisão:** a Etapa 2 conterá somente ESP32, DHT22, potenciômetro, LED e resistor; o botão offline será incluído na Etapa 3.
- **Motivo:** separar a evidência de sensoriamento da evidência de resiliência de rede.
- **Estado:** aprovada para validação na Etapa 2.

## D-013 — Injeção reproduzível de falha do DHT22

- **Decisão:** aceitar os comandos seriais `F` e `R` para ativar e remover uma falha sintética do DHT22 durante a mesma execução.
- **Motivo:** produzir evidência contínua e reproduzível de `sensor_error` e recuperação sem reiniciar o ESP32 nem depender de desconexão física no simulador.
- **Limitação:** é um recurso de teste do protótipo educacional; não representa uma falha física real nem deve ser usado como mecanismo clínico.
- **Estado:** aprovada para completar a validação da Etapa 2.
