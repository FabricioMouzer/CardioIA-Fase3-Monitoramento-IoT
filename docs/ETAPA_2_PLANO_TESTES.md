# Etapa 2 — plano de testes dos sensores e circuito

## Critério de saída

A Etapa 2 somente poderá ser finalizada quando os arquivos exatos da branch `main` forem executados no Wokwi e as evidências abaixo forem preservadas.

| ID | Cenário | Entrada | Resultado esperado | Estado | Evidência |
|---|---|---|---|---|---|
| T2-01 | Compilação e boot | Arquivos exatos da `main` | Simulação inicia sem erro e imprime `BOOT` | Aprovado | E2-02 |
| T2-02 | Normal | 36,5 °C, 55%, BPM entre 50–120 | `alert_code=0`, `alert=normal`, LED apagado | Aprovado | E2-02 |
| T2-03 | BPM baixo | Potenciômetro mínimo | BPM 40, `low_bpm`, LED aceso | Aprovado | E2-02 |
| T2-04 | BPM alto | Potenciômetro máximo | BPM 180, `high_bpm`, LED aceso | Aprovado | E2-02 |
| T2-05 | Temperatura alta | DHT22 acima de 38,0 °C | `high_temperature`, LED aceso | Aprovado | E2-02 |
| T2-06 | Retorno ao normal | Restaurar valores normais | Alerta volta a `normal`, LED apaga | Aprovado | E2-02 |
| T2-07 | Falha do DHT22 | Comando serial `F` e depois `R`, sem reinício | `sensor_valid=false`, `sensor_error` e recuperação posterior | Aprovado | E2-03 + captura E2-04 |
| T2-08 | Limites exatos | 50/120 BPM e 38,0 °C | Permanecem normais; alertar apenas fora dos limites | Aprovado | E2-01 |
| T2-09 | Cadência | Várias amostras sem reinício | Intervalo nominal de 5.000 ms; aceitar atraso de até 1% (5.000–5.050 ms) | Aprovado: 5.018 ms, +18 ms/+0,36% | E2-02 + E2-03 |
| T2-10 | Link público | Abrir sem sessão | Circuito e código ficam acessíveis | Pendente | Aguardando publicação |
| T2-11 | Transições contínuas | Alterar alerta e falha sem reiniciar | Sequência comprova `alerta → normal` e `falha DHT22 → recuperação` | Aprovado | E2-03 |
| T2-12 | Capturas preservadas | Capturar circuito, LED e Serial nos ensaios | Imagens legíveis, versionadas e vinculadas ao registro | Parcial: Serial preservado; faltam vistas completas do circuito/LED | E2-03 e E2-04 (JPG) |

## Controles de qualidade

- Registrar o SHA do sketch e do circuito utilizados.
- Não editar uma cópia compactada no navegador sem repetir a comparação.
- Não confundir tempo real do navegador com `uptime_ms` simulado.
- Não declarar MQTT, offline ou Node-RED como validados nesta etapa.
- Manter as capturas completas, mostrando circuito, Serial e estado dos componentes.
- A Etapa 2 não será encerrada apenas com a publicação do link: T2-10, T2-11 e T2-12 devem estar aprovados.

## Portão de conclusão

- [ ] T2-10 — link público do Wokwi salvo e aberto sem sessão.
- [x] T2-11 — logs contínuos preservados, sem segundo `BOOT`.
- [ ] T2-12 — capturas do Serial preservadas e identificadas por hash; faltam as vistas completas do circuito e do LED nos estados de alerta e normal.

Enquanto qualquer caixa estiver desmarcada, a Etapa 2 permanece **em execução** e a Etapa 3 permanece bloqueada.
