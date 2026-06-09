from src.config.database import obter_conexao

def testar():
    print("Tentando conectar ao banco de dados EventHub...")
    conexao = obter_conexao()
    
    if conexao:
        print("Conexão realizada com sucesso!")
        cursor = conexao.cursor()
        try:
            cursor.execute("SHOW TABLES;")
            tabelas = cursor.fetchall()
            print("\nTabelas encontradas no banco:")
            for tabela in tabelas:
                print(f"- {tabela[0]}")
        except Exception as e:
            print(f"Conectou, mas houve um erro ao listar tabelas: {e}")
            print("Dica: Você já criou o banco 'EventHub' e as tabelas com o script SQL?")
        finally:
            cursor.close()
            conexao.close()
            print("\nConexão fechada com segurança.")
    else:
        print("Falha na conexão. Verifique o arquivo .env.")

if __name__ == "__main__":
    testar()