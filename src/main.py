from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="EventHub API")

# 🔓 Configuração de CORS (Essencial para o JavaScript conseguir falar com a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📂 Caminho absoluto para a pasta public
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

# 🌐 Rota para carregar o HTML principal do site
@app.get("/site")
def read_site():
    return FileResponse(os.path.join(PUBLIC_DIR, "index.html"))

# 🛠️ A LINHA MÁGICA: Monta a pasta public para servir o app.js e o style.css automaticamente
app.mount("/", StaticFiles(directory=PUBLIC_DIR), name="public")