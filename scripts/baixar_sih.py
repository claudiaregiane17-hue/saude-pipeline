"""Baixa os arquivos mensais do SIH (AIH reduzida, RD) de MG em 2025.

Camada raw: copia os arquivos Parquet entregues pelo PySUS, sem alterar.
Os arquivos ficam em data/raw/sih/ (ignorado pelo Git); só a contagem
de linhas por mês é versionada.
"""
import json
import shutil
from pathlib import Path

import pyarrow.parquet as pq
from pysus import sih

UF = "MG"
ANO = 2025
DESTINO = Path("data/raw/sih")
RESUMO = Path("docs/contagem_raw_sih.json")


def baixar_mes(mes: int) -> list[Path]:
    """Baixa o mês e devolve os caminhos dos Parquet do grupo RD."""
    try:
        resultado = sih(state=UF, year=ANO, month=mes)
    except Exception:
        return []

    if not resultado:
        return []

    # O PySUS devolve os 4 grupos (RD, RJ, SP, ER).
    # Filtramos apenas o grupo RD (AIH reduzida):
    caminhos = []
    for item in resultado:
        caminho = Path(getattr(item, "path", item))
        if caminho.name.upper().startswith("RD"):
            caminhos.append(caminho)

    return caminhos


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    RESUMO.parent.mkdir(parents=True, exist_ok=True)
    resumo = {}

    for mes in range(1, 13):
        rotulo = f"{ANO}-{mes:02d}"
        try:
            caminhos = baixar_mes(mes)
        except Exception as erro:
            resumo[rotulo] = {"status": "falhou", "erro": str(erro)[:200]}
            print(f"{rotulo}: FALHOU ({erro})")
            continue

        if not caminhos:
            resumo[rotulo] = {"status": "indisponivel", "linhas": 0}
            print(f"{rotulo}: sem dados")
            continue

        linhas = 0
        colunas = 0
        for origem in caminhos:
            destino = DESTINO / origem.name
            shutil.copy2(origem, destino)
            meta = pq.ParquetFile(destino).metadata
            linhas += meta.num_rows
            colunas = meta.num_columns

        resumo[rotulo] = {
            "status": "ok",
            "arquivos": [c.name for c in caminhos],
            "linhas": linhas,
            "colunas": colunas,
        }
        print(f"{rotulo}: {linhas:,} linhas, {colunas} colunas")

    RESUMO.write_text(
        json.dumps(resumo, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
