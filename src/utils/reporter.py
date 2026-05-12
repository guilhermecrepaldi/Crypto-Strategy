import os
import json
import numpy as np
import pandas as pd
from datetime import datetime

class StrategyReporter:
    def __init__(self, reports_dir='reports'):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)

    def generate_report(self, strategy_id, metrics, trades_sample, equity_series=None, next_hypothesis=None, run_id=None):
        """
        Gera os relatórios MD e JSON para uma execução.
        """
        if run_id is None:
            run_id = f"RUN-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        md_content = self._build_markdown(strategy_id, run_id, metrics, trades_sample, next_hypothesis)
        json_data = self._build_json(strategy_id, run_id, metrics, equity_series, next_hypothesis)
        
        # Salvar MD
        md_path = os.path.join(self.reports_dir, f"{run_id}_{strategy_id}.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        # 2. Salvar JSON (Com conversão de tipos para evitar erros de serialização)
        def convert_types(obj):
            if isinstance(obj, (np.int64, np.int32)):
                return int(obj)
            if isinstance(obj, (np.float64, np.float32)):
                return float(obj)
            if isinstance(obj, pd.Timestamp):
                return str(obj)
            return obj

        # Limpar o dict de métricas para serialização
        serializable_metrics = {k: convert_types(v) for k, v in json_data['metrics'].items()}
        json_data['metrics'] = serializable_metrics

        # Salvar JSON
        json_path = os.path.join(self.reports_dir, f"{run_id}_{strategy_id}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, default=convert_types)
            
        print(f"Relatórios gerados em: {self.reports_dir}")
        return md_path, json_path

    def _build_markdown(self, strategy_id, run_id, metrics, trades_sample, next_hypothesis):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = "Aprovada" if metrics['profit_factor'] > 1.5 else "Estudo"
        
        md = f"""# Relatório de Simulação: {strategy_id}

**Run ID:** {run_id}  
**Status:** {status}  
**Data do Relatório:** {now}  
**Capital Inicial:** {metrics['initial_value']:.4f} BTC

---

## 1. Performance Sumária

- Capital Inicial: {metrics['initial_value']:.4f} BTC
- Capital Final: {metrics['final_value']:.4f} BTC
- Retorno Líquido: {metrics['total_return_pct']:.2f}%
- Drawdown Máximo: {metrics['max_drawdown_pct']:.2f}%
- Score Operacional: {self._calculate_score(metrics)}

---

## 2. Estatísticas Operacionais

- Total de Trades: {metrics['total_trades']}
- Taxa de Acerto: {metrics['win_rate_pct']:.2f}%
- Profit Factor: {metrics['profit_factor']:.2f}

---

## 3. Log de Operações — Amostra

| Data/Hora Entrada | Ativo | Resultado |
|---|---|---|
"""
        for trade in trades_sample:
            md += f"| {trade.get('entry_date')} | {trade.get('symbol')} | {trade.get('result_pct'):.2f}% |\n"
            
        md += "\n---\n\n## 4. Próxima Hipótese\n\n"
        if next_hypothesis:
            md += f"**Nova Estratégia Sugerida:** {next_hypothesis['next_strategy_id']}\n\n"
            md += f"**Motivo:** {next_hypothesis['reason']}\n\n"
            md += f"**Parâmetros Propostos:** `{json.dumps(next_hypothesis['params'])}`\n"
        else:
            md += "Aguardando diagnóstico evolutivo.\n"
            
        return md

    def _build_json(self, strategy_id, run_id, metrics, equity_series, next_hypothesis):
        equity_data = []
        if equity_series is not None:
            # Converter Series para lista de dicionários [{date, value}, ...]
            equity_data = equity_series.reset_index().rename(columns={'index': 'date', 'value': 'equity'}).to_dict('records')
            # Garantir que a data seja string
            for item in equity_data:
                item['date'] = str(item['date'])

        return {
            "run_id": run_id,
            "strategy_id": strategy_id,
            "metrics": metrics,
            "equity_curve": equity_data,
            "next_hypothesis": next_hypothesis,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }

    def _calculate_score(self, metrics):
        # Lógica simples de score conforme o handoff
        score = 0
        if metrics['total_return_pct'] > 0: score += 20
        if metrics['max_drawdown_pct'] < 15: score += 20
        if metrics['profit_factor'] > 1.2: score += 20
        if metrics['win_rate_pct'] > 50: score += 20
        if metrics['total_trades'] > 10: score += 20
        return score
