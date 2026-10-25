# Etapa 3 — Blueprint de resiliência offline no Edge

## Estado

**Em execução.** Este documento define o comportamento a ser implementado e
testado. A etapa só poderá ser encerrada após execução no Wokwi, preservação dos
logs e das capturas e aprovação de todos os testes do portão.

## Fluxo funcional

1. O ESP32 coleta DHT22 e BPM sintético a cada 5 segundos.
2. Online: envia a leitura pelo Monitor Serial como `CLOUD_SEND source=live`.
3. Offline: armazena a leitura no FIFO circular e registra `BUFFER_STORE`.
4. Reconexão: envia primeiro todas as pendências, da mais antiga à mais recente.
5. Após `SYNC_DONE`, novas leituras voltam a ser enviadas como `source=live`.
6. Se as 2.160 posições estiverem ocupadas, a leitura mais antiga é substituída
   e `dropped_samples` é incrementado.

## Capacidade e retenção

| Parâmetro | Valor |
|---|---:|
| Intervalo nominal | 5 segundos |
| Capacidade | 2.160 amostras |
| Retenção nominal | 10.800 segundos = 3 horas |
| Política de estouro | sobrescrever a mais antiga |
| Contabilização | contador monotônico `dropped_samples` |

Na disposição atual, cada `Sample` ocupa 20 bytes; as 2.160 posições reservam
43.200 bytes (aproximadamente 42,19 KiB), além de poucos bytes de controle. Esse
valor é compatível com a RAM do ESP32 simulado e permanece fixo durante a
execução, evitando fragmentação por alocação dinâmica.

O buffer vive em RAM porque o SPIFFS do simulador é volátil. A decisão atende
ao enunciado sem alegar persistência inexistente. O envio à nuvem nesta etapa é
uma simulação textual; MQTT será implementado somente na Etapa 4.

## Controles de teste

| Controle | Ação |
|---|---|
| Botão azul no GPIO 4 | alterna online/offline |
| Comando `O` | força offline |
| Comando `N` | força online e sincroniza |
| Comando `F` | injeta falha sintética do DHT22 |
| Comando `R` | remove falha sintética do DHT22 |

## Invariantes verificáveis

- uma sequência enviada do buffer não pode ser enviada novamente;
- a ordem de sincronização deve ser crescente;
- `pending` deve chegar a zero após sincronização completa;
- descarte só pode ocorrer com o buffer cheio;
- todo descarte deve aparecer em `dropped_samples`;
- a coleta deve continuar durante o período offline;
- o firmware desta etapa não pode conter cliente MQTT nem credenciais.
