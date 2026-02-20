# 🚀 Como Rodar INFANT.ID + Ollama - Guia Rápido

**Pasta:** `c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer`

---

## ⚡ 5 Passos Rápidos

### 1️⃣ Instalar e Rodar Ollama (PowerShell 1)

```powershell
# Download: https://ollama.ai (se não tiver)

# Baixar modelo
ollama pull llama2

# Rodar servidor (deixar aberto)
ollama serve
```

**Esperado:**
```
Listening on 127.0.0.1:11434 (and on 0.0.0.0:11434)
```

---

### 2️⃣ Preparar Backend (PowerShell 2)

```powershell
cd "c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\backend"

# Criar ambiente virtual (1ª vez)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependências (1ª vez)
pip install -r requirements.txt

# Teste rápido
python test_ollama.py
```

**Esperado:**
```
✅ Todos testes passando
```

---

### 3️⃣ Rodar Backend (PowerShell 2, continua)

```powershell
# Backend está rodando agora
python run.py
```

**Esperado:**
```
Running on http://127.0.0.1:5000
```

---

### 4️⃣ Rodar Frontend (PowerShell 3)

```powershell
cd "c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer"

# Servidor HTTP
python -m http.server 8000
```

**Esperado:**
```
Serving HTTP on 0.0.0.0 port 8000
```

---

### 5️⃣ Testar Chat (Browser)

Abra: **http://localhost:8000/pages/ia-chat.html**

1. Digite uma pergunta
2. Clique em "Enviar"
3. Aguarde resposta (5-20 segundos na 1ª vez)

**Esperado:**
```
Assistente responde em português
Resposta aparece no chat em tempo real
```

---

## ✅ Checklist Rápido

```
☐ Ollama instalado (ollama --version)
☐ Ollama servidor rodando (PowerShell 1)
☐ Backend rodando (PowerShell 2) 
☐ Frontend rodando (PowerShell 3)
☐ test_ollama.py passou 6/6 testes
☐ Chat respondendo em http://localhost:8000/pages/ia-chat.html
```

---

## 🚨 Troubleshooting Rápido

| Erro | Solução |
|------|---------|
| "Ollama not found" | Reinstalar ou adicionar ao PATH |
| Connection refused :11434 | Rodar `ollama serve` em PowerShell 1 |
| ImportError openai | `pip install openai` |
| 404 in chat | Verifique se backend está rodando |
| Resposta lenta | Normal na 1ª vez (10-30s) |

---

## 📁 Arquivos Principais

```
Ollama:
└─ C:\Users\maximo.silva\AppData\Local\Programs\Ollama\

Backend:
├─ backend/run.py              ← Executar isto
├─ backend/test_ollama.py      ← Testar isto
├─ backend/.env                (Verificar variáveis)
└─ backend/app/services/ai_service.py

Frontend:
├─ pages/ia-chat.html          ← Abrir isto no browser
├─ js/ia-chat.js
└─ css/ia-chat.css

Documentação:
├─ docs/SETUP_OLLAMA.md        (Guia detalhado)
├─ docs/OLLAMA_CHECKLIST.md    (Checklist)
└─ docs/OLLAMA_ANALISE_COMPLETA.md
```

---

## 📊 URLs

| Serviço | URL | Porta |
|---------|-----|-------|
| **Ollama API** | http://localhost:11434 | 11434 |
| **Backend** | http://localhost:5000 | 5000 |
| **Frontend** | http://localhost:8000 | 8000 |
| **Chat** | http://localhost:8000/pages/ia-chat.html | 8000 |

---

## 🎯 Teste Completo

```powershell
# PowerShell 1 - Ollama
ollama serve

# PowerShell 2 - Backend
cd backend
python test_ollama.py
python run.py

# PowerShell 3 - Frontend
python -m http.server 8000

# Browser - Chat
http://localhost:8000/pages/ia-chat.html

# Pergunta de teste:
"Como funciona a coleta biométrica?"

# Esperado:
Resposta em português sobre coleta biométrica
```

---

## 💡 Dicas

1. **Llama2 é lento?** Tentar:
   ```powershell
   ollama pull mistral
   # Trocar OPENAI_MODEL=mistral em .env
   ```

2. **Quer OpenAI de fallback?**
   ```env
   # .env já tem OPENAI_API_KEY configurada
   # Fallback automático se Ollama cair
   ```

3. **Quer resetar everything?**
   ```powershell
   ollama rm llama2      # Remover modelo
   ollama pull llama2    # Baixar novamente
   rm backend/*.db       # Limpar banco dados
   ```

4. **Ver logs?**
   ```powershell
   # Terminal onde roda "ollama serve"
   # Mostra tudo que acontece
   ```

---

## 🎓 Próximas Aulas

1. **Customizar prompts** - `backend/app/services/ai_service.py`
2. **Adicionar avaliação** - Salvado automaticamente
3. **Análise de histórico** - Endpoint `/api/ia/historico/{user_id}`
4. **Fine-tuning do modelo** - Avançado

---

## 📞 Precisa de Ajuda?

1. Leia `docs/SETUP_OLLAMA.md`
2. Execute `backend/test_ollama.py`
3. Veja `docs/OLLAMA_CHECKLIST.md`
4. Consulte `docs/OLLAMA_ANALISE_COMPLETA.md`

---

**Tudo pronto! Divirta-se com Ollama! 🚀**
