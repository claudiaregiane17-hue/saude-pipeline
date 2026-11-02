"""Executa a transformação da camada Raw para a camada Refined no DuckDB."""
from pathlib import Path
import duckdb

DB_PATH = Path("data/saude.duckdb")
SQL_PATH = Path("sql/refined/refined_internacoes.sql")

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    
    print("Criando tabela refined_internacoes a partir dos Parquets...")
    query = SQL_PATH.read_text(encoding="utf-8")
    
    con.execute(f"CREATE OR REPLACE TABLE refined_internacoes AS {query}")
    
    total = con.execute("SELECT count(*) FROM refined_internacoes").fetchone()[0]
    print(f"Camada Refined pronta: {total:,} registros limpos e tipados.")
    con.close()

if __name__ == "__main__":
    main()
