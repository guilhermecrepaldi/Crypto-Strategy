# Handoff Técnico — Dashboard Quant Strategy Loop

## 1. Objetivo
Este handoff é destinado a uma IA especialista em **UI/UX e Visualização de Dados** com Streamlit e Plotly. O objetivo é evoluir o `dashboard.py` atual para uma ferramenta de nível institucional.

## 2. Estado Atual
O dashboard já é capaz de:
- Listar todas as runs gravadas na pasta `reports/` (arquivos `.json`).
- Exibir métricas de resumo (Destaques no topo).
- Exibir uma tabela de ranking de estratégias.
- Plotar um gráfico de dispersão Risco (Drawdown) vs Retorno.
- Renderizar a **Curva de Equity** (evolução do capital) ao selecionar uma run específica.

## 3. Estrutura de Dados (Data Source)
O Dashboard consome arquivos JSON gerados pelo `src/utils/reporter.py`.
Schema simplificado:
```json
{
  "run_id": "RUN-XXXX",
  "strategy_id": "STR-XXXX",
  "metrics": {
    "total_return_pct": 0.0,
    "max_drawdown_pct": 0.0,
    "profit_factor": 0.0,
    "win_rate_pct": 0.0,
    "total_trades": 0
  },
  "equity_curve": [
    {"date": "YYYY-MM-DD HH:MM:SS", "equity": 1.0},
    ...
  ],
  "next_hypothesis": { ... }
}
```

## 4. Backlog de Melhorias (Missão da Próxima IA)

### 4.1 Interface e Layout
- [ ] **Glassmorphism / Dark Mode:** Refinar o CSS do Streamlit para um visual mais premium e moderno.
- [ ] **Sidebar Avançada:** Adicionar filtros por Timeframe, Exchange e Intervalo de Datas.
- [ ] **Cards de KPI:** Melhorar o design dos cards de métricas (crescimento, cores dinâmicas para win rate).

### 4.2 Visualização de Dados
- [ ] **Tabela de Trades:** Exibir a lista completa de trades da run selecionada (disponível no VectorBT, mas precisa ser exportada para o JSON ou lida do DB).
- [ ] **Gráfico de Drawdown:** Adicionar um gráfico de área abaixo da equity curve mostrando o drawdown submerso no tempo.
- [ ] **Distribuição de Retornos:** Adicionar histograma de retornos por trade para avaliar a regularidade da estratégia.

### 4.3 Funcionalidades
- [ ] **Comparação de Runs:** Permitir selecionar duas ou mais runs e sobrepor suas curvas de equity no mesmo gráfico.
- [ ] **Controle de Otimização:** Adicionar um botão na interface para disparar o `main.py` com o parâmetro `optimize=True` e exibir o progresso.
- [ ] **Visualização da Próxima Hipótese:** Exibir de forma destacada a sugestão do Evolver para a run selecionada.

## 5. Instruções de Implementação
- Mantenha o desacoplamento: O Dashboard **lê** relatórios; ele não deve conter a lógica de trading.
- Use `st.cache_data` para evitar re-leitura constante dos arquivos JSON se a pasta `reports/` for grande.
- Priorize Plotly para interatividade nos gráficos.

## 6. Prompt para Iniciar
> Você é uma IA Especialista em Dashboards e Data Science.
> Sua tarefa é evoluir o arquivo `dashboard.py` do projeto Quant Strategy Loop.
> O sistema já possui o core funcional. Foque em transformar a experiência visual em algo premium (Dark Mode, KPIs avançados, gráficos de drawdown e comparação de estratégias).
> Leia o `HANDOFF_DASHBOARD.md` para entender a estrutura dos dados JSON em `reports/`.
