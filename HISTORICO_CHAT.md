# HISTÓRICO DE CHAT - crypto_Strategy
Projeto: Estratégias de Criptoativos
Início: 2026-05-12

## [2026-05-12 14:50] - Refinamento: Ingestão de Yield (APY)
**Status:** Dados de Rendimento Ativos
**Objetivo:** Capturar a atratividade das pools de liquidez do Pendle.
**Resumo:** Expandido o `OnchainIngestor` para suportar a coleta de histórico de APY via DeFiLlama Yields API.
**Decisões:** 
1. Implementada descoberta dinâmica de pools por projeto (`project='pendle'`).
2. Preparação para indicadores de sentimento baseados em Yield (Leading Indicators).
