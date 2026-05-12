from src.data.ingestor import DataIngestor
from src.data.onchain_ingestor import OnchainIngestor
from src.database.manager import LocalDB
from src.strategy.trend_rsi_strategy import TrendRSIStrategy
from src.strategy.onchain_rsi_strategy import OnchainRSIStrategy
from src.strategy.optimizer import StrategyOptimizer
from src.strategy.evolver import StrategyEvolver
from src.utils.reporter import StrategyReporter
from src.utils.validator import WalkForwardValidator
import os
from datetime import datetime

def run_strategy_loop(symbol='BTC/USDT', timeframe='1h', optimize=False, use_onchain=False):
    print(f"--- Iniciando Quant Strategy Loop [{symbol}] ---")
    
    # 1. Ingestão e Banco (Market Data)
    ingestor = DataIngestor()
    since_date = ingestor.exchange.parse8601('2025-01-01T00:00:00Z')
    df = ingestor.fetch_ohlcv(symbol, timeframe, since=since_date)
    
    if df.empty:
        print("Falha ao baixar dados.")
        return
    
    # 2. Ingestão On-chain (Opcional - Fase 6)
    df_tvl = None
    if use_onchain:
        onchain = OnchainIngestor()
        df_tvl = onchain.fetch_pendle_tvl()
        onchain.save_onchain_data(df_tvl)

    # 3. Preparação do Banco
    parquet_path = ingestor.save_to_parquet(df, symbol, timeframe)
    db = LocalDB()
    table_name = symbol.replace('/', '_').lower()
    db.register_parquet(table_name, parquet_path)
    
    # 4. Otimização (Opcional)
    best_params = {}
    if optimize:
        print("Iniciando Otimização de Hiperparâmetros...")
        optimizer = StrategyOptimizer(df)
        best_params = optimizer.optimize_rsi_trend(n_trials=30)
    
    # 5. Execução da Estratégia
    if use_onchain and df_tvl is not None:
        strategy = OnchainRSIStrategy()
        print(f"Executando {strategy.name} (Híbrida)...")
        portfolio = strategy.run_backtest(df, df_tvl)
    else:
        strategy = TrendRSIStrategy(**best_params) if best_params else TrendRSIStrategy()
        print(f"Executando {strategy.name}...")
        portfolio = strategy.run_backtest(df)
    
    # 6. Validação Estatística (Walk-Forward)
    validator = WalkForwardValidator(strategy)
    wf_results, stability_score = validator.validate(df)
    
    # 7. Geração de Métricas e Evolução
    metrics = strategy.get_metrics(portfolio)
    metrics['stability_score'] = stability_score # Integrar score nas métricas
    
    # 4. Geração de Relatório com Evolução
    # Para evoluir, precisamos salvar o JSON primeiro ou simular o path
    run_id = f"RUN-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    # Amostra de trades
    trades = portfolio.trades.records_readable
    trades_sample = []
    for _, t in trades.head(5).iterrows():
        trades_sample.append({
            "entry_date": str(t['Entry Timestamp']),
            "symbol": symbol,
            "result_pct": t['Return'] * 100
        })

    # Simular a evolução antes de salvar o arquivo físico final
    # Criamos um dict temporário para o evolver analisar
    temp_run_data = {
        "strategy_id": strategy.strategy_id,
        "metrics": metrics
    }
    
    # Criar um arquivo temporário para o evolver (ou modificar o evolver para aceitar dict)
    # Por simplicidade industrial, vou instanciar o evolver e passar o dict se possível,
    # mas o evolver atual espera um path. Vou ajustar o evolver para aceitar dict.
    evolver = StrategyEvolver()
    # Mock de evolução direta para este loop
    next_hypo = evolver.evolve_from_dict(temp_run_data)
    
    reporter = StrategyReporter()
    md_path, json_path = reporter.generate_report(
        strategy.strategy_id, 
        metrics, 
        trades_sample,
        equity_series=portfolio.value(),
        next_hypothesis=next_hypo,
        run_id=run_id
    )
    
    print(f"\n--- Resultado da Rodada ---")
    print(f"Retorno Total: {metrics['total_return_pct']:.2f}%")
    print(f"Profit Factor: {metrics['profit_factor']:.2f}")
    print(f"Relatório MD: {md_path}")
    
    db.close()
    print("\nLoop concluído com sucesso.")

if __name__ == "__main__":
    run_strategy_loop()
