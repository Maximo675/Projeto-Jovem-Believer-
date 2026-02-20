# ✅ Checklist de Validação - Ollama Setup

**Projeto:** INFANT.ID  
**Data:** 19 de Fevereiro de 2026  
**Status:** Em Validação ✓

---

## 📋 Checklist de Instalação

### Pré-requisitos
- [ ] Windows 10/11 com PowerShell
- [ ] Python 3.9+ instalado
- [ ] Git instalado
- [ ] Conexão com internet (para download)

### Ollama
- [ ] Ollama instalado (`ollama --version` funciona)
- [ ] Ollama no PATH do Windows
- [ ] Servidor Ollama rodando (`ollama serve`)
- [ ] Modelo llama2 baixado (`ollama list` mostra llama2)
- [ ] Porta 11434 acessível (não bloqueada)

### Backend INFANT.ID
- [ ] Arquivo `.env` existe
- [ ] `USE_OLLAMA=true` configurado
- [ ] `USE_MOCK_AI=false` configurado
- [ ] `OPENAI_MODEL=llama2` configurado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)

### Frontend
- [ ] Página `pages/ia-chat.html` criada
- [ ] JavaScript `js/ia-chat.js` criado
- [ ] CSS `css/ia-chat.css` criado
- [ ] Arquivo `js/theme.js` integrado

### Documentação
- [ ] `docs/SETUP_OLLAMA.md` criado
- [ ] `backend/test_ollama.py` criado
- [ ] `docs/OLLAMA_CHECKLIST.md` criado

---

## 🧪 Checklist de Testes

### Teste 1: Ollama Servidor
```powershell
# Execute:
curl http://localhost:11434/api/tags

# Esperado: JSON com lista de modelos
```
- [ ] Resposta HTTP 200
- [ ] JSON contém "models"
- [ ] llama2 está na lista

### Teste 2: Ollama Chat
```powershell
# Execute:
ollama run llama2 "Olá, como você funciona?"

# Esperado: Resposta em português
```
- [ ] Modelo responde
- [ ] Resposta em português
- [ ] Resposta faz sentido

### Teste 3: Serviço de IA do Backend
```powershell
# No backend/:
python -c "
from app.services.ai_service import AiService
service = AiService()
resposta, tokens = service.responder_pergunta('Teste')
print('✅ OK' if resposta else '❌ FALHOU')
"

# Esperado: ✅ OK
```
- [ ] Sem erros de importação
- [ ] Modo é 'ollama'
- [ ] Resposta não vazia
- [ ] Tokens > 0

### Teste 4: Script de Teste Completo
```powershell
cd backend
python test_ollama.py

# Esperado: 6/6 testes passam
```
- [ ] Servidor Ollama rodando
- [ ] Modelos disponíveis
- [ ] Chat funciona
- [ ] Config .env OK
- [ ] AiService OK
- [ ] API respondendo

### Teste 5: API HTTP
```powershell
# Com Flask rodando em http://localhost:5000
$body = '{"pergunta":"Teste","usuario_id":null}' | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:5000/api/ia/consult" `
    -Method Post -ContentType "application/json" -Body $body

# Esperado: JSON com resposta
```
- [ ] Status 200
- [ ] JSON contém "resposta"
- [ ] Resposta não vazia
- [ ] "tokens" > 0

### Teste 6: Chat no Frontend
```
1. Abrir http://localhost:8000/pages/ia-chat.html
2. Digitar pergunta
3. Clicar em "Enviar"

Esperado: Resposta aparece em tempo real
```
- [ ] Página carrega sem erros
- [ ] Botões funcionam
- [ ] Resposta aparece
- [ ] Auto-scroll funciona

---

## 🔧 Checklist de Configuração

### Variáveis de Ambiente

**File:** `backend/.env`

```env
✅ FLASK_ENV=development
✅ FLASK_DEBUG=True
✅ USE_OLLAMA=true
✅ USE_MOCK_AI=false
✅ OPENAI_MODEL=llama2
✅ OPENAI_API_KEY=sk-proj-... (opcional, fallback)
```

Verifique:
- [ ] `USE_OLLAMA=true`
- [ ] `USE_MOCK_AI=false`
- [ ] `OPENAI_MODEL=llama2` (ou outro modelo baixado)
- [ ] `OPENAI_API_KEY` set (para fallback)

---

## 📁 Checklist de Arquivos

### Backend
```
backend/
├── .env                          ✅ Criado
├── app/
│   ├── services/
│   │   └── ai_service.py        ✅ Existente
│   └── routes/
│       └── ai.py                ✅ Existente
├── test_ollama.py               ✅ Criado
└── requirements.txt             ✅ Verificado
```

- [ ] `ai_service.py` tem suporte Ollama
- [ ] `ai.py` tem endpoint `/consult`
- [ ] `test_ollama.py` existe
- [ ] `requirements.txt` tem `openai>=1.0`

### Frontend
```
frontend/
├── pages/
│   └── ia-chat.html             ✅ Criado
├── js/
│   ├── main.js                  ✅ Existente
│   ├── theme.js                 ✅ Existente
│   └── ia-chat.js               ✅ Criado
└── css/
    ├── style.css                ✅ Existente
    └── ia-chat.css              ✅ Criado
