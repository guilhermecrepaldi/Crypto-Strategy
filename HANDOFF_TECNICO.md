# Handoff Técnico — Quant Strategy Loop (v1.0.0-MVP)

## 1. Visão Geral
O **Quant Strategy Loop** é um laboratório de simulação evolutiva para estratégias quantitativas de criptoativos. O sistema foca em automação de backtesting, auditoria de resultados e sugestão de melhorias (loops evolutivos).

**Status Atual:** MVP Concluído e Operacional (Fases 1, 2, 3 e 4 completas).
**Progresso Global:** ~65% do Roadmap original.

---

## 2. Arquitetura do Sistema
O projeto segue uma estrutura modular industrial para evitar acoplamento:

- **`src/data/ingestor.py`**: Coleta dados OHLCV via CCXT (Binance) e persiste em Parquet (Imutável).
- **`src/database/manager.py`**: Camada SQL via DuckDB. Registra Views sobre os arquivos Parquet para queries de alta performance.
- **`src/strategy/base.py`**: Classe abstrata (ABC) que define o contrato para todas as estratégias.
- **`src/strategy/rsi_strategy.py`**: Primeira estratégia funcional (STR-0001).
- **`src/data/onchain_ingestor.py`**: Coleta dados DeFi (Pendle/DeFiLlama) e persiste em Parquet.
- **`src/strategy/onchain_rsi_strategy.py`**: Estratégia híbrida Preço + TVL (STR-0003).
- **`src/strategy/yield_momentum_strategy.py`**: Estratégia de Momentum de Yield (STR-0004).
- **`src/strategy/trend_rsi_strategy.py`**: Estratégia evoluída com filtro SMA (STR-0002).
- **`src/strategy/optimizer.py`**: Motor de otimização de hiperparâmetros via Optuna.
- **`src/strategy/evolver.py`**: Motor de heurísticas que analisa métricas e propõe a `next_hypothesis`.
- **`src/utils/reporter.py`**: Gerador de relatórios auditáveis em Markdown e JSON (inclui curva de equity).
- **`main.py`**: Orquestrador do loop completo.
- **`dashboard.py`**: Interface visual Streamlit para análise de Rankings e Risco/Retorno.

---

## 3. Stack Tecnológica
- **Linguagem:** Python 3.10+
- **Backtesting:** VectorBT (Vetorizado, alta velocidade)
- **Dados:** CCXT (Exchange API), Pandas, PyArrow (Parquet)
- **Banco de Dados:** DuckDB (OLAP local)
- **Interface:** Streamlit, Plotly
- **Governança:** Git, HISTORICO_CHAT.md

---

## 4. Como Operar
1. **Configurar:** `pip install -r requirements.txt`
2. **Executar Loop:** `python main.py`
   - Isso baixará dados (se não houver cache), rodará a STR-0001 e gerará relatórios em `reports/`.
3. **Visualizar:** `streamlit run dashboard.py`
   - Permite ver o gráfico da curva de capital e comparar Runs.

---

## 5. Próximos Passos (Backlog para a Próxima IA)
1. **Implementar STR-0002:** Criar uma estratégia que utilize o filtro de tendência (SMA) conforme sugerido pelo `Evolver`.
2. **Fase 6 (Pesquisa Avançada):**
   - Integrar dados On-chain da Pendle (TVL, Yield).
   - Implementar validação Walk-Forward para evitar overfitting.
   - Adicionar simulação de Monte Carlo.
3. **Persistência de Metadados:** Migrar a leitura de relatórios de arquivos JSON para uma tabela consolidada no DuckDB para performance em larga escala.

---

## 6. Prompt Sugerido para a Próxima IA
> Você é uma IA Arquiteta Quantitativa Sênior. Receba este projeto "Quant Strategy Loop".
> Analise a estrutura modular e o motor evolutivo.
> Sua missão é:
> 1. Validar a lógica do `src/strategy/evolver.py`.
> 2. Propor a implementação da `STR-0002` integrando indicadores de volume ou tendência.
> 3. Sugerir como integrar os dados da Pendle (on-chain) no pipeline de ingestão atual.
