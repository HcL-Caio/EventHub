from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.config.database import get_db_connection

router = APIRouter(prefix="/campeonatos", tags=["Campeonatos"])

class CampeonatoSchema(BaseModel):
    id_evento: int
    modalidade: str
    premiacao: float = 0.00
    vagas_limitadas: int

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar_campeonato(camp: CampeonatoSchema):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_evento FROM eventos WHERE id_evento = ?", (camp.id_evento,))
    if not cursor.fetchone():
        conexao.close()
        raise HTTPException(status_code=400, detail="O ID do evento fornecido não existe.")
    try:
        cursor.execute(
            "INSERT INTO campeonatos (id_evento, modalidade, premiacao, vagas_limitadas) VALUES (?, ?, ?, ?)",
            (camp.id_evento, camp.modalidade, camp.premiacao, camp.vagas_limitadas)
        )
        conexao.commit()
        return {"mensagem": "Campeonato criado com sucesso!", "modalidade": camp.modalidade}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conexao.close()

@router.get("/")
def listar_campeonatos():
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        query = """
            SELECT c.id_campeonato, c.modalidade, c.premiacao, c.vagas_limitadas, e.nome AS nome_evento, c.id_evento
            FROM campeonatos c
            INNER JOIN eventos e ON c.id_evento = e.id_evento
        """
        cursor.execute(query)
        return [
            {"id_campeonato": r[0], "modalidade": r[1], "premiacao": r[2], "vagas_limitadas": r[3], "nome_evento": r[4], "id_evento": r[5]}
            for r in resultados
        ] if (resultados := cursor.fetchall()) else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conexao.close()

@router.put("/{id_campeonato}")
def atualizar_campeonato(id_campeonato: int, camp: CampeonatoSchema):
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE campeonatos SET id_evento = ?, modalidade = ?, premiacao = ?, vagas_limitadas = ? WHERE id_campeonato = ?",
            (camp.id_evento, camp.modalidade, camp.premiacao, camp.vagas_limitadas, id_campeonato)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Campeonato não encontrado.")
        conexao.commit()
        return {"mensagem": "Campeonato atualizado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conexao.close()

@router.delete("/{id_campeonato}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_campeonato(id_campeonato: int):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM campeonatos WHERE id_campeonato = ?", (id_campeonato,))
    if cursor.rowcount == 0:
        conexao.close()
        raise HTTPException(status_code=404, detail="Campeonato não encontrado.")
    conexao.commit()
    conexao.close()