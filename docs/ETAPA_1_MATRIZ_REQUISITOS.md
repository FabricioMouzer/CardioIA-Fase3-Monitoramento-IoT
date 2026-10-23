# Etapa 1 — matriz de requisitos e rastreabilidade

## Núcleo obrigatório — 10 pontos

| ID | Requisito do enunciado | Peso | Decisão de projeto | Etapa de execução | Evidência exigida |
|---|---|---:|---|---:|---|
| R-01 | ESP32 no Wokwi com pelo menos dois sensores distintos | 2 | DHT22 + potenciômetro/BPM | 2 | Link público, circuito, compilação e logs |
| R-02 | DHT22 com temperatura e umidade | 2 | GPIO15, leitura a cada 5 s | 2 | Valores coerentes e teste de falha |
| R-03 | Segundo sensor livre | 2 | Potenciômetro no ADC GPIO34, convertido para 40–180 BPM | 2 | Normal, limites, BPM baixo e alto |
| R-04 | Código C++ comentado | 2 | Firmware organizado por coleta, alerta, fila e comunicação | 2–4 | Arquivo exato compilado e revisado |
| R-05 | Resiliência sem conexão | 2 | Buffer circular FIFO de 2.160 amostras em RAM | 3 | Fila cresce offline e sincroniza em ordem |
| R-06 | Limite de armazenamento definido | 2 | Três horas a uma amostra/5 s; descarta a mais antiga ao lotar | 3 | Teste de capacidade e contador de perdas |
| R-07 | Envio MQTT para nuvem | 2 | HiveMQ público, três tópicos e JSON versão 1 | 4 | Assinante independente recebe mensagens |
| R-08 | Gráfico em tempo real | 2 | Gráfico temporal de BPM | 5 | Captura e fluxo exportado |
| R-09 | Gauge de outro parâmetro | 2 | Gauge de temperatura | 5 | Captura com valores variáveis |
| R-10 | Alerta visual automático | 2 | Estado normal/alerta + LED virtual | 2 e 5 | Cenários normal, baixo, alto, febre e falha |
| R-11 | Relatório Edge com pelo menos uma página | 2 | Relatório atualizado após testes | 7 | Documento coerente com os logs |
| R-12 | Relatório MQTT/dashboard com pelo menos duas páginas | 2 | Relatório atualizado após integração | 7 | Documento coerente com MQTT e dashboard |
| R-13 | Prints ou export do dashboard | 2 | Export JSON + capturas legíveis | 5–7 | Arquivos públicos no repositório |
| R-14 | Documentação clara | 2 | README, arquitetura, contratos, testes e limitações | todas | Auditoria sem contradições |

Os pesos são aplicados aos cinco critérios do barema: sensores, resiliência, MQTT, dashboard e documentação. Requisitos associados compartilham o mesmo bloco de pontuação; a soma máxima permanece 10.

## Entregáveis obrigatórios

| Entregável | Caminho previsto | Estado na Etapa 1 |
|---|---|---|
| Link público do Wokwi | README e relatório Edge | Planejado; não criado |
| Firmware C++ | `wokwi/sketch.ino` | Rascunho na PR nº 10; ainda não transportado |
| Circuito | `wokwi/diagram.json` | Rascunho na PR nº 10; ainda não transportado |
| Relatório Edge | `docs/RELATORIO_EDGE_COMPUTING.md` | Base antiga; exige atualização após testes |
| Flow Node-RED | `node-red/cardioia-dashboard-flow.json` | Flow clássico antigo; será migrado na Etapa 5 |
| Relatório MQTT/dashboard | `docs/RELATORIO_MQTT_DASHBOARD.md` | Base antiga; exige atualização após testes |
| Evidências | `evidencias/etapa-N/` | Obrigatórias antes de cada confirmação |

## Itens opcionais

- SPIFFS em hardware físico: não integra o caminho obrigatório no simulador.
- Grafana Cloud: somente após o dashboard obrigatório estar aprovado.
- REST e e-mail: “Ir Além 1”, bloqueado até o núcleo obrigatório estar estável.
- IA em séries temporais e vídeo de quatro minutos: “Ir Além 2”, bloqueado até o núcleo obrigatório estar estável.
- O vídeo não é requisito do núcleo obrigatório desta fase; se o grupo optar pelo Ir Além 2, deverá ser publicado como não listado e testado sem autenticação.

## Pendência administrativa

O texto transcrito do enunciado disponível no histórico não exibe de forma inequívoca a data e o horário de encerramento. Essa informação deverá ser registrada a partir do Portal FIAP antes da Etapa 8 e não será inventada.
