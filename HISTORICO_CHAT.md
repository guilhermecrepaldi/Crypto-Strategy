# HISTÓRICO DE CHAT - crypto_Strategy
Projeto: Estratégias de Criptoativos
Início: 2026-05-12

## [2026-05-12 14:44] - Inovação: Estratégia Híbrida (STR-0003)
**Status:** Alpha Test (On-chain Integrated)
**Objetivo:** Usar fundamentos de rede (TVL) como filtro de sentimento.
**Resumo:** Implementada a `OnchainRSIStrategy` que cruza dados de OHLCV com o TVL do Pendle Finance.
**Decisões:** 
1. Alinhamento de dados temporais via Forward Fill (`ffill`).
2. Filtro de "Saúde do Ecossistema": Operar apenas com TVL em tendência de alta.
