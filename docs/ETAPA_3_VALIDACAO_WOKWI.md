# Etapa 3 — Validação da resiliência no Wokwi

Data: 25/10/2026  
Projeto: <https://wokwi.com/projects/478851580032675841>

## Execução observada

O firmware compilou e iniciou no Wokwi. A execução final foi pausada depois da
sincronização para manter a captura visual e o log correlacionados.

```text
CLOUD_SEND seq=1 source=live
CONNECTIVITY state=offline source=serial pending=0
BUFFER_STORE seq=2 pending=1 capacity=2160 dropped_samples=0 overwritten=false
BUFFER_STORE seq=3 pending=2 capacity=2160 dropped_samples=0 overwritten=false
BUFFER_STORE seq=4 pending=3 capacity=2160 dropped_samples=0 overwritten=false
CONNECTIVITY state=online source=serial pending=3
SYNC_START pending=3 dropped_samples=0
CLOUD_SEND seq=2 source=buffered
CLOUD_SEND seq=3 source=buffered
CLOUD_SEND seq=4 source=buffered
SYNC_DONE sent=3 pending=0 dropped_samples=0
```

## Análise

- A coleta continuou offline em cadência aproximada de cinco segundos.
- As três sequências armazenadas foram enviadas exatamente uma vez.
- A ordem FIFO `2, 3, 4` foi preservada.
- Não houve perda inexplicada nem duplicação.
- O buffer terminou vazio.
- O contador de descartes permaneceu zero porque a execução não atingiu o limite.
- O estouro foi validado na mesma classe C++ com capacidade reduzida no teste
  unitário: o item mais antigo é substituído e `dropped_samples` aumenta.
- O botão consta no circuito; comandos `O` e `N` produziram a evidência
  determinística sem reiniciar o ESP32.

## Acesso público

Uma requisição sem cookies autenticados ao link retornou HTTP 200 e apresentou
o título e os arquivos `sketch.ino`, `diagram.json` e `edge_buffer.h`. O projeto
está configurado como público na conta Wokwi de Fabrício.

## Evidências

| Arquivo | Finalidade | SHA-256 |
|---|---|---|
| `E3-02-wokwi-offline-buffer.jpg` | circuito e buffer offline | `f5f4f1d132824d51492e064c56339e8242f976cbeef257e73b7a6488be495455` |
| `E3-04-log-continuo-online-offline-sync.txt` | execução extensa com seis amostras | `5895a7b41d5feb7e43aca530d8b76aed16124fdbcf523d5f4c24c8032af056c1` |
| `E3-05-wokwi-ciclo-completo-pausado.jpg` | circuito e `SYNC_DONE` correlacionados | `20c3a5cb3a5f747230f997e9e69de2a12ff809862b6544ae920ac1e3b75cba1d` |
| `E3-06-log-final-ciclo-correlacionado.txt` | log exato da captura final | `528e1e19e8795f1dd0dc1fc90d59bc75d6bb6ba5e9ea36febf73a235f3c5ab07` |

`E3-03` foi preservada como captura intermediária histórica, mas `E3-05` e
`E3-06` são a dupla autoritativa para a execução final.
