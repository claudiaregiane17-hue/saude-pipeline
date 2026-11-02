import duckdb
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Monitor SUS MG 2025", page_icon="🏥", layout="wide")

DB_PATH = "data/saude.duckdb"

@st.cache_data
def ler_dados():
    """Abre e fecha a conexão internamente para evitar lock no DuckDB."""
    con = duckdb.connect(DB_PATH, read_only=True)
    kpis = con.execute("SELECT * FROM mart_kpis_gerais").df().iloc[0]
    mensal = con.execute("SELECT * FROM mart_internacoes_mensais").df()
    causas = con.execute("SELECT * FROM mart_top_causas_internacao LIMIT 10").df()
    con.close()
    return kpis, mensal, causas

# Botão de recarregar dados conforme solicitado na spec do curso
if st.sidebar.button("🔄 Recarregar dados"):
    st.cache_data.clear()

kpis, mensal, causas = ler_dados()

st.title("🏥 Monitor de Internações Hospitalares — SUS MG (2025)")
st.caption("Painel analítico alimentado pela camada de Marts (DuckDB). Fonte: DATASUS / PySUS.")

# Cartões de KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Internações", f"{int(kpis['total_internacoes']):,}".replace(",", "."))
col2.metric("Gasto Total (R$)", f"R$ {kpis['faturamento_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col3.metric("Taxa de Mortalidade", f"{kpis['taxa_mortalidade_pct']}%")
col4.metric("Permanência Média", f"{kpis['permanencia_media_dias']} dias")

st.divider()

# Gráficos
col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("📅 Evolução Mensal de Internações")
    fig_mensal = px.line(
        mensal,
        x="mes_ano",
        y="qtd_internacoes",
        markers=True,
        labels={"mes_ano": "Mês", "qtd_internacoes": "Internações"},
    )
    st.plotly_chart(fig_mensal, width="stretch")

with col_dir:
    st.subheader("🩺 Top Causas de Hospitalização (CID-10)")
    # Ordenação decrescente: o maior no topo
    fig_causas = px.bar(
        causas,
        x="total_internacoes",
        y="causa_internacao",
        orientation="h",
        labels={"total_internacoes": "Internações", "causa_internacao": "Capítulo CID-10"},
    )
    fig_causas.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_causas, width="stretch")
