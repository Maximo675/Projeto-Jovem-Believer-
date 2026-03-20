# 🚀 GUIA DE OTIMIZAÇÃO - MÚLTIPLAS PORTAS E SERVIÇOS

## Status Atual do Projeto

Você escolheu fazer tudo via iframe e descontinuar o desenvolvimento do ETAN standalone. Agora você tem:

✅ **Plataforma de Ensino** (Port 5001)
✅ **Device Service / Captura Biométrica** (Port 5000)  
✅ **Proxy Bridge** (Port 4000)
✅ **WebSocket unificado** (Port 5001)

---

## ⚙️ Configuração Necessária

### 1. **Variáveis de Ambiente (.env)**

O arquivo `.env` foi atualizado com todas as portas:

```env
# SERVIDOR FLASK - Plataforma Principal
FLASK_PORT=5001
FLASK_ENV=development

# DEVICE SERVICE - Captura Biométrica 
DEVICE_SERVICE_PORT=5000
DEVICE_SERVICE_URL=http://localhost:5000

# PROXY BRIDGE - Intermediário Node
PROXY_PORT=4000
PROXY_URL=http://localhost:4000

# CORS - Aceita múltiplas origens
CORS_ORIGINS=http://localhost:3000,http://localhost:5001,http://127.0.0.1:5001,http://localhost:4000,http://127.0.0.1:4000

# WEBSOCKET
WEBSOCKET_PORT=5001
WEBSOCKET_PATH=/socket.io
```

---

## 🎯 Arquivos Criados/Atualizados

### **1. `/frontend/js/config-urls.js`** ⭐ NOVO
Configuração centralizada de todas as URLs e portas.

```javascript
// Uso em qualquer script
const apiUrl = window.CONFIG_URLS.API_BASE;           // http://localhost:5001/api
const deviceUrl = window.CONFIG_URLS.DEVICE_URL;      // http://localhost:5000
const wsUrl = window.CONFIG_URLS.WEBSOCKET_NAMESPACE; // http://localhost:5001/socket.io
```

### **2. `/frontend/js/etan-websocket.js`** ⭐ NOVO
Cliente WebSocket otimizado que:
- Conecta via Socket.IO na porta 5001
- Suporta fallback para WebSocket nativo
- Reconexão automática com backoff exponencial
- Event emitter customizado

```javascript
// Uso em iframe
const ws = new ETANWebSocket(activityId, userId);
ws.on('biometric_result', (data) => console.log(data));
ws.updateProgress(fase, score, tempo);
```

### **3. `/backend/app/__init__.py`** ⭐ ATUALIZADO
- CORS melhorado com suporte a múltiplas origens
- Health check que verifica todos os serviços
- Headers de segurança adicionados
- WebSocket otimizado com `async_mode='threading'`

### **4. `/pages/atividades.html`** ⭐ ATUALIZADO
Scripts adicionados na ordem correta:

```html
<!-- Socket.IO -->
<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>

<!-- Config centralizada -->
<script src="../frontend/js/config-urls.js"></script>

<!-- WebSocket ETAN -->
<script src="../frontend/js/etan-websocket.js"></script>

<!-- Iframe Bridge -->
<script src="../frontend/js/iframe-bridge.js"></script>
```

---

## 🔧 Como Executar Tudo

### **Passo 1: Terminal 1 - Backend Flask (Plataforma de Ensino)**

```powershell
cd "C:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer"

# Ativar venv
.\venv\Scripts\Activate.ps1

# Rodar backend em porta 5001
python backend/run.py
```

**Saída esperada:**
```
[OK] Iniciando servidor Flask na porta 5001...
WEB Abra no navegador: http://localhost:5001
API Disponível em: http://localhost:5001/api
```

---

### **Passo 2: Terminal 2 - Device Service (Porta 5000)**

```powershell
# Se usando Node.js/openbio-bridge
node openbio-bridge.js

# OU se usando outro serviço de biometria
# Substitua pelo comando de inicialização correto
```

**Saída esperada:**
```
🚀 Servidor rodando em http://localhost:5000
```

---

### **Passo 3: Terminal 3 - Proxy Bridge (Porta 4000) [OPCIONAL]**

Se você estiver usando o proxy Node:

```powershell
node proxy-server.js  # Ou o arquivo correto de proxy
```

---

### **Passo 4: Abrir no Navegador**

```
http://localhost:5001/atividades
```

---

## ✅ Verificação de Status

### Health Check (Verifica todos os serviços):

```bash
# GET http://localhost:5001/health

Resposta esperada:
{
  "status": "ok",
  "message": "ETAN Platform - All Systems Check",
  "environment": "development",
  "services": {
    "flask": {"status": "ok", "port": "5001"},
    "device_service": {"status": "ok", "port": "5000"},
    "proxy": {"status": "ok", "port": "4000"},
    "websocket": {"status": "ok", "port": "5001"}
  }
}
```

