$readme = @'
# Pipeline de saúde: coorte sintética COVID-19 (Synthea)

Projeto final do curso de engenharia de dados. Pipeline em Python + SQL + DuckDB,
com três camadas (raw → refined → marts), testes com pytest e histórico de commits por etapa.

## Fonte do dado

- **Conjunto:** Synthetic Cohort for VHA Innovation Ecosystem and precisionFDA
  COVID-19 Risk Factor Modeling Challenge (147.451 pacientes sintéticos, gerados
  pelo Synthea, módulo COVID-19).
- **Página:** https://www.data.va.gov/d/f6q6-hh5x
- **Licença:** CC0 1.0 (domínio público), conforme o catálogo do dado.
  Confirmada em: _(preencher a data ao baixar)_
- **Dicionário de dados (formato CSV do Synthea):**
  https://github.com/synthetichealth/synthea/wiki/CSV-File-Data-Dictionary
- Os dados são **sintéticos**: não representam pessoas reais.

## Estrutura

    data/raw/      dado bruto, exatamente como baixado (fora do git)
    data/db/       banco DuckDB gerado pelo pipeline (fora do git)
    sql/refined/   transformações da camada refined
    sql/marts/     um .sql por indicador
    src/           scripts Python do pipeline
    tests/         testes pytest (dado inventado, sem abrir o banco)

## Como rodar

Requisitos: Python 3.14.2 (versão em que o projeto foi desenvolvido) e Git.
As dependências têm versão fixa em `requirements.txt` para o pipeline rodar
igual em outra máquina.

    git clone <url-do-repositorio>
    cd saude-pipeline
    python -m venv .venv
    .venv\Scripts\Activate.ps1      # Windows (PowerShell)
    pip install -r requirements.txt

_(os próximos passos entram conforme as etapas forem entregues)_

## Perguntas que o dado responde

_(a preencher na etapa de exploração)_

## Onde a IA errou ou assumiu algo

1. **Sistema operacional.** A IA passou comandos de bash sem perguntar qual era
   o terminal; no PowerShell eles falharam (o texto do