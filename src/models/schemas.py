from pydantic import BaseModel

# Modelos do CRUD 1 (Usuários)
class UsuarioCadastro(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str

# Modelo do CRUD 2 (Torneios)
class TorneioCadastro(BaseModel):
    nome: str
    data: str
    status: str = "Inscrições Abertas"