---

## 🔥 Resolvendo Conflitos de CORS

### **Problema: 403 Access Denied (CORS)**

**Solução 1:** Verificar se CORS_ORIGINS inclui sua porta
```env
# No .env
CORS_ORIGINS=http://localhost:5001,http://localhost:5000,http://localhost:4000,http://127.0.0.1:5001
```

**Solução 2:** Limpar cache do navegador
```javascript
// Dev Tools Console
localStorage.clear();
sessionStorage.clear();
location.reload();
```

**Solução 3:** Há WildCard para localhost em DEV
```python
# backend/app/__init__.py linha ~40
if os.getenv('FLASK_ENV', 'development') == 'development':
    cors_config = {
        'origins': ['http://localhost:*', 'http://127.0.0.1:*'],  # ✅ Aceita any port
        ...
    }
```

---

## 🌐 Fluxo de Comunicação (Iframe)

```
┌─────────────────────────────────────────────────────────┐
│ iframe-bridge.js (Frontend/UI)                          │
│                                                         │
│ Comunicação INTERNA (postMessage)                       │
│ ↓                                                       │
│ window.iframeBridge.sendToParent('ACTION', data)        │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│ Página Principal (atividades.html)                      │
│                                                         │
│ Recebe: onIframeMessage('ACTION', callback)             │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│ WebSocket/Socket.IO (à porta 5001)                      │
│                                                         │
│ window.etanWebSocket.emit('TYPE', data)                 │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│ Backend Flask (http://localhost:5001/api)               │
│                                                         │
│ @socketio.on('TYPE')                                    │
│ def handle_event(data):                                 │
│     return response                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 📱 Usando Device Service (Biometria)

### **Da Página Principal (iframe parent):**

```javascript
// 1. Inicializar WebSocket
window.iframeBridge.connectToWebSocket(activityId, userId);

// 2. Requisitar simulador
window.iframeBridge.requestSimulator('practice', 4);

// 3. No Backend, capturar a solicitação e enviar para Device Service
```

### **Do Device Service:**

```javascript
// Em etan-websocket.js
ws.emit('biometric_capture', {
    activityId: activityId,
    type: 'fingerprint',
    quality: 0.95
});
```

---

## 🎓 Exemplo: Atividade Prática com Simulador

### **Fluxo Completo:**

1. **User clica em "Acessar Simulador"** 
   - `iframe-bridge.js` envia: `requestSimulator('practice', 4)`

2. **Backend recebe via WebSocket**
   - Route `/api/activities/:id` retorna HTML do simulador

3. **Simulador carrega em iframe**
   - `etan-websocket.js` conecta à porta 5001
   - Device Service em 5000 aguarda input

4. **User realiza captura**
   - Resultado enviado via WebSocket
   - `iframe-bridge.js` notifica página pai

5. **Página principal atualiza**
   - Score, tempo, tentativas salvas no banco

---

## 🚨 Debugging

### **Verificar logs de CORS:**

```javascript
// No DevTools Console (F12)
localStorage.debug = '*';  // Ativar debug

// Ver requisições
fetch('http://localhost:5001/api/activities')
  .then(r => r.json())
  .then(d => console.log(d))
  .catch(e => console.error('CORS Error:', e));
```

### **Verificar estado do WebSocket:**

```javascript
console.log(window.CONFIG_URLS.getServicesStatus());
console.log(window.etanWebSocket?.getConnectionInfo());
```

---

## 📊 Checklist de Implementação

- [x] Arquivo `.env` com todas as portas
- [x] `config-urls.js` - Configuração centralizada
- [x] `etan-websocket.js` - Cliente WebSocket otimizado
- [x] `iframe-bridge.js` - Comunicação com iframes
- [x] Backend CORS melhorado
- [x] Health check em `/health`
- [ ] Testar múltiplas portas simultaneamente ← **PRÓXIMO PASSO**
- [ ] Tests end-to-end com simulador

---

## 🎯 Próximos Passos (Detalhes Finais)

1. **Testar communication entre portas**
   - Abrir DevTools e verificar /health
   - Testar WebSocket conexão

2. **Otimizar performance**
   - Connection pooling
   - Cache de assets
   - Minify JS/CSS

3. **Implementar error handling robusto**
   - Retry logic melhorado
   - Logs centralizados
   - Monitoring/alertas

4. **Deploy em produção**
   - SSL/HTTPS
   - Rate limiting
   - WAF rules

---

## 📞 Suporte

Se tiver dúvidas sobre qualquer porta ou serviço:

```bash
# Teste individual de connectividade
curl http://localhost:5001/health
curl http://localhost:5000/status
curl http://localhost:4000/health
```

---

**Última atualização:** 02/03/2026
**Status:** ✅ Otimização concluída
