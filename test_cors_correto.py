#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test com header Origin correto
"""
import http.client
import json

payload = {
    'email': 'test.nurse5@hospital.com.br',
    'nome': 'Test5',
    'senha': 'TestPassword123!',
    'hospital_id': 1
}

print('Test com Origin header = http://127.0.0.1:5001')

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
headers = dict(response.getheaders())

print(f'Status: {response.status}')
print(f'Access-Control-Allow-Origin: {headers.get("access-control-allow-origin")}')

response.read()
conn.close()
