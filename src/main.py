from fastapi import FastAPI
from src.routes.eventos import router as eventos_router

app = FastAPI(
    title="EventHub API",
    description="API para gestão de eventos, campeonatos e inscrições",
    version="1.0.0"
)

@app.get("/")
def raiz():
    return {"mensagem": "Bem-vindo ao EventHub! A API está online."}

# Registra as rotas de eventos no sistema
app.include_router(eventos_router)