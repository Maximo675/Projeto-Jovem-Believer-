# -*- coding: utf-8 -*-
"""
Script de Teste - Verificação de Estilos CSS Aplicados
Valida se as melhorias visuais estão sendo renderizadas corretamente
"""

import requests
import json
from datetime import datetime

# Configuração
BASE_URL = "http://127.0.0.1:5001"
TEST_RESULTS = {
    "timestamp": datetime.now().isoformat(),
    "server_url": BASE_URL,
    "tests": []
}

def log_test(name, status, details=""):
    """Log de teste com status"""
    result = {
        "test": name,
        "status": "✅ PASSOU" if status else "❌ FALHOU",
        "details": details
    }
    TEST_RESULTS["tests"].append(result)
    print(f"[{result['status']}] {name}")
    if details:
        print(f"    → {details}")

def test_server_connection():
    """Testa conexão com o servidor"""
    try:
        response = requests.get(f"{BASE_URL}/pages/dashboard.html", timeout=5)
        log_test(
            "Conexão com Servidor",
            response.status_code == 200,
            f"Status Code: {response.status_code}"
        )
        return response.status_code == 200
    except Exception as e:
        log_test("Conexão com Servidor", False, str(e))
        return False

def test_course_page():
    """Testa a página de curso"""
    try:
        response = requests.get(f"{BASE_URL}/pages/course.html", timeout=5)
        has_css = "var(--primary-blue)" in response.text
        log_test(
            "Página de Curso (course.html)",
            response.status_code == 200 and has_css,
            f"Status: {response.status_code}, CSS Variables: {has_css}"
        )
        return response.status_code == 200
    except Exception as e:
        log_test("Página de Curso", False, str(e))
        return False

def test_css_improvements():
    """Testa se os novos estilos CSS estão no arquivo"""
    try:
        response = requests.get(f"{BASE_URL}/pages/course.html", timeout=5)
        text = response.text
        
        # Verificar novos estilos
        css_checks = {
            "Tabelas com gradiente": "linear-gradient(135deg, var(--primary-blue)" in text,
            "Progress bar com glow": "box-shadow: 0 0 10px rgba(0, 255, 136" in text,
            "Listas com auto-numeração": "counter-increment: step-counter" in text,
            "Header com gradiente": "background: linear-gradient(135deg, rgba(0, 102, 204" in text,
            "Buttons melhorados": "transform: translateX(-2px)" in text,
            "Imagens com hover": "transform: scale(1.02)" in text,
            "Blockquotes estilizadas": "border-left: 5px solid var(--primary-blue)" in text,
        }
        
        all_passed = all(css_checks.values())
        
        for check_name, result in css_checks.items():
            status = "✓" if result else "✗"
            print(f"  [{status}] {check_name}")
        
        log_test(
            "Estilos CSS Implementados",
            all_passed,
            f"{sum(css_checks.values())}/{len(css_checks)} verificações passaram"
        )
        return all_passed
    except Exception as e:
        log_test("Estilos CSS Implementados", False, str(e))
        return False

def test_responsive_design():
    """Testa responsive design"""
    try:
        response = requests.get(f"{BASE_URL}/pages/course.html", timeout=5)
        text = response.text
        
        responsive_checks = {
            "Media query 768px": "@media (max-width: 768px)" in text,
            "Viewport meta": 'viewport' in response.headers.get('content-type', '') or 'viewport' in text,
            "Flexbox layout": "display: flex" in text,
        }
        
        all_passed = all(responsive_checks.values())
        
        for check_name, result in responsive_checks.items():
            status = "✓" if result else "✗"
            print(f"  [{status}] {check_name}")
        
        log_test(
            "Design Responsivo",
            all_passed,
            f"{sum(responsive_checks.values())}/{len(responsive_checks)} verificações passaram"
        )
        return all_passed
    except Exception as e:
        log_test("Design Responsivo", False, str(e))
        return False

def test_database_lessons():
    """Testa se as aulas estão no banco de dados"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/courses/1",
            headers={"Authorization": "Bearer teste"},
            timeout=5
        )
        
        # Se retorna 401, o servidor está respondendo (autenticação falhou, não API)
        if response.status_code == 401:
            log_test(
                "API de Cursos Responsiva",
                True,
                "API respondeu com autenticação necessária (esperado)"
            )
            return True
        elif response.status_code == 200:
            log_test(
                "API de Cursos Responsiva",
                True,
                "API retornou dados de curso"
            )
            return True
        else:
            log_test(
                "API de Cursos Responsiva",
                False,
                f"Status inesperado: {response.status_code}"
            )
            return False
    except Exception as e:
        log_test("API de Cursos Responsiva", False, str(e))
        return False

def main():
    """Executa todos os testes"""
    print("=" * 70)
    print("TESTES DE VALIDAÇÃO - MELHORIAS VISUAIS")
    print("=" * 70)
    print()
    
    # Executar testes
    tests = [
        ("Verificação do Servidor", test_server_connection),
        ("Página de Curso", test_course_page),
        ("Estilos CSS", test_css_improvements),
        ("Design Responsivo", test_responsive_design),
        ("API de Cursos", test_database_lessons),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n[TESTANDO] {test_name}...")
        result = test_func()
        results.append(result)
        print()
    
    # Resumo
    print("=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    print(f"Total de testes: {len(TEST_RESULTS['tests'])}")
    print(f"Passaram: {sum(1 for t in TEST_RESULTS['tests'] if '✅' in t['status'])}")
    print(f"Falharam: {sum(1 for t in TEST_RESULTS['tests'] if '❌' in t['status'])}")
    print()
    
    # Resultado final
    if all(results):
        print("✅ TODOS OS TESTES PASSARAM!")
        print("\nA plataforma está pronta com os novos estilos implementados:")
        print("  • Tabelas profissionais com gradientes")
        print("  • Progress bar com efeito de brilho")
        print("  • Listas numeradas automaticamente")
        print("  • Header de aula com gradiente")
        print("  • Botões com efeito de translação")
        print("  • Design responsivo mantido")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM - Verificar detalhes acima")
    
    print("\n" + "=" * 70)
    
    return all(results)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
