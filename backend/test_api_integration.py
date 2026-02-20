"""
Script de teste de integração front-back
Testa todos os endpoints da API
"""

import requests
import json
from datetime import datetime

# Configuração
BASE_URL = "http://localhost:5001/api"
TOKEN = None

# Cores para output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_test(name, method, endpoint, status_code):
    """Imprime resultado do teste"""
    symbol = GREEN + "✓" + RESET if status_code < 400 else RED + "✗" + RESET
    print(f"{symbol} {method:6} {endpoint:40} -> {status_code}")


def test_auth():
    """Testa endpoints de autenticação"""
    global TOKEN
    
    print("\n" + "="*70)
    print("🔐 TESTANDO AUTENTICAÇÃO")
    print("="*70)
    
    # 1. Registrar novo usuário
    print("\n1. POST /api/auth/register")
    payload = {
        "email": f"teste_{int(datetime.now().timestamp())}@teste.com",
        "nome": "Usuário Teste",
        "senha": "senha_segura_123",
        "hospital_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print_test("Register", "POST", "/auth/register", response.status_code)
    
    if response.status_code == 201:
        print(f"  Resposta: {json.dumps(response.json(), indent=2)}")
        user_email = payload['email']
        user_password = payload['senha']
    else:
        print(f"  ❌ Erro: {response.text}")
        return False
    
    # 2. Login
    print("\n2. POST /api/auth/login")
    payload = {
        "email": user_email,
        "senha": user_password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    print_test("Login", "POST", "/auth/login", response.status_code)
    
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ Login bem-sucedido")
        TOKEN = data.get('data', {}).get('token') or data.get('token')
        
        if not TOKEN:
            # Se for padrão antigo
            TOKEN = data.get('token')
        
        print(f"  Token: {TOKEN[:20]}..." if TOKEN else "  ⚠️ Token não encontrado")
    else:
        print(f"  ❌ Erro: {response.text}")
        return False
    
    # 3. Logout
    print("\n3. POST /api/auth/logout")
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    print_test("Logout", "POST", "/auth/logout", response.status_code)
    
    return True


def test_users():
    """Testa endpoints de usuários"""
    print("\n" + "="*70)
    print("👥 TESTANDO USUÁRIOS")
    print("="*70)
    
    if not TOKEN:
        print("⚠️ Token não disponível, pulando testes de usuários")
        return False
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # 1. Obter usuário
    print("\n1. GET /api/users/{user_id}")
    response = requests.get(f"{BASE_URL}/users/1", headers=headers)
    print_test("Get User", "GET", "/users/1", response.status_code)
    
    if response.status_code == 200:
        print(f"  ✓ Usuário obtido")
    else:
        print(f"  ℹ️ Resposta: {response.text[:100]}")
    
    # 2. Atualizar usuário
    print("\n2. PUT /api/users/{user_id}")
    payload = {"nome": "Novo Nome Teste"}
    response = requests.put(f"{BASE_URL}/users/1", json=payload, headers=headers)
    print_test("Update User", "PUT", "/users/1", response.status_code)
    
    if response.status_code in [200, 404]:
        print(f"  ℹ️ Resposta: {response.text[:100]}")


def test_courses():
    """Testa endpoints de cursos"""
    print("\n" + "="*70)
    print("📚 TESTANDO CURSOS")
    print("="*70)
    
    if not TOKEN:
        print("⚠️ Token não disponível, pulando testes de cursos")
        return False
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # 1. Listar cursos
    print("\n1. GET /api/courses")
    response = requests.get(f"{BASE_URL}/courses", headers=headers)
    print_test("List Courses", "GET", "/courses", response.status_code)
    
    if response.status_code == 200:
        data = response.json()
        total = data.get('data', {}).get('total') or data.get('total', 0)
        print(f"  ✓ {total} cursos encontrados")
    
    # 2. Obter curso por ID
    print("\n2. GET /api/courses/{course_id}")
    response = requests.get(f"{BASE_URL}/courses/1", headers=headers)
    print_test("Get Course", "GET", "/courses/1", response.status_code)
    
    if response.status_code == 200:
        print(f"  ✓ Curso obtido")
    elif response.status_code == 404:
        print(f"  ℹ️ Curso não encontrado (esperado se banco vazio)")


def test_hospitals():
    """Testa endpoints de hospitais"""
    print("\n" + "="*70)
    print("🏥 TESTANDO HOSPITAIS")
    print("="*70)
    
    if not TOKEN:
        print("⚠️ Token não disponível, pulando testes de hospitais")
        return False
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # 1. Listar hospitais
    print("\n1. GET /api/hospitals")
    response = requests.get(f"{BASE_URL}/hospitals", headers=headers)
    print_test("List Hospitals", "GET", "/hospitals", response.status_code)
    
    if response.status_code == 200:
        data = response.json()
        count = len(data.get('data', {}).get('hospitais', []))
        print(f"  ✓ {count} hospitais encontrados")
    
    # 2. Obter hospital por ID
    print("\n2. GET /api/hospitals/{hospital_id}")
    response = requests.get(f"{BASE_URL}/hospitals/1", headers=headers)
    print_test("Get Hospital", "GET", "/hospitals/1", response.status_code)


def test_ai():
    """Testa endpoints de IA"""
    print("\n" + "="*70)
    print("🤖 TESTANDO IA")
    print("="*70)
    
    if not TOKEN:
        print("⚠️ Token não disponível, pulando testes de IA")
        return False
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # 1. Chat com IA
    print("\n1. POST /api/ai/chat")
    payload = {
        "mensagem": "Qual é o objetivo do SUS?",
        "usuario_id": 1
    }
    response = requests.post(f"{BASE_URL}/ai/chat", json=payload, headers=headers)
    print_test("AI Chat", "POST", "/ai/chat", response.status_code)
    
    if response.status_code in [200, 404, 500]:
        print(f"  ℹ️ Resposta: {response.text[:100]}")


def test_error_cases():
    """Testa casos de erro"""
    print("\n" + "="*70)
    print("⚠️ TESTANDO CASOS DE ERRO")
    print("="*70)
    
    # 1. Registro sem email
    print("\n1. POST /api/auth/register - SEM EMAIL")
    payload = {"nome": "Test", "senha": "teste123"}
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print_test("Register Error", "POST", "/auth/register", response.status_code)
    print(f"  Status esperado: 400 Bad Request")
    print(f"  Resposta: {response.text[:200]}")
    
    # 2. Login com email errado
    print("\n2. POST /api/auth/login - CREDENCIAIS INVÁLIDAS")
    payload = {"email": "nao_existe@teste.com", "senha": "errada"}
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    print_test("Login Error", "POST", "/auth/login", response.status_code)
    print(f"  Status esperado: 401 Unauthorized")
    print(f"  Resposta: {response.text[:200]}")
    
    # 3. Acessar recurso não encontrado
    print("\n3. GET /api/users/99999 - NÃO ENCONTRADO")
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    response = requests.get(f"{BASE_URL}/users/99999", headers=headers)
    print_test("Get User Error", "GET", "/users/99999", response.status_code)
    print(f"  Status esperado: 404 Not Found")
    print(f"  Resposta: {response.text[:200]}")


def main():
    """Executa todos os testes"""
    print("\n" + RED + "="*70 + RESET)
    print("🧪 TESTE DE INTEGRAÇÃO FRONT-BACK")
    print("="*70)
    print(f"Base URL: {BASE_URL}")
    print(f"Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Testar autenticação
        if not test_auth():
            print(RED + "\n❌ Autenticação falhou, abortando outros testes" + RESET)
            return
        
        # Testar outros endpoints
        test_users()
        test_courses()
        test_hospitals()
        test_ai()
        test_error_cases()
        
        # Resumo
        print("\n" + "="*70)
        print(GREEN + "✓ TESTES CONCLUÍDOS" + RESET)
        print("="*70)
        print("\nPróximos passos:")
        print("1. Verifique os status codes (esperados 200, 201, 400, 401, 404)")
        print("2. Verifique as respostas (padrão JSON esperado)")
        print("3. Se houver erros 400/404 inesperados, verifique a rota no backend")
        print("4. Se houver erro 500, verifique os logs do servidor")
        
    except Exception as e:
        print(f"\n" + RED + f"❌ ERRO: {str(e)}" + RESET)
        print(f"Verifique se o servidor está rodando em {BASE_URL}")


if __name__ == "__main__":
    main()
