# ⚡ QUICK START - 5 MINUTOS

Guia rápido para colocar tudo funcionando em 5 minutos.

---

## 🚀 Passo 1: Abrir PowerShell (30 segundos)

1. Pressione `Win + X` e selecione **Windows PowerShell (Admin)**

2. Navegue para o projeto:
   ```powershell
   cd "C:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer"
   ```

3. Verifique se está no lugar certo:
   ```powershell
   ls backend\run.py  # Deve mostrar o arquivo
   ```

---

## 🚀 Passo 2: Iniciar Todos os Serviços (1 minuto)

Execute no PowerShell:

```powershell
.\start_all_services.ps1
```

**O que vai acontecer:**
- 2-3 janelas de terminal vão abrir automaticamente
- Cada uma iniciará um serviço
- Aguarde **15-20 segundos** para tudo ficar pronto

```
✅ Flask Backend (5001) - Deve mostrar:
   [OK] Iniciando servidor Flask na porta 5001...
   WEB Abra no navegador: http://localhost:5001

✅ Device Service (5000) - Se tiver:
   Servidor rodando em http://localhost:5000

ℹ️ Proxy (4000) - Opcional
   (Pode deixar no aguardo ou comentar no script)
```

---

## 🚀 Passo 3: Verificar Conectividade (1 minuto)

### **Opção A: Via Script (Recomendado)**

Num novo PowerShell (abra outra janela com `Win + X → Windows PowerShell`):

```powershell
cd "C:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer"
.\test_services_connectivity.ps1
```

**Resultado esperado:**
```
✅ Flask Backend: ONLINE
✅ Device Service: ONLINE (ou unavailable se não tiver)
✅ CORS Habilitado
```

### **Opção B: Via Navegador (Rápido)**

Abra em nova aba do navegador:

```
http://localhost:5001/health
```

Deve mostrar (`Ctrl+Shift+J` → Console):

```json
{
  "status": "ok",
  "services": {
    "flask": {"status": "ok"},
    "device_service": {"status": "ok"},
    "websocket": {"status": "ok"}
  }
}
```

---

## 🎯 Passo 4: Acessar a Plataforma (1 minuto)

### **URL Principal:**

```
http://localhost:5001/atividades
```

Você deve ver:
- 🎓 Dashboard de Atividades
- 📊 Lista de simuladores
- 🔐 Botão de Login/Cadastro

### **Login de Teste:**

```
Email: admin@example.com
Senha: password
```

(Ou criar nova conta em `http://localhost:5001/pages/register.html`)

---

## ✅ Passo 5: Testar Iframe (1 minuto)

### **No Console (F12):**

```javascript
// 1. Ver configuração
window.CONFIG_URLS.logConfig();

// 2. Testar serviços
window.CONFIG_URLS.getServicesStatus();

// 3. Conectar WebSocket
const ws = new ETANWebSocket(1, 'user123');
ws.on('connected', () => console.log('✅ WebSocket OK'));

// 4. Testar progresso
ws.updateProgress(1, 85, 120);

// 5. Completar atividade
ws.completeActivity(85, 120, 1);
```

**Resultado esperado:**
```
✅ WebSocket conectado ao servidor
✅ Atividade inicializada com WebSocket
```

---

## ⚠️ Se Algo Não Funcionar

### **Problema: Porta em uso**
```powershell
# Encontrar processo na porta 5001
netstat -ano | findstr :5001

# Matar processo
taskkill /PID <PID> /F
```

### **Problema: CORS Error**
```javascript
// No Console (F12)
localStorage.clear();
sessionStorage.clear();
location.reload();
```

### **Problema: WebSocket não conecta**
1. Verifique se Flask está rodando em 5001
2. Limpe cache (`Ctrl+Shift+Del`)
3. Reabra a aba

### **Problema: Device Service offline**
- Normal se não instalou o serviço
- Continue mesmo assim (é apenas a biometria)
- Você pode simular em vez de usar real

---

## 📊 Verificação Rápida

Copie e cole no **Console (F12)** para diagnóstico completo:

