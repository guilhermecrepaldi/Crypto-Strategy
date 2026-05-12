from src.data.ingestor import DataIngestor
from src.database.manager import LocalDB
from src.strategy.rsi_strategy import RSIStrategy
from src.utils.reporter import StrategyReporter
import os
from datetime import datetime

def run_strategy_loop(symbol='BTC/USDT', timeframe='1h'):
    print(f"--- Iniciando Quant Strategy Loop [{symbol}] ---")
    
    # 1. Ingestão e Banco
    ingestor = DataIngestor()
    since_date = ingestor.exchange.parse8601('2025-01-01T00:00:00Z')
    df = ingestor.fetch_ohlcv(symbol, timeframe, since=since_date)
    
    if df.empty:
        print("Falha ao baixar dados.")
        return
    
    parquet_path = ingestor.save_to_parquet(df, symbol, timeframe)
    
    db = LocalDB()
    table_name = symbol.replace('/', '_').lower()
    db.register_parquet(table_name, parquet_path)
    
    # 2. Execução da Estratégia
    strategy = RSIStrategy()
    print(f"Executando {strategy.name}...")
    portfolio = strategy.run_backtest(df)
    
    # 3. Geração de Métricas e Relatório
    metrics = strategy.get_metrics(portfolio)
    
    # Extrair amostra de trades para o relatório
    trades = portfolio.trades.records_readable
    trades_sample = []
    for _, t in trades.head(5).iterrows():
        trades_sample.append({
            "entry_date": str(t['Entry Timestamp']),
            "symbol": symbol,
            "result_pct": t['Return'] * 100
        })
    
    reporter = StrategyReporter()
    md_path, json_path = reporter.generate_report(strategy.strategy_id, metrics, trades_sample)
    
    print(f"\n--- Resultado da Rodada ---")
    print(f"Retorno Total: {metrics['total_return_pct']:.2f}%")
    print(f"Profit Factor: {metrics['profit_factor']:.2f}")
    print(f"Relatório MD: {md_path}")
    
    db.close()
    print("\nLoop concluído com sucesso.")

if __name__ == "__main__":
    run_strategy_loop()
