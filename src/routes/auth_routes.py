from fastapi import APIRouter, HTTPException
import sqlite3
from src.config.database import get_db_connection
from src.models.schemas import UsuarioCadastro, UsuarioLogin

router = APIRouter(prefix="/api", tags=["1. CRUD Usuários"])

@router.post("/cadastro")
async def cadastrar_usuario(usuario: UsuarioCadastro):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, 'user')", (usuario.nome, usuario.email, usuario.senha))
        conn.commit()
        return {"status": "sucesso", "mensagem": "Usuário cadastrado com sucesso!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")
    finally:
        conn.close()

@router.post("/login")
async def realizar_login(usuario: UsuarioLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, tipo FROM usuarios WHERE email = ? AND senha = ?", (usuario.email, usuario.senha))
    user = cursor.fetchone()
    conn.close()
    
    if user: 
        return {"status": "sucesso", "nome": user[0], "tipo": user[1]}
    raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

@router.get("/admin/usuarios")
async def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, tipo FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return [{"id": u[0], "nome": u[1], "email": u[2], "tipo": u[3]} for u in users]

@router.delete("/admin/usuarios/{user_id}")
async def deletar_usuario(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ? AND tipo != 'admin'", (user_id,))
    conn.commit()
    conn.close()
    return {"status": "sucesso", "mensagem": "Usuário removido do banco relacional."}