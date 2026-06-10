from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import date
from typing import Optional
from src.config.database import get_db_connection

router = APIRouter(prefix="/eventos", tags=["Eventos"])

class EventoSchema(BaseModel):
    nome: str
    data_inicio: date
    local_evento: str
    descricao: Optional[str] = None

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar_evento(evento: EventoSchema):
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        comando_sql = "INSERT INTO eventos (nome, data_inicio, local_evento, descricao) VALUES (?, ?, ?, ?)"
        valores = (evento.nome, str(evento.data_inicio), evento.local_evento, evento.descricao)
        cursor.execute(comando_sql, valores)
        conexao.commit()
        return {"mensagem": "Evento cadastrado com sucesso!", "nome": evento.nome}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao salvar: {str(e)}")
    finally:
        conexao.close()

@router.get("/")
def listar_eventos():
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        cursor.execute("SELECT id_evento, nome, data_inicio, local_evento, descricao, criado_em FROM eventos")
        resultados = cursor.fetchall()
        return [
            {"id_evento": r[0], "nome": r[1], "data_inicio": r[2], "local_evento": r[3], "descricao": r[4], "criado_em": r[5]}
            for r in resultados
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar: {str(e)}")
    finally:
        conexao.close()

@router.put("/{id_evento}")
def atualizar_evento(id_evento: int, evento: EventoSchema):
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE eventos SET nome = ?, data_inicio = ?, local_evento = ?, descricao = ? WHERE id_evento = ?",
            (evento.nome, str(evento.data_inicio), evento.local_evento, evento.descricao, id_evento)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Evento não encontrado.")
        conexao.commit()
        return {"mensagem": "Evento atualizado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conexao.close()

@router.delete("/{id_evento}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_evento(id_evento: int):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM eventos WHERE id_evento = ?", (id_evento,))
    if cursor.rowcount == 0:
        conexao.close()
        raise HTTPException(status_code=404, detail="Evento não encontrado.")
    conexao.commit()
    conexao.close()