import optuna
import pandas as pd
from src.strategy.trend_rsi_strategy import TrendRSIStrategy

class StrategyOptimizer:
    def __init__(self, data):
        self.data = data

    def optimize_rsi_trend(self, n_trials=50):
        """
        Otimiza a TrendRSIStrategy (STR-0002).
        """
        def objective(trial):
            # Definir o espaço de busca
            rsi_window = trial.suggest_int('rsi_window', 7, 30)
            sma_window = trial.suggest_int('sma_window', 50, 300)
            entry_level = trial.suggest_int('entry_level', 20, 40)
            exit_level = trial.suggest_int('exit_level', 60, 80)
            
            # Instanciar estratégia com os parâmetros sugeridos
            strategy = TrendRSIStrategy(
                rsi_window=rsi_window,
                sma_window=sma_window,
                entry_level=entry_level,
                exit_level=exit_level
            )
            
            # Rodar backtest
            portfolio = strategy.run_backtest(self.data)
            metrics = strategy.get_metrics(portfolio)
            
            # Função Objetivo: Maximizar Profit Factor
            # Adicionamos uma penalidade se o número de trades for muito baixo
            if metrics['total_trades'] < 10:
                return -1.0
            
            return metrics['profit_factor']

        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials)
        
        print("\n--- Otimização Concluída ---")
        print(f"Melhor Profit Factor: {study.best_value:.2f}")
        print(f"Melhores Parâmetros: {study.best_params}")
        
        return study.best_params

if __name__ == "__main__":
    # Mock data para teste
    import numpy as np
    close = np.linspace(20000, 30000, 1000) + np.random.normal(0, 500, 1000)
    data = pd.DataFrame({'close': close})
    
    optimizer = StrategyOptimizer(data)
    best = optimizer.optimize_rsi_trend(n_trials=20)
    print(best)
