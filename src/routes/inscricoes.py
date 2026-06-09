from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.config.database import obter_conexao

router = APIRouter(prefix="/inscricoes", tags=["Inscrições"])

class InscricaoSchema(BaseModel):
    id_participante: int
    id_campeonato: int

# 1. REALIZAR INSCRIÇÃO (POST)
@router.post("/", status_code=201)
def realizar_inscricao(inscricao: InscricaoSchema):
    conexao = obter_conexao()
    if not conexao:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    try:
        cursor = conexao.cursor()
        
        # Query SQL para inserir a inscrição (status padrão será 'Pendente' como no banco)
        comando_sql = """
            INSERT INTO inscricoes (id_participante, id_campeonato)
            VALUES (%s, %s)
        """
        valores = (inscricao.id_participante, inscricao.id_campeonato)
        cursor.execute(comando_sql, valores)
        conexao.commit()
        
        return {"mensagem": "Inscrição realizada com sucesso!", "status": "Pendente"}
    except Exception as e:
        # Se o cara tentar se inscrever duas vezes no mesmo campeonato (Garantido pelo CONSTRAINT do banco)
        if "Duplicate entry" in str(e):
            raise HTTPException(status_code=400, detail="Este participante já está inscrito neste campeonato.")
        # Se um dos IDs (participante ou campeonato) não existir
        if "Foreign key constraint fails" in str(e) or "foreign key" in str(e).lower():
            raise HTTPException(status_code=400, detail="ID de participante ou campeonato inválido.")
        raise HTTPException(status_code=400, detail=f"Erro ao salvar no banco: {str(e)}")
    finally:
        cursor.close()
        conexao.close()

# 2. LISTAR INSCRIÇÕES COM DADOS RELACIONADOS (GET)
@router.get("/")
def listar_inscricoes():
    conexao = obter_conexao()
    if not conexao:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    try:
        cursor = conexao.cursor(dictionary=True)
        # Esse JOIN monstro traz o nome do participante, modalidade do campeonato e nome do evento de uma vez só!
        query = """
            SELECT 
                i.id_inscricao, 
                p.nome AS nome_participante, 
                c.modalidade AS modalidade_campeonato, 
                e.nome AS nome_evento,
                i.data_inscricao, 
                i.status_inscricao
            FROM inscricoes i
            INNER JOIN participantes p ON i.id_participante = p.id_participante
            INNER JOIN campeonatos c ON i.id_campeonato = c.id_campeonato
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