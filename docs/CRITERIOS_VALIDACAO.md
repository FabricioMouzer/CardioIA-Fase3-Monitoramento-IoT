# Critérios de validação e evidências

## Estados permitidos

| Estado | Significado |
|---|---|
| Bloqueada | A etapa anterior ainda não foi concluída. |
| Planejada | Escopo definido, sem execução iniciada. |
| Em execução | Trabalho iniciado, ainda sem validação completa. |
| Em correção | Uma evidência ou teste falhou. |
| Aguardando revisão | Testes aprovados, aguardando revisão do grupo. |
| Confirmada e finalizada | Critérios, evidências e revisão aprovados. |

## Evidência mínima aceitável

Uma evidência deve registrar:

- requisito comprovado;
- data da execução;
- ambiente utilizado;
- passos do teste;
- resultado esperado;
- resultado observado;
- arquivo, link, print ou log correspondente;
- responsável pela execução;
- status aprovado/reprovado.

## O que não é evidência

- texto afirmando que funcionou sem log, print ou teste;
- código que ainda não foi executado;
- link que exige acesso não disponibilizado ao avaliador;
- print cortado sem contexto suficiente;
- vídeo indicado no README, mas ausente ou inacessível;
- checklist marcado antes da execução.

## Mensagem obrigatória de encerramento

Ao concluir uma etapa, publicar:

```text
✅ ETAPA N CONFIRMADA E FINALIZADA

Entregáveis: [lista]
Testes aprovados: [lista]
Evidências: [links/caminhos]
Pendências críticas: nenhuma
Próxima etapa liberada: Etapa N+1
```

Se houver qualquer pendência crítica, a mensagem de conclusão não poderá ser emitida.