```

- [ ] Todos os arquivos existem
- [ ] `ia-chat.html` referencia `ia-chat.js`
- [ ] `ia-chat.html` referencia `ia-chat.css`
- [ ] `js/theme.js` está incluído

### Documentação
```
docs/
├── SETUP_OLLAMA.md              ✅ Criado
└── OLLAMA_CHECKLIST.md          ✅ Criado
```

- [ ] `SETUP_OLLAMA.md` com guia completo
- [ ] `SETUP_OLLAMA.md` tem troubleshooting

---

## 🚀 Checklist de Operação

### Iniciar Ollama
- [ ] PowerShell 1: Iniciar servidor
  ```powershell
  ollama serve
  ```
  Esperado: "Listening on...":11434"

### Iniciar Backend
- [ ] PowerShell 2: Iniciar Flask
  ```powershell
  cd backend
  python run.py
  ```
  Esperado: "Running on http://localhost:5000"

### Iniciar Frontend
- [ ] PowerShell 3 (ou browser)
  ```powershell
  # Se usar servidor local
  cd frontend
  python -m http.server 8000
  ```
  Esperado: Servidor em http://localhost:8000

### Testar Fluxo Completo
- [ ] Abrir http://localhost:8000/pages/ia-chat.html
- [ ] Digitar: "Como funciona a coleta biométrica?"
- [ ] Clicar em "Enviar"
- [ ] Aguardar 5-30 segundos
- [ ] Resposta aparece no chat

---

## ⚠️ Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Ollama command not found | Reinstalar ou adicionar ao PATH|
| Connection refused :11434 | Executar `ollama serve` em outro terminal |
| No models available | Executar `ollama pull llama2` |
| Resposta lenta | Usar modelo menor (`mistral`) |
| Import error openai | `pip install openai>=1.0` |
| 404 /api/ia/consult | Verifique se rota está registrada em `app/routes/ai.py` |
| Chat não aparece | Verifique console (F12) para erros JS |

---

## 📊 Performance Esperada

| Operação | Tempo Esperado | Ideal |
|----------|----------------|-------|
| Primeiro request Ollama | 5-10s | < 3s |
| Requisição subsequente | 2-5s | < 2s |
| Resposta llama2 (completa) | 10-30s | < 10s |
| Resposta mistral (completa) | 5-15s | < 5s |

---

## ✅ Marcadores de Conclusão

Quando cada seção estiver OK, marque:

```
✅ Instalação Completa
✅ Testes Passando
✅ Configuração OK
✅ Arquivos Criados
✅ Operação Normal
```

---

## 📋 Próximos Passos

1. **Após passar em TODOS os testes:**
   - [ ] Documentar modelos disponíveis
   - [ ] Criar backup da configuração
   - [ ] Configurar logging
   - [ ] Otimizar prompts

2. **Para produção:**
   - [ ] Usar PostgreSQL em vez de SQLite
   - [ ] Configurar CORS corretamente
   - [ ] Usar HTTPS
   - [ ] Configurar rate limiting
   - [ ] Adicionar autenticação de API

3. **Melhorias futuras:**
   - [ ] Cache de respostas frequentes
   - [ ] Análise de sentimento
   - [ ] Histórico persistente no banco
   - [ ] Suporte a múltiplos idiomas
   - [ ] Fine-tuning de modelo

---

## 📞 Contato/Suporte

Se encontrar problemas:

1. Verifique o arquivo `docs/SETUP_OLLAMA.md`
2. Rode `backend/test_ollama.py`
3. Verifique console (F12) no navegador
4. Veja logs do Ollama (terminal onde roda `ollama serve`)

---

**Última verificação:** 19/02/2026  
**Status:** ✅ Pronto para Implementação
