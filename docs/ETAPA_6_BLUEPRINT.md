# Etapa 6 — Blueprint do teste integrado

## Objetivo

Comprovar a repetibilidade do fluxo completo do CardioIA em duas execuções
independentes, correlacionando sequência, logs e capturas desde o ESP32 simulado
até o dashboard público.

## Fluxo sob teste

```text
DHT22 + potenciômetro → ESP32/Wokwi → buffer Edge → HiveMQ → Node-RED/Render
→ validação do contrato → gráfico, gauges, estado e alerta
```

## Execução A — conectividade e risco elevado

1. iniciar uma nova simulação;
2. confirmar estado normal e publicação ao vivo;
3. provocar BPM alto e confirmar alerta;
4. retornar ao normal sem reiniciar;
5. interromper a conectividade simulada;
6. acumular pelo menos três amostras no FIFO;
7. restaurar a conexão e confirmar sincronização ordenada até fila zero;
8. confirmar o dashboard recebendo novamente dados ao vivo.

## Execução B — diversidade, falha e limites

1. iniciar outra simulação independente;
2. confirmar estado normal;
3. provocar BPM baixo e confirmar alerta;
4. injetar falha do DHT22 e confirmar alerta explícito;
5. recuperar o sensor sem reiniciar;
6. testar exatamente 50 BPM, 120 BPM e 38,0 °C como valores normais;
7. restaurar 110 BPM e 36,5 °C;
8. confirmar fila e descartes em zero.

## Correlação obrigatória

Cada execução deve preservar:

- log serial contínuo com números de sequência;
- captura do Wokwi com contexto do circuito;
- captura do dashboard com estado, sequência, origem e fila;
- horário/data da execução;
- resultado esperado e observado;
- registro de falhas, correções e nova execução, quando houver.

## Critério de repetibilidade

As duas execuções devem partir de reinicializações diferentes, alcançar o
estado final normal e não apresentar perda não explicada, alerta falso negativo,
fila pendente ou descarte de amostras.

## Portão

A Etapa 6 somente poderá ser encerrada após as duas execuções, a correlação das
evidências, a regressão completa das Etapas 1–5 e a busca por contradições.
