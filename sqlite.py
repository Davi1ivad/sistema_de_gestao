import sqlite3


acessar_db = sqlite3.connect("database.db")
acessar_db.execute("PRAGMA foreign_keys = ON")

cursor = acessar_db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS plenipotenciario(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL,
        codigo TEXT NOT NULL,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS empresas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        razao_social TEXT NOT NULL,
        nome_fantasia TEXT NOT NULL,
        cnpj TEXT UNIQUE NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL,
        endereco TEXT NOT NULL,
        status TEXT DEFAULT 'ATIVO',
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS clientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL,
        empresa_id INTEGER,
        status TEXT DEFAULT 'ATIVO',
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (empresa_id)REFERENCES empresas(id));""")

cursor.execute("""CREATE TABLE IF NOT EXISTS documentos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        empresa_id INTEGER,
        tipo_documento TEXT NOT NULL,
        numero_documento TEXT NOT NULL,
        data_emissao DATE,
        data_validade DATE,
        caminho_arquivo TEXT,
        status TEXT DEFAULT 'PENDENTE',
        observacao TEXT,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (cliente_id)REFERENCES clientes(id),

        FOREIGN KEY (empresa_id)REFERENCES empresas(id));""")

cursor.execute("""CREATE TABLE IF NOT EXISTS auditoria(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        acao TEXT NOT NULL,
        tabela TEXT,
        registro_id INTEGER,
        descricao TEXT,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (usuario_id)REFERENCES usuarios(id));""")

cursor.execute("""CREATE  TABLE IF NOT EXISTS colaborador(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS vinculo_cliente_empresa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cpf_cliente TEXT NOT NULL,
        cnpj_empresa TEXT NOT NULL,
        data_vinculo DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cpf_cliente) REFERENCES clientes(cpf),
        FOREIGN KEY (cnpj_empresa) REFERENCES empresas(cnpj),
        UNIQUE (cpf_cliente, cnpj_empresa));""")

#cursor.execute("ALTER TABLE clientes ADD COLUMN senha TEXT NOT NULL")

#cursor.execute("DELETE FROM plenipotenciario WHERE nome IS NULL OR nome = ''")

#cursor.execute("DROP TABLE IF EXISTS vinculo_cliente_empresa")




acessar_db.commit()
acessar_db.close()

print("Banco de dados configurado com sucesso!")