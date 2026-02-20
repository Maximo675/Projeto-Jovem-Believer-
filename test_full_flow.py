#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste simples de fluxo: Register -> Login
"""
import urllib.request
import json
import time

# Email único
email = f'nurse.{int(time.time())}@hospital.com.br'
senha = 'TestPassword123!'
nome = f'Nurse Test {int(time.time())}'

data_register = {
    'email': email,
    'nome': nome,
    'senha': senha,
    'hospital_id': 1
}

print('=' * 60)
print('1. REGISTRO DE NOVO USUARIO')
print('=' * 60)
print(f'Email: {email}')
print(f'Nome: {nome}')
print(f'Senha: {senha}')
print()

try:
    req = urllib.request.Request(
        'http://localhost:5001/api/auth/register',
        data=json.dumps(data_register).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    
    print('✅ REGISTRO BEM-SUCEDIDO - HTTP 201')
    print(f'   Usuario ID: {result["usuario"]["id"]}')
    print(f'   Email: {result["usuario"]["email"]}')
    print(f'   Funcao: {result["usuario"]["funcao"]}')
    print()
    
    print('=' * 60)
    print('2. LOGIN COM CREDENCIAIS')
    print('=' * 60)
    
    data_login = {
        'email': email,
        'senha': senha
    }
    
    req = urllib.request.Request(
        'http://localhost:5001/api/auth/login',
        data=json.dumps(data_login).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    
    print('✅ LOGIN BEM-SUCEDIDO - HTTP 200')
    print(f'   Token: {result["token"][:30]}...')
    print()
    print('FLUXO COMPLETO FUNCIONANDO!')
    
except urllib.error.HTTPError as e:
    try:
        error = json.loads(e.read())
        print(f'❌ HTTP {e.code} ERROR')
        print(f'   Erro: {error.get("erro")}')
    except:
        print(f'❌ HTTP {e.code}')
        
except Exception as e:
    print(f'❌ ERROR: {type(e).__name__}: {e}')
