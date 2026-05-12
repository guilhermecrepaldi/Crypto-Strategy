# Handoff de Pesquisa e Benchmark — Quant Strategy Loop

## 1. Objetivo do projeto

O **Quant Strategy Loop** é um sistema de simulação evolutiva de estratégias quantitativas.

O objetivo **não é prever tendência** e **não é operar automaticamente no início**.

O objetivo é:

> Receber uma estratégia, simular sua execução histórica desde uma data definida, registrar todas as operações, avaliar o desempenho, gerar um relatório técnico e propor uma nova estratégia candidata para o próximo ciclo.

Exemplo de pergunta central:

> Se eu tivesse iniciado esta estratégia em 01/01/2025 com 1 BTC de capital, quanto eu teria hoje?

---

## 2. Conceito operacional

O sistema funciona em ciclos:

```text
STR-0001 criada
↓
Simulação histórica
↓
Log completo de operações
↓
Avaliação estatística
↓
Relatório Markdown + JSON
↓
Diagnóstico da estratégia
↓
Proposta de STR-0002
↓
Nova simulação
↓
Comparação STR-0001 vs STR-0002
↓
Repetição do loop
```

Cada rodada deve gerar um caso auditável.

Nada de “deu bom”.  
Cada resultado precisa deixar rastro.

---

## 3. Benchmark técnico

### 3.1 VectorBT / VectorBT PRO

**Função:** backtesting vetorizado em alta velocidade usando estruturas pandas/NumPy, com aceleração para testar muitas combinações de parâmetros.

**Uso recomendado no projeto:**  
Motor principal de simulação rápida para testar muitas variações de uma estratégia.

**Ponto forte:** velocidade.

**Ponto de atenção:** pode ficar menos intuitivo para estratégias altamente event-driven, com lógica muito condicional.

---

### 3.2 LEAN / QuantConnect

**Função:** engine open-source institucional para pesquisa, backtesting e trading ao vivo.

**Uso recomendado no projeto:**  
Referência arquitetural para logs, eventos, custos, slippage, ordens e simulação mais realista.

**Ponto forte:** maturidade e estrutura profissional.

**Ponto de atenção:** ecossistema mais pesado; pode ser exagerado para o MVP local.

---

### 3.3 Freqtrade

**Função:** bot open-source de trading cripto em Python, com backtesting, hyperopt, webserver e ferramentas de gestão de estratégia.

**Uso recomendado no projeto:**  
Referência para organização de estratégias, configuração, proteção de capital, backtesting cripto e interface operacional.

**Ponto forte:** já nasceu para cripto.

**Ponto de atenção:** o projeto não deve virar apenas um clone de bot trader. Nosso diferencial é o **loop evolutivo documentado**.

---

### 3.4 Backtrader

**Função:** framework Python popular para backtesting baseado em estratégias, indicadores e analyzers.

**Uso recomendado no projeto:**  
Referência didática para separação entre dados, estratégia, broker, analyzers e resultado.

**Ponto forte:** arquitetura clara.

**Ponto de atenção:** tende a ser mais lento que abordagens vetorizadas para testes massivos.

---

## 4. Decisão arquitetural sugerida

Para o MVP, a melhor direção é:

```text
VectorBT como motor rápido de simulação
+
PostgreSQL/TimescaleDB para persistência futura
+
DuckDB + Parquet para protótipo local
+
Streamlit ou Dash para dashboard inicial
+
Markdown + JSON para relatórios de rodada
+
Docker para empacotamento
```

LEAN e Freqtrade devem ser estudados como referência, mas não necessariamente usados como base principal agora.

### Opinião arquitetural

Começar com LEAN pode deixar o projeto grande demais.  
Começar com Freqtrade pode desviar o foco para bot.  
Começar com VectorBT deixa o MVP rápido e alinhado com o objetivo: **simular muita coisa, comparar e registrar**.

---

## 5. Componentes principais

### 5.1 Data Ingestion

Responsável por coletar e padronizar dados.

Fontes iniciais:

