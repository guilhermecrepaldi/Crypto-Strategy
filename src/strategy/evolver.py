import json
import os

class StrategyEvolver:
    def __init__(self):
        pass

    def evolve(self, run_json_path):
        """
        Lê o resultado de uma run de um arquivo e sugere a próxima mutação.
        """
        with open(run_json_path, 'r') as f:
            data = json.load(f)
        return self.evolve_from_dict(data)

    def evolve_from_dict(self, data):
        """
        Analisa os dados de uma run e sugere a próxima mutação.
        """
        metrics = data['metrics']
        strategy_id = data['strategy_id']
        
        # Lógica de Mutação Heurística (Fase Inicial)
        # Exemplo focado em RSI (STR-0001)
        next_params = {}
        reason = ""
        
        if strategy_id == "STR-0001":
            current_rsi = 14 # Idealmente leríamos do JSON de config, mas vamos assumir default
            
            if metrics['win_rate_pct'] < 40:
                # Se acerta pouco, talvez o RSI esteja capturando muito ruído. 
                # Sugerimos aumentar a janela do RSI para filtrar.
                next_params['rsi_window'] = 21
                reason = "Win Rate baixo (<40%). Aumentando janela do RSI para 21 para reduzir sinais falsos."
            elif metrics['total_trades'] < 5:
                # Se opera pouco, talvez os níveis estejam muito extremos.
                # Sugerimos afrouxar os níveis de entrada.
                next_params['entry_level'] = 35
                next_params['exit_level'] = 65
                reason = "Poucos trades. Afrouxando níveis de RSI para 35/65 para aumentar frequência."
            else:
                # Mutação padrão: tentar um RSI mais rápido (ex: 9) se o drawdown permitir
                if metrics['max_drawdown_pct'] < 10:
                    next_params['rsi_window'] = 9
                    reason = "Drawdown saudável. Testando RSI 9 para maior agressividade."
                else:
                    next_params['rsi_window'] = 14
                    reason = "Mantendo RSI 14, mas sugerindo filtro de tendência (Fase Futura)."

        # Construir ID da Próxima Estratégia
        try:
            current_num = int(strategy_id.split('-')[1])
            next_id = f"STR-{str(current_num + 1).zfill(4)}"
        except:
            next_id = "STR-0002"

        return {
            "next_strategy_id": next_id,
            "params": next_params,
            "reason": reason
        }

if __name__ == "__main__":
    # Teste se houver algum relatório
    reports = [f for f in os.listdir('reports') if f.endswith('.json')]
    if reports:
        evolver = StrategyEvolver()
        suggestion = evolver.evolve(os.path.join('reports', reports[0]))
        print(f"Sugestão de Evolução:")
        print(json.dumps(suggestion, indent=2))
    else:
        print("Nenhum relatório encontrado para testar a evolução.")
