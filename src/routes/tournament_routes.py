from fastapi import APIRouter, HTTPException
from src.config.database import get_db_connection
from src.models.schemas import TorneioCadastro

router = APIRouter(prefix="/api", tags=["2. CRUD Torneios"])

@router.post("/admin/torneios")
async def criar_novo_torneio(torneio: TorneioCadastro):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO torneios (nome, data, status) VALUES (?, ?, ?)", (torneio.nome, torneio.data, torneio.status))
    conn.commit()
    conn.close()
    return {"status": "sucesso", "mensagem": "Novo torneio registrado no SQLite!"}

@router.get("/user/torneios")
async def listar_todos_torneios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, data, status FROM torneios")
    torneios = cursor.fetchall()
    conn.close()
    return [{"id": t[0], "nome": t[1], "data": t[2], "status": t[3]} for t in torneios]

@router.delete("/admin/torneios/{torneio_id}")
async def deletar_torneio(torneio_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM torneios WHERE id = ?", (torneio_id,))
    conn.commit()
    conn.close()
    return {"status": "sucesso", "mensagem": f"Torneio {torneio_id} deletado com sucesso."}