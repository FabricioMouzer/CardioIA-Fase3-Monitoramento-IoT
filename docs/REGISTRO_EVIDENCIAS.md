# Registro de evidências

| ID | Etapa | Requisito | Evidência | Data | Responsável | Resultado |
|---|---:|---|---|---|---|---|
| E-001 | 0 | Repositório exclusivo e público | [CardioIA-Fase3-Monitoramento-IoT](https://github.com/FabricioMouzer/CardioIA-Fase3-Monitoramento-IoT) | 23/10/2026 | Fabrício | Aprovado |
| E-002 | 0 | Visibilidade pública | `evidencias/etapa-0/E0-01-repositorio-publico.jpg` | 23/10/2026 | Fabrício | Aprovado |
| E-003 | 0 | Acesso externo à branch principal | `git ls-remote` retornou `HEAD` e `refs/heads/main` no commit `51f950c` | 23/10/2026 | Codex | Aprovado |
| E-004 | 0 | Documentação na branch `main` | README, `.gitignore` e cinco documentos de governança lidos diretamente do GitHub | 23/10/2026 | Codex | Aprovado |

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
