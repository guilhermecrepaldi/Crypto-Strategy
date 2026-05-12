import duckdb
import pandas as pd
import os

class LocalDB:
    def __init__(self, db_path='data/crypto_strategy.db'):
        """
        Inicializa o DuckDB. Pode ser um arquivo local ou :memory:
        """
        self.db_path = db_path
        # Garantir que o diretório data existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = duckdb.connect(db_path)

    def register_parquet(self, table_name, parquet_path):
        """
        Cria uma view ou tabela no DuckDB apontando para o arquivo Parquet.
        Isso permite usar SQL diretamente no arquivo.
        """
        if not os.path.exists(parquet_path):
            raise FileNotFoundError(f"Arquivo Parquet não encontrado: {parquet_path}")
        
        self.conn.execute(f"CREATE OR REPLACE VIEW {table_name} AS SELECT * FROM read_parquet('{parquet_path}')")
        print(f"Tabela '{table_name}' registrada a partir de {parquet_path}")

    def query(self, sql):
        """
        Executa uma query SQL e retorna um DataFrame Pandas.
        """
        return self.conn.execute(sql).df()

    def get_available_tables(self):
        """
        Lista as tabelas/views registradas.
        """
        return self.conn.execute("SHOW TABLES").df()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = LocalDB()
    # Exemplo de uso (assumindo que o arquivo existe após rodar o ingestor)
    parquet_file = 'data/raw/BTC_USDT_1h.parquet'
    if os.path.exists(parquet_file):
        db.register_parquet('btc_1h', parquet_file)
        
        # Exemplo de Query: Média de fechamento
        df_res = db.query("SELECT AVG(close) as avg_close FROM btc_1h")
        print("\nMédia de Fechamento (SQL via DuckDB):")
        print(df_res)
        
        # Exemplo de Query: Primeiros 5 registros
        df_head = db.query("SELECT datetime, close, volume FROM btc_1h LIMIT 5")
        print("\nPrimeiros 5 registros:")
        print(df_head)
    else:
        print(f"Aguardando arquivo {parquet_file} para teste. Rode o ingestor primeiro.")
