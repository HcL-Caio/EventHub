from fastapi import FastAPI
from src.routes import eventos, campeonatos, participantes, inscricoes

app = FastAPI(title="EventHub API", version="1.0")

# Inclui os seus 4 CRUDs completos de volta no sistema
app.include_router(eventos.router)
app.include_router(campeonatos.router)
app.include_router(participantes.router)
app.include_router(inscricoes.router)