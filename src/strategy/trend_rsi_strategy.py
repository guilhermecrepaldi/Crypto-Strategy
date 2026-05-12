import vectorbt as vbt
from src.strategy.base import BaseStrategy

class TrendRSIStrategy(BaseStrategy):
    def __init__(self, strategy_id="STR-0002", rsi_window=14, sma_window=200, entry_level=30, exit_level=70):
        super().__init__(strategy_id, "RSI Reversal + Trend Filter")
        self.params = {
            "rsi_window": rsi_window,
            "sma_window": sma_window,
            "entry_level": entry_level,
            "exit_level": exit_level
        }

    def generate_signals(self, df):
        """
        Gera sinais baseados em RSI com filtro de tendência:
        Entrada: RSI < entry_level E Preço > SMA(sma_window)
        Saída: RSI > exit_level OU Preço < SMA(sma_window)
        """
        rsi = vbt.RSI.run(df['close'], window=self.params['rsi_window']).rsi
        sma = vbt.MA.run(df['close'], window=self.params['sma_window']).ma
        
        # Filtro de tendência: Preço acima da média móvel
        trend_long = df['close'] > sma
        
        # Sinais de RSI
        rsi_entry = rsi < self.params['entry_level']
        rsi_exit = rsi > self.params['exit_level']
        
        # Combinação: Entrar apenas a favor da tendência
        entries = rsi_entry & trend_long
        
        # Saída: RSI sobrecomprado OU quebra da tendência
        exits = rsi_exit | (~trend_long)
        
        return entries, exits

if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    
    # Mock data com tendência de alta
    close = np.linspace(20000, 30000, 1000) + np.random.normal(0, 500, 1000)
    data = pd.DataFrame({'close': close})
    
    str_0002 = TrendRSIStrategy()
    portfolio = str_0002.run_backtest(data)
    print(f"Métricas {str_0002.name}:")
    print(str_0002.get_metrics(portfolio))
