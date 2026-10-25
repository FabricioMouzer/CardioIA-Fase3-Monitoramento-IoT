# Lições aprendidas — Fases anteriores

## Práticas que devem ser preservadas

- manter estrutura clara de pastas e documentação abrangente;
- garantir reprodutibilidade com instruções completas de instalação e execução;
- utilizar testes automatizados sempre que possível;
- documentar métricas, limitações, governança, vieses e riscos;
- separar dados sintéticos de qualquer dado real;
- testar links fora da conta autenticada;
- registrar resultados observados, não apenas resultados esperados.

## Erros que não podem se repetir

### 1. Entregável obrigatório sem comprovação

Na Fase 2, o vídeo estava citado, mas sua publicação não ficou comprovada e o checklist ainda o indicava como pendente.

**Regra para a Fase 3:** nenhum link ou vídeo será declarado concluído antes de abrir sem login e demonstrar o requisito correto.

### 2. Documentação contraditória

O estado declarado da entrega não pode divergir do checklist ou das evidências.

**Regra para a Fase 3:** antes de encerrar cada etapa, pesquisar por `pendente`, `TODO`, `[ ]`, `aguardando` e afirmações de conclusão.

### 3. Pouca diversidade de cenários

A avaliação anterior recomendou ampliar formas de expressão e situações inéditas.

**Aplicação na Fase 3:** testar faixas normais, limites, valores acima/abaixo dos limites, falha do sensor, perda de conexão, retorno da conexão e entradas atípicas.

### 4. Falsos negativos em situações críticas

Na Fase 2, os falsos negativos de alto risco exigiam prioridade.

**Aplicação na Fase 3:** testar especialmente se condições críticas deixam de acionar alertas, incluindo valores exatamente nos limites e mudanças rápidas.

### 5. Generalização insuficiente

A avaliação recomendou conjuntos independentes e frases inéditas.

**Aplicação na Fase 3:** repetir os testes em duas execuções independentes e variar os dados de entrada, sem depender de uma única sequência preparada.

### 6. Modelos ou componentes fracos devem ser investigados

A baixa acurácia da Árvore de Decisão mostrou que apresentar uma alternativa sem entender seu mau desempenho não é suficiente.

**Aplicação na Fase 3:** qualquer sensor, fluxo, regra ou dashboard que falhar deve receber análise de causa, correção e novo teste antes da aprovação.

## Definição de pronto

Uma etapa está pronta somente quando funciona, é reproduzível, está documentada, possui evidências acessíveis e não contém contradições.

## Lições confirmadas na Etapa 4

- `publish()` retornar verdadeiro comprova apenas aceitação local; o recebimento
  deve ser demonstrado por um assinante MQTT independente;
- transferência de código pode alterar escapes; toda versão publicada deve ser
  recompilada no ambiente de destino;
- status retido, alerta e telemetria precisam ser conferidos separadamente;
- uma reconexão só está concluída quando o FIFO chega a zero e o assinante
  externo recebe as amostras pendentes;
- o broker público serve somente para dados sintéticos e testes educacionais.

## Lições confirmadas na Etapa 6

- reiniciar o simulador e observar `sequence=1` é a evidência objetiva de uma
  nova execução independente;
- a sequência do payload é um correlator mais confiável que o horário visual;
- uma leitura inválida do DHT22 na inicialização deve ser preservada no log e
  seguida de comprovação explícita de recuperação;
- testar exatamente 50 BPM, 120 BPM e 38,0 °C evita ambiguidade nas fronteiras;
- uma sincronização somente termina quando a ordem é preservada, a fila chega a
  zero, o fluxo `live` retorna e `dropped_samples` permanece zero;
- desempenho insuficiente do simulador invalida a tentativa, não o requisito:
  a execução deve ser reiniciada em ambiente estável e documentada novamente.
