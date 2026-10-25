# Etapa 5 — Blueprint do dashboard e alertas

## Objetivo

Construir e validar um dashboard Node-RED Dashboard 2.0 que receba o contrato
MQTT aprovado na Etapa 4 e exiba os sinais sintéticos do CardioIA em tempo real.

## Arquitetura desta etapa

```text
HiveMQ público
  ├─ /telemetria ─> validação JSON ─> gráfico BPM
  │                                  ├> gauge temperatura
  │                                  ├> gauge umidade
  │                                  └> indicador de alerta
  ├─ /alerta ─────> auditoria/debug
  └─ /status ─────> estado do dispositivo e fila Edge
```

## Hierarquia visual

1. estado do dispositivo e alerta atual;
2. gráfico temporal de BPM;
3. gauge de temperatura;
4. gauge de umidade;
5. sequência, origem (`live`/`buffered`) e pendências do Edge.

## Regras clínicas sintéticas

- normal: BPM entre 50 e 120 e temperatura até 38,0 °C;
- BPM baixo: menor que 50;
- BPM alto: maior que 120;
- temperatura alta: maior que 38,0 °C;
- falha do sensor: `sensor_valid=false` ou bit 8 ativo.

Valores exatamente 50, 120 e 38,0 são normais conforme o firmware. O protótipo
é educacional e não realiza diagnóstico médico.

## Estratégia de validação

- validar o JSON e os 13 campos antes de atualizar widgets;
- descartar entradas incompatíveis e registrar o motivo;
- importar o flow em runtime limpo sem nós desconhecidos;
- usar entradas de teste determinísticas para quatro cenários;
- receber MQTT real do Wokwi após os testes controlados;
- preservar flow exportado, logs e capturas.

## Portão

A Etapa 5 só termina quando o dashboard tiver sido renderizado e os estados
normal, BPM alto, BPM baixo, temperatura alta e falha de sensor estiverem
comprovados. Código ou flow não executado não constitui evidência.
