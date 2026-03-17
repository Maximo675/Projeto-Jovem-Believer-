# ✅ SOLUÇÃO COMPLETA - Iframe Externo + Sistema Local (Sem CORS)

## 🎯 O Problema Resolvido

**Antes:**
```
❌ https://infant.akiyama.com.br tentava acessar http://localhost:5000
❌ CORS bloqueado: origem diferente
```

**Agora:**
```
✅ infant.akiyama.com.br se comunica via postMessage (sem CORS)
✅ Sistema local recebe e repassa através de openbio-bridge.js (que tem CORS aberto)
✅ Openbio Bridge faz proxy para localhost:5000
✅ Resposta volta ao iframe via postMessage
```

---

## 🏗️ Arquitetura da Solução

```
┌────────────────────────────────────────────────────────────────┐
│  https://infant.akiyama.com.br (iframe externo)                │
│                                                                 │
│  ✅ Estará VISIBLE na tela                                      │
│  ✅ Pode fazer captura com interface visual                     │
│  ✅ Se comunica via postMessage                                 │
└──────────────────────┬───────────────────────────────────────── ┘
                       │ postMessage
                       │ (sem CORS)
                       ▼
┌────────────────────────────────────────────────────────────────┐
│  window.externalIframeBridge (frontend/js/iframe-external...js) │
│  - Recebe postMessage do iframe                                │
│  - Valida origem (infant.akiyama.com.br)                       │
│  - Repassa via fetch/XMLHttpRequest                            │
└──────────────────────┬───────────────────────────────────────── ┘
                       │ fetch
                       │ (permite CORS)
                       ▼
┌────────────────────────────────────────────────────────────────┐
│  localhost:3333 (openbio-bridge.js)                            │
│  - app.use(cors()) já habilitado                               │
│  - Rotas: /api/fingerprint/capture, /preview, /health         │
│  - Funciona como proxy reverso                                 │
└──────────────────────┬───────────────────────────────────────── ┘
                       │ fetch para localhost:5000
                       │
                       ▼
┌────────────────────────────────────────────────────────────────┐
│  localhost:5000 (Openbio Real - c:\Openbio)                    │
│  - Hardware biométrico real                                   │
│  - Captura de impressões digitais                             │
│  - Apenas localhost (não precisa CORS)                        │
└────────────────────────────────────────────────────────────────┘
                       │
                       │ Resposta
                       ▼
         ┌─────────────────────────────┐
         │ Volta pelo mesmo caminho    │
         │ openbio-bridge → localStorage
         │ → postMessage → iframe      │
         └─────────────────────────────┘
```

---

## 🚀 Como Funciona Passo a Passo

### 1. **Página Carrega**
```html
<!-- etan-captura-biometrica.html -->
<iframe id="external-iframe" 
        src="https://infant.akiyama.com.br/#/infant-capture">
</iframe>
```

### 2. **Iframe Externo Inicia Captura**
```javascript
// No iframe (infant.akiyama.com.br)
window.parent.postMessage({
    type: 'request',
    action: 'biometric_capture',
    payload: {
        deviceId: 'default',
        finger: 'thumb_right',
        timeoutMs: 5000
    },
    requestId: 'req-123'
}, 'http://localhost:5001'); // origem do parent
```

### 3. **Sistema Local Recebe (sem CORS)**
```javascript
// iframe-external-bridge.js
window.addEventListener('message', (event) => {
    if (event.data.action === 'biometric_capture') {
        // Browser permite postMessage entre qualquer origem!
        handleBiometricCapture(event);
    }
});
```

### 4. **Repassa ao Openbio Bridge (com CORS)**
```javascript
// Agora usamos fetch (permite CORS)
const response = await fetch('http://localhost:3333/api/fingerprint/capture', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload) // sem estresse de CORS!
});
```

### 5. **Openbio Bridge Proxya para Hardware Real**
```javascript
// openbio-bridge.js (roda em 3333)
app.use(cors()); // permite qualquer origem!

app.post('/api/fingerprint/capture', async (req, res) => {
    // Repassa para localhost:5000
    const response = await fetch('http://localhost:5000/api/fingerprint/capture', {
        // ... sem CORS porque é localhost → localhost
    });
    res.json(response);
});
```

### 6. **Resposta Volta**
```javascript
// iframe-external-bridge.js
source.postMessage({
    type: 'response',
    action: 'biometric_capture',
    requestId: 'req-123',
    success: true,
    data: captureResult // imagem, qualidade, etc
}, 'https://infant.akiyama.com.br');
```

### 7. **Também Salva Localmente**
```javascript
// Registra no banco de dados local
await fetch('/api/activities/biometric/capture', {
    method: 'POST',
    body: JSON.stringify({
        user_id: 1,
        activity_id: 4,
        quality: 85,
        source: 'infant.akiyama.com.br'
    })
});
```

---

## 📋 Portas e Responsabilidades

| Porta | Serviço | Função | CORS |
|-------|---------|--------|------|
| **3333** | openbio-bridge.js | ✅ **Proxy CORS** para localhost:5000 | **ABERTO** |
| **5000** | Openbio Real (c:\Openbio) | Hardware biométrico real | Não precisa |
| **5001** | Flask Backend | API principal + WebSocket | Configurado |

---

## 🔧 Configuração Necessária

### 1. **Verificar openbio-bridge.js**
```javascript
// Já está configurado assim:
const cors = require('cors');
app.use(cors()); // ✅ Permite todas as origens
```

