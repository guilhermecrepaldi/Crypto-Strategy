# HISTÓRICO DE CHAT - crypto_Strategy
Projeto: Estratégias de Criptoativos
Início: 2026-05-12

## [2026-05-12 14:52] - Integração: Auditoria de Robustez no Loop
**Status:** Governança Estatística 100%
**Objetivo:** Automatizar a validação de toda estratégia gerada.
**Resumo:** O `main.py` agora executa automaticamente o `WalkForwardValidator`, integrando o "Stability Score" aos relatórios finais.
**Decisões:** 
1. Bloqueio conceitual de estratégias com baixa estabilidade.
2. Inclusão da métrica de consistência no schema JSON de auditoria.
