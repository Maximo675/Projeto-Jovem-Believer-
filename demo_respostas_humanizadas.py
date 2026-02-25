#!/usr/bin/env python3
"""
Demo das respostas humanizadas e fluidas da IA
"""
import requests
import json
from datetime import datetime, timedelta
import jwt

BASE_URL = "http://localhost:5001"
USUARIO_ID = 5
USUARIO_EMAIL = "maximo.teste@gmail.com"
SECRET_KEY = "your_secret_key"

def gerar_token():
    payload = {
        'usuario_id': USUARIO_ID,
        'email': USUARIO_EMAIL,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def fazer_req(pergunta):
    token = gerar_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    url = f"{BASE_URL}/api/ia/consult"
    dados = {
        'usuario_id': USUARIO_ID,
        'curso_id': 1,
        'pergunta': pergunta
    }
    
    try:
        resp = requests.post(url, json=dados, headers=headers, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('resposta', '')
        return "Erro na requisicao"
    except:
        return "Erro de conexao"

def main():
    print("\n" + "=" * 70)
    print("DEMO - RESPOSTAS HUMANIZADAS E FLUIDAS DA IA")
    print("=" * 70)
    
    # Teste 1: Coleta Biometrica
    print("\n[PERGUNTA 1] Como funciona a coleta biometrica de recem-nascidos?")
    print("-" * 70)
    resposta = fazer_req("Como funciona a coleta biometrica de recem-nascidos?")
    print(resposta)
    
    # Teste 2: Seguranca
    print("\n" + "=" * 70)
    print("\n[PERGUNTA 2] Quais sao os protocolos de seguranca?")
    print("-" * 70)
    resposta = fazer_req("Quais sao os protocolos de seguranca?")
    print(resposta)
    
    # Teste 3: Equipamento
    print("\n" + "=" * 70)
    print("\n[PERGUNTA 3] Como funciona o ETAN?")
    print("-" * 70)
    resposta = fazer_req("Como funciona o ETAN?")
    print(resposta)
    
    # Teste 4: Duvida comum
    print("\n" + "=" * 70)
    print("\n[PERGUNTA 4] O equipamento nao esta reconhecendo, o que faco?")
    print("-" * 70)
    resposta = fazer_req("O equipamento nao esta reconhecendo, o que faco?")
    print(resposta)
    
    print("\n" + "=" * 70)
    print("CONCLUSAO")
    print("=" * 70)
    print("""
Respostas agora sao:
- Mais humanizadas: Conversam como um colega experiente
- Mais fluidas: Texto natural e facil de ler
- Mais acessiveis: Palavras simples, sem jargao excessivo
- Mais praticas: Vao direto ao ponto com passos claros
- Mais empaticas: Entendem as dificuldades da enfermeira

PROXIMAS MELHORIAS:
- Adicionar mais perguntas comuns ao dicionario
- Personalizar respostas por experiencia da enfermeira
- Integrar com historico de conversas para contexto
""")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()
