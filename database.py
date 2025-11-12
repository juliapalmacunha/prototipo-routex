import sqlite3
import json


def criar_tabela():
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enderecos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_logradouro TEXT NOT NULL,
            nome_logradouro TEXT NOT NULL,
            numero TEXT NOT NULL,
            complemento TEXT,
            bairro TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL,
            cep TEXT,
            nome_local TEXT
        )
    """)
    conn.commit()
    conn.close()


def adicionar_endereco(tipo_logradouro, nome_logradouro, numero, complemento,
                       bairro, cidade, estado, cep, nome_local):
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO enderecos (tipo_logradouro, nome_logradouro, numero, complemento,
                               bairro, cidade, estado, cep, nome_local)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (tipo_logradouro, nome_logradouro, numero, complemento,
          bairro, cidade, estado, cep, nome_local))
    conn.commit()
    conn.close()



def listar_enderecos():
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enderecos")
    linhas = cursor.fetchall()
    conn.close()

    enderecos = []
    for linha in linhas:
        enderecos.append({
            "id": linha[0],
            "tipo_logradouro": linha[1],
            "nome_logradouro": linha[2],
            "número": linha[3],
            "complemento": linha[4],
            "bairro": linha[5],
            "cidade": linha[6],
            "estado": linha[7],
            "cep": linha[8],
            "nome_local": linha[9],
        })
    return enderecos


def criar_tabela_rotas():
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_rota TEXT NOT NULL,
            enderecos_json TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def salvar_rota(nome_rota, enderecos):
    """
    Salva uma rota no banco de dados.
    :param nome_rota: nome da rota (string)
    :param enderecos: lista de endereços na ordem correta
    """
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    enderecos_json = json.dumps(enderecos, ensure_ascii=False)
    cursor.execute("""
        INSERT INTO rotas (nome_rota, enderecos_json)
        VALUES (?, ?)
    """, (nome_rota, enderecos_json))
    conn.commit()
    conn.close()



def listar_rotas():
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_rota, enderecos_json FROM rotas")
    linhas = cursor.fetchall()
    conn.close()

    rotas = []
    for id_rota, nome_rota, enderecos_json in linhas:
        rotas.append({
            "id": id_rota,
            "nome_rota": nome_rota,
            "enderecos": json.loads(enderecos_json)
        })
    return rotas


def deletar_rota(nome_rota):
    """
    Deleta uma rota do banco de dados pelo nome.
    """
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rotas WHERE nome_rota = ?", (nome_rota,))
    conn.commit()
    conn.close()




criar_tabela()
criar_tabela_rotas()
