# 🧪 Guia de Testes - INFANT.ID

## ✅ O Que Testar Agora

Sua plataforma está pronta! Aqui estão todos os testes que você pode fazer:

---

## 1️⃣ Testar Interface de Login

```bash
# Abrir no navegador:
http://localhost:5000/pages/login.html
```

### Checklist Visual
- ✅ Logo aparece corretamente
- ✅ Cores (verde e azul médico) aparecem
- ✅ Formulário é responsivo
- ✅ Botões funcionam (visuais)
- ✅ Animações funcionam

### Dados de Teste
```
Email: teste@hospital.com
Senha: senha123
```

---

## 2️⃣ Testar Interface de Registro

```bash
# Abrir no navegador:
http://localhost:5000/pages/register.html
```

### Checklist
- ✅ Formulário completo aparece
- ✅ Seletor de hospital carrega
- ✅ Validações funcionam
- ✅ Design é profissional

---

## 3️⃣ Testar Logo nas Páginas

### Verificar Presença da Logo
```bash
# Abrir: http://localhost:5000/index.html
# Verificar se logo aparece no navbar

# Abrir: http://localhost:5000/pages/login.html
# Verificar se logo aparece na página
```

---

## 4️⃣ Testar API de Documentos

### Com cURL
```bash
# Terminal aberto na pasta do projeto

# Listar documentos
curl http://localhost:5000/api/documents

# Obter conteúdo de um documento
curl "http://localhost:5000/api/documents/Informativo Etan"

# Fazer download
curl -o documento.docx "http://localhost:5000/api/documents/Informativo Etan/download"

# Ver índice
curl http://localhost:5000/api/documents/indice
```

### Com Postman/Insomnia
```
GET http://localhost:5000/api/documents
GET http://localhost:5000/api/documents/Informativo%20Etan
GET http://localhost:5000/api/documents/indice
GET http://localhost:5000/api/documents/Informativo%20Etan/download
```

### Com Python
```python
import requests

# Listar documentos
response = requests.get('http://localhost:5000/api/documents')
print(response.json())

# Conteúdo
response = requests.get('http://localhost:5000/api/documents/Informativo Etan')
print(response.json()['conteudo'][:200])  # Primeiros 200 chars
```

---

## 5️⃣ Testar API de Hospitais

```bash
# Listar hospitais
curl http://localhost:5000/api/hospitals

# Detalhes de hospital
curl http://localhost:5000/api/hospitals/1

# Criar hospital (requer token auth, teste depois)
curl -X POST http://localhost:5000/api/hospitals \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Hospital Teste",
    "estado": "SP",
    "cidade": "São Paulo",
    "endereco": "Rua Test, 123",
    "telefone": "1234567890",
    "email": "test@hospital.com"
  }'
```

---

## 6️⃣ Testar Fluxo Completo de Autenticação

### 1. Registrar Usuário
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "novo.usuario@hospital.com",
    "nome": "João Silva",
    "senha": "SenhaForte123",
    "hospital_id": 1
  }'
```

### 2. Response Esperada
```json
{
  "mensagem": "Usuário registrado com sucesso",
  "usuario": {
    "id": 1,
    "email": "novo.usuario@hospital.com",
    "nome": "João Silva",
    "funcao": "usuario",
    "ativo": true
  }
}
```

### 3. Fazer Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "novo.usuario@hospital.com",
    "senha": "SenhaForte123"
  }'
```

### 4. Salvar Token Retornado
```json
{
  "mensagem": "Login realizado com sucesso",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "usuario": { ... }
}
```

---

## 7️⃣ Testar Rotas Protegidas com Token

```bash
# Use o token obtido no login

curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  http://localhost:5000/api/users/1

curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  http://localhost:5000/api/courses

curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -X POST http://localhost:5000/api/ia/consult \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 1,
    "pergunta": "Como fazer o procedimento de coleta?",
    "curso_id": 1
  }'
```

---

## 8️⃣ Testar Responsividade

### Desktop (1920x1080)
```bash
# Abrir em navegador em tela cheia
http://localhost:5000/index.html
http://localhost:5000/pages/login.html
```
Verificar se layout expande bem

### Tablet (768x1024)
```
F12 → Devtools → Device Toolbar → iPad
```
Verificar se elementos se reorganizam

### Mobile (375x667)
```
F12 → Devtools → Device Toolbar → iPhone SE
```
Verificar se é necessário scroll, botões clickáveis

---

## 9️⃣ Testar Cores de Design

