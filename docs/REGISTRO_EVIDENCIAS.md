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
