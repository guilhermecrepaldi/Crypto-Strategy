import ccxt
import pandas as pd
import os
from datetime import datetime
import time

class DataIngestor:
    def __init__(self, exchange_id='binance'):
        self.exchange = getattr(ccxt, exchange_id)({
            'enableRateLimit': True,
        })
        self.raw_data_path = os.path.join('data', 'raw')
        if not os.path.exists(self.raw_data_path):
            os.makedirs(self.raw_data_path)

    def fetch_ohlcv(self, symbol, timeframe='1h', since=None, limit=1000):
        """
        Busca dados OHLCV da exchange.
        since: timestamp em milissegundos
        """
        print(f"Baixando {symbol} no timeframe {timeframe}...")
        
        all_ohlcv = []
        current_since = since
        
        while True:
            try:
                ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, current_since, limit)
                if not ohlcv:
                    break
                
                all_ohlcv.extend(ohlcv)
                
                # O último timestamp + 1ms para a próxima iteração
                last_timestamp = ohlcv[-1][0]
                current_since = last_timestamp + 1
                
                # Se pegamos menos que o limite, chegamos ao final (ou dados recentes)
                if len(ohlcv) < limit:
                    break
                
                # Evitar rate limit manual se necessário, embora enableRateLimit esteja True
                time.sleep(self.exchange.rateLimit / 1000)
                
                # Log de progresso simples
                print(f"  Coletados {len(all_ohlcv)} candles. Próximo início: {datetime.fromtimestamp(current_since/1000)}")
                
                # Se o próximo since for maior que o tempo atual, paramos
                if current_since > self.exchange.milliseconds():
                    break
                    
            except Exception as e:
                print(f"Erro ao baixar dados: {e}")
                break
                
        df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def save_to_parquet(self, df, symbol, timeframe):
        """
        Salva o DataFrame em formato Parquet para cache imutável.
        """
        symbol_clean = symbol.replace('/', '_').replace(':', '_')
        filename = f"{symbol_clean}_{timeframe}.parquet"
        filepath = os.path.join(self.raw_data_path, filename)
        
        df.to_parquet(filepath, index=False)
        print(f"Dados salvos em: {filepath}")
        return filepath

if __name__ == "__main__":
    ingestor = DataIngestor()
    # Exemplo: BTC/USDT desde 01/01/2025
    since_date = ingestor.exchange.parse8601('2025-01-01T00:00:00Z')
    df_btc = ingestor.fetch_ohlcv('BTC/USDT', '1h', since=since_date)
    if not df_btc.empty:
        ingestor.save_to_parquet(df_btc, 'BTC/USDT', '1h')
