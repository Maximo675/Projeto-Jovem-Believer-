# 🚀 Quick Start - Testes de Autenticação OpenBio (5 minutos)

## ✅ Pré-requisitos

- [ ] Python 3.8+ instalado
- [ ] Node.js 14+ instalado  
- [ ] OpenBio instalado em `C:\Openbio`
- [ ] Certificado HTTPS em `cert.pem` e `key.pem` (ou será gerado automaticamente)

---

## 🎯 Iniciar Tudo em 3 Passos

### Passo 1: Backend Python (Terminal 1)

```bash
# Entrar na pasta backend
cd backend

# Ativar ambiente virtual (se existir)
# Windows:
venv\Scripts\activate
# ou Mac/Linux:
# source venv/bin/activate

# Instalar dependências (primeira vez)
pip install -r requirements.txt

# Iniciar servidor
python run.py
```

**Esperado:**
```
✅ Flask rodando em http://localhost:5001
✅ Database conectado
✅ Aguardando requisições...
```

---

### Passo 2: OpenBio Principal (Terminal 2)

```bash
# Entrar na pasta do OpenBio
cd C:\Openbio

# Iniciar o servidor principal
# (Não precisa iniciar devices e API separadamente conforme sua informação)

node start.js
# ou
npm start
# ou dependendo da versão
java -jar openbio-server.jar
```

**Esperado:**
```
✅ OpenBio rodando em http://localhost:5000
✅ Serviços biométricos inicializados
✅ Aguardando conexões...
```

---

### Passo 3: OpenBio Bridge (Terminal 3)

```bash
# Na raiz do projeto (mesmo nível de openbio-bridge.js)
cd "c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer"

# Iniciar proxy HTTPS
node openbio-bridge.js
```

**Esperado:**
```
✅ Certificado encontrado (ou gerado novo)
✅ Servidor rodando em https://localhost:3333
✅ Endpoints disponíveis:
   🔐 POST /api/auth/login
   🔐 POST /api/auth/logout
   POST /api/fingerprint/capture
   ...
```

---

## 🧪 Teste Completo (3 minutos)

### 1. Abrir Dashboard

```
http://localhost:5001
```

### 2. Fazer Login

```
Email: seu_email@example.com
Senha: sua_senha
```

**Log esperado no console (F12):**
```
✅ [IframeExternalBridge] Pronto para comunicação
💡 Use IframeBridgeAPI.getAuthStatus() para verificar autenticação
```

### 3. Verificar Autenticação no Console (F12)

```javascript
// Copiar e colar no console:
IframeBridgeAPI.getAuthStatus()
```

**Resposta esperada:**
```javascript
{
  dashboardAuthenticated: true,
  openbioAuthenticated: false,  // Ainda não conectou
  user: {
    usuario_id: 123,
    email: "seu_email@example.com",
    nome: "Seu Nome"
  },
  sessionId: null
}
```

### 4. Conectar ao OpenBio

```javascript
// No console:
await IframeBridgeAPI.authenticateOpenbio()
```

**Resposta esperada:**
```javascript
true
```

**Log esperado:**
```
🔐 [OpenBio Auth] Autenticando usuário: seu_email@example.com
✅ [OpenBio Auth] Autenticado com sessão: session_123_1234567890
```

### 5. Verificar Status Novamente

```javascript
// No console:
IframeBridgeAPI.getAuthStatus()
```

**Resposta esperada:**
```javascript
{
  dashboardAuthenticated: true,
  openbioAuthenticated: true,    // ✅ Conectado!
  user: { ... },
  sessionId: "session_123_1234567890"
}
```

### 6. Fazer Logout (Opcional)

```javascript
// No console:
await IframeBridgeAPI.logout()
```

**Log esperado:**
```
🔓 [OpenBio] Sessão encerrada
```

---

## 🎨 Usar a Página de Atividade (Visualmente)

Se preferir interface gráfica em vez de console:

