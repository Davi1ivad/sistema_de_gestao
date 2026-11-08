import streamlit as st
import registradores.registro_pessoa as registro_pessoa
from validacoes import validar_cpf, limpar

if st.button("Login"):
    st.switch_page("index.py")

st.title("Registro Simples")

opcao = st.radio("",["Cliente", "Colaborador","Plenipotenciário"],horizontal=True,label_visibility="collapsed")
#bloco do cadastro do cliente(
if opcao == "Cliente":
    with st.form("formulario_cadastro_cliente"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome")
        with col2:
            senha = st.text_input("Senha",type="password")
        col1, col2 = st.columns(2)
        with col1:
            cpf = st.text_input("CPF", placeholder="000.000.000-00", max_chars=11)
        with col2:
            telefone = st.text_input("Telefone")
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("E-mail")
        with col2:
            empresa_id = st.text_input("ID da Empresa")
        cadastrar_cliente = st.form_submit_button("Cadastrar")
    if cadastrar_cliente:
        if (nome == ""or senha == ""or cpf == "" or telefone == ""or email == ""or empresa_id == ""):
            st.error("Preencha todos os dados.")
        elif not validar_cpf(cpf):
            st.error("CPF inválido. Confira os 11 dígitos verificadores.")
        else:
            try:
                registro_pessoa.Registrar_Dados_Cliente(nome,senha,limpar(cpf),telefone,email,empresa_id)
                st.success("Cliente cadastrado com sucesso!")
            except Exception as erro:
                st.error(f"Erro ao cadastrar cliente: {erro}")
#bloco do cadastro do cliente)

#bloco do cadastro do colaborador(
elif opcao == "Colaborador":
    with st.form("formulario_cadastro_colaborador"):
        col1, col2 = st.columns(2)
        with col1:
            nome_colaborador = st.text_input("Nome")
        with col2:   
            senha_colaborador = st.text_input("Senha",type="password")
        cadastrar_colaborador = st.form_submit_button("Cadastrar")
    if cadastrar_colaborador:
        if (nome_colaborador == ""or senha_colaborador == ""):
            st.error("🦀Preencha o nome e a senha.")
        else:
            try:
                registro_pessoa.Registrar_Dados_Colaborador(nome_colaborador,senha_colaborador)
                st.success("Colaborador cadastrado com sucesso!")
            except Exception as erro:
                st.error(f"Erro ao cadastrar colaborador: {erro}")
#bloco do cadastro do colaborador)

#bloco do cadastro do Plenipotenciário)
elif opcao =="Plenipotenciário":
    with st.form("formulario_cadastro_plenipotenciario)"):
        col1, col2 = st.columns(2)
    with col1:
        nome_plenipotenciario = st.text_input("Nome")
        codigo = st.text_input("Codigo de acesso")
    with col2:   
        senha_plenipotenciario = st.text_input("Senha",type="password")
        cadastrar_plenipotenciario = st.form_submit_button("Cadastrar")
    if cadastrar_plenipotenciario:
        if (nome_plenipotenciario == ""or senha_plenipotenciario == "" or codigo ==""):
            st.error("🦀Preencha o nome e a senha.")
        else:
            try:
                registro_pessoa.Registrar_Dados_Plenipotenciario(nome_plenipotenciario,senha_plenipotenciario,codigo)
                st.success("Colaborador cadastrado com sucesso!")
            except Exception as erro:
                st.error(f"Erro ao cadastrar colaborador: {erro}")
#bloco do cadastro do Plenipotenciário)
