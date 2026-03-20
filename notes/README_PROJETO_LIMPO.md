# 🚀 GUIA RÁPIDO - PROJETO LIMPO

**Status**: Projeto reorganizado e limpeza concluída  
**Última atualização**: 02/03/2026

---

## 🎯 ESTRUTURA FINAL

```
Alura Jovem Believer/
├── backend/
│   ├── app/                          ← CÓDIGO PRINCIPAL
│   │   ├── __init__.py              (rotas Flask)
│   │   ├── config.py
│   │   ├── database.py
│   │   └── websocket_handlers.py
│   ├── run.py                        ← EXECUTAR SERVIDOR (único)
│   ├── setup_database_correctly.py   ← SETUP BANCO DE DADOS
│   └── requirements.txt
│
├── frontend/js/                      ← JAVASCRIPT LIMPO (7 arquivos)
│   ├── config-urls.js               (configuração)
│   ├── etan-image-processor.js      (processamento de imagens)
│   ├── etan-simulator-manager.js    (guia simulador)
│   ├── etan-websocket*.js           (websockets)
│   ├── iframe-external-bridge.js    (comunicação com iframe)
│   └── license-bypass.js            (bypass de licença)
│
├── pages/                            ← PÁGINAS PRINCIPAIS
│   ├── etan-captura-biometrica.html ← PÁGINA PRINCIPAL (biometria)
│   ├── ia-chat.html                 (chat com IA)
│   ├── atividades.html              (atividades)
│   ├── infant-bridge.html           (helper para CORS)
│   ├── login.html / register.html
│   ├── dashboard.html / course.html
│   └── OLD/                         (backup - não mexer)
│
├── assets/                           (imagens, ícones)
├── css/                              (estilos)
├── js/
│   └── openbio-bridge.js            (bridge para openbio)
│
└── instance/
    └── infant_id_platform.db        (banco de dados SQLite)
```

---

## ⚙️ COMO USAR

### 1️⃣ PRIMEIRA VEZ (Setup Inicial)

```powershell
# Dentro do diretório do projeto
cd "c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer"

# Criar e ativar venv (se necessário)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Setup do banco de dados
python backend/setup_database_correctly.py
python backend/init_activity_tables.py

# Inicializar atividades (se necessário)
# python backend/init_activity_tables.py
```

### 2️⃣ INICIAR O SERVIDOR

```powershell
# Terminal 1: Backend Flask
python backend/run.py
# Esperado: "Running on http://localhost:5001"

# Terminal 2: Openbio Bridge (se necessário para biometria)
node openbio-bridge.js
# Esperado: "Listening on localhost:3333"

# Terminal 3: Iniciar Openbio Services
& "c:\Openbio\start-services.ps1"
# Esperado: Openbio devices, enroll API, etc.
```

### 3️⃣ ACESSAR A APLICAÇÃO

```
🌐 Principal:      http://localhost:5001/pages/etan-captura-biometrica.html
🤖 Chat IA:        http://localhost:5001/pages/ia-chat.html
📝 Atividades:     http://localhost:5001/pages/atividades.html
🔐 Login:          http://localhost:5001/pages/login.html
```

---

## 🔍 VERIFICAR SE ESTÁ FUNCIONANDO

### DevTools Console (F12)
```javascript
// Deve haver logs como:
[INFANT OVERRIDE] XMLHttpRequest override carregado
[INFANT] XHR reescrita: ... → :5001
```

### Network Tab (F12)
```
Procure por requisições terminando em:
- /db/api/config  (Device Service)
- /api/chat       (Chat IA)
- Status: 200 OK  (não CORS error)
```

### Terminal
```
Flask: 127.0.0.1:5001 - GET /pages/etan-captura-biometrica.html 200
openbio-bridge: Listening on localhost:3333
```

---

## 🎨 ARQUIVOS PRINCIPAIS PARA MODIFICAR

### Para adicionar novas rotas Flask:
**Arquivo**: `backend/app/__init__.py`
```python
@app.route('/api/minha-rota', methods=['GET', 'POST'])
def minha_funcao():
    return {'status': 'ok'}
```

### Para modificar interface JavaScript:
**Arquivo**: `frontend/js/config-urls.js` (configuração)  
**Arquivo**: `frontend/js/etan-simulator-manager.js` (lógica)

### Para novas páginas HTML:
```html
<!-- pages/minha-pagina.html -->
<script src="../frontend/js/config-urls.js"></script>
<!-- resto do HTML -->
```

---

## 🗑️ ARQUIVOS DELETADOS (NÃO RECUPERAR)

Os seguintes arquivos foram deletados por serem **código morto/obsoleto**:
- ❌ 25 scripts Python da raiz (fix_*, update_*, convert_*, etc.)
- ❌ 11 Service Workers e interceptadores conflitantes
- ❌ 6 páginas HTML de teste/backup

Se precisar deles, estão em `/pages/OLD/` (páginas) ou foram completamente deletados.

---

## 🆘 TROUBLESHOOTING

### "Module not found" ao rodar `run.py`
```powershell
pip install -r requirements.txt
# Ou especificamente:
pip install flask flask-cors flask-sqlalchemy python-socketio
```

### "CORS error" no console
```
✅ Esperado! O sistema redireciona:
   localhost:5000 → localhost:5001 → openbio-bridge via proxy
```

### "contentDocument não accessible"
```
✅ Verificar browser console para logs [INFANT BRIDGE]
```

### Biometria não aparece
```
1. Verificar se openbio services estão rodando
2. Verificar se openbio-bridge.js está rodando
3. Verificar console para erros
```

---

## 📊 VERIFICAR INTEGRIDADE

Para confirmar que a limpeza foi bem sucedida:

```powershell
# Contar arquivos atuais
cd c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer

# Frontend/JS deve ter 7 arquivos
ls frontend\js | Measure-Object

# Backend deve ter poucos scripts
ls backend\*.py | Measure-Object

# Pages deve ter ~11 páginas HTML
ls pages\*.html | Measure-Object
```

---

## ✨ DIFERENÇAS PÓS-LIMPEZA

| Feature | Antes | Depois |
|---------|-------|--------|
| Scripts raiz | 31 | 6 |
| Service Workers | 5 | 0 |
| Interceptadores | 7+ | 0 |
| Frontend/JS | 18 | 7 |
| Backend scripts | 21+ | 3 |
| Páginas HTML | 18 | 17 |
| **Tamanho reduzido** | - | 60% ↓ |
| **Conflitos** | Muitos | Nenhum |

---

## 📝 NOTAS

- **infant-bridge.html**: Arquivo novo criado para contornar CORS. Usado internamente.
- **Pasta `/pages/OLD/`**: Backup de testes. Não mexer.
- **config.py**: Guarda credenciais e configuração. Editar com cuidado.
- **openbio-bridge.js**: Bridge para serviços biométricos. Manter rodando em paralelo.

---

**Projeto pronto para desenvolvimento focado! 🚀**

