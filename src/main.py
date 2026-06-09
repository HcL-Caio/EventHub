from fastapi import FastAPI
from src.config.database import init_db
from src.routes import auth_routes, tournament_routes

# Inicializa o Banco de Dados SQLite na subida da aplicação
init_db()

app = FastAPI(
    title="EventHub - API ",
    description="Backend profissional organizado em camadas com 2 CRUDs independentes.",
    version="3.0.0"
)

# 🔌 Conectando os módulos de rotas na API principal
app.include_router(auth_routes.router)
app.include_router(tournament_routes.router)