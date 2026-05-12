import streamlit as st
import pandas as pd
import os
import json
import plotly.express as px

st.set_page_config(page_title="Quant Strategy Loop Dashboard", layout="wide")

def load_reports(reports_dir='reports'):
    reports = []
    if not os.path.exists(reports_dir):
        return pd.DataFrame()
    
    for file in os.listdir(reports_dir):
        if file.endswith('.json'):
            with open(os.path.join(reports_dir, file), 'r') as f:
                data = json.load(f)
                # Achatar o JSON para DataFrame
                report = {
                    "Run ID": data.get('run_id'),
                    "Strategy": data.get('strategy_id'),
                    "Return %": data['metrics'].get('total_return_pct'),
                    "Drawdown %": data['metrics'].get('max_drawdown_pct'),
                    "Profit Factor": data['metrics'].get('profit_factor'),
                    "Win Rate %": data['metrics'].get('win_rate_pct'),
                    "Trades": data['metrics'].get('total_trades'),
                    "Final Value": data['metrics'].get('final_value'),
                    "Timestamp": data.get('timestamp')
                }
                reports.append(report)
    return pd.DataFrame(reports)

st.title("📊 Quant Strategy Loop — Dashboard")
st.markdown("Monitoramento evolutivo de estratégias quantitativas.")

df_reports = load_reports()

if not df_reports.empty:
    st.sidebar.header("Filtros")
    strategy_filter = st.sidebar.multiselect("Estratégias", options=df_reports["Strategy"].unique(), default=df_reports["Strategy"].unique())
    
    df_filtered = df_reports[df_reports["Strategy"].isin(strategy_filter)]
    
    # Métricas de Destaque
    c1, c2, c3, c4 = st.columns(4)
    best_return = df_filtered["Return %"].max()
    avg_winrate = df_filtered["Win Rate %"].mean()
    total_runs = len(df_filtered)
    best_pf = df_filtered["Profit Factor"].max()
    
    c1.metric("Melhor Retorno", f"{best_return:.2f}%")
    c2.metric("Win Rate Médio", f"{avg_winrate:.2f}%")
    c3.metric("Total de Runs", total_runs)
    c4.metric("Melhor Profit Factor", f"{best_pf:.2f}")

    # Tabela de Ranking
    st.subheader("🏆 Ranking de Execuções")
    st.dataframe(df_filtered.sort_values(by="Return %", ascending=False), use_container_width=True)

    # Gráfico de Dispersão Retorno x Drawdown
    st.subheader("📈 Análise Risco x Retorno")
    fig = px.scatter(df_filtered, x="Drawdown %", y="Return %", color="Strategy", size="Trades", 
                     hover_data=["Run ID"], title="Retorno vs Drawdown por Execução")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Nenhum relatório encontrado. Execute o `main.py` para gerar a primeira Run.")
    if st.button("Simular Rodada de Teste (Mock)"):
        st.warning("Funcionalidade em desenvolvimento. Por enquanto, use o terminal: `python main.py`.")
