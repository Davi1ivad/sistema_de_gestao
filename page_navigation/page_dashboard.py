import streamlit as st# Main page content
import sqlite3


def conectar_banco():
    return sqlite3.connect("database.db")

st.title('📊 Dashboard📊')

#botao para ir pro login
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("Sair para o login"):
        st.session_state.logado = False
        st.session_state.colaborador = None
        st.switch_page("index.py")
st.divider()      


with st.container(horizontal=True):
     paginas = {
        "🔎 Auditoria": "page_navigation/page_auditoria.py",
        "👥 Cliente": "page_navigation/page_cliente.py",
        "📊 Dashboard": "page_navigation/page_dashboard.py",
        "📁 Documento": "page_navigation/page_documento.py",
        "🏢 Empresa": "page_navigation/page_empresa.py",
        "✍️ Relatório": "page_navigation/page_relatorio.py"}
     for nome,pagina in paginas.items():
         if st.button(nome):
            st.switch_page(pagina)     


def contar_cliente():
    acessar_db = conectar_banco()
    cursor = acessar_db.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchone()[0]
    acessar_db.close()
    return total

def contar_empresas():
    acessar_db = conectar_banco()
    cursor = acessar_db.cursor()
    cursor.execute("SELECT COUNT(*) FROM empresas")
    total = cursor.fetchone()[0]
    acessar_db.close()
    return total

def contar_pendentes():
    acessar_db = conectar_banco()
    cursor = acessar_db.cursor()
    cursor.execute("SELECT COUNT(*) FROM empresas")
    total = cursor.fetchone()[0]
    acessar_db.close()
    return total

st.divider()
st.write("### Visão geral do sistema")
try:
    total_clientes = contar_cliente()
    total_empresas = contar_empresas()
except Exception as erro:
    st.error(f"Erro ao consultar o banco de dados: {erro}")
    st.stop()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total de clientes",value=total_clientes)
with col2:
    st.metric(label="Total de empresas",value=total_empresas)
st.divider()
