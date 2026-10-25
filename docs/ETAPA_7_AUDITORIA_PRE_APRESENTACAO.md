# Etapa 7 — Auditoria antes da apresentação

## Resultado

O núcleo obrigatório da Fase 3 está implementado e possui evidências. A entrega
ainda não pode receber o estado de 100% porque depende da revisão dos quatro
integrantes, do registro inequívoco do prazo no Portal FIAP e da Etapa 8.

## Requisitos do barema

| Bloco | Evidência principal | Estado |
|---|---|---|
| Dois sensores e código C++ | DHT22, BPM sintético, circuito e logs | Aprovado |
| Resiliência offline | FIFO de 2.160 amostras, descarte observável e sincronização | Aprovado |
| MQTT e broker | Três tópicos, JSON v1 e assinante independente | Aprovado |
| Dashboard e alertas | Gráfico, gauges, estados e limites | Aprovado |
| Documentação | README, dois relatórios, PDFs e evidências | Aprovado tecnicamente |

## Verificações executadas

- Etapa 1: documentos, tópicos, contrato e revisão aprovados.
- Estrutura: 20 testes Python aprovados.
- Alertas C++: oito cenários aprovados.
- FIFO: 23 verificações aprovadas.
- Runtime offline: 10 verificações aprovadas.
- MQTT: 13 campos e 20 verificações de evidência aprovados.
- Dashboard: 35 verificações estruturais, lógicas e de segurança aprovadas.
- Integração: 38 verificações de evidência aprovadas.
- Documentação: 21 verificações aprovadas.
- GitHub, Wokwi, dashboard, PDFs e PowerPoint: HTTP 200 sem autenticação.

## Correções realizadas nesta auditoria

1. O flow passou a rejeitar enumerações inválidas de `alert` e `source`.
2. `body-parser` foi atualizado para 1.20.9 e `multer` para 2.5.0.
3. O gerenciador de paleta não permite instalação nem upload dinâmico.
4. O relatório da Parte 2 e o README foram alinhados ao comportamento atual.
5. Entradas históricas do registro de evidências agora apontam para a resolução.
6. A regra de uma única simulação do Wokwi por vez foi documentada.
7. O `package-lock.json` corrompido durante a primeira publicação da auditoria
   foi reenviado como JSON íntegro. O commit `dd83ed3` gerou o deploy
   `dep-dbf3btgm7kps73fk77b0`, marcado como `live`; o dashboard respondeu HTTP
   200 e a raiz administrativa permaneceu bloqueada com HTTP 404.

## Risco residual aceito

O `npm audit` ainda lista um alerta alto de `undici` e um moderado de
`ip-address` dentro do pacote `npm` usado pelo registro administrativo do
Node-RED. Não existe versão mais recente do Node-RED que elimine esses avisos, e
a correção automática propõe um downgrade incompatível. O Render desabilita os
endpoints administrativos com `httpAdminRoot=false`; a paleta também não pode
instalar nem receber módulos. O grupo deve reavaliar quando surgir uma versão
compatível.

## Pendências que impedem 100%

1. Obter no Portal FIAP a data e o horário exatos da entrega e registrar a
   evidência.
2. Criar a apresentação pós-auditoria e disponibilizar a versão pública.
3. Receber de cada integrante a confirmação `APROVADO SEM CORREÇÕES` ou tratar
   as correções solicitadas.
4. Concluir T7-14, T7-15 e T7-16 e emitir o encerramento formal da Etapa 7.
5. Iniciar a Etapa 8 somente após esse encerramento.
6. Na Etapa 8, revisar o barema, criar a release final, realizar a entrega no
   Portal FIAP e preservar o comprovante.

O vídeo e os desafios “Ir Além” permanecem opcionais e não bloqueiam o núcleo
obrigatório desta atividade.
