from src.data.ingestor import DataIngestor
from src.database.manager import LocalDB
import os
from datetime import datetime

def run_fase_1(symbol='BTC/USDT', timeframe='1h'):
    print(f"--- Iniciando Fase 1: Ingestão e Cache [{symbol}] ---")
    
    # 1. Ingestão
    ingestor = DataIngestor()
    since_date = ingestor.exchange.parse8601('2025-01-01T00:00:00Z')
    
    df = ingestor.fetch_ohlcv(symbol, timeframe, since=since_date)
    
    if df.empty:
        print("Falha ao baixar dados ou nenhum dado encontrado.")
        return
    
    parquet_path = ingestor.save_to_parquet(df, symbol, timeframe)
    
    # 2. Persistência e Query via LocalDB
    db = LocalDB()
    table_name = symbol.replace('/', '_').lower()
    
    db.register_parquet(table_name, parquet_path)
    
    # Validação
    res = db.query(f"SELECT COUNT(*) as total, MIN(datetime) as inicio, MAX(datetime) as fim FROM {table_name}")
    
    print("\n--- Validação do Banco de Dados ---")
    print(res)
    
    db.close()
    print("\nFase 1 concluída com sucesso.")

if __name__ == "__main__":
    run_fase_1()