- candles de exchange;
- dados via `ccxt`;
- CSV manual;
- taxas;
- pares BTC, ETH e PENDLE;
- dados on-chain em fase futura.

Dados mínimos:

- timestamp;
- open;
- high;
- low;
- close;
- volume;
- exchange;
- symbol;
- timeframe.

---

### 5.2 Strategy Registry

Cadastro de estratégias testáveis.

Cada estratégia precisa ter:

- ID único;
- nome;
- versão;
- família;
- hipótese;
- regras de entrada;
- regras de saída;
- stop;
- alvo;
- gestão de posição;
- custos considerados;
- parâmetros variáveis;
- estratégia anterior de origem, quando houver.

Exemplo:

```text
STR-0001 — RSI Reversal Basic
STR-0002 — RSI Reversal + Trend Filter
STR-0003 — RSI Reversal + ATR Stop
```

---

### 5.3 Simulation Engine

Responsável por rodar o backtest.

Entrada:

- estratégia;
- ativo;
- período;
- timeframe;
- capital inicial;
- taxa;
- slippage;
- regra de alocação;
- restrições de risco.

Saída:

- curva de capital;
- lista de trades;
- métricas;
- diagnóstico;
- arquivos `.md` e `.json`.

---

### 5.4 Operation Log

Cada operação simulada deve ser registrada.

Campos mínimos:

```text
trade_id
strategy_id
run_id
asset
entry_datetime
entry_price
entry_reason
exit_datetime
exit_price
exit_reason
gross_result
fees
slippage
net_result
capital_before
capital_after
duration
status
```

Esse log é obrigatório.  
Sem ele, o projeto perde o valor.

---

### 5.5 Evaluation Engine

Avalia a estratégia.

Métricas principais:

- capital inicial;
- capital final;
- retorno líquido;
- drawdown máximo;
- taxa de acerto;
- profit factor;
- payoff médio;
- número de trades;
- maior sequência de perdas;
- custo total com taxas;
- exposição ao mercado;
- comparação com buy and hold;
- regularidade mensal;
- sensibilidade ao slippage.

---

## 6. Score Operacional

Criar um score padronizado de 0 a 100.

Sugestão:

| Critério | Peso |
|---|---:|
| Retorno líquido ajustado ao benchmark | 20% |
| Drawdown máximo | 20% |
| Profit factor | 15% |
| Estabilidade mensal/semanal | 15% |
| Quantidade mínima de trades | 10% |
| Sequência máxima de perdas | 10% |
| Sensibilidade a custos/slippage | 5% |
| Simplicidade da estratégia | 5% |

Classificação:

```text
0–39   Reprovada
40–59  Fraca
60–74  Promissora
75–89  Forte
90–100 Excelente, exige validação fora da amostra
```

Importante: score alto **não autoriza operação real**. Ele apenas prioriza estudo.

---

## 7. Controle contra overfitting

O sistema precisa impedir autoengano.

Regras obrigatórias:

- mínimo de trades por período;
- comparação com buy and hold;
- validação fora da amostra;
- teste em subperíodos;
- penalidade para estratégias complexas demais;
- teste de slippage maior;
- teste de aumento de taxa;
- Monte Carlo opcional;
- walk-forward em fase posterior.

Regra de ouro:

> Estratégia que só funciona em um recorte perfeito não é estratégia; é coincidência estatística bem vestida.

---

## 8. Formato de saída Markdown

