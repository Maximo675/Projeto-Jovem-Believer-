# ⚡ Guia Rápido de Comandos - INFANT.ID

## 🚀 Começar em 30 Segundos

### Windows PowerShell

```powershell
# Passo 1: Navegar para pasta do backend
cd backend

# Passo 2: Instalar dependências (primeira vez)
pip install -r requirements.txt

# Passo 3: Iniciar servidor
python run.py

# Resultado esperado:
# * Running on http://127.0.0.1:5000
# * Press CTRL+C to quit
```

### Linux/Mac (Bash)

```bash
# Passo 1: Navegar para pasta do backend
cd backend

# Passo 2: Instalar dependências (primeira vez)
pip install -r requirements.txt

# Passo 3: Iniciar servidor
python run.py
```

---

## 🌐 Acessar no Navegador

Depois que o servidor iniciar, abra seu navegador e acesse:

```
http://localhost:5000/

# Página inicial

http://localhost:5000/pages/login.html

# Fazer login

http://localhost:5000/pages/register.html

# Criar conta

http://localhost:5000/pages/dashboard.html

# Dashboard (após login)
```

---

## 📝 Testar APIs via Terminal

### Listar Documentos

```powershell
# Windows PowerShell
curl http://localhost:5000/api/documents
```

```bash
# Linux/Mac
curl http://localhost:5000/api/documents
```

### Listar Hospitais

```powershell
curl http://localhost:5000/api/hospitals
```

```bash
curl http://localhost:5000/api/hospitals
```

### Registrar Novo Usuário

```powershell
$body = @{
    email = "novo@hospital.com"
    nome = "João Silva"
    senha = "SenhaTest123"
    hospital_id = 1
} | ConvertTo-Json

curl -X POST http://localhost:5000/api/auth/register `
  -H "Content-Type: application/json" `
  -Body $body
```

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "novo@hospital.com",
    "nome": "João Silva",
    "senha": "SenhaTest123",
    "hospital_id": 1
  }'
```

### Fazer Login

```powershell
$body = @{
    email = "novo@hospital.com"
    senha = "SenhaTest123"
} | ConvertTo-Json

curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -Body $body
```

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "novo@hospital.com",
    "senha": "SenhaTest123"
  }'
```

### Obter Documento Específico

```powershell
curl "http://localhost:5000/api/documents/Informativo%20Etan"
```

```bash
curl "http://localhost:5000/api/documents/Informativo%20Etan"
```

---

## 🗄️ Comandos do Banco de Dados

### Criar Banco (Primeira Vez)

```bash
# Windows (abra prompt do MySQL)
mysql -u root -p
```

```sql
-- Depois de conectar ao MySQL, execute:
CREATE DATABASE infant_id_platform;
USE infant_id_platform;
SOURCE backend/database/schema.sql;
```

### Verificar Tabelas Criadas

```sql
USE infant_id_platform;
SHOW TABLES;

-- Resultado esperado:
-- users
-- hospitals
-- courses
-- lessons
-- progress
-- ia_conversations
-- certificates
```

### Limpar Banco Completo

```sql
-- ⚠️ CUIDADO: Deleta TUDO
DROP DATABASE infant_id_platform;
```

---

## 👥 Testes de Usuário

### Registrar Usuário de Teste

**Via Browser:**
1. Acesse: `http://localhost:5000/pages/register.html`
2. Preencha:
   - Nome: `Teste Silva`
   - Email: `teste@hospital.com`
   - Hospital: Selecione na lista
   - Senha: `Teste123`
3. Clique "Registrar"

**Via API:**

```powershell
$body = @{
    email = "teste@hospital.com"
    nome = "Teste Silva"
    senha = "Teste123"
    hospital_id = 1
} | ConvertTo-Json

curl -X POST http://localhost:5000/api/auth/register `
  -H "Content-Type: application/json" `
  -Body $body
```

### Analisar Resposta

Procure por:
- ✅ `"mensagem": "Usuário registrado com sucesso"`
- ✅ ID do usuário
- ✅ Email confirmado

---

## 🔐 Manipular Tokens JWT

### Extrair Token de Login

```powershell
$response = curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -Body (@{
    email = "teste@hospital.com"
    senha = "Teste123"
  } | ConvertTo-Json)

# O token está em: $response.token
# Salve para usar nos próximos comandos
```

### Usar Token em Requisições Protegidas

```powershell
$token = "eyJhbGciOiJIUzI1NiIs..."  # Cole seu token aqui

curl -H "Authorization: Bearer $token" `
  http://localhost:5000/api/users/1
```

```bash
TOKEN="eyJhbGciOiJIUzI1NiIs..."
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/users/1
```

---

## 🧪 Testes Automatizados

### Rodar Todos os Testes

```bash
cd backend
pytest tests/
```

### Rodar Teste Específico

```bash
cd backend
pytest tests/test_auth.py -v
```

### Ver Cobertura

```bash
cd backend
pytest --cov=app tests/
```

---

## 🐛 Troubleshooting Rápido

### Erro: "Port 5000 already in use"

```powershell
# Encontrar processo usando porta 5000
netstat -ano | findstr :5000

# Matar processo (Windows)
taskkill /PID <PID> /F
```

```bash
# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Erro: "ModuleNotFoundError: No module named 'flask'"

```bash
pip install -r requirements.txt
```

### Erro: "Connection refused" ao acessar API

```
Verificar se servidor está rodando:
curl http://localhost:5000/

Se não funcionar, abra novo terminal e execute:
cd backend
python run.py
```

### Erro: "ModuleNotFoundError: No module named 'docx'"

```bash
pip install python-docx
```

---

## 📊 Monitorar Servidor

