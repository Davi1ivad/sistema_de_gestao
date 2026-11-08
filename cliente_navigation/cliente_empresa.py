import streamlit as st
import registradores.registro_empresa as registro_empresa
from validacoes import validar_cnpj
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from io import BytesIO
from datetime import datetime
import sqlite3


def conectar_banco():
    acessar_db = sqlite3.connect("database.db")
    acessar_db.execute("PRAGMA foreign_keys = ON")
    return acessar_db

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


opcao = st.radio("",["Cadastro","relatorio"],horizontal=True,label_visibility="collapsed")

if opcao =="Cadastro":
    with st.form("formulario_empresa"):
        col1, col2 = st.columns(2)
        with col1:
            razao_social = st.text_input("Razão Social")
        with col2:
            nome_fantasia = st.text_input("Nome Fantasia")
        col1, col2 = st.columns(2)
        with col1:
            cnpj = st.text_input("CNPJ")
        with col2:
            telefone = st.text_input("Telefone")
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("E-mail")
        with col2:
            endereco = st.text_input("Endereço")
            status = st.selectbox("Status",["Ativa", "Inativa"])
        cadastrar = st.form_submit_button("Cadastrar")

        if cadastrar:
            if razao_social == "" or nome_fantasia == ""or cnpj == ""or telefone == ""or email == ""or endereco == ""or status == "":
                st.error("Preencha TODOS OS CAMPOS CORRETAMENTE.")
            elif not validar_cnpj(cnpj):
                st.error("CNPJ inválido. Confira os caracteres e dígitos verificadores.")
            else:
                try:
                    registro_empresa.InserirDados(razao_social,nome_fantasia,cnpj,telefone,email,endereco,status)
                    st.success("Empresa cadastrada com sucesso!")
                except Exception as erro:
                    st.error(f"Erro ao cadastrar: {erro}")

elif opcao == "relatorio":
    # BLOCO DO BUSCADOR
    with st.form("formulario_busca_relatorio"):
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("E-mail")
        with col2:
            cnpj = st.text_input("CNPJ")
        buscar = st.form_submit_button("Buscar")
    # BLOCO DA VERIFICAÇÃO
    if buscar:
        if email == "" and cnpj == "":
            st.error("Preencha o e-mail ou o CNPJ.")
        else:
            empresa = registro_empresa.buscar_empresa(email, cnpj)
            if empresa:
                st.session_state.empresa_relatorio = empresa
                st.success("Empresa encontrada!")
            else:
                st.session_state.empresa_relatorio = None
                st.warning("Empresa não encontrada.")
    # MOSTRA A EMPRESA ENCONTRADA
    if st.session_state.get("empresa_relatorio"):
        empresa = st.session_state.empresa_relatorio
        st.subheader("#Empresa selecionada")
        st.write("**Razão Social:**", empresa[1])
        st.write("**Nome Fantasia:**", empresa[2])
        st.write("**CNPJ:**", empresa[3])
        st.write("**Telefone:**", empresa[4])
        st.write("**E-mail:**", empresa[5])
        st.write("**Endereço:**", empresa[6])
        st.write("**Status:**", empresa[7])

        # BOTÃO PARA GERAR PDF
        if st.button("Gerar PDF"):
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=A4)
            largura, altura = A4

            # TÍTULO
            pdf.setFont("Helvetica-Bold", 18)
            pdf.drawString(2 * cm,altura - 2 * cm,"RELATÓRIO DA EMPRESA")
            pdf.line(2 * cm,altura - 2.4 * cm,largura - 2 * cm,altura - 2.4 * cm)

            # DADOS DA EMPRESA
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(2 * cm,altura - 3.5 * cm,"Dados da Empresa")

            pdf.setFont("Helvetica", 11)
            y = altura - 4.3 * cm
            pdf.drawString(2 * cm,y,f"Razão Social: {empresa[1]}")
            y -= 0.7 * cm
            pdf.drawString(2 * cm,y,f"Nome Fantasia: {empresa[2]}")
            y -= 0.7 * cm
            pdf.drawString(2 * cm,y,f"CNPJ: {empresa[3]}")
            y -= 0.7 * cm
            pdf.drawString(2 * cm,y,f"Telefone: {empresa[4]}")
            y -= 0.7 * cm
            pdf.drawString(2 * cm,y,f"E-mail: {empresa[5]}")
            y -= 0.7 * cm
            pdf.drawString(2 * cm,y,f"Endereço: {empresa[6]}")
            y -= 0.7 * cm
            pdf.drawString(2 * cm,y,f"Status: {empresa[7]}")
            y -= 0.7 * cm
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            pdf.drawString(2 * cm,y,f"Gerado em: {data_hora}")

            pdf.save()
            buffer.seek(0)
    
            st.download_button(label="Baixar PDF",data=buffer,file_name=f"relatorio_{empresa[2]}.pdf",mime="application/pdf")

