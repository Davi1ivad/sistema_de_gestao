import sqlite3
from validacoes import limpar, validar_cnpj

def conectardb():
    acessar_db = sqlite3.connect("database.db")
    return acessar_db

#cadastro
def InserirDados(razao_social,nome_fantasia,cnpj,telefone,email,endereco,status):
    cnpj = limpar(cnpj)
    if not validar_cnpj(cnpj):
        raise ValueError("CNPJ inválido. Informe um CNPJ brasileiro válido.")
    acessar_db = conectardb()
    cursor = acessar_db.cursor()
    cursor.execute("INSERT INTO empresas(razao_social,nome_fantasia,cnpj,telefone,email,endereco,status) VALUES (?,?,?,?,?,?,?)",(razao_social,nome_fantasia,cnpj,telefone,email,endereco,status))
    acessar_db.commit()
    acessar_db.close()

#editar
def buscar_empresa(email="", cnpj=""):
    conexao = conectardb()
    cursor = conexao.cursor()
    if email != "" and cnpj != "":
        cursor.execute("SELECT * FROM empresas WHERE email = ? AND cnpj = ?",(email, cnpj))
    elif email != "":
        cursor.execute("SELECT * FROM empresas WHERE email = ?",(email,))
    elif cnpj != "":
        cursor.execute("SELECT * FROM empresas WHERE cnpj = ?",(cnpj,))
    empresa = cursor.fetchone()
    conexao.close()
    return empresa

def atualizar_empresa(id_empresa, razao_social, nome_fantasia, cnpj, telefone, email, endereco, status):
    cnpj = limpar(cnpj)
    if not validar_cnpj(cnpj):
        raise ValueError("CNPJ inválido. Informe um CNPJ brasileiro válido.")
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE empresas
        SET razao_social = ?,
            nome_fantasia = ?,
            cnpj = ?,
            telefone = ?,
            email = ?,
            endereco = ?,
            status = ?
        WHERE id = ?
    """, (razao_social, nome_fantasia, cnpj, telefone, email, endereco, status, id_empresa))
    conexao.commit()
    conexao.close()

def contar_empresas_sem_vinculo():
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM empresas e
        WHERE NOT EXISTS (
            SELECT 1
            FROM vinculo_cliente_empresa v
            WHERE v.cnpj_empresa = e.cnpj)""")
    total = cursor.fetchone()[0]
    conexao.close()
    return total
