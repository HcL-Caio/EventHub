import requests

# Suas credenciais reais do Supabase
SUPABASE_URL = "https://mrpiwecmxwjtinwfcxvc.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_P1rcAxytTaM7bhDwMgBPVg_0-xMhdG2"

# Rota HTTP (Porta 443) para ler a tabela 'eventos' que você criou no SQL Editor
url_rest = f"{SUPABASE_URL}/rest/v1/eventos"

headers = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
}

print("Tentando conexão via API Web HTTP (Fura-Bloqueio de Rede)...")

try:
    resposta = requests.get(url_rest, headers=headers)
    if resposta.status_code == 200:
        print("\n✅ SUCESSO ABSOLUTO! O código burlou o bloqueio da rede local.")
        print(f"Banco respondendo via HTTP. Dados atuais: {resposta.json()}")
    else:
        print(f"\n❌ Conectou na nuvem, mas a tabela retornou erro {resposta.status_code}: {resposta.text}")
        print("Dica: Certifique-se de que clicou em 'Run without RLS' lá no site para criar as tabelas.")
except Exception as e:
    print(f"\n❌ ERRO DE REDE: {e}")