### Verde Saúde (#00a86b)
- [ ] Botões primários
- [ ] Links destacados
- [ ] Icons de sucesso

### Azul Médico (#1e90ff)
- [ ] Navbar
- [ ] Logo
- [ ] Botões secundários

### Vermelho Alerta (#ff6b6b)
- [ ] Mensagens de erro
- [ ] Icons de alerta

### Fundo Claro (#f0f8f5)
- [ ] Background das seções

---

## 🔟 Script de Teste Automático

```python
# save as test_manual.py
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_suite():
    print("🧪 Iniciando testes da API INFANT.ID\n")
    
    # 1. Testar Documentos
    print("1️⃣ Testando API de Documentos...")
    try:
        resp = requests.get(f"{BASE_URL}/documents")
        assert resp.status_code == 200
        print(f"   ✅ Documentos carregados: {resp.json()['total']} encontrados")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 2. Testar Hospitais
    print("2️⃣ Testando API de Hospitais...")
    try:
        resp = requests.get(f"{BASE_URL}/hospitals")
        assert resp.status_code == 200
        print(f"   ✅ Hospitais carregados: {resp.json()['total']} encontrados")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 3. Testar Registro
    print("3️⃣ Testando Registro...")
    try:
        resp = requests.post(f"{BASE_URL}/auth/register", json={
            "email": f"teste_{int(time.time())}@hospital.com",
            "nome": "Teste User",
            "senha": "SenhaTest123",
            "hospital_id": 1
        })
        assert resp.status_code == 201
        print(f"   ✅ Usuário registrado com sucesso")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 4. Testar Índice
    print("4️⃣ Testando Índice de Conhecimento...")
    try:
        resp = requests.get(f"{BASE_URL}/documents/indice")
        assert resp.status_code == 200
        print(f"   ✅ Índice gerado com sucesso")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print("\n✅ Testes completados!")

if __name__ == "__main__":
    import time
    test_suite()
```

Rodar:
```bash
python test_manual.py
```

---

## 📊 Checklist Final de Validação

### Frontend
- [ ] Logo aparece em todas páginas
- [ ] Cores de saúde estão aplicadas
- [ ] Formulário de login funciona
- [ ] Formulário de register funciona
- [ ] Design é responsivo (mobile, tablet, desktop)
- [ ] Animações são suaves
- [ ] Links funcionam

### Backend
- [ ] Servidor inicia sem erros
- [ ] API /documents funciona
- [ ] API /hospitals funciona
- [ ] API /auth/register funciona
- [ ] API /auth/login funciona
- [ ] Documentos são extraídos corretamente
- [ ] Tokens JWT são gerados

### Banco de Dados
- [ ] Documentos aparecem em /assets/documents/
- [ ] Logo aparece em /assets/logo/
- [ ] Arquivos Word podem ser lidos
- [ ] Conteúdo é extraído com sucesso

### Documentação
- [ ] README.md está completo
- [ ] QUICKSTART.md faz sentido
- [ ] ISSUES.md lista os problemas
- [ ] SESSION_SUMMARY.md explica o que foi feito
- [ ] API.md documenta as rotas

---

## 🐛 Se Algo Não Funcionar

### Problema: "ModuleNotFoundError: No module named 'docx'"
```bash
pip install python-docx
```

### Problema: "ModuleNotFoundError: No module named 'flask_cors'"
```bash
pip install Flask-CORS
```

### Problema: "CORS policy error"
Verifique se CORS foi adicionado ao __init__.py

### Problema: Documentos não aparecem
Verifique se os arquivos .docx estão em `/assets/documents/`

### Problema: Logo não aparece
Verifique se `logo.png` está em `/assets/logo/`

### Problema: Banco de Dados erro
Você ainda precisa configurar MySQL/PostgreSQL (próximo passo)

---

## 📝 Relatório de Testes

Depois de fazer os testes, crie um arquivo `TEST_REPORT.md` com:

```markdown
# Relatório de Testes - INFANT.ID

## Data: 11/02/2026

### Testes Executados
- [ ] Frontend: Login
- [ ] Frontend: Register
- [ ] Frontend: Responsividade
- [ ] API: Documentos
- [ ] API: Hospitais
- [ ] API: Autenticação
- [ ] Documentação
- [ ] Cores e Design

### Resultados
- ✅ Passou
- ⚠️ Aviso
- ❌ Falhou

### Notas
Escreva aqui quaisquer observações importantes

### Próximos Passos
1. ...
2. ...
```

---

**Pronto para começar os testes? 🚀**

Comece com: `http://localhost:5000/index.html`
