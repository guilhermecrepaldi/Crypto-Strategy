import vectorbt as vbt
from src.strategy.base import BaseStrategy

class RSIStrategy(BaseStrategy):
    def __init__(self, strategy_id="STR-0001", rsi_window=14, entry_level=30, exit_level=70):
        super().__init__(strategy_id, "RSI Reversal Basic")
        self.params = {
            "rsi_window": rsi_window,
            "entry_level": entry_level,
            "exit_level": exit_level
        }

    def generate_signals(self, df):
        """
        Gera sinais baseados em RSI:
        Entrada: RSI cruza abaixo de entry_level (Sobrevevenda)
        Saída: RSI cruza acima de exit_level (Sobrecompra)
        """
        rsi = vbt.RSI.run(df['close'], window=self.params['rsi_window'])
        
        entries = rsi.rsi_crossed_below(self.params['entry_level'])
        exits = rsi.rsi_crossed_above(self.params['exit_level'])
        
        return entries, exits

if __name__ == "__main__":
    # Teste rápido se houver dados
    import pandas as pd
    import numpy as np
    
    # Mock data
    data = pd.DataFrame({
        'close': np.random.uniform(20000, 30000, 100)
    })
    
    str_0001 = RSIStrategy()
    portfolio = str_0001.run_backtest(data)
    print(str_0001.get_metrics(portfolio))
