import sqlite3
import hashlib


# ==================================
# CONEXÃO
# ==================================

def conectar():
    return sqlite3.connect("tarefas.db")


# ==================================
# CRIAR TABELAS
# ==================================

def criar_tabelas():

    conexao = conectar()
    cursor = conexao.cursor()

    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    # Tabela de tarefas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            categoria TEXT,
            data_vencimento TEXT,
            concluida INTEGER DEFAULT 0
        )
    """)

    conexao.commit()
    conexao.close()


# ==================================
# CADASTRO
# ==================================

def cadastrar_usuario():

    usuario = input("Novo usuário: ")
    senha = input("Nova senha: ")

    senha_hash = hashlib.sha256(
        senha.encode()
    ).hexdigest()

    try:

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO usuarios
            (usuario, senha)
            VALUES (?, ?)
        """, (
            usuario,
            senha_hash
        ))

        conexao.commit()
        conexao.close()

        print("\n✅ Usuário cadastrado com sucesso!")

    except sqlite3.IntegrityError:
        print("\n❌ Usuário já existe.")


# ==================================
# LOGIN
# ==================================

def login():

    usuario = input("Usuário: ")
    senha = input("Senha: ")

    senha_hash = hashlib.sha256(
        senha.encode()
    ).hexdigest()

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE usuario = ?
        AND senha = ?
    """, (
        usuario,
        senha_hash
    ))

    resultado = cursor.fetchone()

    conexao.close()

    if resultado:
        print(f"\n✅ Bem-vindo, {usuario}!")
        return True

    print("\n❌ Usuário ou senha incorretos.")
    return False


# ==================================
# ADICIONAR TAREFA
# ==================================

def adicionar_tarefa():

    descricao = input("Descrição: ")
    prioridade = input(
        "Prioridade (Alta, Média, Baixa): "
    )
    categoria = input("Categoria: ")
    data = input(
        "Data de vencimento (dd/mm/aaaa): "
    )

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO tarefas
        (
            descricao,
            prioridade,
            categoria,
            data_vencimento
        )
        VALUES (?, ?, ?, ?)
    """, (
        descricao,
        prioridade,
        categoria,
        data
    ))

    conexao.commit()
    conexao.close()

    print("\n✅ Tarefa cadastrada!")


# ==================================
# LISTAR TAREFAS
# ==================================

def listar_tarefas():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM tarefas
        ORDER BY id
    """)

    tarefas = cursor.fetchall()

    conexao.close()

    if not tarefas:
        print("\nNenhuma tarefa cadastrada.")
        return

    print("\n========== TAREFAS ==========")

    for tarefa in tarefas:

        status = (
            "✅ Concluída"
            if tarefa[5]
            else "❌ Pendente"
        )

        print(f"""
ID: {tarefa[0]}
Descrição: {tarefa[1]}
Prioridade: {tarefa[2]}
Categoria: {tarefa[3]}
Vencimento: {tarefa[4]}
Status: {status}
------------------------------
""")


# ==================================
# CONCLUIR TAREFA
# ==================================

def concluir_tarefa():

    listar_tarefas()

    try:

        id_tarefa = int(
            input("ID da tarefa concluída: ")
        )

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE tarefas
            SET concluida = 1
            WHERE id = ?
        """, (id_tarefa,))

        conexao.commit()
        conexao.close()

        print("✅ Tarefa concluída!")

    except ValueError:
        print("❌ Número inválido.")


# ==================================
# REMOVER TAREFA
# ==================================

def remover_tarefa():

    listar_tarefas()

    try:

        id_tarefa = int(
            input("ID da tarefa para remover: ")
        )

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM tarefas
            WHERE id = ?
        """, (id_tarefa,))

        conexao.commit()
        conexao.close()

        print("🗑️ Tarefa removida!")

    except ValueError:
        print("❌ Número inválido.")


# ==================================
# BUSCAR POR PRIORIDADE
# ==================================

def buscar_por_prioridade():

    prioridade = input(
        "Digite Alta, Média ou Baixa: "
    )

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM tarefas
        WHERE prioridade = ?
    """, (prioridade,))

    tarefas = cursor.fetchall()

    conexao.close()

    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return

    for tarefa in tarefas:

        status = (
            "✅"
            if tarefa[5]
            else "❌"
        )

        print(
            f"{tarefa[0]} - "
            f"{tarefa[1]} - "
            f"{status}"
        )


# ==================================
# ESTATÍSTICAS
# ==================================

def estatisticas():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM tarefas"
    )

    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM tarefas
        WHERE concluida = 1
    """)

    concluidas = cursor.fetchone()[0]

    pendentes = total - concluidas

    conexao.close()

    print("\n===== ESTATÍSTICAS =====")
    print(f"Total: {total}")
    print(f"Concluídas: {concluidas}")
    print(f"Pendentes: {pendentes}")


# ==================================
# MENU TAREFAS
# ==================================

def menu_tarefas():

    while True:

        print("""

======== GERENCIADOR ========

1 - Adicionar tarefa
2 - Listar tarefas
3 - Concluir tarefa
4 - Remover tarefa
5 - Buscar por prioridade
6 - Estatísticas
7 - Logout

============================
""")

        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_tarefa()

        elif opcao == "2":
            listar_tarefas()

        elif opcao == "3":
            concluir_tarefa()

        elif opcao == "4":
            remover_tarefa()

        elif opcao == "5":
            buscar_por_prioridade()

        elif opcao == "6":
            estatisticas()

        elif opcao == "7":
            break

        else:
            print("❌ Opção inválida.")


# ==================================
# MENU LOGIN
# ==================================

def menu_login():

    while True:

        print("""

======== SISTEMA ========

1 - Login
2 - Cadastrar usuário
3 - Sair

========================
""")

        opcao = input("Escolha: ")

        if opcao == "1":

            if login():
                menu_tarefas()

        elif opcao == "2":
            cadastrar_usuario()

        elif opcao == "3":

            print("Até logo!")
            break

        else:
            print("❌ Opção inválida.")


# ==================================
# INÍCIO
# ==================================

if __name__ == "__main__":

    criar_tabelas()
    menu_login()