```markdown
# Relatório de Simulação: [ID_ESTRATEGIA]

**Run ID:** [RUN-XXXX]  
**Status:** [Aprovada | Reprovada | Promissora | Estudo]  
**Período:** 01/01/2025 - [Data_Atual]  
**Ativos:** [ETH/BTC, PENDLE/BTC]  
**Timeframe:** [10m]  
**Capital Inicial:** [1.00 BTC]

---

## 1. Hipótese da Estratégia

[Descrever a tese operacional da estratégia.]

---

## 2. Regras

### Entrada

[Regras de entrada.]

### Saída

[Regras de saída.]

### Stop

[Regra de stop.]

### Gestão de posição

[Como o capital é alocado.]

### Custos

- Taxa: [x%]
- Slippage: [x%]

---

## 3. Performance Sumária

- Capital Inicial: [1.00 BTC]
- Capital Final: [X.XX BTC]
- Retorno Líquido: [X%]
- Benchmark Buy and Hold: [X%]
- Diferença contra Benchmark: [X p.p.]
- Drawdown Máximo: [-X%]
- Score Operacional: [0-100]

---

## 4. Estatísticas Operacionais

- Total de Trades: [N]
- Taxa de Acerto: [X%]
- Profit Factor: [X.X]
- Payoff Médio: [X.X]
- Maior Sequência de Perdas: [N]
- Custo Total com Taxas: [X]
- Tempo Médio por Operação: [X]

---

## 5. Log de Operações — Amostra

| Data/Hora Entrada | Ativo | Tipo | Entrada | Saída | Resultado | Motivo |
|---|---|---|---:|---:|---:|---|
| 2025-02-10 10:00 | PENDLE/BTC | BUY | 0.000... | 0.000... | +X% | RSI < 30 |

---

## 6. Diagnóstico

### O que funcionou

[Insights.]

### Riscos detectados

[Problemas.]

### Fragilidades estatísticas

[Overfitting, baixa amostra, concentração etc.]

---

## 7. Decisão da Rodada

**Status final:** [Aprovada/Reprovada/Promissora/Estudo]

**Justificativa:**  
[Explicação.]

---

## 8. Próxima Hipótese

**Nova estratégia sugerida:** [STR-XXXX]

**Mudança proposta:**  
[Descrição.]

**Motivo:**  
[Por que essa mudança será testada.]
```

---

## 9. Formato JSON complementar

```json
{
  "run_id": "RUN-0001",
  "strategy_id": "STR-0001",
  "strategy_name": "RSI Reversal Basic",
  "period_start": "2025-01-01",
  "period_end": "CURRENT_DATE",
  "assets": ["ETH/BTC", "PENDLE/BTC"],
  "timeframe": "10m",
  "initial_capital": 1.0,
  "capital_currency": "BTC",
  "final_capital": null,
  "net_return_pct": null,
  "benchmark_return_pct": null,
  "max_drawdown_pct": null,
  "win_rate_pct": null,
  "profit_factor": null,
  "avg_payoff": null,
  "total_trades": null,
  "max_losing_streak": null,
  "total_fees": null,
  "operational_score": null,
  "status": "pending",
  "diagnosis": {
    "what_worked": [],
    "risks_detected": [],
    "statistical_weaknesses": []
  },
  "next_hypothesis": {
    "next_strategy_id": "STR-0002",
    "change_proposed": "",
    "reason": ""
  }
}
```

---

## 10. Backlog de pesquisa para próxima IA

### 10.1 Integração on-chain para Pendle

Pesquisar:

- TVL;
- yield implícito;
- maturidade dos pools;
- variação de liquidez;
- dados via DeFiLlama;
- dados via The Graph;
- dados oficiais Pendle, se disponíveis.

Objetivo: usar esses dados como filtros ou contexto, não como promessa de previsão.

---

### 10.2 Banco de séries temporais

Comparar:

- TimescaleDB;
- QuestDB;
- DuckDB para análise local;
- Parquet para cache;
- PostgreSQL puro para MVP.

Critérios:

- velocidade de leitura;
- facilidade de instalação;
- compatibilidade com Python;
- custo de manutenção;
- simplicidade do MVP;
- performance em candles multiativos.

Para o MVP, considerar **DuckDB + Parquet** antes de TimescaleDB, porque é mais simples e rápido para protótipo local. TimescaleDB entra bem quando o sistema virar serviço contínuo.

---

### 10.3 Mutação de estratégia

Pesquisar:

- DEAP;
- PyGAD;
- Optuna;
- Hyperopt;
- algoritmos genéticos;
- busca bayesiana;
- grid search;
- random search.

