# 🚀 Guia de Instalação e Execução - Ollama + Backend

## ⚠️ Erros Que Você Encontrou

1. **Ollama não rodando** - Erro: `connectex: Nenhuma conexão pôde ser feita porque a máquina de destino as recusou ativamente`
   - Solução: Ollama precisa estar rodando em um terminal separado

2. **PowerShell não reconhece run.py** - Erro: `O termo './backend/run.py' não é reconhecido`
   - Solução: Use `python backend\run.py` em vez de `./backend/run.py`

---

## 📋 Pré-Requisitos

✅ Python 3.8+ instalado
✅ Ollama instalado (https://ollama.ai)
✅ pip funcionando

---

## ⚙️ Instalação Rápida (Primeira Vez)

### 1️⃣ Instale Ollama
```
https://ollama.ai
```
Baixe, instale e reinicie seu PC.

### 2️⃣ Instale Dependências Python
```powershell
cd C:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer
python -m pip install -r backend\requirements.txt
```

### 3️⃣ (Opcional) Crie Ambiente Virtual
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

---

## 🎯 Como Executar (Todos os Dias)

### Opção A: Scripts Automáticos (RECOMENDADO)

#### Terminal 1 - Iniciar Ollama:
```powershell
powershell -ExecutionPolicy Bypass -File start_ollama.ps1
```

Ou use o .bat (mais simples):
```
start_ollama.bat
```

#### Terminal 2 - Iniciar Backend:
```powershell
powershell -ExecutionPolicy Bypass -File start_backend.ps1
```

Ou use o .bat:
```
start_backend.bat
```

---

### Opção B: Comandos Manuais

#### Terminal 1 - Ollama:
```powershell
ollama serve
```

#### Terminal 2 - Backend:
```powershell
python backend\run.py
```

---

## ✅ Teste Se Está Funcionando

### Quando Ollama Inicia:
Você verá:
```
[Ollama] The Ollama API is now available at http://localhost:11434
```

### Quando Backend Inicia:
Você verá:
```
* Running on http://127.0.0.1:5000
```

### Teste a API:
```powershell
# Teste Ollama (Terminal 3)
curl http://localhost:11434/api/tags

# Teste Backend
curl http://localhost:5000/api/health
```

---

## 🔧 Modelos Ollama Disponíveis

Se Ollama não tem modelos, baixe um:

```powershell
# Llama2 (recomendado, ~4GB)
ollama pull llama2

# Alternativas
ollama pull mistral
ollama pull neural-chat
ollama pull phi
```

---

## 📁 Estrutura de Arquivos

```
Project Root/
├── .env                    ← Arquivo de configuração (NOVO)
├── start_ollama.bat       ← Script para iniciar Ollama (NOVO)
├── start_ollama.ps1       ← Script PowerShell para Ollama (NOVO)
├── start_backend.bat      ← Script para iniciar Backend (NOVO)
├── start_backend.ps1      ← Script PowerShell para Backend (NOVO)
├── backend/
│   ├── run.py            ← Servidor Flask
│   ├── requirements.txt   ← Dependências
│   └── app/
│       ├── config.py     ← Configurações
│       └── services/
│           └── ai_service.py ← Conexão com Ollama
```

---

## 🔍 Troubleshooting

### "Ollama não inicia"
```powershell
# Verifique se está instalado
ollama version

# Se não funcionar, instale em:
# https://ollama.ai
```

### "Backend diz 'Ollama não disponível'"
```powershell
# Verifique se Ollama está rodando
curl http://localhost:11434/api/tags

# Se não funcionar, inicie Ollama primeiro
ollama serve
```

### "Porta 5000 ou 11434 já em uso"
```powershell
# Encontre o processo usando a porta
netstat -ano | findstr :5000

# Mate o processo (substitua PID)
taskkill /PID <PID> /F
```

### "ImportError: No module named 'flask'"
```powershell
# Reinstale dependências
python -m pip install --upgrade -r backend\requirements.txt
```

---

## 📊 Fluxo de Execução

```
Terminal 1              Terminal 2
┌──────────────┐        ┌──────────────┐
│   Ollama     │        │   Backend    │
│   :11434     │        │   :5000      │
└──────────────┘        └──────────────┘
       ▲                       ▲
       │ REST API              │
       └───────────────────────┘
              Frontend
           http://localhost
```

---

## 🎉 Pronto Para Usar!

Depois de iniciar ambos os serviços:

1. Abra no navegador: `http://localhost`
2. Login/Register
3. Chat com IA funcionando!

---

## 📞 Próximas Etapas

- [ ] Testar chat com IA
- [ ] Adicionar mais modelos Ollama
- [ ] Configurar banco de dados PostgreSQL
- [ ] Deploy em produção

---

**Data:** 19 de Fevereiro de 2026  
**Projeto:** Alura Jovem Believer
