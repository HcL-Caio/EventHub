from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 🔌 1. Importando as rotas de cada um dos 4 módulos
from src.routes import eventos, campeonatos, participantes, inscricoes

app = FastAPI(
    title="EventHub - API Modular de Alta Performance",
    description="Backend oficial estruturado com 4 tabelas relacionais em conformidade com o script do seminário.",
    version="4.0.0"
)

# Configuração de CORS (Evita bloqueios de requisições se testado de outras máquinas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 2. Ativando e incluindo os roteadores na aplicação principal
app.include_router(eventos.router)
app.include_router(campeonatos.router)
app.include_router(participantes.router)
app.include_router(inscricoes.router)

@app.get("/", tags=["Home"])
def read_root():
    return {"mensagem": "API EventHub rodando com sucesso! Acesse /docs para a documentação completa."}