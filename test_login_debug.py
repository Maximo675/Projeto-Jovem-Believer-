"""
Debug de Login - Simula exatamente o que o navegador está fazendo
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5001"

# Headers que o navegador envia
headers = {
    "Content-Type": "application/json",
    "Origin": "http://127.0.0.1:5001",
    "User-Agent": "Mozilla/5.0"
}

# Dados de login - use o email que registrou
email = "maximo.testes@gmail.com"  # MUDE PARA O SEU EMAIL REGISTRADO
senha = "TestPassword123!"  # MUDE PARA A SUA SENHA

print(f"[TEST] Tentando login com: {email}")
print(f"[TEST] URL: {BASE_URL}/api/auth/login")
print(f"[TEST] Enviando payload: {{'email': '{email}', 'senha': '***'}}")
print()

try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "senha": senha},
        headers=headers,
        timeout=5
    )
    
    print(f"[TEST] Status Code: {response.status_code}")
    print(f"[TEST] Headers: {dict(response.headers)}")
    print(f"[TEST] Response Body:")
    
    try:
        json_response = response.json()
        print(json.dumps(json_response, indent=2, ensure_ascii=False))
    except:
        print(f"[TEST] (Não é JSON): {response.text}")
    
    print()
    print("[TEST] ANÁLISE:")
    if response.status_code == 200:
        print("✅ Login bem-sucedido!")
    elif response.status_code == 400:
        print("❌ Erro 400 - Verifique os dados enviados")
        if "email" in response.text.lower():
            print("   → Problema: Email não existe ou inválido")
        if "senha" in response.text.lower():
            print("   → Problema: Senha incorreta")
    elif response.status_code == 401:
        print("❌ Erro 401 - Credenciais inválidas")
    else:
        print(f"❌ Erro {response.status_code} - Problema no servidor")
        
except requests.exceptions.ConnectionError as e:
    print(f"❌ ERRO DE CONEXÃO: Não conseguiu conectar em {BASE_URL}")
    print(f"   Verifique se o Flask está rodando em http://127.0.0.1:5001")
    print(f"   Erro: {e}")
except Exception as e:
    print(f"❌ ERRO: {e}")
