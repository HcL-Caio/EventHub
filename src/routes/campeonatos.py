from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.config.database import get_db_connection

router = APIRouter(prefix="/campeonatos", tags=["Campeonatos"])

class CampeonatoSchema(BaseModel):
    id_evento: int
    modalidade: str
    premiacao: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar_campeonato(camp: CampeonatoSchema):
    db = get_db_connection()
    try:
        dados = {"id_evento": camp.id_evento, "modalidade": camp.modalidade, "premiacao": camp.premiacao}
        db.table("campeonatos").insert(dados).execute()
        return {"mensagem": "Campeonato cadastrado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def listar_campeonatos():
    db = get_db_connection()
    try:
        resposta = db.table("campeonatos").select("id_campeonato, id_evento, modalidade, premiacao").execute()
        return resposta.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id_campeonato}")
def atualizar_campeonato(id_campeonato: int, camp: CampeonatoSchema):
    db = get_db_connection()
    try:
        dados = {"id_evento": camp.id_evento, "modalidade": camp.modalidade, "premiacao": camp.premiacao}
        resposta = db.table("campeonatos").update(dados).eq("id_campeonato", id_campeonato).execute()
        if not resposta.data:
            raise HTTPException(status_code=404, detail="Campeonato não encontrado.")
        return {"mensagem": "Campeonato atualizado com sucesso!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_campeonato}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_campeonato(id_campeonato: int):
    db = get_db_connection()
    try:
        resposta = db.table("campeonatos").delete().eq("id_campeonato", id_campeonato).execute()
        if not resposta.data:
            raise HTTPException(status_code=404, detail="Campeonato não encontrado.")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))