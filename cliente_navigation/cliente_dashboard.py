import streamlit as st



col1, col2 = st.columns([4, 1])
with col2:
    if st.button("Sair para o login"):
        st.session_state.logado = False
        st.session_state.colaborador = None
        st.switch_page("index.py")

st.write("### 'Nome da empresa(Em validação)'")
st.divider()

with st.container(horizontal=True):
     paginas = {
        "📊 Dashboard": "cliente_navigation/cliente_dashboard.py",
        "🏢 Empresa": "cliente_navigation/cliente_empresa.py"}
     for nome,pagina in paginas.items():
         if st.button(nome):
            st.switch_page(pagina)