# HISTÓRICO DE CHAT - crypto_Strategy
Projeto: Estratégias de Criptoativos
Início: 2026-05-12

## [2026-05-12 13:45] - Evolução: TrendRSIStrategy (STR-0002)
**Status:** Estratégia Evoluída Implementada
**Objetivo:** Reduzir trades perdedores contra a tendência principal.
**Resumo:** Criada a `TrendRSIStrategy` que combina RSI com uma Média Móvel Simples (SMA 200) como filtro de tendência.
**Decisões:** 
1. Entradas permitidas apenas quando o preço está acima da SMA 200.
2. Saída antecipada se a tendência de alta for quebrada.
