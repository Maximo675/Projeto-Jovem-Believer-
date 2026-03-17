# 🔐 Guia de Autenticação OpenBio - iframe-external-bridge.js

## 📋 Visão Geral

O arquivo `iframe-external-bridge.js` foi aprimorado para integrar **autenticação do dashboard** com o **OpenBio**. Agora:

1. ✅ Quando usuário faz login no dashboard, o token é armazenado
2. ✅ Antes de capturar biometria, verifica se usuário está autenticado
3. ✅ Faz autenticação automática com OpenBio
4. ✅ Passa informações do usuário para todas as requisições biométricas
5. ✅ Registra qual usuário fez cada captura

---

## 🔄 Fluxo de Autenticação

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUÁRIO FOCA LOGIN                       │
├─────────────────────────────────────────────────────────────────┤
│ 1. Faz login no dashboard                                       │
│ 2. Backend gera JWT e envia ao frontend                         │
│ 3. Frontend salva token em localStorage                         │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  USUÁRIO TENTA CAPTURAR BIOMETRIA              │
├─────────────────────────────────────────────────────────────────┤
│ 1. IframeExternalBridge recebe evento de captura                │
│ 2. Verifica se usuário do dashboard está autenticado            │
│    (Decodifica JWT do localStorage)                             │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
    ┌─ Autenticado? ─┐
    │      SIM       │
    └────────┬────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│           AUTENTICAR COM OPENBIO (Se necessário)               │
├─────────────────────────────────────────────────────────────────┤
│ 1. POST {proxyUrl}/api/auth/login com credenciais do usuário   │
│ 2. OpenBio retorna sessionId                                    │
│ 3. Armazena sessionId em this.openbioSessionId                  │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│              FAZER CAPTURA BIOMÉTRICA AUTENTICADA              │
├─────────────────────────────────────────────────────────────────┤
│ POST {proxyUrl}/api/fingerprint/capture com Headers:            │
│ - Authorization: Bearer {token}                                 │
│ - X-User-ID: {usuario_id}                                       │
│ - X-Session-ID: {sessionId}                                     │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│              SALVAR CAPTURA COM INFORMAÇÕES DE USUÁRIO         │
├─────────────────────────────────────────────────────────────────┤
│ POST /api/activities/biometric/capture com:                     │
│ - user_id                                                       │
│ - user_email                                                    │
│ - openbio_session_id                                            │
│ - timestamp                                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Como Usar (No Frontend)

### 1️⃣ Verificar Status de Autenticação

```javascript
// Em qualquer lugar do código
const status = IframeBridgeAPI.getAuthStatus();

if (status.dashboardAuthenticated) {
    console.log('✅ Usuário logado:', status.user.email);
    console.log('OpenBio autenticado?', status.openbioAuthenticated);
} else {
    console.log('❌ Usuário não logado - redirecionar para login');
}
```

### 2️⃣ Fazer Autenticação com OpenBio Explicitamente

```javascript
// Se precisar fazer login no OpenBio manualmente
const success = await IframeBridgeAPI.authenticateOpenbio();

if (success) {
    console.log('✅ OpenBio autenticado');
    console.log(IframeBridgeAPI.getAuthStatus());
} else {
    console.log('❌ Falha na autenticação');
}
```

### 3️⃣ Fazer Logout

```javascript
// Encerra sessão com OpenBio
await IframeBridgeAPI.logout();
```

---

## 🔧 Classes e Métodos Principais

### Classe: `IframeExternalBridge`

#### Propriedades
- `openbioSessionId`: ID da sessão com OpenBio
- `openbioUser`: Dados do usuário autenticado
- `isOpenbioAuthenticated`: Boolean indicando status

#### Métodos

##### `getCurrentUserData()`
Extrai informações do usuário do JWT armazenado em localStorage.

**Retorna:**
```javascript
{
    usuario_id: 123,
    email: "usuario@example.com",
    nome: "John Doe",
    funcao: "admin",
    exp: 1234567890
}
```

**Uso:**
```javascript
const user = window.externalIframeBridge.getCurrentUserData();
```

---

##### `authenticateWithOpenbio(userData)`
Faz login no OpenBio com credenciais do usuário autenticado.

**Parâmetros:**
- `userData` (Object): Dados do usuário retornados por `getCurrentUserData()`

**Retorna:** Boolean

**Uso:**
```javascript
const userData = window.externalIframeBridge.getCurrentUserData();
const success = await window.externalIframeBridge.authenticateWithOpenbio(userData);
```

---

##### `logoutFromOpenbio()`
Encerra sessão com OpenBio.

**Uso:**
```javascript
await window.externalIframeBridge.logoutFromOpenbio();
```

---

## 🗂️ URLs Esperadas pelo OpenBio

O sistema espera os seguintes endpoints na instância do OpenBio:

