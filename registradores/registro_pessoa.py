import sqlite3
from validacoes import limpar, validar_cpf

#sempre criar def com nomes diferente para cada bloco de inserção diferente

#ativar o db(
def conectardb():
    acessar_db = sqlite3.connect("database.db")
    return acessar_db
#ativar o db)

#registrar pessoas que trabalham com o sistema(plenipotenciario)
def Registrar_Dados_Plenipotenciario(nome,senha,codigo):
    acessar_db = conectardb()
    cursor = acessar_db.cursor()
    cursor.execute("INSERT INTO plenipotenciario(nome,senha,codigo) VALUES (?,?,?)",(nome,senha,codigo))
    acessar_db.commit()
    acessar_db.close()

def Buscador_Plenipotenciario(nome,senha):
    acessar_db = conectardb()
    cursor = acessar_db.cursor()
    cursor.execute("SELECT nome,senha FROM plenipotenciario WHERE nome = ? AND senha = ?",(nome,senha))
    dados = cursor.fetchone()
    cursor.close()
    acessar_db.close()
    return dados

def Autenticar_Plenipotenciario(nome, senha):
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM plenipotenciario WHERE nome = ? AND senha = ?", (nome, senha))
    plenipotenciario = cursor.fetchone()
    conexao.close()
    return plenipotenciario
#registrar pessoas que trabalham com o plenipotenciario)

#registrar pessoas que trabalham com o sistema colaborador)
def Registrar_Dados_Colaborador(nome,senha):
    acessar_db = conectardb()
    cursor = acessar_db.cursor()
    cursor.execute("INSERT INTO colaborador(nome,senha) VALUES (?,?)",(nome, senha))
    acessar_db.commit()
    acessar_db.close()

def Buscador_Colaborador(nome,senha):
    acessar_db = conectardb()
    cursor = acessar_db.cursor()
    cursor.execute("SELECT nome,senha FROM colaborador WHERE nome = ? AND senha = ?",(nome,senha))
    dados = cursor.fetchone()
    cursor.close()
    acessar_db.close()
    return dados

def Autenticar_Colaborador(nome, senha):
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM colaborador WHERE nome = ? AND senha = ?", (nome, senha))
    colaborador = cursor.fetchone()
    conexao.close()
    return colaborador
#registrar pessoas que trabalham com o sistemacolaborador)

#registrar pessoas que usam com o sistema(
def Registrar_Dados_Cliente(nome,senha, cpf, telefone, email, empresa_id):
    cpf = limpar(cpf)
    if not validar_cpf(cpf):
        raise ValueError("CPF inválido. Informe um CPF brasileiro válido.")
    acessar_db = conectardb()
    cursor = acessar_db.cursor()
    cursor.execute("INSERT INTO clientes(nome,senha, cpf, telefone, email, empresa_id) VALUES (?, ?, ?, ?, ?, ?)",(nome, senha,cpf, telefone, email, empresa_id ))
    acessar_db.commit()
    acessar_db.close()

def Buscador_Cliente(nome,senha):
    acessar_db = conectardb()
    cursor = acessar_db.cursor()
    cursor.execute("SELECT nome,senha FROM clientes WHERE nome = ? AND senha = ?",(nome,senha))
    dados = cursor.fetchone()
    cursor.close()
    acessar_db.close()
    return dados

def Autenticar_Cliente(nome, senha):
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM clientes WHERE nome = ? AND senha = ?", (nome, senha))
    cliente = cursor.fetchone()
    conexao.close()
    return cliente
#registrar pessoas que usam com o sistema)
