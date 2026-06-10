# 🏆 EventHub - API Gamer Modular
## 🚀 Status do Projeto
Banco de dados atualizado para o Supabase via HTTP.

O **EventHub** é uma API RESTful de alta performance desenvolvida para o gerenciamento de torneios de eSports. O projeto foi projetado seguindo uma arquitetura em camadas (modular), separando completamente a lógica de negócios e persistência de dados de qualquer interface com o usuário (Frontend/Client).

O sistema conta com dois **CRUDs completos e independentes** integrados nativamente com o banco de dados relacional SQLite.

---

## 🚀 Tecnologias Utilizadas

* **Python 3.11+**
* **FastAPI**: Framework web moderno e ágil para construção de APIs.
* **Pydantic**: Camada de validação de dados e tipagem estrita via esquemas.
* **SQLite3**: Banco de dados relacional embutido para persistência local de dados.
* **Uvicorn**: Servidor ASGI de alta performance para execução da aplicação.

---

## ⚙️ Funcionalidades e Endpoints (Os 2 CRUDs)

A documentação interativa e testes das rotas podem ser acessados em tempo real através da interface do Swagger em: `http://127.0.0.1:8000/docs`.

### 1. CRUD de Usuários & Autenticação
Gerencia o controle de acesso e contas cadastradas na plataforma.
* `POST /api/cadastro`: Realiza o registro de competidores comuns (nível `user`) impedindo a duplicação de e-mails via restrições no SQLite.
* `POST /api/login`: Valida credenciais e retorna o perfil e o nível de autoridade da conta (`user` ou `admin`).
* `GET /api/admin/usuarios`: Rota administrativa para listagem em tempo real de todas as contas salvas no banco.
* `DELETE /api/admin/usuarios/{user_id}`: Rota administrativa para exclusão de contas, com proteção nativa contra a exclusão acidental do Administrador Principal.

### 2. CRUD de Torneios
Camada de gerenciamento de regras de negócio para os campeonatos de eSports.
* `POST /api/admin/torneios`: Permite ao painel administrativo registrar um novo campeonato no banco de dados fornecendo nome, data e status.
* `GET /api/user/torneios`: Rota global que consulta o SQLite e retorna a listagem estruturada em JSON de todos os torneios disponíveis.
* `DELETE /api/admin/torneios/{torneio_id}`: Permite a remoção definitiva de um torneio através de seu ID de registro.

---

## 💾 Mecanismo de Semente de Dados (Data Seeding)

Para facilitar a avaliação e garantir o funcionamento imediato do ecossistema, o módulo `database.py` executa uma rotina automática durante a inicialização do servidor:
1. Verifica e cria o arquivo físico do banco de dados e suas respectivas tabelas caso não existam.
2. Injeta a conta mestre do administrador se o banco estiver vazio:
   * **E-mail:** `admin@eventhub.com`
   * **Senha:** `admin123`
3. Popula a tabela de campeonatos com dados fictícios iniciais para validação imediata do método `GET`.

---

## 🛠️ Como Executar o Projeto

1. Certifique-se de ter o Python instalado em sua máquina.
2. Clone o repositório para o seu ambiente local.
3. Abra o terminal na pasta raiz do projeto (`EventHub/`) e execute o servidor através do módulo do Uvicorn:

```bash
python -m uvicorn src.main:app --reload

📐 Arquitetura do Projeto (Divisão em Camadas)
Para garantir a escalabilidade e a separação de conceitos (SoC), o código está estruturado da seguinte forma:
EventHub/
├── database/
│   └── eventhub.db          # Arquivo do banco de dados relacional (gerado localmente)
├── src/
│   ├── config/
│   │   └── database.py       # Inicialização das tabelas e gerenciamento de conexões
│   ├── models/
│   │   └── schemas.py        # Modelos Pydantic para validação das requisições (Payloads)
│   ├── routes/
│   │   ├── auth_routes.py    # Endpoints do CRUD 1 (Usuários e Autenticação)
│   │   └── tournament_routes.py # Endpoints do CRUD 2 (Gerenciamento de Torneios)
│   └── main.py               # Ponto de entrada (Orquestrador) da aplicação FastAPI
├── .gitignore                # Regras de exclusão para arquivos locais e caches do Python
└── README.md                 # Documentação oficial do projeto

---

### 🔥 Último Envio para o GitHub

Com todos os arquivos salvos e organizados, vá no Git Bash e execute os comandos finais para deixar seu repositório impecável:

```bash
git add .
git commit -m "feat: versão final da API modular com documentação concluída"
git push origin main