1. Abrir: `http://localhost:5001/pages/atividade_1_captura_biometrica.html`
2. Clicar em "Conectar OpenBio"  (ou "Capturar Digital" se já conectado)
3. Acompanhar logs em tempo real na página

---

## 🔍 Verificação de Conectividade

Se algo não funcionar, fazer estes testes no console:

### Testar Backend (5001)
```javascript
fetch('http://localhost:5001/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        email: 'test@example.com',
        senha: 'test123'
    })
})
.then(r => r.json())
.then(d => console.log('✅ Backend respondendo:', d))
.catch(e => console.error('❌ Backend offline:', e))
```

### Testar OpenBio (5000)
```javascript
fetch('http://localhost:5000/health')
    .then(r => r.json())
    .then(d => console.log('✅ OpenBio respondendo:', d))
    .catch(e => console.error('❌ OpenBio offline:', e))
```

### Testar Bridge (3333)
```javascript
fetch('https://localhost:3333/health', {
    method: 'GET'
})
.then(r => r.json())
.then(d => console.log('✅ Bridge respondendo:', d))
.catch(e => console.error('❌ Bridge offline ou cert inválido:', e))
```

> **Nota**: Bridge retorna erro de certificado no browser (normal, é auto-assinado)

---

## ⚠️ Troubleshooting Rápido

| Erro | Solução |
|------|---------|
| "Backend offline" | Verificar se `python run.py` está rodando |
| "OpenBio offline" | Verificar se OpenBio está rodando em localhost:5000 |
| "Bridge offline" | Verificar se `node openbio-bridge.js` está rodando |
| "Usuário não autenticado" | Fazer login no dashboard primeiro |
| "CORS error" | Bridge está recebendo requisição direto, usar certificado |
| "X-Session-ID undefined" | Recarregar página, JWT pode ter expirado |
| Certificado inválido | Deletar `cert.pem` e `key.pem` para regerar |

---

## 📝 Checklist Final

- [ ] Terminal 1: Backend Python VERDE (http://localhost:5001)
- [ ] Terminal 2: OpenBio VERDE (http://localhost:5000)
- [ ] Terminal 3: Bridge Node VERDE (https://localhost:3333)
- [ ] Login no dashboard ✅
- [ ] Console: `IframeBridgeAPI.getAuthStatus()` retorna `openbioAuthenticated: true` ✅
- [ ] Página de atividade carrega sem erro ✅
- [ ] Botão "Capturar Digital" está ativado ✅

**Se tudo estiver verde ✅ → Sistema está pronto para usar!**

---

## 🎓 Próximas Ações

1. ✅ **Testar captura real** de digital (se scanner conectado)
2. ✅ **Validar registro** no banco de dados com `user_email` e `user_id`
3. ✅ **Testar com múltiplos usuários** para garantir isolamento
4. ✅ **Completar atividade** do dashboard com captura funcionando

---

## 📚 Referências Rápidas

- Documentação detalhada: [GUIA_AUTENTICACAO_OPENBIO.md](./GUIA_AUTENTICACAO_OPENBIO.md)
- Resumo de implementação: [RESUMO_AUTENTICACAO_OPENBIO.md](./RESUMO_AUTENTICACAO_OPENBIO.md)
- Página de atividade: [pages/atividade_1_captura_biometrica.html](./pages/atividade_1_captura_biometrica.html)
- Bridge server: [openbio-bridge.js](./openbio-bridge.js) (linhas 395+ para auth)
- Cliente frontend: [frontend/js/iframe-external-bridge.js](./frontend/js/iframe-external-bridge.js)

---

## 💬 Perguntas/Problemas?

Se surgir algo inesperado:

1. Verificar logs dos 3 terminais
2. Abrir F12 no navegador (Console e Network)
3. Procurar por `🔐` (autenticação) ou `❌` (erros) nos logs
4. Fazer print de erro e procurar solução em [GUIA_AUTENTICACAO_OPENBIO.md](./GUIA_AUTENTICACAO_OPENBIO.md)

**Status**: ✅ Tudo pronto para teste!
**Tempo estimado**: 5-10 minutos completos

