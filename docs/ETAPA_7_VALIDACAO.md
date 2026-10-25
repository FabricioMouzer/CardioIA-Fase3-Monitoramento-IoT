# Etapa 7 — Validação documental parcial

## Estado

Os entregáveis técnicos da Etapa 7 estão preparados e validados. O portão
permanece aberto porque os quatro integrantes ainda precisam revisar e aprovar
o pacote.

## Artefatos produzidos

| Artefato | Resultado técnico |
|---|---|
| Relatório Parte 1 | PDF A4 com quatro páginas e links clicáveis |
| Relatório Parte 2 | PDF A4 com cinco páginas e links clicáveis |
| README | arquitetura, tecnologias, execução, limites e acessos |
| PowerPoint | 12 slides, 9 imagens incorporadas e 5 links públicos |
| Revisão do grupo | checklist e mensagem de WhatsApp preparados |

## Revisão visual

As nove páginas dos relatórios foram renderizadas e inspecionadas em tamanho
integral. Uma primeira paginação com duas páginas quase vazias foi rejeitada. As
quebras foram corrigidas e a versão atual não apresenta corte, sobreposição,
página vazia ou texto ilegível.

Os 12 slides também foram renderizados e inspecionados. A primeira exportação
do PowerPoint mostrou espaços reservados em vez das capturas e setas invertidas
na arquitetura. Essa versão não foi publicada. A versão `v2` incorpora as
imagens no arquivo, corrige o fluxo e ajusta o slide do dashboard.

## Validação automatizada

O script [`tests/validate_stage7_artifacts.py`](../tests/validate_stage7_artifacts.py)
aprovou 21 verificações, incluindo existência e tamanho dos arquivos, número de
páginas, conteúdo técnico, anotações de links nos PDFs, 12 slides, imagens
incorporadas, cinco hyperlinks e referências no README.

A regressão preservou os resultados das Etapas 1–6: 38 verificações integradas,
35 verificações do dashboard, 20 verificações MQTT, 20 testes estruturais, 23
verificações do FIFO, oito cenários de alerta e validação documental da Etapa 1.

## Correção durante a revisão

Uma verificação manual do grupo encontrou o cartão **Dispositivo** em
`offline_unexpected`, embora o dashboard estivesse disponível. O endpoint
respondia HTTP 200; o valor era o Last Will retido de uma sessão anterior. Uma
nova simulação comprovou o buffer da primeira amostra, a sincronização com fila
zero e o recebimento de telemetria ao vivo. Como o cartão ainda conservava o
status antigo, o flow foi corrigido para que toda telemetria válida reafirme
`online (telemetria ativa)`, sem remover o Last Will. A ocorrência, a causa, os
logs e a validação estão em
[`E7-04-diagnostico-status-dashboard.txt`](../evidencias/etapa-7/E7-04-diagnostico-status-dashboard.txt).
O commit `d309109` foi implantado no Render e o reteste público mostrou
sequência `#3`, origem `live`, fila e descartes zerados, 110 BPM no gráfico e o
dispositivo como `online (telemetria ativa)`.
Para impedir nova interpretação equivocada, a apresentação do Last Will também
foi traduzida para `offline — inicie o Wokwi`, mantendo
`offline_unexpected` inalterado no contrato MQTT.
O commit `83090f3` foi implantado e validado no endereço público com o Wokwi
deliberadamente parado; a mensagem orientativa apareceu com fila e descartes
zerados.

Na auditoria pré-apresentação, a primeira publicação do novo
`package-lock.json` chegou corrompida ao GitHub e o Render rejeitou `npm ci`.
O arquivo local já validado foi reenviado em codificação binária segura no
commit `dd83ed3`. O deploy `dep-dbf3btgm7kps73fk77b0` ficou `live`; no reteste,
`/dashboard/monitoramento` respondeu HTTP 200 e a raiz administrativa respondeu
HTTP 404.

## Hashes SHA-256

```text
2bd248d778eb8519c00f1b113e7fe29cba5f380d033e270f3d4708741f51ae4e  CardioIA_Parte_1_Edge_Computing.pdf
26ec56f00c1bcaccd0dcd09eee3274312153dede29dad8d500684465ea70ea81  CardioIA_Parte_2_MQTT_Dashboard.pdf
9b93c0ef6f7319e48661964d6474ce27192f01bda2503bb72371b058ca439eb2  CardioIA_Fase3_Apresentacao_Equipe_v2.pptx
```

## Pendências para encerramento

1. receber a revisão dos quatro integrantes;
2. resolver eventuais correções;
3. registrar a aprovação coletiva.

Enquanto esses itens não forem concluídos, a Etapa 7 não receberá a mensagem de
encerramento e a Etapa 8 continuará bloqueada.
