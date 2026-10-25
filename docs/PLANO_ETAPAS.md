# Plano executável por etapas

## Regra de passagem

A passagem entre etapas exige quatro condições simultâneas:

- checklist da etapa sem pendências críticas;
- evidências salvas nos caminhos definidos;
- validação técnica executada;
- mensagem `ETAPA N CONFIRMADA E FINALIZADA` registrada no histórico do projeto.

Se qualquer condição falhar, o estado será `BLOQUEADA` ou `EM CORREÇÃO`.

## Etapa 0 — Governança e repositório

### Entregáveis

- repositório exclusivo e público;
- README com equipe e regra de passagem;
- plano por etapas;
- critérios de validação;
- lições aprendidas;
- registro de evidências;
- registro de decisões.

### Evidências

- URL pública do repositório;
- captura da página inicial mostrando a visibilidade pública;
- leitura sem autenticação;
- arquivos de governança presentes na branch principal.

### Critério de saída

Todos os entregáveis acima devem estar disponíveis publicamente e sem contradições.

## Etapa 1 — Requisitos e arquitetura

### Entregáveis

- matriz completa do enunciado e do barema;
- arquitetura Edge → MQTT → Fog/Cloud → Dashboard → Alerta;
- escolha justificada do segundo sensor;
- contrato JSON e tópicos MQTT;
- estratégia de resiliência e limite de armazenamento;
- estratégia de segurança e dados sintéticos.

### Evidências

- rastreabilidade de cada requisito para um arquivo e um teste planejado;
- revisão do grupo registrada.

## Etapa 2 — Sensores e circuito no Wokwi

### Entregáveis

- ESP32 com DHT22;
- segundo sensor aprovado na Etapa 1;
- código C++ comentado;
- circuito funcional;
- link público do Wokwi.

### Evidências

- compilação sem erro;
- captura do circuito;
- log de leituras coerentes;
- teste de valores normais e limites;
- link aberto em janela anônima.

## Etapa 3 — Resiliência offline

### Entregáveis

- estratégia de armazenamento limitado;
- coleta mantida sem conexão;
- sincronização ordenada após reconexão;
- tratamento de limite excedido.

### Evidências

- log antes, durante e depois da interrupção;
- quantidade de amostras acumuladas e sincronizadas;
- teste do limite e política de descarte;
- ausência de duplicação ou perda não explicada.

## Etapa 4 — MQTT e broker

### Entregáveis

- broker configurado;
- publicação dos sinais em JSON;
- tópicos documentados;
- reconexão e tratamento de falhas.

### Evidências

- mensagens reais recebidas por um cliente assinante;
- payload validado contra o contrato;
- testes de conexão, desconexão e retorno;
- nenhuma credencial versionada.

## Etapa 5 — Node-RED e alertas

### Entregáveis

- Node-RED instalado;
- flow exportado;
- gráfico do sinal escolhido;
- gauge de outro parâmetro;
- indicador visual de alerta;
- limites documentados.

### Evidências

- importação do flow sem nós desconhecidos;
- dashboard recebendo MQTT em tempo real;
- capturas dos estados normal, BPM alto, BPM baixo e temperatura alta;
- teste dos valores exatamente nos limites.

## Etapa 6 — Teste integrado

### Entregáveis

- plano de testes ponta a ponta;
- execução completa do fluxo;
- registro de falhas e correções;
- teste de repetibilidade.

### Evidências

- captura e logs correlacionados por horário/sequência;
- duas execuções independentes;
- checklist de regressão aprovado.

## Etapa 7 — Documentação, vídeo e revisão

### Entregáveis

- relatório da Parte 1 com pelo menos uma página;
- relatório da Parte 2 com pelo menos duas páginas;
- README final;
- apresentação profissional em PowerPoint com links públicos para GitHub,
  Wokwi, relatórios e evidências;
- vídeo, se exigido/planejado;
- revisão dos quatro integrantes.

### Evidências

- links funcionando sem login;
- vídeo publicado e testado, quando aplicável;
- documentação consistente com o estado real;
- aprovação registrada do grupo.

## Etapa 8 — Auditoria e entrega

### Entregáveis

- matriz do barema final;
- auditoria de segredos, links e arquivos;
- tag/release final;
- comprovante da entrega.

### Evidências

- acesso anônimo validado;
- todos os critérios do barema associados a evidências;
- ausência de `TODO`, “pendente” ou afirmações contraditórias não justificadas;
- comprovante preservado no local definido.
