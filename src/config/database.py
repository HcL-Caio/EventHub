import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "eventhub.db")

def get_db_connection():
    """Retorna uma nova conexão com o banco SQLite."""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Cria as tabelas e injeta dados iniciais (Seed) se o banco estiver vazio."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1️⃣ Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'user'
        )
    ''')
    
    # 2️⃣ Tabela de Torneios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS torneios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Inscrições Abertas'
        )
    ''')
    
    # Seed: Injetar Admin padrão se não existir
    cursor.execute("SELECT * FROM usuarios WHERE email = 'admin@eventhub.com'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            ("Administrador Principal", "admin@eventhub.com", "admin123", "admin")
        )
        
    # Seed: Injetar Torneios iniciais se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM torneios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO torneios (nome, data, status) VALUES (?, ?, ?)", ("Copa Masters Valorant", "20/Jun às 19:00", "Inscrições Abertas"))
        cursor.execute("INSERT INTO torneios (nome, data, status) VALUES (?, ?, ?)", ("LoL Community Cup", "25/Jun às 14:00", "Em Breve"))
        cursor.execute("INSERT INTO torneios (nome, data, status) VALUES (?, ?, ?)", ("Torneio Counter-Strike 2", "02/Jul às 20:00", "Inscrições Abertas"))
        
    conn.commit()
    conn.close()