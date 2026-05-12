# Quant Strategy Loop (v1.0.0-stable)

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![VectorBT](https://img.shields.io/badge/backtest-VectorBT-orange.svg)

Laboratório industrial de simulação e evolução de estratégias quantitativas para criptoativos, integrando dados de Exchanges (CEX) e fundamentos On-chain (Pendle Finance).

## 🚀 Funcionalidades
- **Ingestão Híbrida:** Coleta automática de OHLCV (CCXT) e dados DeFi (TVL/Yield via DeFiLlama).
- **Backtesting Vetorizado:** Motor ultra-rápido baseado em VectorBT.
- **Otimização Bayesiana:** Busca de hiperparâmetros automatizada via Optuna.
- **Auditoria de Robustez:** Validação Walk-Forward para evitar overfitting.
- **Governança:** Relatórios automáticos em JSON/MD para cada simulação.
- **Dashboard:** Interface Streamlit interativa com curva de equity e insights on-chain.

## 📦 Estrutura do Projeto
- `src/data/`: Ingestores de mercado e on-chain.
- `src/strategy/`: Implementações de estratégias (STR-0001 a STR-0004).
- `src/utils/`: Gerador de relatórios e validador estatístico.
- `main.py`: Orquestrador do loop de simulação.
- `dashboard.py`: Dashboard de visualização.

## 🛠️ Instalação
```bash
pip install -r requirements.txt
```

## 📈 Como Usar
Para rodar uma simulação completa:
```bash
python main.py
```

Para abrir o dashboard:
```bash
streamlit run dashboard.py
```

## 📄 Documentação de Handoff
- [HANDOFF_TECNICO.md](HANDOFF_TECNICO.md): Guia de arquitetura e lógica.
- [HANDOFF_DASHBOARD.md](HANDOFF_DASHBOARD.md): Guia para expansão da UI/UX.
- [HISTORICO_CHAT.md](HISTORICO_CHAT.md): Auditoria cronológica do desenvolvimento.

## ⚖️ Licença
MIT License.
