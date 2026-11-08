import streamlit as st# Main page content


#botao para ir pro login
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("Sair para o login"):
        st.session_state.logado = False
        st.session_state.colaborador = None
        st.switch_page("index.py")
        


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