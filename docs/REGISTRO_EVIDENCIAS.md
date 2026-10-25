# Registro de evidências

| ID | Etapa | Requisito | Evidência | Data | Responsável | Resultado |
|---|---:|---|---|---|---|---|
| E-001 | 0 | Repositório exclusivo e público | [CardioIA-Fase3-Monitoramento-IoT](https://github.com/FabricioMouzer/CardioIA-Fase3-Monitoramento-IoT) | 23/10/2026 | Fabrício | Aprovado |
| E-002 | 0 | Visibilidade pública | `evidencias/etapa-0/E0-01-repositorio-publico.jpg` | 23/10/2026 | Fabrício | Aprovado |
| E-003 | 0 | Acesso externo à branch principal | `git ls-remote` retornou `HEAD` e `refs/heads/main` no commit `51f950c` | 23/10/2026 | Codex | Aprovado |
| E-004 | 0 | Documentação na branch `main` | README, `.gitignore` e cinco documentos de governança lidos diretamente do GitHub | 23/10/2026 | Codex | Aprovado |
| E-101 | 1 | Matriz de requisitos e arquitetura | `docs/ETAPA_1_MATRIZ_REQUISITOS.md` e `docs/ETAPA_1_ARQUITETURA.md` | 23/10/2026 | Codex | Aprovado tecnicamente |
| E-102 | 1 | Contrato MQTT e JSON | `docs/ETAPA_1_CONTRATO_MQTT.md` e `data/exemplo-telemetria-v1.json` | 23/10/2026 | Codex | Aprovado tecnicamente |
| E-103 | 1 | Auditoria da PR nº 10 | `docs/ETAPA_1_AUDITORIA_PR10.md` | 23/10/2026 | Codex | Aprovado tecnicamente |
| E-104 | 1 | Validador executado no commit público `2fa0838` | `evidencias/etapa-1/E1-01-validacao-documental.txt` | 23/10/2026 | Codex | Aprovado |
| E-105 | 1 | Revisão dos quatro integrantes | `docs/ETAPA_1_REVISAO_GRUPO.md` | 23/10/2026 | Equipe | Aprovado |
| E-106 | 1 | Validação após aprovação coletiva | `evidencias/etapa-1/E1-03-validacao-final.txt` | 23/10/2026 | Codex | Aprovado |
| E-201 | 2 | Estrutura, circuito e lógica C++ | `evidencias/etapa-2/E2-01-validacao-estatica.txt` | 23/10/2026 | Codex | Aprovado |
| E-202 | 2 | Execução dos cenários T2-01 a T2-09 no Wokwi | `evidencias/etapa-2/E2-02-execucao-wokwi.txt` | 23/10/2026 | Codex | Aprovado |
| E-203 | 2 | Link público do projeto Wokwi | [CardioIA Fase 3 — Etapa 2](https://wokwi.com/projects/478845707855731713), aberto e executado sem sessão | 25/10/2026 | Codex | Aprovado |
| E-204 | 2 | Transições contínuas sem reinício | `evidencias/etapa-2/E2-03-transicoes-continuas.txt` | 24/10/2026 | Codex | Aprovado |
| E-205 | 2 | Captura de alerta de BPM alto e retorno ao normal | `evidencias/etapa-2/E2-03-alerta-normal-sem-reinicio.jpg` | 24/10/2026 | Codex | Aprovado |
| E-206 | 2 | Captura de falha controlada do DHT22 e recuperação | `evidencias/etapa-2/E2-04-dht-falha-recuperacao-sem-reinicio.jpg` | 24/10/2026 | Codex | Aprovado |
| E-207 | 2 | Tolerância da cadência de 5.000 ms | Medição de 5.018 ms (+18 ms; +0,36%), dentro da faixa de 5.000–5.050 ms documentada em E2-03 | 24/10/2026 | Codex | Aprovado |
| E-208 | 2 | Validação automatizada dos logs e hashes das capturas | `evidencias/etapa-2/E2-05-validacao-complementar.txt` | 24/10/2026 | Codex | 6/6 testes + 8/8 cenários aprovados |
| E-209 | 2 | Circuito e LED no estado normal | `evidencias/etapa-2/E2-06-circuito-led-normal-link-publico.jpg` | 25/10/2026 | Codex | Aprovado |
| E-210 | 2 | Circuito e LED no estado de alerta | `evidencias/etapa-2/E2-07-circuito-led-alerta-link-publico.jpg` | 25/10/2026 | Codex | Aprovado |
| E-211 | 2 | Circuito e LED após retorno ao normal | `evidencias/etapa-2/E2-08-circuito-led-recuperado-link-publico.jpg` | 25/10/2026 | Codex | Aprovado |
| E-212 | 2 | Correspondência entre link, circuito, LED e logs | `evidencias/etapa-2/E2-09-validacao-final-link-publico.txt` | 25/10/2026 | Codex | Aprovado |
| E-213 | 2 | Encerramento formal da etapa | `docs/ETAPA_2_CONCLUSAO.md` | 25/10/2026 | Codex | Aprovado |
| E-214 | 2 | Portão automatizado final e correção da inconsistência | `evidencias/etapa-2/E2-10-portao-final.txt` | 25/10/2026 | Codex | 7/7 testes + 8/8 cenários aprovados |
| E-301 | 3 | Blueprint, buffer limitado e início formal | `docs/ETAPA_3_BLUEPRINT.md` e `evidencias/etapa-3/E3-01-inicio-e-validacao-estatica.txt` | 25/10/2026 | Codex | Checkpoint inicial; execução concluída posteriormente em E-302 a E-307 |
| E-302 | 3 | Coleta offline visível | `evidencias/etapa-3/E3-02-wokwi-offline-buffer.jpg` | 25/10/2026 | Codex | Aprovado |
| E-303 | 3 | Sincronização intermediária | `evidencias/etapa-3/E3-03-wokwi-sincronizacao-concluida.jpg` | 25/10/2026 | Codex | Preservado; substituído como evidência principal por E-305/E-306 |
| E-304 | 3 | Log contínuo com seis amostras | `evidencias/etapa-3/E3-04-log-continuo-online-offline-sync.txt` | 25/10/2026 | Codex | Aprovado |
| E-305 | 3 | Captura final correlacionada | `evidencias/etapa-3/E3-05-wokwi-ciclo-completo-pausado.jpg` | 25/10/2026 | Codex | Aprovado |
| E-306 | 3 | Log final online → offline → sincronização | `evidencias/etapa-3/E3-06-log-final-ciclo-correlacionado.txt` | 25/10/2026 | Codex | 3 armazenadas, 3 sincronizadas, pendentes 0 |
| E-307 | 3 | Portão automatizado e acesso público | `evidencias/etapa-3/E3-07-validacao-final.txt` | 25/10/2026 | Codex | Aprovado |
| E-401 | 4 | Início, contrato MQTT e validação estática | `evidencias/etapa-4/E4-01-inicio-validacao-estatica.txt` | 25/10/2026 | Codex | Aprovado |
| E-402 | 4 | Compilação, Wi-Fi, broker e publicação JSON | `evidencias/etapa-4/E4-02-compilacao-conexao.jpg` | 25/10/2026 | Codex | Aprovado |
| E-403 | 4 | Recebimento por assinante independente | `evidencias/etapa-4/E4-03-assinante-independente.jpg` | 25/10/2026 | Codex | Aprovado |
| E-404 | 4 | Alerta de BPM alto e circuito | `evidencias/etapa-4/E4-04-alerta-resiliencia.jpg` | 25/10/2026 | Codex | Aprovado |
| E-405 | 4 | Log contínuo do Wokwi | `evidencias/etapa-4/E4-05-log-wokwi-serial.txt` | 25/10/2026 | Codex | Aprovado |
| E-406 | 4 | Log do cliente HiveMQ independente | `evidencias/etapa-4/E4-06-log-assinante-hivemq.txt` | 25/10/2026 | Codex | 3 tópicos e JSON recebidos |
| E-407 | 4 | Link público sem sessão | `evidencias/etapa-4/E4-07-link-publico.txt` | 25/10/2026 | Codex | HTTP 200 e arquivos públicos |
| E-408 | 4 | Portão automatizado e regressão | `evidencias/etapa-4/E4-08-validacao-automatizada.txt` | 25/10/2026 | Codex | Aprovado |
| E-409 | 4 | Encerramento formal | `docs/ETAPA_4_CONCLUSAO.md` | 25/10/2026 | Codex | Aprovado |
| E-501 | 5 | Início controlado e diagnóstico do ambiente | `evidencias/etapa-5/E5-01-inicio-da-etapa.txt` | 25/10/2026 | Codex | Aprovado |
| E-502 | 5 | Instalação isolada e importação do flow | `evidencias/etapa-5/E5-02-instalacao-e-importacao.txt` | 25/10/2026 | Codex | Aprovado; MQTT real pendente |

## Padrão de nomes

```text
evidencias/etapa-N/EN-ID-descricao.ext
```

Exemplos futuros:

```text
evidencias/etapa-2/E2-01-compilacao-wokwi.png
evidencias/etapa-3/E3-02-log-sincronizacao.txt
evidencias/etapa-5/E5-03-alerta-temperatura-alta.png
```

Uma evidência nunca deve ser substituída silenciosamente. Quando houver nova execução, criar uma nova versão ou registrar a alteração no histórico.
