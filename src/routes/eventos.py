from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from src.config.database import obter_conexao

router = APIRouter(prefix="/eventos", tags=["Eventos"])

class EventoSchema(BaseModel):
    nome: str
    data_inicio: date
    local_evento: str
    descricao: str | None = None

@router.post("/", status_code=201)
def cadastrar_evento(evento: EventoSchema):
    conexao = obter_conexao()
    if not conexao:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    try:
        cursor = conexao.cursor()
        comando_sql = """
            INSERT INTO eventos (nome, data_inicio, local_evento, descricao)
            VALUES (%s, %s, %s, %s)
        """
        valores = (evento.nome, evento.data_inicio, evento.local_evento, evento.descricao)
        
        cursor.execute(comando_sql, valores)
        conexao.commit()
        return {"mensagem": "Evento cadastrado com sucesso!", "nome": evento.nome}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao salvar no banco: {str(e)}")
    finally:
        cursor.close()
        conexao.close()

@router.get("/")
def listar_eventos():
    conexao = obter_conexao()
    if not conexao:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM eventos")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar no banco: {str(e)}")
    finally:
        cursor.close()
        conexao.close()