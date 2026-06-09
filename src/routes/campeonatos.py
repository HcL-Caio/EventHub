from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from decimal import Decimal
from src.config.database import obter_conexao

router = APIRouter(prefix="/campeonatos", tags=["Campeonatos"])

class CampeonatoSchema(BaseModel):
    id_evento: int
    modalidade: str
    premiacao: Decimal = Decimal("0.00")
    vagas_limitadas: int

# 1. CADASTRAR CAMPEONATO (POST)
@router.post("/", status_code=201)
def cadastrar_campeonato(campeonato: CampeonatoSchema):
    conexao = obter_conexao()
    if not conexao:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    try:
        cursor = conexao.cursor()
        comando_sql = """
            INSERT INTO campeonatos (id_evento, modalidade, premiacao, vagas_limitadas)
            VALUES (%s, %s, %s, %s)
        """
        valores = (campeonato.id_evento, campeonato.modalidade, campeonato.premiacao, campeonato.vagas_limitadas)
        cursor.execute(comando_sql, valores)
        conexao.commit()
        return {"mensagem": "Campeonato criado com sucesso!", "modalidade": campeonato.modalidade}
    except Exception as e:
        # Se tentar cadastrar um campeonato para um id_evento que não existe no banco
        if "Foreign key constraint fails" in str(e) or "foreign key" in str(e).lower():
            raise HTTPException(status_code=400, detail="O ID do evento fornecido não existe.")
        raise HTTPException(status_code=400, detail=f"Erro ao salvar no banco: {str(e)}")
    finally:
        cursor.close()
        conexao.close()

# 2. LISTAR CAMPEONATOS (GET)
@router.get("/")
def listar_campeonatos():
    conexao = obter_conexao()
    if not conexao:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    try:
        cursor = conexao.cursor(dictionary=True)
        # Faz um JOIN simples para trazer o nome do evento junto com o campeonato
        query = """
            SELECT c.id_campeonato, c.modalidade, c.premiacao, c.vagas_limitadas, e.nome AS nome_evento
            FROM campeonatos c
            INNER JOIN eventos e ON c.id_evento = e.id_evento
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar no banco: {str(e)}")
    finally:
        cursor.close()
        conexao.close()