### Ver Logs em Tempo Real

O servidor mostrará logs automáticamente no terminal.

Procure por linhas como:
```
[INFO] GET /api/documents - 200
[INFO] POST /api/auth/register - 201
[ERROR] POST /api/auth/login - 401
```

### Ver Requisições HTTP

Se tiver `requests` instalado:

```bash
pip install requests

python -c "
import requests
r = requests.get('http://localhost:5000/')
print(f'Status: {r.status_code}')
print(f'Tipo: {r.headers.get(\"content-type\")}')
"
```

---

## 🔄 Reiniciar Servidor

### Quando Você Fez Mudanças no Código

1. **Pare o servidor:**
   - Pressione `CTRL + C` no terminal

2. **Reinice:**
   ```bash
   python run.py
   ```

3. **Atualize o navegador:**
   - Pressione `CTRL + SHIFT + R` (hard refresh)

---

## 🌍 Variáveis de Ambiente

### Criar Arquivo .env

Na pasta `backend/`, crie arquivo `.env`:

```env
# Flask
FLASK_ENV=development
SECRET_KEY=sua-chave-muito-secreta-aqui

# Database
DATABASE_URL=mysql://root:password@localhost/infant_id_platform

# OpenAI
OPENAI_API_KEY=sk-...sua-chave...

# CORS
CORS_ORIGINS=http://localhost:5000,http://localhost:3000
```

### Usar Variáveis no Código

```python
import os
api_key = os.getenv('OPENAI_API_KEY')
```

---

## 💾 Backup Essencial

### Criar Backup

```powershell
# Windows
Copy-Item -Path "backend", "pages", "assets" -Destination "backup_$(Get-Date -Format yyyyMMdd)" -Recurse
```

```bash
# Linux/Mac
tar -czf backup_$(date +%Y%m%d).tar.gz backend/ pages/ assets/ docs/
```

### Restaurar de Backup

```powershell
# Windows
Copy-Item -Path "backup_20250211\*" -Destination "." -Recurse -Force
```

```bash
# Linux/Mac
tar -xzf backup_20250211.tar.gz
```

---

## 🎯 Checklist de Testes Manuais

```powershell
# 1. Iniciar servidor
cd backend
python run.py

# 2. Testar homepage
curl http://localhost:5000/

# 3. Registrar usuário
curl -X POST http://localhost:5000/api/auth/register `
  -H "Content-Type: application/json" `
  -Body (@{ email = "teste@hospital.com"; nome = "Teste"; senha = "Teste123"; hospital_id = 1 } | ConvertTo-Json)

# 4. Fazer login
curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -Body (@{ email = "teste@hospital.com"; senha = "Teste123" } | ConvertTo-Json)

# 5. Listar documentos
curl http://localhost:5000/api/documents

# 6. Listar hospitais
curl http://localhost:5000/api/hospitals

# 7. Testar página de login
# Abra: http://localhost:5000/pages/login.html

# 8. Testar registro
# Abra: http://localhost:5000/pages/register.html

# Resultado esperado: TODOS os testes devem retornar 200 ou 201
```

---

## 📱 Testar Responsividade

### iPhone SE (375x667)

```
F12 (abrir DevTools)
Ctrl + Shift + M (modo responsivo)
Selecionar: iPhone SE
```

### iPad (768x1024)

```
F12
Ctrl + Shift + M
Device Toolbar → iPad
```

### Desktop (1920x1080)

```
F12
Desativar Device Toolbar
```

---

## 🚀 Deploy Local Rápido

### Com Python SimpleHTTP (Frontend only)

```bash
# Na pasta raiz do projeto
python -m http.server 8000

# Acesse: http://localhost:8000
```

### Com Flask Production (Completo)

```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## 📞 Verificar Versões Instaladas

```bash
python --version
pip --version
```

```bash
cd backend
pip show flask
pip show sqlalchemy
pip show python-docx
pip show Flask-CORS
```

---

## 🔧 Limpar Cache e Reinstalar

```bash
# Remover cache Python
cd backend
rm -r __pycache__ .pytest_cache *.pyc

# Remover env virtual (se existir)
deactivate  # Se estiver em venv
rm -r venv

# Reinstalar tudo do zero
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📊 Monitoramento Básico

### Ver recursos usados pelo servidor

```bash
# Windows Task Manager
# Procure por "python" na lista de processos

# Linux
ps aux | grep python
top  # Ver uso de CPU e memória

# Mac
top -o MEM | grep python
```

---

## ✅ Checklist Final

- [ ] Terminal aberto em `backend/`
- [ ] `python run.py` executado
- [ ] Servidor rodando em `http://localhost:5000`
- [ ] Homepage carrega em `http://localhost:5000/`
- [ ] Login page funciona em `http://localhost:5000/pages/login.html`
- [ ] Register page funciona em `http://localhost:5000/pages/register.html`
- [ ] Conseguiu registrar um usuário
- [ ] Conseguiu fazer login
- [ ] Dashboard carrega após login
- [ ] Documentos aparecem
- [ ] APIs funcionam (testou com curl)

---

## 📞 Próximos Passos

Se tudo funcionou:
1. Leia `QUICKSTART.md` (seção 3) para configurar banco de dados
2. Execute `backend/database/schema.sql` no MySQL
3. Teste com dados reais
4. Leia `TEST_GUIDE.md` para testes completos

Se algo não funcionou:
1. Veja `ISSUES.md` para problemas comuns
2. Revise logs do terminal
3. Verifique firewall/antivírus bloqueando porta 5000

---

**Status:** Pronto para usar!
**Data:** 11 de Fevereiro de 2025
**Próximo:** `QUICKSTART.md` (Database Setup)
