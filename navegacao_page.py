import streamlit as st

#definir como cada pagina deve ser chamada
index_page = st.Page("index.py",title="Login")
registro_simples = st.Page("registradores/registro_simples.py",title="Registro Simples")
login = st.Page("login.py",title="Login")

#paginas dentro do login do colaborador
auditoria = st.Page("page_navigation/page_auditoria.py",title="Auditoria")
cliente  = st.Page("page_navigation/page_cliente.py",title="cliente")
dashboard  = st.Page("page_navigation/page_dashboard.py",title="dashboard")
documento = st.Page("page_navigation/page_documento.py",title="documento")
empresa = st.Page("page_navigation/page_empresa.py",title="empresa")
relatorio = st.Page("page_navigation/page_relatorio.py",title="relatorio")

#paginas dentro do login do cliente
cliente_empresa = st.Page("cliente_navigation/cliente_empresa.py",title="Cliente")
cliente_dashboard = st.Page("cliente_navigation/cliente_dashboard.py",title="Dashboard")


pg = st.navigation([index_page, registro_simples,login,auditoria,cliente,dashboard,documento,empresa,relatorio,cliente_empresa,cliente_dashboard],position='hidden')
pg.run()