Objetivo: gerar STR-0002 a partir da STR-0001 com base no diagnóstico anterior.

Atenção: mutação automática sem controle vira fábrica de overfitting.

---

### 10.4 Slippage e liquidez

Pesquisar:

- slippage fixo;
- slippage proporcional ao volume;
- spread médio;
- book depth;
- market impact;
- liquidez por horário;
- pares de baixo volume como PENDLE/BTC.

Objetivo: impedir simulação bonita e irreal.

---

## 11. Infraestrutura sugerida

### Linguagem principal

```text
Python 3.10+
```

### Bibliotecas base

```text
pandas
numpy
ccxt
vectorbt
plotly
sqlalchemy
duckdb
pyarrow
streamlit
```

### Banco/cache inicial

```text
Parquet + DuckDB
```

### Banco futuro

```text
TimescaleDB ou QuestDB
```

### Dashboard inicial

```text
Streamlit
```

### Relatórios

```text
Markdown + JSON
```

### Empacotamento

```text
Docker
```

---

## 12. Roadmap de implementação

### Fase 1 — Ingestão e cache

- baixar candles;
- salvar em Parquet;
- consultar com DuckDB;
- validar integridade dos dados.

### Fase 2 — Primeira estratégia

- criar STR-0001 manual;
- rodar simulação;
- gerar métricas;
- gerar log de trades.

### Fase 3 — Relatório de rodada

- gerar `.md`;
- gerar `.json`;
- salvar histórico de runs.

### Fase 4 — Dashboard

- tela Strategy Loop;
- ranking de runs;
- curva de capital;
- tabela de trades;
- diagnóstico.

### Fase 5 — Evolução de estratégia

- gerar STR-0002;
- comparar com STR-0001;
- criar árvore de estratégias.

### Fase 6 — Pesquisa avançada

- on-chain Pendle;
- slippage realista;
- walk-forward;
- Monte Carlo;
- mutação assistida por IA.

---

## 13. Diferenciação competitiva

O diferencial do Quant Strategy Loop não é ser mais um backtester.

O diferencial é:

```text
Backtest + Log + Diagnóstico + Relatório IA + Nova Hipótese + Comparação Evolutiva
```

Ou seja:

> O sistema não apenas testa uma estratégia; ele documenta o aprendizado de cada rodada e constrói uma árvore de evolução.

Isso é o que transforma o projeto de “simuladorzinho” em laboratório de estratégia.

---

## 14. Próxima etapa objetiva

A próxima IA ou equipe deve começar por:

```text
1. Definir o schema de Strategy, Run e TradeLog.
2. Criar o primeiro pipeline de ingestão de candles.
3. Rodar uma estratégia simples STR-0001.
4. Gerar relatório .md e .json.
5. Salvar resultado como primeiro caso auditável.
```

Esse é o primeiro tijolo real. Sem isso, vira só arquitetura bonita.

---

## 15. Prompt para outra IA continuar a pesquisa

```text
Você é uma IA arquiteta sênior de software quantitativo, backtesting e engenharia de dados.

Leia este handoff do projeto Quant Strategy Loop.

Sua tarefa é aprimorar a pesquisa técnica e propor uma especificação mais detalhada para implementação.

O sistema não deve prever tendências nem operar automaticamente. Ele deve receber estratégias, simular de uma data passada até hoje, registrar operações, avaliar desempenho, gerar relatórios Markdown/JSON e propor novas hipóteses de estratégia para o próximo ciclo.

Foque em:
1. Comparar VectorBT, Freqtrade, LEAN e Backtrader para o MVP.
2. Definir a melhor arquitetura inicial.
3. Sugerir schemas para Strategy, Run, TradeLog e Evaluation.
4. Propor formato de arquivos e pastas.
5. Definir métricas de avaliação e Score Operacional.
6. Apontar riscos de overfitting.
7. Recomendar próximos passos práticos.
8. Evitar promessas de lucro ou execução automática precoce.

Entregue uma resposta técnica, objetiva e estruturada para que uma equipe consiga iniciar a prototipagem.
```
