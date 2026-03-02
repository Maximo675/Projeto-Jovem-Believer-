import requests

# Testar redirect da URL antiga para nova
r = requests.get('http://127.0.0.1:5001/frontend/activities/etan-captura-biometrica.html', allow_redirects=False)
print(f'Status do Redirect: {r.status_code}')
print(f'Location Header: {r.headers.get("Location", "Nenhum")}')

# Testar URL correta
r2 = requests.get('http://127.0.0.1:5001/activities/etan-captura-biometrica.html')
print(f'\nStatus da URL correta: {r2.status_code}')
print(f'Primeiros 300 chars: {r2.text[:300]}...')
