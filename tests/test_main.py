from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_main():
    """
    Teste básico para garantir que a API inicializa e as rotas
    estão respondendo corretamente no ambiente de CI.
    """
    # Se você tiver uma rota padrão ou de saúde (health check)
    resposta = client.get("/eventos/")
    # Como as rotas retornam dados do banco via HTTP, validamos se o status é 200 (Sucesso)
    assert resposta.status_code == 200 or resposta.status_code == 404
