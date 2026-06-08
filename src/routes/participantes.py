from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.config.database import obter_conexao

router = APIRouter(prefix="/participantes", tags=["Participantes"])

class ParticipanteSchema(BaseModel):
    nome: str
    email: str
    telefone: str | None = None

# 1. ROTA PARA CADASTRAR PARTICIPANTE (POST)
@router.post("/", status_code=201)
def cadastrar_participante(participante: ParticipanteSchema):
    conexao = obter_conexao()
    if not conexao:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    try:
        cursor = conexao.cursor()
        comando_sql = """
            INSERT INTO participantes (nome, email, telefone)
            VALUES (%s, %s, %s)
        """
        valores = (participante.nome, participante.email, participante.telefone)
        cursor.execute(comando_sql, valores)
        conexao.commit()
        return {"mensagem": "Participante cadastrado com sucesso!", "email": participante.email}
    except Exception as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")
        raise HTTPException(status_code=400, detail=f"Erro ao salvar no banco: {str(e)}")
    finally:
        cursor.close()
        conexao.close()

# 2. ROTA PARA LISTAR TODOS OS PARTICIPANTES (GET)
@router.get("/")
def listar_participantes():
    conexao = obter_conexao()
    if not conexao:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT id_participante, nome, email, telefone, data_cadastro FROM participantes")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar no banco: {str(e)}")
    finally:
        cursor.close()
        conexao.close()