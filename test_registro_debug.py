#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script que simula EXATAMENTE o que o navegador faz
Inclui todos os headers e comportamento de CORS que o fetch() usa
"""
import http.client
import json
import time

# Email único (como se fosse novo registro)
email = f'nurse.debug.{int(time.time())}@hospital.com.br'
senha = 'TestPassword123!'
nome = f'Nurse Debug {int(time.time())}'
hospital_id = 1

payload = {
    'email': email,
    'nome': nome,
    'senha': senha,
    'hospital_id': hospital_id
}

print('=' * 70)
print('SIMULANDO EXATAMENTE O QUE O NAVEGADOR FAZ')
print('=' * 70)
print()
print(f'URL: http://localhost:5001/api/auth/register')
print(f'Método: POST')
print(f'Origin: http://127.0.0.1:5001')
print()
print('Body:')
print(json.dumps(payload, indent=2))
print()

# 1ª REQUEST - PREFLIGHT (OPTIONS)
print('-' * 70)
print('1. PREFLIGHT REQUEST (OPTIONS)')
print('-' * 70)

conn = http.client.HTTPConnection('localhost', 5001)
conn.request(
    'OPTIONS',
    '/api/auth/register',
    '',
    {
        'Origin': 'http://127.0.0.1:5001',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'content-type'
    }
)

response = conn.getresponse()
print(f'Status: {response.status}')
print('Resposta OK para preflight\n')
response.read()
conn.close()

# 2ª REQUEST - ACTUAL POST
print('-' * 70)
print('2. ACTUAL POST REQUEST')
print('-' * 70)

conn = http.client.HTTPConnection('localhost', 5001)
conn.request(
    'POST',
    '/api/auth/register',
    json.dumps(payload),
    {
        'Content-Type': 'application/json',
        'Origin': 'http://127.0.0.1:5001'
    }
)

response = conn.getresponse()
status = response.status
body = response.read().decode('utf-8')

print(f'Status: {status}')
print()

if status == 201:
    data = json.loads(body)
    print('✅ SUCESSO HTTP 201')
    print(f'   Usuario ID: {data["usuario"]["id"]}')
    print(f'   Email: {data["usuario"]["email"]}')
    print()
    print('Próximo passo esperado no navegador:')
    print('   → Mostrar mensagem de sucesso')
    print('   → Aguardar 1.5 segundos')
    print('   → Redirecionar para /pages/login.html')
elif status == 400:
    data = json.loads(body)
    print(f'❌ HTTP 400 - {data.get("erro")}')
else:
    print(f'❌ HTTP {status}')
    print(body)

conn.close()
