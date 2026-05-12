import vectorbt as vbt
import pandas as pd
from src.strategy.base import BaseStrategy

class YieldMomentumStrategy(BaseStrategy):
    def __init__(self, strategy_id="STR-0004", rsi_window=14, sma_window=200):
        super().__init__(strategy_id, "Yield Momentum (Pendle APY Filter)")
        self.params = {
            "rsi_window": rsi_window,
            "sma_window": sma_window
        }

    def generate_signals(self, df, df_apy):
        """
        Sinal:
        - Long: RSI < 40 AND Trend Up AND APY em Aceleração (Momentum)
        """
        # Calcular indicadores de preço
        rsi = vbt.RSI.run(df['close'], window=self.params['rsi_window']).rsi
        sma = vbt.MA.run(df['close'], window=self.params['sma_window']).ma
        
        # Alinhar APY (DeFiLlama Yields)
        # Assumindo que df_apy tem colunas ['timestamp', 'apy']
        df_apy = df_apy.set_index('timestamp').sort_index()
        apy_aligned = df_apy['apy'].reindex(df.index, method='ffill')
        
        # Momentum do Yield: APY atual > Média Móvel do APY
        apy_sma = apy_aligned.rolling(window=72).mean() # 72h = 3 dias
        yield_momentum = apy_aligned > apy_sma
        
        # Sinais
        trend_long = df['close'] > sma
        rsi_long = rsi < 40
        
        entries = rsi_long & trend_long & yield_momentum
        exits = (rsi > 70) | (apy_aligned < apy_sma * 0.8) # Sai se RSI alto ou APY cair 20% abaixo da média
        
        return entries, exits

    def run_backtest(self, df, df_apy):
        """
        Executa backtest híbrido com dados de APY.
        """
        entries, exits = self.generate_signals(df, df_apy)
        portfolio = vbt.Portfolio.from_signals(df['close'], entries, exits, init_cash=1.0)
        return portfolio
