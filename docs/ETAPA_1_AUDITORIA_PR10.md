# Etapa 1 — auditoria da PR nº 10

Fonte analisada: [PR nº 10 do repositório anterior](https://github.com/FabricioMouzer/fiap-segundo-ano-2026/pull/10), branch `feat/cardioia-fase3-iot`.

## Resultado

A PR contém uma base técnica relevante, mas permanece em rascunho e não será mesclada nem copiada integralmente. O novo repositório é a fonte oficial da Fase 3.

| Elemento antigo | Classificação | Tratamento |
|---|---|---|
| DHT22 + potenciômetro + botão + LED | Reaproveitável como decisão | Revalidar ligações e arquivos exatos na Etapa 2 |
| Mapeamento do potenciômetro para 40–180 BPM | Reaproveitável | Manter e testar limites |
| Regras de alerta | Reaproveitável com ajustes | Manter limites; adicionar `sensor_valid` ao contrato |
| Buffer de 720 amostras | Substituir | Ampliar para 2.160 amostras na Etapa 3 |
| Tópicos MQTT | Inconsistente | Adotar somente a versão com `rm566777` |
| Broker público e QoS 0 | Reaproveitável com limitação | Exigir assinante independente na Etapa 4 |
| Flow `node-red-dashboard` clássico | Não transportar | Migrar para FlowFuse Dashboard 2.0 na Etapa 5 |
| Relatórios antigos | Referência textual | Atualizar apenas após testes reais |
| Testes estruturais | Reaproveitáveis como base | Adaptar ao novo repositório; não contam como execução do ESP32 |
| Prints e ensaio preliminar | Evidência histórica | Não substituem os testes controlados das novas etapas |

## Achados críticos

1. O README antigo e os arquivos executáveis já divergiram quanto ao prefixo MQTT.
2. O sketch ensaiado no Wokwi não era byte a byte igual ao arquivo oficial da branch.
3. O MQTT foi aceito localmente, mas nenhum assinante independente comprovou a recepção.
4. Não foram concluídos retorno ao normal, falha DHT22, limites exatos e cadência prolongada.
5. O flow antigo depende de pacote descontinuado.
6. A PR contém arquivos anômalos com nomes em base64 fora da pasta oficial.

## Regra de migração

Cada arquivo técnico será transportado isoladamente somente na etapa responsável, acompanhado de revisão, teste e evidência. Nenhum status de “implementado” ou “validado” será herdado automaticamente.
