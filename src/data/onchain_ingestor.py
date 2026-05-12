import requests
import pandas as pd
import os
from datetime import datetime

class OnchainIngestor:
    def __init__(self):
        self.base_url = "https://api.llama.fi"

    def fetch_pendle_tvl(self):
        """
        Busca o histórico de TVL do Pendle Finance via DeFiLlama.
        """
        print("Buscando dados históricos de TVL do Pendle...")
        url = f"{self.base_url}/protocol/pendle"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            tvl_history = data.get('tvl', [])
            
            df = pd.DataFrame(tvl_history)
            # Converter timestamp para datetime
            df['date'] = pd.to_datetime(df['date'], unit='s')
            df.rename(columns={'totalLiquidityUSD': 'tvl_usd'}, inplace=True)
            
            print(f"Sucesso: {len(df)} registros de TVL coletados.")
            return df
        else:
            print(f"Erro ao acessar DeFiLlama: {response.status_code}")
            return pd.DataFrame()

    def fetch_pendle_yields(self):
        """
        Busca todos os pools de yield do Pendle Finance via DeFiLlama Yields.
        """
        print("Buscando pools de Yield do Pendle...")
        url = "https://yields.llama.fi/pools"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            pools = data.get('data', [])
            df = pd.DataFrame(pools)
            
            # Filtrar apenas Pendle
            df_pendle = df[df['project'] == 'pendle'].copy()
            print(f"Encontrados {len(df_pendle)} pools no Pendle.")
            return df_pendle
        return pd.DataFrame()

    def fetch_pool_history(self, pool_uuid):
        """
        Busca o histórico de APY e TVL de um pool específico.
        """
        print(f"Buscando histórico do pool {pool_uuid}...")
        url = f"https://yields.llama.fi/chart/{pool_uuid}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            history = data.get('data', [])
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        return pd.DataFrame()

    def save_onchain_data(self, df, protocol_name="pendle", suffix="tvl"):
        """
        Salva os dados on-chain em formato Parquet para cache imutável.
        """
        if df.empty:
            return None
            
        os.makedirs('data/onchain', exist_ok=True)
        filename = f"data/onchain/{protocol_name}_tvl.parquet"
        df.to_parquet(filename)
        print(f"Dados on-chain salvos em: {filename}")
        return filename

if __name__ == "__main__":
    ingestor = OnchainIngestor()
    df_tvl = ingestor.fetch_pendle_tvl()
    if not df_tvl.empty:
        print(df_tvl.tail())
        ingestor.save_onchain_data(df_tvl)
