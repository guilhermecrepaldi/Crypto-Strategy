import vectorbt as vbt
import pandas as pd
from src.strategy.base import BaseStrategy

class OnchainRSIStrategy(BaseStrategy):
    def __init__(self, strategy_id="STR-0003", rsi_window=14, sma_window=200):
        super().__init__(strategy_id, "RSI + SMA + Pendle TVL Filter")
        self.params = {
            "rsi_window": rsi_window,
            "sma_window": sma_window
        }

    def generate_signals(self, df, df_tvl):
        """
        Sinal:
        - Long: RSI < 30 AND Preço > SMA 200 AND TVL_Pendle (Tendência de Alta)
        """
        # Calcular indicadores de preço
        rsi = vbt.RSI.run(df['close'], window=self.params['rsi_window']).rsi
        sma = vbt.MA.run(df['close'], window=self.params['sma_window']).ma
        
        # Alinhar TVL (DeFiLlama é diário, df pode ser 1h)
        # Vamos reindexar o TVL para o índice do dataframe de preços
        df_tvl = df_tvl.set_index('date').sort_index()
        tvl_aligned = df_tvl['tvl_usd'].reindex(df.index, method='ffill')
        
        # Tendência do TVL (Média Móvel do TVL de 7 dias se diário, ou proporcional)
        # Aqui simplificamos: TVL atual > TVL de 7 dias atrás
        tvl_sma = tvl_aligned.rolling(window=168).mean() # 168h = 7 dias
        tvl_trend_long = tvl_aligned > tvl_sma
        
        # Sinais
        trend_long = df['close'] > sma
        rsi_entry = rsi < 30
        
        entries = rsi_entry & trend_long & tvl_trend_long
        exits = rsi > 70
        
        return entries, exits

    def run_backtest(self, df, df_tvl):
        """
        Sobrescreve run_backtest para aceitar dados on-chain.
        """
        entries, exits = self.generate_signals(df, df_tvl)
        portfolio = vbt.Portfolio.from_signals(df['close'], entries, exits, init_cash=1.0)
        return portfolio
