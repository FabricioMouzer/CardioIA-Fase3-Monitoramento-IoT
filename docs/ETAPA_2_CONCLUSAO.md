# Etapa 2 — conclusão formal

Data: 25/10/2026  
Projeto público: <https://wokwi.com/projects/478845707855731713>

## ✅ ETAPA 2 CONFIRMADA E FINALIZADA

**Entregáveis:** ESP32, DHT22, potenciômetro como sensor sintético de BPM, LED de alerta, código C++ comentado, biblioteca declarada, circuito funcional e link público do Wokwi.

**Testes aprovados:** T2-01 a T2-12; 7/7 testes automatizados de estrutura; 8/8 cenários da lógica C++; execução pública `normal → high_bpm → normal`; falha controlada do DHT22 e recuperação; cadência validada.

**Evidências:** `evidencias/etapa-2/`, especialmente E2-03, E2-04, E2-06, E2-07, E2-08, E2-09 e E2-10.

**Pendências críticas:** nenhuma.

**Próxima etapa liberada:** Etapa 3, porém **não iniciada** por determinação expressa de Fabrício.

A Etapa 3 não foi iniciada.

## Índice de acesso

- Repositório: <https://github.com/FabricioMouzer/CardioIA-Fase3-Monitoramento-IoT>
- Projeto Wokwi: <https://wokwi.com/projects/478845707855731713>
- Plano de testes: `docs/ETAPA_2_PLANO_TESTES.md`
- Relatório de validação: `docs/ETAPA_2_VALIDACAO_WOKWI.md`
- Registro geral: `docs/REGISTRO_EVIDENCIAS.md`
- Logs contínuos: `evidencias/etapa-2/E2-03-transicoes-continuas.txt`
- Validação final do link: `evidencias/etapa-2/E2-09-validacao-final-link-publico.txt`
- Portão automatizado final: `evidencias/etapa-2/E2-10-portao-final.txt`

## Verificação final

- O link abriu e executou com `SIGN IN / SIGN UP` visível, sem sessão autenticada.
- Nenhuma solicitação adicional de acesso ao GitHub foi apresentada.
- Circuito, estado do LED e logs foram capturados juntos.
- Os logs e as imagens representam a mesma sequência e os mesmos valores.
- O intervalo de 5.018 ms está dentro da tolerância documentada de até 1%.
- Nenhum item de MQTT, resiliência offline ou Node-RED foi iniciado ou declarado validado.
