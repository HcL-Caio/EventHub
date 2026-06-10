from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.config.database import get_db_connection

router = APIRouter(prefix="/participantes", tags=["Participantes"])

class ParticipanteSchema(BaseModel):
    nome: str
    email: str
    telefone: str

# 1. CADASTRAR (POST)
@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar_participante(part: ParticipanteSchema):
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO participantes (nome, email, telefone) VALUES (?, ?, ?)", 
            (part.nome, part.email, part.telefone)
        )
        conexao.commit()
        return {"mensagem": "Participante cadastrado com sucesso!", "nome": part.nome}
    except Exception as e:
        if "UNIQUE" in str(e):
            raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")
        raise HTTPException(status_code=400, detail=f"Erro ao salvar: {str(e)}")
    finally:
        conexao.close()

# 2. LISTAR (GET)
@router.get("/")
def listar_participantes():
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        cursor.execute("SELECT id_participante, nome, email, telefone, data_cadastro FROM participantes")
        resultados = cursor.fetchall()
        return [
            {"id_participante": r[0], "nome": r[1], "email": r[2], "telefone": r[3], "data_cadastro": r[4]}
            for r in resultados
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conexao.close()

# 3. ATUALIZAR (PUT)
@router.put("/{id_participante}")
def atualizar_participante(id_participante: int, part: ParticipanteSchema):
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE participantes SET nome = ?, email = ?, telefone = ? WHERE id_participante = ?",
            (part.nome, part.email, part.telefone, id_participante)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Participante não encontrado.")
        conexao.commit()
        return {"mensagem": "Participante atualizado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conexao.close()

# 4. EXCLUIR (DELETE)
@router.delete("/{id_participante}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_participante(id_participante: int):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM participantes WHERE id_participante = ?", (id_participante,))
    if cursor.rowcount == 0:
        conexao.close()
        raise HTTPException(status_code=404, detail="Participante não encontrado.")
    conexao.commit()
    conexao.close()