"""Testes unitários das regras de negócio do pipeline de saúde com dados sintéticos."""
import duckdb
import pytest

@pytest.fixture
def con_memoria():
    """Conexão DuckDB em memória com tabela sintética de internações."""
    con = duckdb.connect(":memory:")
    con.execute("""
        CREATE TABLE refined_internacoes (
            id_internacao VARCHAR,
            data_internacao DATE,
            data_saida DATE,
            dias_permanencia INTEGER,
            flag_obito INTEGER,
            valor_total_hospitalar DOUBLE,
            valor_uti DOUBLE
        );
        INSERT INTO refined_internacoes VALUES
            ('001', '2025-01-01', '2025-01-04', 3, 0, 1500.0, 0.0),
            ('002', '2025-01-02', '2025-01-02', 1, 0, 500.0, 0.0),
            ('003', '2025-01-05', '2025-01-15', 10, 1, 10000.0, 5000.0),
            ('004', '2025-01-10', '2025-01-12', 2, 0, 800.0, 0.0);
    """)
    yield con
    con.close()

def test_calculo_taxa_mortalidade(con_memoria):
    """Testa se a taxa de mortalidade reflete óbitos/internações."""
    res = con_memoria.execute("""
        SELECT ROUND(100.0 * SUM(flag_obito) / COUNT(*), 2) FROM refined_internacoes
    """).fetchone()[0]
    # 1 óbito em 4 internações = 25%
    assert res == 25.0

def test_permanencia_media(con_memoria):
    """Testa o cálculo da permanência média em dias."""
    res = con_memoria.execute("""
        SELECT ROUND(AVG(dias_permanencia), 1) FROM refined_internacoes
    """).fetchone()[0]
    # (3 + 1 + 10 + 2) / 4 = 4.0
    assert res == 4.0

def test_faturamento_total(con_memoria):
    """Testa a agregação de custo hospitalar total."""
    res = con_memoria.execute("""
        SELECT SUM(valor_total_hospitalar) FROM refined_internacoes
    """).fetchone()[0]
    # 1500 + 500 + 10000 + 800 = 12800.0
    assert res == 12800.0

def test_garantia_diaria_minima():
    """Garante que a permanência nunca seja menor que 1, mesmo para internação de 1 dia."""
    con = duckdb.connect(":memory:")
    dias = con.execute("SELECT GREATEST('2025-01-01'::DATE - '2025-01-01'::DATE, 1)").fetchone()[0]
    assert dias == 1
