import pandas as pd
import numpy as np

class WalkForwardValidator:
    def __init__(self, strategy, n_folds=5):
        self.strategy = strategy
        self.n_folds = n_folds

    def validate(self, df):
        """
        Realiza a validação Walk-Forward dividindo os dados em N janelas.
        """
        print(f"Iniciando Validação Walk-Forward ({self.n_folds} folds) para {self.strategy.name}...")
        
        # Dividir o dataframe em fatias
        split_size = len(df) // self.n_folds
        results = []
        
        for i in range(self.n_folds):
            start_idx = i * split_size
            end_idx = (i + 1) * split_size
            
            fold_data = df.iloc[start_idx:end_idx]
            
            # Rodar Backtest no Fold
            portfolio = self.strategy.run_backtest(fold_data)
            metrics = self.strategy.get_metrics(portfolio)
            
            results.append({
                "fold": i + 1,
                "start": fold_data.index[0],
                "end": fold_data.index[-1],
                "return_pct": metrics['total_return_pct'],
                "drawdown_pct": metrics['max_drawdown_pct'],
                "profit_factor": metrics['profit_factor']
            })
            
        df_results = pd.DataFrame(results)
        
        # Calcular Estabilidade (Média / Desvio Padrão)
        stability_score = df_results['return_pct'].mean() / (df_results['return_pct'].std() + 1e-6)
        
        print(f"Validação Concluída. Stability Score: {stability_score:.2f}")
        return df_results, stability_score

if __name__ == "__main__":
    # Teste rápido
    from src.strategy.trend_rsi_strategy import TrendRSIStrategy
    import numpy as np
    
    close = np.linspace(20000, 30000, 1000) + np.random.normal(0, 500, 1000)
    data = pd.DataFrame({'close': close}, index=pd.date_range('2025-01-01', periods=1000, freq='H'))
    
    validator = WalkForwardValidator(TrendRSIStrategy())
    res, score = validator.validate(data)
    print(res)
