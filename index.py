import streamlit as st
import registradores.registro_pessoa as registro_pessoa


st.set_page_config(page_title="Sistema de Gestão",page_icon="📚",layout="wide")

if "logado" not in st.session_state:
    st.session_state.logado = False
if "colaborador" not in st.session_state:
    st.session_state.colaborador = None
if "cliente" not in st.session_state:
    st.session_state.cliente = None
if "plenipotenciario" not in st.session_state:
    st.session_state.plenipotenciario = None
    

if st.button("Registrar"):
    st.switch_page("registradores/registro_simples.py")
#login

st.divider()
if not st.session_state.logado:
    st.title("📚 Sistema de Gestão")
    st.divider()
    st.subheader("Login")
    nome = st.text_input("Nome")
    senha = st.text_input("Senha",type="password")
    if st.button("Entrar"):
        if nome.strip() == "" or senha.strip() == "":
            st.error("🦀Preencha o nome e a senha.")
        else:
            # PRIMEIRO: VERIFICA SE É CLIENTE
            dados_cliente = registro_pessoa.Autenticar_Cliente(nome,senha)
            if dados_cliente:
                st.session_state.logado = True
                st.session_state.cliente = {"id": dados_cliente[0],"nome": dados_cliente[1]}
                st.switch_page("cliente_navigation/cliente_empresa.py")
            else:
                # SE NÃO FOR CLIENTE, VERIFICA SE É COLABORADOR ou chefe
                dados_colaborador = registro_pessoa.Autenticar_Colaborador(nome,senha)
                dados_plenipotenciario = registro_pessoa.Autenticar_Plenipotenciario(nome,senha)
                if dados_colaborador:
                    st.session_state.logado = True
                    st.session_state.colaborador = {"id": dados_colaborador[0],"nome": dados_colaborador[1]}
                    st.switch_page("login.py")
                elif dados_plenipotenciario:
                        st.session_state.logado = True
                        st.session_state.colaborador = {"id": dados_plenipotenciario[0],"nome": dados_plenipotenciario[1]}
                        st.switch_page("login.py")
                else:
                    st.error("🦀 Nome ou senha incorretos.")