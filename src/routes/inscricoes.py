from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.config.database import get_db_connection

router = APIRouter(prefix="/inscricoes", tags=["Inscrições"])

class InscricaoSchema(BaseModel):
    id_participante: int
    id_campeonato: int
    status_inscricao: str = "Pendente"

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_inscricao(insc: InscricaoSchema):
    db = get_db_connection()
    
    # Validações relacionais idênticas ao seu original
    part_check = db.table("participantes").select("id_participante").eq("id_participante", insc.id_participante).execute()
    if not part_check.data:
        raise HTTPException(status_code=400, detail="O ID do participante informado não existe.")
        
    camp_check = db.table("campeonatos").select("id_campeonato").eq("id_campeonato", insc.id_campeonato).execute()
    if not camp_check.data:
        raise HTTPException(status_code=400, detail="O ID do campeonato informado não existe.")

    try:
        dados = {
            "id_participante": insc.id_participante, 
            "id_campeonato": insc.id_campeonato, 
            "status_inscricao": insc.status_inscricao
        }
        db.table("inscricoes").insert(dados).execute()
        return {"mensagem": "Inscrição realizada com sucesso no Supabase!"}
    except Exception as e:
        if "unique" in str(e).lower() or "duplicate" in str(e).lower():
            raise HTTPException(status_code=400, detail="Este participante já está inscrito neste campeonato.")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def listar_inscricoes():
    db = get_db_connection()
    try:
        # Trazendo os dados com o INNER JOIN automático que o cliente HTTP do Supabase faz pelas chaves estrangeiras
        resposta = db.table("inscricoes").select("id_inscricao, status_inscricao, participantes(nome), campeonatos(modalidade)").execute()
        
        # Formata o retorno para ficar idêntico ao seu dicionário original
        return [
            {
                "id_inscricao": r["id_inscricao"],
                "participante": r["participantes"]["nome"] if r.get("participantes") else "N/A",
                "campeonato": r["campeonatos"]["modalidade"] if r.get("campeonatos") else "N/A",
                "status": r["status_inscricao"]
            }
            for r in resposta.data
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id_inscricao}")
def atualizar_status_inscricao(id_inscricao: int, insc: InscricaoSchema):
    db = get_db_connection()
    try:
        resposta = db.table("inscricoes").update({"status_inscricao": insc.status_inscricao}).eq("id_inscricao", id_inscricao).execute()
        if not resposta.data:
            raise HTTPException(status_code=404, detail="Inscrição não encontrada.")
        return {"mensagem": "Status da inscrição updated!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_inscricao}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_inscricao(id_inscricao: int):
    db = get_db_connection()
    try:
        resposta = db.table("inscricoes").delete().eq("id_inscricao", id_inscricao).execute()
        if not resposta.data:
            raise HTTPException(status_code=404, detail="Inscrição não encontrada.")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))