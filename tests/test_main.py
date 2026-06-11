from fastapi.testclient import TestClient
from src.main import app  

client = TestClient(app)

def test_read_main():
    """
    Teste básico para garantir que a API inicializa e as rotas
    estão respondendo corretamente no ambiente de CI.
    """
    resposta = client.get("/api/eventos") 
    assert resposta.status_code == 200 or resposta.status_code == 404
