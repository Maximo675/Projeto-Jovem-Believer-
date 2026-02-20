#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test vendo todos os headers
"""
import http.client
import json

payload = {
    'email': 'test.nurse6@hospital.com.br',
    'nome': 'Test6',
    'senha': 'TestPassword123!',
    'hospital_id': 1
}

print('=== Teste com Origin ===')
print('Origin: http://127.0.0.1:5001\n')

conn = http.client.HTTPConnection('localhost', 5001)
conn.request(
    'POST',
    '/api/auth/register',
    json.dumps(payload),
    {
        'Content-Type': 'application/json',
        'Origin': 'http://127.0.0.1:5001'  # Origin correto
    }
)

response = conn.getresponse()
print(f'Status: {response.status}\n')
print('Headers na resposta:')
for key, value in response.getheaders():
    if 'access' in key.lower() or 'origin' in key.lower():
        print(f'  {key}: {value}')

response.read()
conn.close()