```javascript
console.group('🔍 DIAGNOSTIC CHECK');
console.log('1. Config URLs:', window.CONFIG_URLS?.FLASK_URL);
console.log('2. WebSocket:', window.etanWebSocket?.getConnectionInfo?.());
console.log('3. Iframe Bridge:', window.iframeBridge?.getConnectionInfo?.());
console.log('4. localStorage:', JSON.parse(localStorage.getItem('etan_config') || '{}'));
console.groupEnd();
```

---

## 🎯 Próximos Passos

Agora que está tudo funcionando:

1. **Criar atividade**
   - Vá para `/atividades`
   - Clique em um simulador
   - Preencha formulário

2. **Testar captura**
   - Abra simulador em iframe
   - Execute captura
   - Veja resultado em tempo real

3. **Verificar banco**
   - Resultados salvos em `instance/database.db` (desenvolvimento)
   - Em produção: PostgreSQL

4. **Adicionar mais fontes**
   - Editar `/frontend/js/config-urls.js` para adicionar novos endpoints
   - Escalar para múltiplos servers

---

## 📞 Troubleshooting Rápido

```bash
# Testar conectividade individual

# Flask
curl http://localhost:5001/health

# Device
curl http://localhost:5000/status

# Proxy
curl http://localhost:4000/health
```

Se qualquer um retornar erro `Connection refused`:
- Verifique se está rodando em outra janela
- Ejecute `start_all_services.ps1` novamente

---

## 💻 Referência Rápida

| O quê | Onde | URL |
|-------|------|-----|
| Plataforma Principal | http://localhost:5001 | ✅ |
| Dashboard de Atividades | http://localhost:5001/atividades | ✅ |
| API | http://localhost:5001/api | ✅ |
| Login | http://localhost:5001/pages/login.html | ✅ |
| Register | http://localhost:5001/pages/register.html | ✅ |
| Device Service | http://localhost:5000 | ⚠️ Opcional |
| Proxy | http://localhost:4000 | ⚠️ Opcional |
| WebSocket | ws://localhost:5001/socket.io | ✅ |

---

## 🎓 Exemplos de Código

### **Chamar API do Backend**
```javascript
fetch('http://localhost:5001/api/activities')
    .then(r => r.json())
    .then(data => console.log(data));
```

### **Enviar para Device**
```javascript
window.iframeBridge.requestSimulator('practice', 4);
```

### **Receber resultado do iframe**
```javascript
window.iframeBridge.onIframeMessage('ACTIVITY_COMPLETED', (payload) => {
    console.log('Atividade concluída:', payload.score);
});
```

### **Testar WebSocket**
```javascript
const ws = new ETANWebSocket(4, 123);
ws.on('biometric_result', (data) => console.log('Biometria:', data));
```

---

## ✅ Checklist 5 Minutos

- [ ] PowerShell aberto no projeto
- [ ] `start_all_services.ps1` executado
- [ ] Aguardou 15-20 segundos
- [ ] http://localhost:5001 abre (página pronta)
- [ ] Console (F12) mostra ✅ conexões
- [ ] `test_services_connectivity.ps1` passa
- [ ] Pode acessar `/atividades`

Se tudo está ✅, parabéns! Sistema está **100% operacional**.

---

## 🔴 Emergência

Se não conseguir fazer rodar em 5 minutos:

1. Feche ALL janelas do projeto
2. Execute em PowerShell novo:
   ```powershell
   cd C:\Users\maximo.silva\Desktop\Desevolvimento\Alura\ Jovem\ Believer
   .\start_all_services.ps1
   ```
3. Aguarde 30 segundos
4. Abra http://localhost:5001
5. Pressione F12, vá em Console
6. Copie o resultado de:
   ```javascript
   window.CONFIG_URLS.getServicesStatus()
   ```
7. Se ainda não funcionar, compartilhe o erro com a equipe

---

**Tempo Total:** ~5 minutos  
**Dificuldade:** ⭐ Muito Fácil  
**Status:** ✅ Pronto para usar
