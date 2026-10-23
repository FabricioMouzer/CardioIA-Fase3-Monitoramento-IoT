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
