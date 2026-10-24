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
| T2-07 | Falha do DHT22 | Desconectar sinal durante ensaio controlado | `sensor_valid=false`, `sensor_error`, loop continua | Aprovado | E2-02 |
| T2-08 | Limites exatos | 50/120 BPM e 38,0 °C | Permanecem normais; alertar apenas fora dos limites | Aprovado | E2-01 |
| T2-09 | Cadência | Várias amostras sem reinício | Sequência cresce e intervalo simulado é de 5.000 ms | Aprovado | E2-02 |
| T2-10 | Link público | Abrir sem sessão | Circuito e código ficam acessíveis | Pendente | Aguardando publicação |

## Controles de qualidade

- Registrar o SHA do sketch e do circuito utilizados.
- Não editar uma cópia compactada no navegador sem repetir a comparação.
- Não confundir tempo real do navegador com `uptime_ms` simulado.
- Não declarar MQTT, offline ou Node-RED como validados nesta etapa.
- Manter as capturas completas, mostrando circuito, Serial e estado dos componentes.
