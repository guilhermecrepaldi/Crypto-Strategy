# HISTÓRICO DE CHAT - crypto_Strategy
Projeto: Estratégias de Criptoativos
Início: 2026-05-12

## [2026-05-12 13:11] - Implementação: DataIngestor
**Status:** Módulo de Ingestão Concluído
**Objetivo:** Automatizar a coleta de OHLCV histórico.
**Resumo:** Criada classe `DataIngestor` com suporte a paginação CCXT e persistência Parquet.
**Decisões:** 
1. Uso de `pyarrow` para garantir compactação e velocidade no Parquet.
2. Armazenamento em `data/raw/` para separação de dados crus.
