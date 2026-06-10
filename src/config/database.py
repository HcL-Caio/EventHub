import sqlite3
import os

# Mantém a gerência inteligente de pastas locais que você já usava
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "eventhub.db")

def get_db_connection():
    """Retorna uma nova conexão com o banco SQLite."""
    conn = sqlite3.connect(DB_PATH)
    # ⚠️ CRUCIAL: Ativa o suporte do SQLite para monitorar as Chaves Estrangeiras (FOREIGN KEY)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Cria as 4 tabelas oficiais do professor e injeta dados iniciais (Seed)."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            local_evento TEXT NOT NULL,
            descricao TEXT,
            criado_em TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participantes (
            id_participante INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT,
            data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campeonatos (
            id_campeonato INTEGER PRIMARY KEY AUTOINCREMENT,
            id_evento INTEGER NOT NULL,
            modalidade TEXT NOT NULL,
            premiacao REAL DEFAULT 0.00,
            vagas_limitadas INTEGER NOT NULL,
            FOREIGN KEY (id_evento) REFERENCES eventos(id_evento) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscricoes (
            id_inscricao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_participante INTEGER NOT NULL,
            id_campeonato INTEGER NOT NULL,
            data_inscricao TEXT DEFAULT CURRENT_TIMESTAMP,
            status_inscricao TEXT NOT NULL DEFAULT 'Pendente',
            FOREIGN KEY (id_participante) REFERENCES participantes(id_participante) ON DELETE CASCADE,
            FOREIGN KEY (id_campeonato) REFERENCES campeonatos(id_campeonato) ON DELETE CASCADE,
            UNIQUE (id_participante, id_campeonato)
        )
    ''')
    
    # =================================================================
    # 🚀 DATA SEEDING (Alimenta o banco automaticamente para a apresentação)
    # =================================================================
    
    # Seed: Injetar Eventos base se estiver vazio
    cursor.execute("SELECT COUNT(*) FROM eventos")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO eventos (nome, data_inicio, local_evento, descricao) VALUES (?, ?, ?, ?)",
            ("Seminário de Sistemas 2026", "16/06/2026", "Auditório Principal - Bloco A", "Apresentações oficiais de projetos acadêmicos.")
        )
        cursor.execute(
            "INSERT INTO eventos (nome, data_inicio, local_evento, descricao) VALUES (?, ?, ?, ?)",
            ("EventHub Geek Festival", "20/07/2026", "Centro de Convenções Central", "Grande celebração de eSports da comunidade.")
        )
        
    # Seed: Injetar Participantes base se estiver vazio
    cursor.execute("SELECT COUNT(*) FROM participantes")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO participantes (nome, email, telefone) VALUES (?, ?, ?)",
            ("Caio Amaral", "caio.amaral@eventhub.com", "(11) 99999-9999")
        )
        cursor.execute(
            "INSERT INTO participantes (nome, email, telefone) VALUES (?, ?, ?)",
            ("Professor Avaliador", "professor@instituicao.edu.br", "(11) 98888-8888")
        )

    # Seed: Injetar Campeonatos associados ao Evento 1 e 2
    cursor.execute("SELECT COUNT(*) FROM campeonatos")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO campeonatos (id_evento, modalidade, premiacao, vagas_limitadas) VALUES (?, ?, ?, ?)",
            (1, "FastAPI Speedrun Dev", 1000.00, 10)
        )
        cursor.execute(
            "INSERT INTO campeonatos (id_evento, modalidade, premiacao, vagas_limitadas) VALUES (?, ?, ?, ?)",
            (2, "Valorant Masters", 2500.00, 16)
        )

    # Seed: Injetar Inscrições associadas
    cursor.execute("SELECT COUNT(*) FROM inscricoes")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO inscricoes (id_participante, id_campeonato, status_inscricao) VALUES (?, ?, ?)",
            (1, 1, "Confirmada")
        )

    conn.commit()
    conn.close()