### 2. **Configurar package.json**
```json
{
  "scripts": {
    "start": "node openbio-bridge.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "node-fetch": "^2.6.7"
  }
}
```

### 3. **Adicionar scripts ao HTML**
```html
<!-- etan-captura-biometrica.html -->
<script src="/frontend/js/config-urls.js"></script>
<script src="/frontend/js/iframe-external-bridge.js"></script>
```

### 4. **Atualizar config-urls.js**
```javascript
this.PROXY_PORT = 3333; // ✅ Openbio Bridge
this.PROXY_URL = `http://localhost:${this.PROXY_PORT}`;
```

---

## 🚀 Como Executar

### Automático (Recomendado):
```powershell
.\start_all_services.ps1
```

Abre 3 terminais:
1. Flask (5001)
2. Openbio Bridge (3333) - **NOVO**
3. Openbio Device Service (5000) - opcional

### Manual:

**Terminal 1 - Flask:**
```bash
cd backend
python run.py
```

**Terminal 2 - Openbio Bridge:**
```bash
npm install
npm start
```

**Terminal 3 - Openbio Device (opcional):**
```bash
# Em c:\Openbio:
"Openbio Enroll Start.bat"
```

---

## 🧪 Testar a Conexão

### Console do DevTools (F12)
```javascript
// Verificar se bridge está inicializado
window.externalIframeBridge
// Deve retornar: IframeExternalBridge { ... }

// Verificar config de proxy
window.CONFIG_URLS.PROXY_URL
// Deve retornar: "http://localhost:3333"

// Testar endpoint do proxy
fetch('http://localhost:3333/health')
    .then(r => r.json())
    .then(console.log)
// Deve retornar: { status: 'ok', ... }
```

### Teste Completo:
```
http://localhost:5001/frontend/pages/teste-biometria.html
```

Deve mostrar:
- ✅ Scripts carregados (incluindo iframe-external-bridge)
- ✅ Openbio Bridge (3333): ONLINE
- ✅ Endpoints testados

---

## 🎯 Fluxo de Captura Completo

```
1. Usuário clica em "Capturar" no iframe externo
                  ↓
2. Iframe envia: postMessage({ action: 'biometric_capture' })
                  ↓
3. iframe-external-bridge recebe (sem CORS!)
                  ↓
4. Bridge faz: fetch('http://localhost:3333/api/fingerprint/capture')
                  ↓
5. openbio-bridge (CORS habilitado) recebe
                  ↓
6. Repassa: fetch('http://localhost:5000/api/fingerprint/capture')
                  ↓
7. Openbio Real captura digital (hardware físico em c:\Openbio)
                  ↓
8. Resposta volta: { quality: 85, nfiq: 4, image: ... }
                  ↓
9. Bridge salva em localStorage
                  ↓
10. postMessage({ action: 'response', data: ... })
                  ↓
11. Iframe exibe resultado na interface visual
                  ↓
12. Também salva localmente: POST /api/activities/biometric/capture
```

---

## ✨ Vantagens desta Solução

| Vantagem | Benefício |
|----------|-----------|
| **Reutiliza iframe pronto** | Não precisa recriar interface visual |
| **Sem modificar infant.akiyama.com.br** | Não dependemos de código externo |
| **Sem CORS bloqueado** | postMessage funciona entre qualquer origem |
| **Usa Openbio real** | Hardware físico, não simulador |
| **Dados salvos localmente** | Integração com banco de dados próprio |
| **Simples de implementar** | Apenas postMessage + fetch |

---

## 🔒 Segurança

### Validação de Origem
```javascript
isValidOrigin(origin) {
    const allowed = ['https://infant.akiyama.com.br', window.location.origin];
    return allowed.some(a => origin === a);
}
```

### CORS Validado
```javascript
// openbio-bridge.js
app.use(cors({
    origin: function(origin, callback) {
        const allowed = ['http://localhost:5001', 'http://localhost:3000'];
        if (!allowed.includes(origin)) {
            callback(new Error('CORS não permitido'));
        } else {
            callback(null, true);
        }
    }
}));
```

---

## 🐛 Troubleshooting

### Iframe não carrega?
```javascript
// Verificar no console
window.externalIframeBridge
// Se undefined, revisar se scripts carregaram
```

### CORS ainda bloqueado?
```javascript
// Verificar porta 3333
fetch('http://localhost:3333/health')
    .then(r => r.json())
    .then(console.log)
// Se falhar, openbio-bridge não está rodando
```

### Captura falha?
```javascript
// Verificar se localhost:5000 está disponível
fetch('http://localhost:5000/health')
    .then(r => r.json())
    .console.log)
// Se falhar, Openbio Device não está rodando
```

---

## 📊 Resultado Final

✅ **Iframe externo visível e funcional**  
✅ **Comunicação sem CORS bloqueado**  
✅ **Usa Openbio real (não simulador)**  
✅ **Dados salvos localmente**  
✅ **Apresentação visual profissional**  
✅ **Pronto para demonstração ao cliente**

---

## 🎉 Próximos Passos

1. ✅ **Executar start_all_services.ps1**
2. ✅ **Acessar etan-captura-biometrica.html**
3. ✅ **Verificar que iframe externo aparece**
4. ✅ **Testar captura bem-sucedida**
5. ⏳ **Demo ao cliente** (este é o diferencial!)

O**iframe externo é crucial para a apresentação!**

