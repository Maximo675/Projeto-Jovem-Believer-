#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Teste para Ollama Integration
Verifica se Ollama está configurado corretamente para INFANT.ID
"""

import os
import sys
import time
import requests
from pathlib import Path

# Cores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

def test_ollama_server():
    """Teste 1: Verificar se servidor Ollama está rodando"""
    print_header("TESTE 1: Servidor Ollama")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            print_success("Servidor Ollama está rodando em http://localhost:11434")
            return True
        else:
            print_error(f"Servidor respondeu com status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Não conseguiu conectar ao Ollama em localhost:11434")
        print_info("Execute em outro terminal: ollama serve")
        return False
    except Exception as e:
        print_error(f"Erro ao conectar: {str(e)}")
        return False

def test_ollama_models():
    """Teste 2: Verificar modelos disponíveis"""
    print_header("TESTE 2: Modelos Disponíveis")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        data = response.json()
        
        if not data.get('models'):
            print_error("Nenhum modelo disponível. Execute: ollama pull llama2")
            return False
        
        print_success(f"Encontrados {len(data['models'])} modelo(s):")
        for model in data['models']:
            print(f"  • {model.get('name', 'Unknown')}")
        
        return True
    except Exception as e:
        print_error(f"Erro ao buscar modelos: {str(e)}")
        return False

def test_ollama_chat():
    """Teste 3: Teste de chat básico"""
    print_header("TESTE 3: Chat Básico")
    
    try:
        payload = {
            "model": "llama2",
            "messages": [
                {"role": "user", "content": "Olá! Responda com 'OK'."}
            ],
            "stream": False
        }
        
        print_info("Enviando pergunta para Ollama...")
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            resposta = data.get('message', {}).get('content', '')
            
            if resposta:
                print_success("Resposta recebida:")
                print(f"  {resposta[:100]}...")
                return True
            else:
                print_error("Resposta vazia")
                return False
        else:
            print_error(f"Erro na requisição: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print_error("Timeout ao aguardar resposta (modelo pode estar lento)")
        return False
    except Exception as e:
        print_error(f"Erro ao testar chat: {str(e)}")
        return False

def test_env_config():
    """Teste 4: Verificar configuração .env"""
    print_header("TESTE 4: Configuração .env")
    
    env_file = Path(__file__).parent.parent / ".env"
    
    if not env_file.exists():
        print_warning(f"Arquivo .env não encontrado em {env_file}")
        return False
    
    # Ler configurações
    config = {}
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                config[key] = value
    
    # Verificar configurações importantes
    checks = {
        'USE_OLLAMA': 'true',
        'OPENAI_MODEL': 'llama2'
    }
    
    all_ok = True
    for key, expected in checks.items():
        actual = config.get(key, 'NÃO ENCONTRADO')
        if actual == expected:
            print_success(f"{key} = {actual}")
        else:
            print_warning(f"{key} = {actual} (esperado: {expected})")
            all_ok = all_ok and (actual == expected)
    
    return all_ok

def test_ai_service():
    """Teste 5: Testar AiService do backend"""
    print_header("TESTE 5: AiService do Backend")
    
    try:
        # Adicionar backend ao path
        backend_path = Path(__file__).parent.parent / "backend"
        sys.path.insert(0, str(backend_path))
        
        # Importar sem iniciar Flask app completo
        from app.services.ai_service import AiService
        
        print_info("Inicializando AiService...")
        ai_service = AiService()
        
        print_info(f"Modo de IA: {ai_service.mode}")
        
        if ai_service.mode == 'mock':
            print_warning("AiService em modo MOCK (Ollama não disponível)")
            return False
        
        if ai_service.mode == 'ollama':
            print_success("AiService usando Ollama ✓")
            
            print_info("Testando pergunta simples...")
            resposta, tokens = ai_service.responder_pergunta("O que é coleta biométrica?")
            
            if resposta and len(resposta) > 10:
                print_success("Resposta recebida e processada:")
                print(f"  {resposta[:80]}...")
                print(f"  Tokens: {tokens}")
                return True
            else:
                print_error("Resposta inválida")
                return False
        
        return True
        
    except ImportError as e:
        print_warning(f"Não conseguiu importar AiService: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Erro ao testar AiService: {str(e)}")
        return False

def test_api_endpoint():
    """Teste 6: Testar endpoint da API"""
    print_header("TESTE 6: API Endpoint")
    
    try:
        payload = {
            "pergunta": "Como funciona o onboarding?",
            "usuario_id": None
        }
        
        print_info("Enviando requisição POST para /api/ia/consult...")
        response = requests.post(
            "http://localhost:5001/api/ia/consult",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("API respondeu com sucesso:")
            print(f"  ID: {data.get('id')}")
            print(f"  Resposta: {data.get('resposta', '')[:80]}...")
            return True
        elif response.status_code == 400:
            print_warning("Requisição inválida (ausência de dados)")
            return False
        elif response.status_code == 500:
            print_error("Erro no servidor: " + response.text)
            return False
        else:
            print_error(f"Status inesperado: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_warning("Flask não está rodando em localhost:5001")
        print_info("Execute em outro terminal: cd backend && python run.py")
        return False
    except Exception as e:
        print_error(f"Erro ao testar API: {str(e)}")
        return False

def main():
    """Executar todos os testes"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("""
    ╔═══════════════════════════════════════════════╗
    ║   TESTE COMPLETO DE OLLAMA - INFANT.ID       ║
    ║   v1.0 - 2026                                ║
    ╚═══════════════════════════════════════════════╝
    """)
    print(f"{Colors.RESET}")
    
    results = {}
    
    # Executar testes
    results['Servidor Ollama'] = test_ollama_server()
    
    if results['Servidor Ollama']:
        results['Modelos Disponíveis'] = test_ollama_models()
        results['Chat Básico'] = test_ollama_chat()
    else:
        print_warning("\nPulando testes dependentes de servidor rodando...")
    
    results['Configuração .env'] = test_env_config()
    results['AiService Backend'] = test_ai_service()
    
    print_warning("\nPara testar endpoint da API, certifique-se que Flask está rodando")
    print_info("Execute em outro terminal: cd backend && python run.py")
    
    # Resumo
    print_header("RESUMO DOS TESTES")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test}: {status}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} testes passaram{Colors.RESET}")
    
    if passed == total:
        print_success("Todos os testes passaram! Ollama está configurado corretamente.")
        return 0
    else:
        print_error(f"{total - passed} teste(s) falharam. Veja acima para detalhes.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print(f"\n{Colors.RESET}")
    sys.exit(exit_code)
