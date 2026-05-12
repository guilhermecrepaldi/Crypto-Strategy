import sys
import importlib

def check_dependencies():
    deps = [
        "pandas", "ccxt", "vectorbt", "duckdb", "optuna", "streamlit", "plotly"
    ]
    print("--- Verificando Dependências ---")
    all_ok = True
    for dep in deps:
        try:
            importlib.import_module(dep)
            print(f"[OK] {dep}")
        except ImportError:
            print(f"[FALHA] {dep} não instalado.")
            all_ok = False
    return all_ok

if __name__ == "__main__":
    if check_dependencies():
        print("\nAmbiente pronto para operação industrial. 🚀")
    else:
        print("\nAlgumas dependências estão faltando. Execute: pip install -r requirements.txt")
        sys.exit(1)
