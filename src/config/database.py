from supabase import create_client, Client

SUPABASE_URL = "https://mrpiwecmxwjtinwfcxvc.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_P1rcAxytTaM7bhDwMgBPVg_0-xMhdG2"

# Inicializa o cliente que fura o bloqueio de rede corporativa/faculdade
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_db_connection():
    return supabase