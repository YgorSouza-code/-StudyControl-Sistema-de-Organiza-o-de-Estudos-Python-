import sqlite3
from datetime import datetime

# Conexão com banco
conn = sqlite3.connect("studycontrol.db")
cursor = conn.cursor()

# Criar tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    senha TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT,
    data_entrega TEXT,
    status TEXT,
    usuario_id INTEGER
)
""")

conn.commit()

# ==========================
# FUNÇÕES
# ==========================

def cadastrar_usuario():
    nome = input("Digite o nome: ")
    senha = input("Digite a senha: ")

    cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))
    conn.commit()

    print("✅ Usuário cadastrado com sucesso!\n")


def login():
    nome = input("Nome: ")
    senha = input("Senha: ")

    cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (nome, senha))
    usuario = cursor.fetchone()

    if usuario:
        print(f"\n✅ Bem-vindo, {nome}!\n")
        return usuario[0]
    else:
        print("❌ Login inválido\n")
        return None


def adicionar_tarefa(usuario_id):
    descricao = input("Descrição da tarefa: ")
    data = input("Data de entrega (YYYY-MM-DD): ")

    cursor.execute("""
    INSERT INTO tarefas (descricao, data_entrega, status, usuario_id)
    VALUES (?, ?, 'pendente', ?)
    """, (descricao, data, usuario_id))

    conn.commit()
    print("📌 Tarefa adicionada!\n")


def listar_tarefas(usuario_id):
    cursor.execute("SELECT * FROM tarefas WHERE usuario_id=?", (usuario_id,))
    tarefas = cursor.fetchall()

    print("\n📋 Suas tarefas:")
    for t in tarefas:
        print(f"ID: {t[0]} | {t[1]} | {t[2]} | Status: {t[3]}")
    print()


def concluir_tarefa(usuario_id):
    listar_tarefas(usuario_id)
    tarefa_id = input("Digite o ID da tarefa para concluir: ")

    cursor.execute("""
    UPDATE tarefas SET status='concluída'
    WHERE id=? AND usuario_id=?
    """, (tarefa_id, usuario_id))

    conn.commit()
    print("✅ Tarefa concluída!\n")


def progresso(usuario_id):
    cursor.execute("SELECT COUNT(*) FROM tarefas WHERE usuario_id=?", (usuario_id,))
    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*) FROM tarefas 
    WHERE usuario_id=? AND status='concluída'
    """, (usuario_id,))
    concluidas = cursor.fetchone()[0]

    if total == 0:
        print("Nenhuma tarefa cadastrada.\n")
    else:
        porcentagem = (concluidas / total) * 100
        print(f"📊 Progresso: {porcentagem:.2f}% ({concluidas}/{total})\n")


# ==========================
# MENU PRINCIPAL
# ==========================

def menu():
    while True:
        print("=== STUDYCONTROL ===")
        print("1 - Cadastrar")
        print("2 - Login")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_usuario()

        elif opcao == "2":
            user_id = login()

            if user_id:
                menu_usuario(user_id)

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida\n")


def menu_usuario(usuario_id):
    while True:
        print("=== MENU ===")
        print("1 - Adicionar tarefa")
        print("2 - Listar tarefas")
        print("3 - Concluir tarefa")
        print("4 - Ver progresso")
        print("0 - Logout")

        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_tarefa(usuario_id)

        elif opcao == "2":
            listar_tarefas(usuario_id)

        elif opcao == "3":
            concluir_tarefa(usuario_id)

        elif opcao == "4":
            progresso(usuario_id)

        elif opcao == "0":
            break

        else:
            print("Opção inválida\n")


# ==========================
# INICIAR SISTEMA
# ==========================

menu()
conn.close()