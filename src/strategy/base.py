import vectorbt as vbt
import pandas as pd
from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, strategy_id, name):
        self.strategy_id = strategy_id
        self.name = name
        self.params = {}

    @abstractmethod
    def generate_signals(self, df):
        """
        Deve retornar um objeto com entradas e saídas (Boolean Series).
        """
        pass

    def run_backtest(self, df, initial_cash=1.0, fees=0.001, slippage=0.001):
        """
        Executa o backtest usando VectorBT.
        """
        entries, exits = self.generate_signals(df)
        
        # Simulação com VectorBT
        portfolio = vbt.Portfolio.from_signals(
            df['close'], 
            entries, 
            exits, 
            init_cash=initial_cash,
            fees=fees,
            slippage=slippage,
            freq='1h' # Ajustar conforme o timeframe do dado
        )
        
        return portfolio

    def get_metrics(self, portfolio):
        """
        Extrai métricas essenciais para o relatório.
        """
        stats = portfolio.stats()
        metrics = {
            "initial_value": portfolio.init_cash,
            "final_value": portfolio.value().iloc[-1],
            "total_return_pct": portfolio.total_return() * 100,
            "max_drawdown_pct": portfolio.max_drawdown() * 100,
            "win_rate_pct": stats.get('Win Rate [%]', 0),
            "profit_factor": stats.get('Profit Factor', 0),
            "total_trades": stats.get('Total Trades', 0),
        }
        return metrics
