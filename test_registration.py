#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script para diagnosticar erro de registro
"""
import urllib.request
import json

# Dados de teste do registro
data = {
    'email': 'test.nurse2@hospital.com.br',
    'nome': 'Teste Enfermeira 2',
    'senha': 'TestPassword123!',
    'hospital_id': 1
}

print('=== TESTE DE REGISTRO ===')
print(f'Email: {data["email"]}')
print(f'Nome: {data["nome"]}')
print(f'Hospital ID: {data["hospital_id"]}')
print()

try:
    req = urllib.request.Request(
        'http://localhost:5001/api/auth/register',
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print('✅ SUCESSO!')
    print('Resposta completa:')
    print(json.dumps(result, indent=2))
    
except urllib.error.HTTPError as e:
    print(f'❌ HTTP ERROR {e.code} - {e.reason}')
    try:
        error_data = json.loads(e.read())
        print('Resposta da API:')
        print(json.dumps(error_data, indent=2))
    except:
        print('Corpo da resposta:')
        print(e.read().decode())
        
except Exception as e:
    print(f'❌ Erro: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()