### 1. POST `/api/auth/login`
Autentica usuário e retorna sessionId

**Request:**
```json
{
    "email": "usuario@example.com",
    "usuario_id": 123,
    "nome": "John Doe",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
    "sessionId": "abc123xyz",
    "message": "Autenticação realizada"
}
```

---

### 2. POST `/api/fingerprint/capture`
Captura digital com autenticação

**Headers:**
```
Authorization: Bearer {token}
X-User-ID: {usuario_id}
X-Session-ID: {sessionId}
```

**Request Body:**
```json
{
    "user": {
        "id": 123,
        "email": "usuario@example.com",
        "name": "John Doe"
    },
    ...outrosCamposDeCaptura
}
```

---

### 3. POST `/api/auth/logout`
Encerra sessão

**Headers:**
```
X-Session-ID: {sessionId}
```

---

## 🚀 Configuração no Proxy (openbio-bridge)

Se você está usando o proxy `openbio-bridge`, certifique-se que os endpoints acima estão mapeados corretamente:

```javascript
// No openbio-bridge.js ou similar
app.post('/api/auth/login', async (req, res) => {
    // Repassa para OpenBio em localhost:5000
    // Ou autentica localmente
});

app.post('/api/fingerprint/capture', async (req, res) => {
    // Verifica X-Session-ID
    // Repassa para OpenBio
});
```

---

## ⚠️ Informações Importantes

### 1. JWT Decoding
O código decodifica o JWT localmente para extrair `usuario_id` e `email`. O JWT é esperado ter este formato:

```javascript
// Payload do JWT
{
    "usuario_id": 123,
    "email": "usuario@example.com",
    "nome": "John Doe",
    "funcao": "admin",
    "exp": 1234567890
}
```

### 2. Fallback de Autenticação
Se o OpenBio não responder ao endpoint `/api/auth/login`, a classe usa a `usuario_id` como `sessionId`. Isso permite que o sistema continue funcionando mesmo que o endpoint não exista.

### 3. localStorage Usado
- `authToken`: Token JWT do usuário logado no dashboard

### 4. Informações Passadas a Cada Captura
```javascript
{
    user_id: userData.usuario_id,
    user_email: userData.email,
    openbio_session_id: sessionId,
    timestamp: ISO8601
}
```

---

## 📝 Exemplo de Implementação Completa

### Dashboard HTML
```html
<button id="btn-biometric" onclick="captureBiometria()">
    Capturar Digital
</button>

<div id="iframe-container">
    <iframe id="external-iframe" 
            src="https://localhost:5000/capture" 
            width="100%" height="600px"></iframe>
</div>

<script src="config-urls.js"></script>
<script src="iframe-external-bridge.js"></script>

<script>
async function captureBiometria() {
    // Verificar autenticação
    const status = IframeBridgeAPI.getAuthStatus();
    
    if (!status.dashboardAuthenticated) {
        alert('❌ Faça login primeiro');
        return;
    }
    
    console.log('✅ Usuário autenticado:', status.user.email);
    
    // Aoopenbio será autenticado automaticamente na primeira captura
    // O handleBiometricCapture cuidará disso
    console.log('🔄 Enviando requisição de captura...');
}
</script>
```

---

## 🐛 Troubleshooting

### Problema: "Usuário não autenticado"
**Solução:** 
- Verificar se `localStorage.authToken` existe
- Verificar se token é válido (não expirado)
- Fazer novo login

### Problema: OpenBio retorna erro de autenticação
**Solução:**
- Verificar se endpoint `/api/auth/login` existe
- Verificar se OpenBio está com `"login": false` na configuração
- Usar fallback que usa `usuario_id` como `sessionId`

### Problema: CORS errors
**Solução:**
- Usar proxy (`openbio-bridge`) conforme implementado
- Verificar headers `X-User-ID` e `X-Session-ID` no proxy

---

## ✅ Checklist de Implementação

- [ ] `iframe-external-bridge.js` carregado no HTML
- [ ] `config-urls.js` carregado antes de `iframe-external-bridge.js`
- [ ] Backend tem rota `/api/auth/login` com JWT
- [ ] Frontend salva `authToken` em localStorage após login
- [ ] JWT contém campos: `usuario_id`, `email`, `nome`
- [ ] OpenBio tem endpoints `/api/auth/login` e `/api/fingerprint/capture`
- [ ] Proxy `openbio-bridge` está ativo em `https://localhost:3333`
- [ ] Testar `IframeBridgeAPI.getAuthStatus()` no console

---

## 📞 Suporte

Se encontrar problemas:

1. Verificar console do navegador (F12 → Console)
2. Procurar por logs com 🔐 (autenticação)
3. Verificar Network tab para ver requisições
4. Verificar se OpenBio está rodando em localhost:5000
5. Verificar se proxy está rodando em localhost:3333

