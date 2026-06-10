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
    conexao = get_db_connection()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id_participante FROM participantes WHERE id_participante = ?", (insc.id_participante,))
    if not cursor.fetchone():
        conexao.close()
        raise HTTPException(status_code=400, detail="O ID do participante informado não existe.")
        
    cursor.execute("SELECT id_campeonato FROM campeonatos WHERE id_campeonato = ?", (insc.id_campeonato,))
    if not cursor.fetchone():
        conexao.close()
        raise HTTPException(status_code=400, detail="O ID do campeonato informado não existe.")

    try:
        cursor.execute(
            "INSERT INTO inscricoes (id_participante, id_campeonato, status_inscricao) VALUES (?, ?, ?)",
            (insc.id_participante, insc.id_campeonato, insc.status_inscricao)
        )
        conexao.commit()
        return {"mensagem": "Inscrição realizada com sucesso!"}
    except Exception as e:
        if "UNIQUE" in str(e):
            raise HTTPException(status_code=400, detail="Este participante já está inscrito neste campeonato.")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conexao.close()

@router.get("/")
def listar_inscricoes():
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        query = """
            SELECT i.id_inscricao, p.nome, c.modalidade, i.status_inscricao 
            FROM inscricoes i
            INNER JOIN participantes p ON i.id_participante = p.id_participante
            INNER JOIN campeonatos c ON i.id_campeonato = c.id_campeonato
        """
        cursor.execute(query)
        return [{"id_inscricao": r[0], "participante": r[1], "campeonato": r[2], "status": r[3]} for r in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conexao.close()

@router.put("/{id_inscricao}")
def atualizar_status_inscricao(id_inscricao: int, insc: InscricaoSchema):
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE inscricoes SET status_inscricao = ? WHERE id_inscricao = ?",
            (insc.status_inscricao, id_inscricao)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Inscrição não encontrada.")
        conexao.commit()
        return {"mensagem": "Status da inscrição atualizado!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conexao.close()

@router.delete("/{id_inscricao}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_inscricao(id_inscricao: int):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM inscricoes WHERE id_inscricao = ?", (id_inscricao,))
    if cursor.rowcount == 0:
        conexao.close()
        raise HTTPException(status_code=404, detail="Inscrição não encontrada.")
    conexao.commit()
    conexao.close()