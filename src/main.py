from fastapi import FastAPI
from routes import eventos, campeonatos, participantes, inscricoes

app = FastAPI(title="EventHub API", version="1.0")

app.include_router(eventos.router)
app.include_router(campeonatos.router)
app.include_router(participantes.router)
app.include_router(inscricoes.router)
