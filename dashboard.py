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

    # --- Tabs de Visualização ---
    tab1, tab2 = st.tabs(["📊 Simulações Quant", "⛓️ Pendle Insights (On-chain)"])

    with tab1:
        # Seleção de Run para Detalhamento
        st.subheader("🔍 Detalhes da Execução")
        selected_run = st.selectbox("Selecione uma Run para ver o gráfico", options=df_filtered["Run ID"].unique())
        
        if selected_run:
            # Localizar o arquivo JSON correspondente
            run_data = None
            for file in os.listdir('reports'):
                if file.startswith(selected_run) and file.endswith('.json'):
                    with open(os.path.join('reports', file), 'r') as f:
                        run_data = json.load(f)
                    break
            
            if run_data and "equity_curve" in run_data and run_data["equity_curve"]:
                df_equity = pd.DataFrame(run_data["equity_curve"])
                df_equity["date"] = pd.to_datetime(df_equity["date"])
                
                fig_equity = px.line(df_equity, x="date", y="equity", title=f"Evolução do Capital - {selected_run}")
                fig_equity.update_layout(yaxis_title="Capital (BTC)", xaxis_title="Data")
                st.plotly_chart(fig_equity, use_container_width=True)
            else:
                st.warning("Dados de curva de capital não encontrados para esta Run.")

        # Gráfico de Dispersão Retorno x Drawdown
        st.subheader("📈 Análise Comparativa: Risco x Retorno")
        fig = px.scatter(df_filtered, x="Drawdown %", y="Return %", color="Strategy", size="Trades", 
                         hover_data=["Run ID"], title="Retorno vs Drawdown por Execução")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("📊 Fundamentos: Pendle Finance")
        st.info("Esta seção carrega dados diretamente do DeFiLlama para análise de fundamentos.")
        
        from src.data.onchain_ingestor import OnchainIngestor
        onchain = OnchainIngestor()
        
        if st.button("Carregar TVL do Pendle"):
            df_tvl = onchain.fetch_pendle_tvl()
            if not df_tvl.empty:
                fig_tvl = px.area(df_tvl, x="date", y="tvl_usd", title="Histórico de TVL - Pendle Finance")
                st.plotly_chart(fig_tvl, use_container_width=True)
                
                st.write("### Top Pools de Yield")
                df_yields = onchain.fetch_pendle_yields()
                if not df_yields.empty:
                    st.dataframe(df_yields[['symbol', 'tvlUsd', 'apy']].sort_values(by='apy', ascending=False).head(10))
            else:
                st.error("Falha ao carregar dados on-chain.")

else:
    st.info("Nenhum relatório encontrado. Execute o `main.py` para gerar a primeira Run.")
    if st.button("Simular Rodada de Teste (Mock)"):
        st.warning("Funcionalidade em desenvolvimento. Por enquanto, use o terminal: `python main.py`.")
