from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.config.database import get_db_connection

router = APIRouter(prefix="/eventos", tags=["Eventos"])

class EventoSchema(BaseModel):
    nome: str
    data: str
    local: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar_evento(evt: EventoSchema):
    db = get_db_connection()
    try:
        dados = {"nome": evt.nome, "data": evt.data, "local": evt.local}
        db.table("eventos").insert(dados).execute()
        return {"mensagem": "Evento cadastrado no Supabase!", "nome": evt.nome}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def listar_eventos():
    db = get_db_connection()
    try:
        resposta = db.table("eventos").select("id_evento, nome, data, local").execute()
        return resposta.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id_evento}")
def atualizar_evento(id_evento: int, evt: EventoSchema):
    db = get_db_connection()
    try:
        dados = {"nome": evt.nome, "data": evt.data, "local": evt.local}
        resposta = db.table("eventos").update(dados).eq("id_evento", id_evento).execute()
        if not resposta.data:
            raise HTTPException(status_code=404, detail="Evento não encontrado.")
        return {"mensagem": "Evento atualizado com sucesso!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_evento}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_evento(id_evento: int):
    db = get_db_connection()
    try:
        resposta = db.table("eventos").delete().eq("id_evento", id_evento).execute()
        if not resposta.data:
            raise HTTPException(status_code=404, detail="Evento não encontrado.")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))