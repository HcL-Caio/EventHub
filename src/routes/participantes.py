from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.config.database import get_db_connection

router = APIRouter(prefix="/participantes", tags=["Participantes"])

class ParticipanteSchema(BaseModel):
    nome: str
    email: str
    telefone: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar_participante(part: ParticipanteSchema):
    db = get_db_connection()
    try:
        dados = {"nome": part.nome, "email": part.email, "telefone": part.telefone}
        db.table("participantes").insert(dados).execute()
        return {"mensagem": "Participante cadastrado no Supabase!", "nome": part.nome}
    except Exception as e:
        if "unique" in str(e).lower() or "duplicate" in str(e).lower():
            raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def listar_participantes():
    db = get_db_connection()
    try:
        resposta = db.table("participantes").select("id_participante, nome, email, telephone:telefone").execute()
        return resposta.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id_participante}")
def atualizar_participante(id_participante: int, part: ParticipanteSchema):
    db = get_db_connection()
    try:
        dados = {"nome": part.nome, "email": part.email, "telefone": part.telefone}
        resposta = db.table("participantes").update(dados).eq("id_participante", id_participante).execute()
        if not resposta.data:
            raise HTTPException(status_code=404, detail="Participante não encontrado.")
        return {"mensagem": "Participante updated com sucesso!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_participante}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_participante(id_participante: int):
    db = get_db_connection()
    try:
        resposta = db.table("participantes").delete().eq("id_participante", id_participante).execute()
        if not resposta.data:
            raise HTTPException(status_code=404, detail="Participante não encontrado.")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))