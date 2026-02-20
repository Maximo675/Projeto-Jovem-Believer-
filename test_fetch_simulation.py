#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test que simula exatamente o que fetch() JavaScript faz
"""
import http.client
import json

# Dados que será enviados
payload = {
    'email': 'test.nurse3@hospital.com.br',
    'nome': 'Teste Enfermeira 3',
    'senha': 'TestPassword123!',
    'hospital_id': 1
}

print('=== TEST FETCH SIMULATION ===')
print('URL: http://localhost:5001/api/auth/register')
print('Method: POST')
print('Headers:')
print('  Content-Type: application/json')
print('  Authorization: Bearer (none)')
print()
print('Body:')
print(json.dumps(payload, indent=2))
print()

# Conectar ao servidor
conn = http.client.HTTPConnection('localhost', 5001)

# Fazer request
conn.request(
    'POST',
    '/api/auth/register',
    json.dumps(payload),
    {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer none'  # Simular token vazio
    }
)

# Receber resposta
response = conn.getresponse()
status = response.status
headers = dict(response.getheaders())
body = response.read().decode('utf-8')

print('=== RESPOSTA ===')
print(f'Status: {status}')
print('Headers:')
for key, value in headers.items():
    print(f'  {key}: {value}')
print()
print('Body:')
try:
    data = json.loads(body)
    print(json.dumps(data, indent=2, ensure_ascii=False))
except:
    print(body)

conn.close()
