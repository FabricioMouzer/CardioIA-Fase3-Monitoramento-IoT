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

## D-014 — Controle reproduzível da conectividade simulada

- **Decisão:** usar um botão no GPIO 4 para alternar entre online e offline e manter os comandos seriais `O` e `N` como mecanismo determinístico de teste.
- **Motivo:** o botão demonstra a interação no circuito; os comandos permitem produzir logs contínuos e repetíveis sem depender do tempo de um clique manual.
- **Comportamento:** ao ficar offline, cada leitura entra no FIFO; ao voltar online, as pendências são enviadas em ordem antes das novas leituras.
- **Limitação:** a conectividade é uma variável booleana e o envio é representado por `Serial.println`/`Serial.printf`, conforme permitido no enunciado. MQTT pertence à Etapa 4.
- **Estado:** aprovada tecnicamente para execução da Etapa 3.

## D-015 — Implementação MQTT da Etapa 4

- **Decisão:** usar `WiFi.h`, `PubSubClient`, `Wokwi-GUEST` e o broker público `broker.hivemq.com:1883`.
- **Reconexão:** tentativas com intervalo mínimo de cinco segundos, sem bloquear a coleta.
- **Entrega:** telemetria e alerta não retidos; status retido e Last Will `offline_unexpected`.
- **Resiliência:** remover do FIFO somente após `publish()` retornar verdadeiro; sequência permite detectar duplicação.
- **Segurança:** somente dados sintéticos; nenhuma senha; broker aberto inadequado para produção.
- **Estado:** aprovada tecnicamente para validação da Etapa 4.

## D-016 — Evidência externa e literais JSON

- **Decisão:** validar o MQTT com um cliente WebSocket separado e usar literais
  C++ `R"json(...)json"` na composição dos payloads.
- **Motivo:** impedir que aceite local seja confundido com entrega ponta a ponta
  e evitar erros de escape observados na primeira compilação.
- **Estado:** validada e encerrada na Etapa 4 em 25/10/2026.

## D-017 — Runtime isolado do Node-RED

- **Decisão:** instalar Node-RED e Dashboard 2.0 apenas em `node-red/`, com
  versões fixadas e `node_modules` ignorado pelo Git.
- **Motivo:** Fabrício não possui Node-RED no computador e a instalação isolada
  permite validar o flow sem alterar globalmente o sistema de um integrante.
- **Versões:** Node-RED 5.0.9 e `@flowfuse/node-red-dashboard` 1.34.0.
- **Estado:** instalação, importação, MQTT real e evidência visual aprovados em
  25/10/2026.

## D-018 — Hospedagem pública do dashboard

- **Decisão:** implantar `node-red/` como Web Service no Render, plano gratuito,
  com `npm ci`, `npm start` e health check em `/dashboard/monitoramento`.
- **Motivo:** oferecer acesso livre à equipe sem exigir instalação local do
  Node-RED no computador de Fabrício.
- **Limitação:** o serviço gratuito pode suspender após inatividade e demorar no
  primeiro acesso seguinte.
- **Estado:** implantado e validado em 25/10/2026.

## D-019 — Superfície administrativa no ambiente público

- **Decisão:** usar `NODE_RED_DISABLE_ADMIN=true` no Render e manter somente o
  dashboard acessível publicamente.
- **Motivo:** reduzir a superfície de ataque e impedir edição anônima do flow.
- **Verificação:** dashboard HTTP 200; raiz administrativa HTTP 404.
- **Estado:** aprovada e validada em 25/10/2026.

## D-020 — Avisos de dependências

- **Decisão:** atualizar `body-parser` para 1.20.9 e `multer` para 2.5.0 por
  `overrides`; não executar `npm audit fix --force`.
- **Motivo:** os `overrides` removem cinco alertas altos sem alterar as versões
  do Node-RED e do dashboard. A correção forçada propõe um downgrade
  incompatível do Node-RED para 0.19.6.
- **Risco residual:** um alerta alto de `undici` e um moderado de `ip-address`
  permanecem dentro do pacote `npm` embarcado no registro administrativo. O
  ambiente público usa `httpAdminRoot=false` e bloqueia instalação e upload
  dinâmicos pela paleta.
- **Estado:** mitigado e validado; monitorar atualização compatível do Node-RED.

## D-021 — Repetibilidade da Etapa 6

- **Decisão:** executar dois ciclos independentes, reiniciando o simulador entre
  eles e variando os cenários.
- **Motivo:** evitar que uma única sequência preparada seja tratada como prova
  de funcionamento geral e aplicar a lição de generalização da Fase 2.
- **Correlação:** usar `sequence`, `source`, `buffer_pending`,
  `dropped_samples`, estado do dispositivo e alerta exibido.
- **Estado:** aprovada para execução em 25/10/2026.

## D-022 — Evidência integrada em duas execuções

- **Decisão:** aceitar somente execuções completas reiniciadas e correlacionar
  log, captura e dashboard principalmente pelo campo `sequence`.
- **Motivo:** horários visuais podem variar entre interfaces; a sequência é
  transportada no payload e preserva a identidade da amostra ponta a ponta.
- **Tratamento de falha:** tentativas preliminares incompletas não compõem a
  evidência; falhas observadas permanecem registradas com sua correção.
- **Estado:** validada e encerrada na Etapa 6 em 25/10/2026.

## D-023 — Vídeo no escopo da Etapa 7

- **Decisão:** não tratar o vídeo do “Ir Além 2” como requisito da atividade
  principal da Fase 3.
- **Motivo:** o enunciado exige vídeo somente no desafio opcional de IA em
  séries temporais, enquanto a decisão D-010 manteve os opcionais fora do escopo
  até a conclusão dos cinco critérios obrigatórios.
- **Controle:** qualquer decisão futura de realizar o desafio opcional exigirá
  produção, publicação não listada, teste sem login e evidência própria.
- **Estado:** aprovada para o escopo obrigatório da Etapa 7 em 25/10/2026.
