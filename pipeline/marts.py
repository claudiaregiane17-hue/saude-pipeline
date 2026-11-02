"""Executa os arquivos SQL da pasta sql/marts e materializa as tabelas no DuckDB."""
from pathlib import Path
import duckdb

DB_PATH = Path("data/saude.duckdb")
MARTS_DIR = Path("sql/marts")

def main():
    con = duckdb.connect(str(DB_PATH))
    
    for arquivo_sql in sorted(MARTS_DIR.glob("*.sql")):
        nome_tabela = f"mart_{arquivo_sql.stem}"
        query = arquivo_sql.read_text(encoding="utf-8")
        con.execute(f"CREATE OR REPLACE TABLE {nome_tabela} AS {query}")
        linhas = con.execute(f"SELECT count(*) FROM {nome_tabela}").fetchone()[0]
        print(f"Mart {nome_tabela} criado com sucesso ({linhas} linhas).")
        
    con.close()

if __name__ == "__main__":
    main()
