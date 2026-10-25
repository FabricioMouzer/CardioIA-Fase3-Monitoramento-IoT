# Conclusão da Etapa 4 — MQTT e broker

**Data:** 25/10/2026  
**Estado:** confirmada e finalizada  
**Wokwi:** https://wokwi.com/projects/478851580032675841

## Entregáveis concluídos

- broker público configurado para dados exclusivamente sintéticos;
- conexão Wi-Fi e MQTT com reconexão limitada a uma tentativa a cada 5 s;
- três tópicos documentados e validados;
- payload JSON versão 1 compatível com o contrato da Etapa 1;
- status retido e Last Will configurados;
- telemetria e alertas publicados sem retenção;
- buffer Edge sincronizado em FIFO somente após aceitação da publicação;
- assinante independente comprovando o recebimento ponta a ponta;
- código, testes, logs e capturas preservados no GitHub.

## Portão de qualidade

Todos os critérios T4-01 a T4-13 foram aprovados. A Etapa 5 está tecnicamente
liberada, mas não foi iniciada neste encerramento. Node-RED não foi instalado,
configurado nem declarado validado durante a Etapa 4.

## Lições aplicadas

- publicação aceita localmente não foi tratada como prova de recebimento;
- o cliente independente eliminou a lacuna de evidência observada em trabalhos anteriores;
- a falha inicial de compilação foi registrada, corrigida e retestada;
- o link público foi testado sem sessão;
- não há vídeo ou entregável marcado como pronto sem evidência correspondente.
