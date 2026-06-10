# 🏆 EventHub - API Gamer Modular
## 👥 Integrantes do Grupo
* **Caio Siqueira Amaral** - Matrícula: 22505969
* **Ryan Brito Gomes** - Matrícula: 22508757

## 🚀 Status do Projeto
* **Banco de Dados:** Conectado ao Supabase (PostgreSQL Remoto via Client HTTP).
* **Pipeline CI (GitHub Actions):** ✅ Passando e totalmente configurada.
* **Deploy Funcional:** (https://eventhub-ure3.onrender.com/docs)

O **EventHub** é uma API RESTful de alta performance desenvolvida para o gerenciamento de torneios de eSports. O projeto foi projetado seguindo uma arquitetura em camadas (modular), separando completamente a lógica de negócios e persistência de dados de qualquer interface com o usuário (Frontend/Client).

O sistema conta com dois **CRUDs completos e independentes** integrados nativamente com o banco de dados relacional SQLite.

---

## 🚀 Tecnologias Utilizadas

* **Python 3.11+**
* **FastAPI**: Framework web moderno para construção de APIs.
* **Pydantic**: Camada de validação de dados e tipagem estrita via esquemas.
* **Supabase (PostgreSQL)**: Banco de dados relacional hospedado na nuvem, consumido via Client HTTP para máxima compatibilidade e bypass de firewalls de rede.
* **Pytest & TestClient**: Infraestrutura de testes automatizados integrada à esteira de CI.
* **Uvicorn**: Servidor ASGI para execução da aplicação.

---

## ⚙️ Funcionalidades e Endpoints (Trabalho em Equipe e os 4 CRUDs)

O sistema agora conta com **4 módulos de CRUD independentes e persistentes na nuvem**:

### 1. CRUD de Usuários & Autenticação
* `POST /api/cadastro`: Registro de competidores comuns.
* `POST /api/login`: Valida credenciais e retorna o perfil e nível de autoridade.
* `GET /api/admin/usuarios`: Listagem de todas as contas salvas no banco.
* `DELETE /api/admin/usuarios/{user_id}`: Remoção de contas com travas de segurança.

### 2. CRUD de Torneios
* `POST /api/admin/torneios`: Registro de novos campeonatos.
* `GET /api/user/torneios`: Consulta e retorna todos os torneios ativos.
* `DELETE /api/admin/torneios/{torneio_id}`: Remoção de torneios do banco de dados.

### 3. CRUD de Participantes & Inscrições (Novas Features)
* Gerenciamento completo de inscrições de atletas e equipes nos respectivos torneios integrados ao Supabase, garantindo integridade referencial nas tabelas de dados.

---

## 🛠️ Como Executar o Projeto

1. Certifique-se de ter o Python instalado em sua máquina.
2. Clone o repositório para o seu ambiente local.
3. Abra o terminal na pasta raiz do projeto (`EventHub/`) e execute o servidor através do módulo do Uvicorn:

```bash
python -m uvicorn src.main:app --reload

EventHub/
├── .github/workflows/
│   └── ci.yml                # Esteira de CI automatizada (GitHub Actions)
├── src/
│   ├── config/
│   │   └── database.py       # Inicialização e cliente de conexão HTTP do Supabase
│   ├── models/
│   │   └── schemas.py        # Modelos Pydantic para validação das requisições
│   ├── routes/
│   │   ├── auth_routes.py    # Endpoints de Usuários e Autenticação
│   │   ├── tournament_routes.py # Endpoints de Gerenciamento de Torneios
│   │   └── participants_routes.py # Endpoints de Participantes e Inscrições
│   └── main.py               # Ponto de entrada (Orquestrador) da aplicação FastAPI
├── tests/
│   └── test_main.py          # Arquivo de testes automatizados para validação do CI
├── pyproject.toml            # Configurações de caminhos de execução do Pytest
└── README.md                 # Documentação oficial do projeto