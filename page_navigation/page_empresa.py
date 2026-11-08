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

st.title('🏢 Empresa🏢')
if "empresa_encontrada" not in st.session_state:
    st.session_state.empresa_encontrada = None

#botao para ir pro login
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("Sair para o login"):
        st.session_state.logado = False
        st.session_state.colaborador = None
        st.switch_page("index.py")
st.divider()
#navegar pelas paginas
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
st.divider()


#bloco de cadastro da empresa(
opcao = st.radio("",["Editar","Relatório","Vinculação"],horizontal=True,label_visibility="collapsed")


if opcao == "Editar":
    #bloco do buscador(
    with st.form("formulario_busca_empresa"):
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("E-mail")
        with col2:
            cnpj = st.text_input("CNPJ")
        buscar = st.form_submit_button("Buscar")
        #bloco do buscador)
        #bloco da verificação(
    if buscar:
        if email == "" and cnpj == "":
            st.error("Preencha o e-mail ou o CNPJ.")
        else:
            empresa = registro_empresa.buscar_empresa(email, cnpj)
            if empresa:
                st.session_state.empresa_encontrada = empresa
                st.success("Empresa encontrada!")
            else:
                st.session_state.empresa_encontrada = None
                st.warning("Empresa não encontrada.")
        #bloco da verificação)
        #bloco das informaçoes do dados(
    if st.session_state.get("empresa_encontrada"):
        empresa = st.session_state.empresa_encontrada
        st.subheader("Dados da empresa")
        col1, col2 = st.columns(2)
        with col1:
            razao_social = st.text_input("Razão Social",value=empresa[1])
        with col2:
            nome_fantasia = st.text_input("Nome Fantasia",value=empresa[2])
        col1, col2 = st.columns(2)
        with col1:
            cnpj = st.text_input("CNPJ",value=empresa[3])
        with col2:
            telefone = st.text_input("Telefone",value=empresa[4])
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("E-mail",value=empresa[5])
        with col2:
            endereco = st.text_input("Endereço",value=empresa[6])
        status = st.selectbox("Status",["Ativa", "Inativa"],index=0 if empresa[7] == "Ativa" else 1)
        atualizar = st.button("Atualizar")
        if atualizar:
            if not validar_cnpj(cnpj):
                st.error("CNPJ inválido. Confira os caracteres e dígitos verificadores.")
            else:
                try:
                    registro_empresa.atualizar_empresa(empresa[0],razao_social,nome_fantasia,cnpj,telefone,email,endereco,status)
                    st.success("Empresa atualizada com sucesso!")
                except Exception as erro:
                    st.error(f"Erro ao atualizar empresa: {erro}")
        if status =="Ativa":
            st.success("Empresa ativada com sucesso!")
        else:
            st.info("Empresa inativada com sucesso!")
        st.rerun()

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

elif opcao == "Vinculação":
    total_sem_vinculo = registro_empresa.contar_empresas_sem_vinculo()
    col1, col2 = st.columns([5, 1])
    with col1:
        st.subheader("Vincular Cliente à Empresa")
    with col2:
        st.markdown(f"""
        <div style="background-color: #542b18; border: 1px solid #a96532;border-radius: 10px;padding: 10px 15px;text-align: center;margin-top: 5px;min-width: 170px;">
        <div style="color: #ffca91;font-size: 13px; font-weight: bold;">Empresas sem vínculo</div>
        <div style="color: #ffb36b;font-size: 30px;font-weight: bold;"> {total_sem_vinculo}</div>""",unsafe_allow_html=True)
    acessar_db = conectar_banco()
    cursor = acessar_db.cursor()
    try:
        cursor.execute("SELECT id, razao_social, nome_fantasia, cnpj, status FROM empresas ORDER BY nome_fantasia")
        empresas = cursor.fetchall()
        if not empresas:
            st.warning("Nenhuma empresa cadastrada.")
            st.stop()
        cursor.execute("SELECT id, nome, cpf, status FROM clientes ORDER BY nome")
        clientes = cursor.fetchall()
        if not clientes:
            st.warning("Nenhum cliente cadastrado.")
        opcoes_clientes = {f"{cliente[1]} - CPF: {cliente[2]}": cliente for cliente in clientes}
        cliente_selecionado = st.selectbox("Selecione o cliente",list(opcoes_clientes.keys()))
        cliente = opcoes_clientes[cliente_selecionado]
        cliente_id = cliente[0]
        cliente_nome = cliente[1]
        cliente_cpf = cliente[2]
        cursor.execute("""
            SELECT
                e.razao_social,
                e.nome_fantasia,
                e.cnpj
            FROM vinculo_cliente_empresa AS v
            INNER JOIN empresas AS e
                ON e.cnpj = v.cnpj_empresa
            WHERE v.cpf_cliente = ?
            ORDER BY e.nome_fantasia
        """, (cliente_cpf,))
        empresas_vinculadas = cursor.fetchall()
        st.markdown("### Empresas vinculadas ao cliente")
        if empresas_vinculadas:
            for empresa_vinculada in empresas_vinculadas:
                st.info(
                    f"**{empresa_vinculada[1]}**  \n"
                    f"Razão social: {empresa_vinculada[0]}  \n"
                    f"CNPJ: {empresa_vinculada[2]}")
        else:
            st.warning("Este cliente ainda não possui empresas vinculadas.")
        st.divider()
        opcoes_empresas = {f"{empresa[2]} - CNPJ: {empresa[3]}": empresa for empresa in empresas}
        empresa_selecionada = st.selectbox("Selecione a empresa para vincular",list(opcoes_empresas.keys()))
        empresa = opcoes_empresas[empresa_selecionada]
        empresa_id = empresa[0]
        empresa_razao = empresa[1]
        empresa_nome = empresa[2]
        empresa_cnpj = empresa[3]
        st.markdown("### Empresa selecionada")
        st.write(f"**Razão social:** {empresa_razao}")
        st.write(f"**Nome fantasia:** {empresa_nome}")
        st.write(f"**CNPJ:** {empresa_cnpj}")
        st.divider()
        if st.button("Vincular cliente à empresa",type="primary"):
            cursor.execute("SELECT id FROM vinculo_cliente_empresa WHERE cpf_cliente = ?AND cnpj_empresa = ?", (cliente_cpf, empresa_cnpj))
            vinculo_existente = cursor.fetchone()
            if vinculo_existente:
                st.warning("Este cliente já está vinculado a esta empresa.")
            else:
                cursor.execute("INSERT INTO vinculo_cliente_empresa (cpf_cliente,cnpj_empresa)VALUES (?, ?)", (cliente_cpf, empresa_cnpj))
                acessar_db.commit()
                st.success(f"Cliente '{cliente_nome}' vinculado " f"à empresa '{empresa_nome}' com sucesso!")
    except Exception as erro:
        st.error(f"Erro ao realizar a vinculação: {erro}")
        acessar_db.close()
