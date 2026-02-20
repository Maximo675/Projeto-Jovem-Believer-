#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test que verifica qual origin está sendo enviado
"""
import http.client
import json

payload = {
    'email': 'test.nurse4@hospital.com.br',
    'nome': 'Test',
    'senha': 'TestPassword123!',
    'hospital_id': 1
}

print('=== TEST COM ORIGIN HEADER ===')

origins_para_testar = [
    'http://127.0.0.1:5001',
    'http://localhost:5001',
    'http://127.0.0.1:8000',  # Origin errada
]

for origin in origins_para_testar:
    print(f'\nTestando com origin: {origin}')
    
    conn = http.client.HTTPConnection('localhost', 5001)
    conn.request(
        'POST',
        '/api/auth/register',
        json.dumps(payload),
        {
            'Content-Type': 'application/json',
            'Origin': origin  # Adicionar header Origin
        }
    )
    
    response = conn.getresponse()
    headers = dict(response.getheaders())
    
    cors_origin = headers.get('access-control-allow-origin', 'NÃO ENCONTRADO')
    print(f'  Response Access-Control-Allow-Origin: {cors_origin}')
    
    response.read()  # Consumir body
    conn.close()
