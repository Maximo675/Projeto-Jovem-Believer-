# ⚡ REFERÊNCIA RÁPIDA - Comandos Essenciais

## 🎯 EXECUTAR AGORA (Copie e Cole)

### Terminal 1 - Ollama
```powershell
powershell -ExecutionPolicy Bypass -File start_ollama.ps1
```

### Terminal 2 - Backend
```powershell
powershell -ExecutionPolicy Bypass -File start_backend.ps1
```

### Terminal 3 - Testes (Opcional)
```powershell
# Teste Ollama
curl http://localhost:11434/api/tags

# Teste Backend
curl http://localhost:5000/api/health

# Teste Chat
curl -X POST http://localhost:5000/api/ai/chat -H "Content-Type: application/json" -d '{"message":"Oi"}'
```

---

## 📊 Verificações Rápidas

```powershell
# Ver Python
python --version

# Ver Ollama
ollama version

# Ver pip
pip --version

# Listar modelos Ollama
ollama list

# Testar conexão Ollama
curl http://localhost:11434/api/tags

# Testar backend rodando
curl http://localhost:5000
```

---

## 🔧 Instalações Rápidas

```powershell
# Instalar Ollama
# https://ollama.ai

# Instalar dependências
pip install -r backend\requirements.txt

# Atualizar dependências
pip install --upgrade -r backend\requirements.txt

# Baixar modelo Ollama
ollama pull llama2
ollama pull mistral
ollama pull neural-chat
```

---

## 🚨 Troubleshooting Rápido

```powershell
# Porta 5000 em uso?
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Porta 11434 em uso?
netstat -ano | findstr :11434
taskkill /PID <PID> /F

# Limpar cache Python
rm -Recurse -Force __pycache__
rm -Recurse -Force backend\__pycache__

# Resetar ambiente virtual
rm -Recurse -Force venv
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

---

## 🌐 URLs Úteis

```
Frontend:     http://localhost
Backend:      http://localhost:5000
API Docs:     http://localhost:5000/api/health
Ollama API:   http://localhost:11434/api/tags
```

---

## 🔐 Logins Teste

```
Email: test@example.com
Senha: test123

# Criar novo via UI:
Register page -> preencha dados
```

---

## 📁 Principais Arquivos

```
backend/run.py              # Servidor principal
backend/app/config.py       # Configurações
backend/app/routes/ai.py    # Rotas de IA
backend/app/services/ai_service.py  # Serviço IA
.env                        # Variáveis de ambiente
```

---

## 🎓 Próximos Passos

1. ✅ Ollama rodando
2. ✅ Backend rodando
3. ⬜ Testar chat com IA
4. ⬜ Adicionar autenticação
5. ⬜ Testar banco de dados
6. ⬜ Deploy em produção

---

**Precisa de ajuda?**  
Veja: `OLLAMA_QUICK_START.md` ou `SOLUCAO_OLLAMA.md`
