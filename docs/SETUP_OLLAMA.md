# 🤖 Guia Completo: Configurar Ollama para INFANT.ID

**Última atualização:** 19 de Fevereiro de 2026  
**Status:** ✅ Pronto para uso

---

## 📋 Índice
1. [O que é Ollama?](#o-que-é-ollama)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Teste](#teste)
5. [Troubleshooting](#troubleshooting)
6. [Alternativas](#alternativas)

---

## O que é Ollama?

**Ollama** é uma plataforma open-source para executar modelos de IA **localmente** em sua máquina, sem usar APIs externas.

### Vantagens:
✅ **Sem custos** - Não paga por tokens   
✅ **Privado** - Dados não saem da seu computador   
✅ **Rápido** - Execução local   
✅ **Offline** - Funciona sem internet   

### Desvantagens:
⚠️ Requer recursos (GPU recomendada)  
⚠️ Qualidade menor que GPT-4  

---

## 🚀 Instalação

### Passo 1: Download e Instalação

#### Windows
1. Acesse: https://ollama.ai
2. Clique em "Download"
3. Escolha "Windows"
4. Execute o instalador `.exe`
5. Siga as instruções na tela
6. Reinicie o Windows após instalar

#### macOS
```bash
curl -fsSLO https://ollama.ai/download/Ollama-darwin.zip
unzip Ollama-darwin.zip
mv Ollama.app /Applications/
```

#### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Passo 2: Verificar Instalação

Abra PowerShell e execute:
```powershell
ollama --version
```

Você deve ver algo como:
```
ollama version 0.1.x
```

**Se falhar:** 
- Verificar se Ollama está no PATH
- Reiniciar o terminal
- Reiniciar o Windows

---

## ⚙️ Configuração

### Passo 1: Baixar Modelo

```powershell
ollama pull llama2
```

Isso vai:
1. Conectar ao repositório de modelos
2. Baixar ~4GB de dados
3. Demorar 5-15min dependendo da internet

**Modelos alternativos:**
```powershell
ollama pull mistral        # Mais rápido, menor qualidade
ollama pull neural-chat    # Otimizado para chat
ollama pull dolphin-mixtral # Alta qualidade
```

### Passo 2: Iniciar Servidor Ollama

```powershell
ollama serve
```

Você deve ver:
```
time=2026-02-19T10:30:00.000Z level=INFO msg="Listening on..." addr=127.0.0.1:11434
```

**Manter esta janela aberta!** O servidor precisa rodar continuamente.

### Passo 3: Testar Localmente

Em **outro PowerShell**, teste:

```powershell
ollama list
```

Deve mostrar:
```
NAME        ID              SIZE    MODIFIED
llama2      xxxxx...       3.8 GB  2 minutes ago
```

Ou teste com uma pergunta:
```powershell
ollama run llama2 "O que é Ollama?"
```

---

## 🧪 Configurar para INFANT.ID

### Passo 1: Verificar .env

Arquivo: `backend/.env`

Verifique se tem:
```env
USE_OLLAMA=true
USE_MOCK_AI=false
OPENAI_MODEL=llama2
```

### Passo 2: Testar Integração com Backend

Com Ollama rodando, execute no backend:

```powershell
cd backend
python -c "
from app.services.ai_service import AiService
service = AiService()
resposta, tokens = service.responder_pergunta('Olá! Como você funciona?')
print('✅ SUCESSO!')
print(f'Resposta: {resposta[:100]}...')
"
```

**Esperado:** Resposta da IA em português

**Se der erro:** Ver [Troubleshooting](#troubleshooting)

### Passo 3: Teste de Integração Completo

```powershell
cd backend
python test_ollama.py
```

Deve testar:
- ✅ Ollama acessível em localhost:11434
- ✅ Modelo llama2 carregado
- ✅ Chat básico funcionando
- ✅ Custo de tokens 0 (teste offline)

---

## 📊 Teste em Tempo Real

### Via API REST (próprio Ollama)

```powershell
$body = @{
    "model" = "llama2"
    "messages" = @(
        @{ "role" = "user"; "content" = "Olá, como você funciona?" }
    )
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:11434/api/chat" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Via Nossa Aplicação

1. Inicie o servidor Flask:
```powershell
cd backend
python run.py
```

2. Faça uma requisição POST em outra aba:
```powershell
$body = @{
    "pergunta" = "Qual é o protocolo de coleta biométrica?"
    "usuario_id" = 1
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/ia/consult" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

**Esperado:** JSON com a resposta da IA

---

## 🔍 Troubleshooting

### Problema: "Ollama command not found"
**Solução:**
1. Ollama pode não estar no PATH
2. Reinicie o Windows após instalar
3. Ou use caminho completo: `C:\Users\[seu_usuário]\AppData\Local\Programs\Ollama\ollama.exe`

### Problema: "Connection refused" ao conectar
**Solução:**
```powershell
# Verificar se Ollama está rodando
netstat -ano | findstr :11434

# Se não estiver, inicie:
ollama serve
```

### Problema: Download do modelo falha
**Solução:**
```powershell
# Cancelar download anterior (Ctrl+C)
# Limpar cache
ollama rm llama2

# Tentar novamente
ollama pull llama2
```

### Problema: Resposta muito lenta
**Solução:**
1. GPU desabilitada - Verifique drivers NVIDIA
2. Modelo grande - Tente `mistral` (menor)
3. Falta de RAM - Feche outros programas

### Problema: "Modelo não encontrado"
**Solução:**
```powershell
# Verificar modelos disponíveis
ollama list

# Se vazio, baixar modelo
ollama pull llama2

# Verificar modelo no .env
# OPENAI_MODEL=llama2 (ou qual você usou)
```

---

## ⚙️ Alternativas

### Opção 1: OpenAI (Padrão)
```env
USE_OLLAMA=false
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-3.5-turbo
```

**Vantagens:** Qualidade superior, funciona via API  
**Desvantagens:** Custoso, não é offline

### Opção 2: Mock (Demo Mode)
```env
USE_MOCK_AI=true
```

**Vantagens:** Sem configuração, funciona sempre  
**Desvantagens:** Respostas falsas

### Opção 3: Híbrido (Recomendado)
```env
USE_OLLAMA=true           # Tenta Ollama primeiro
OPENAI_API_KEY=sk-proj-...  # Fallback para OpenAI
USE_MOCK_AI=false         # Último recurso é mock
```

O sistema tenta:
1. Ollama (local, grátis)
2. OpenAI (remoto, pago)
3. Mock (demo)

---

## 📱 Endpoints da API

### Consultar IA
```http
POST /api/ia/consult
Content-Type: application/json

{
    "pergunta": "Como usar o sistema?",
    "usuario_id": 1,
    "curso_id": 1
}
```

**Resposta:**
```json
{
    "id": 123,
    "pergunta": "Como usar o sistema?",
    "resposta": "Para usar...",
    "tokens": 150
}
```

### Histórico de Conversas
```http
GET /api/ia/historico/1?page=1&per_page=20
```

### Avaliar Resposta
```http
PUT /api/ia/avaliar/123
Content-Type: application/json

{
    "avaliacao": 5
}
```

---

## 🎯 Modelos Recomendados

| Modelo | Tamanho | Velocidade | Qualidade | Ideal para |
|--------|---------|-----------|-----------|-----------|
| mistral | 5GB | ⚡⚡⚡ | ⭐⭐⭐ | Desenvolvimento |
| llama2 | 4GB | ⚡⚡ | ⭐⭐⭐⭐ | Produção |
| neural-chat | 4GB | ⚡⚡ | ⭐⭐⭐⭐ | Chat |
| dolphin-mixtral | 26GB | ⚡ | ⭐⭐⭐⭐⭐ | Máxima qualidade |

---

## 📊 Monitoramento

### Verificar Uso de Recursos
```powershell
# Listar processos Ollama
Get-Process ollama

# Ver modelos carregados
ollama list
```

### Logs
```powershell
# Ver logs do servidor Ollama
# (São exibidos na janela do terminal onde ollama serve roda)
```

---

## 🚀 Performance Tips

1. **Use GPU:** Instale drivers NVIDIA/AMD para acelerar
2. **Modelo Menor:** Use `mistral` para respostas mais rápidas
3. **Keepalive:** Ative keepalive no servidor Ollama
4. **Cache:** Ollama cacheia automaticamente modelos já usados

---

## ✅ Checklist Final

- [ ] Ollama instalado (`ollama --version` funciona)
- [ ] Servidor Ollama rodando (`ollama serve`)
- [ ] Modelo baixado (`ollama list` mostra llama2)
- [ ] .env configurado com `USE_OLLAMA=true`
- [ ] Teste do backend passou
- [ ] API respondendo em http://localhost:11434/v1
- [ ] Chat de IA funcionando no frontend

---

## 📞 Precisando de Ajuda?

1. Verifique [Troubleshooting](#troubleshooting)
2. Rode [testes](#-teste-em-tempo-real)
3. Veja [docs/OLLAMA_CHECKLIST.md](OLLAMA_CHECKLIST.md)
4. Consulte https://ollama.ai/docs

---

**Desenvolvido para INFANT.ID - Alura Jovem Believer**
