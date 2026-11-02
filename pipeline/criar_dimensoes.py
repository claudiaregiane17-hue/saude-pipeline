"""Gera a tabela dimensional de capítulos da CID-10 para o JOIN no pipeline."""
from pathlib import Path
import duckdb

DESTINO = Path("data/raw/dim/capitulos_cid10.parquet")
DESTINO.parent.mkdir(parents=True, exist_ok=True)

# Mapeamento oficial dos capítulos da CID-10 mais frequentes no SUS
dados = [
    ("A", "B", "I - Algumas Doenças Infecciosas e Parasitárias"),
    ("C", "D", "II - Neoplasias (Tumores)"),
    ("E", "E", "IV - Doenças Endócrinas, Nutricionais e Metabólicas"),
    ("F", "F", "V - Transtornos Mentais e Comportamentais"),
    ("G", "G", "VI - Doenças do Sistema Nervoso"),
    ("H", "H", "VII/VIII - Doenças do Olho e Ouvido"),
    ("I", "I", "IX - Doenças do Aparelho Circulatório"),
    ("J", "J", "X - Doenças do Aparelho Respiratório"),
    ("K", "K", "XI - Doenças do Aparelho Digestivo"),
    ("L", "L", "XII - Doenças da Pele e Tecido Subcutâneo"),
    ("M", "M", "XIII - Doenças do Sistema Osteomuscular"),
    ("N", "N", "XIV - Doenças do Aparelho Geniturinário"),
    ("O", "O", "XV - Gravidez, Parto e Puerpério"),
    ("P", "P", "XVI - Algumas Afecções Perinatais"),
    ("Q", "Q", "XVII - Malformações Congênitas"),
    ("R", "R", "XVIII - Sintomas e Sinais Anormais"),
    ("S", "T", "XIX - Lesões, Envenenamentos e Causas Externas"),
    ("U", "Z", "XXI - Fatores que Influenciam o Estado de Saúde"),
]

def main():
    con = duckdb.connect()
    con.execute("""
        CREATE TABLE capitulos (
            letra_inicio VARCHAR,
            letra_fim VARCHAR,
            nome_capitulo VARCHAR
        );
    """)
    for li, lf, nome in dados:
        con.execute("INSERT INTO capitulos VALUES (?, ?, ?)", [li, lf, nome])
    
    con.execute(f"COPY capitulos TO '{DESTINO.as_posix()}' (FORMAT PARQUET)")
    print(f"Dimensão CID-10 gerada com sucesso em {DESTINO}")

if __name__ == "__main__":
    main()
