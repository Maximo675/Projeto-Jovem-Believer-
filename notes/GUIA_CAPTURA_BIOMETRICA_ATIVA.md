# 🔐 Guia de Captura Biométrica - ETAN Ativo

## ✅ Problema Identificado e Corrigido

### O que era o problema?
- **Iframe externo bloqueado por CORS** em `etan-captura-biometrica.html` (linha 362)
- URL externa: `https://infant.akiyama.com.br/#/infant-capture` tentava acessar `localhost:5000`
- Diferentes origens = CORS bloqueado automaticamente pelo navegador

### O que foi corrigido?
✅ **Removido**: Iframe externo que causava conflitos  
✅ **Ativado**: Sistema local de captura completo  
✅ **Adicionado**: Scripts necessários em ordem correta:
   1. Socket.IO (WebSocket)
   2. config-urls.js (URLs centralizadas)
   3. etan-websocket.js (Comunicação com servidor)
   4. etan-simulator-manager.js (Lógica de captura)
   5. iframe-bridge.js (Comunicação entre frames)

---

## 🚀 Como Usar Agora

### 1. **Iniciar Todos os Serviços**
```powershell
# No VS Code Terminal (PowerShell)
.\start_all_services.ps1
```

Isso abre automaticamente:
- ✅ Backend Flask (porta 5001)
- ✅ Device Service (porta 5000)

### 2. **Acessar a Atividade**
```
http://localhost:5001/frontend/activities/etan-captura-biometrica.html
```

### 3. **Sequência de Captura**
1. Clique em **"▶️ Iniciar Captura"**
2. Sistema simula captura de digital com qualidade em tempo real
3. Quando atinge 70%+ de qualidade → Captura bem-sucedida
4. Próximo dedo automaticamente
5. Repita para os 10 dedos (5 mão direita + 5 mão esquerda)
6. Clique em **"✅ Finalizar"** quando concluído

---

## 🔧 Backend - Endpoints Utilizados

### 1. **Registrar Captura Individual**
```http
POST /api/activities/biometric/capture
Authorization: Bearer {JWT_TOKEN}

Body:
{
  "user_id": 1,
  "activity_id": 4,
  "finger_id": 1,
  "finger_name": "Polegar",
  "hand": "Direita",
  "quality": 85,
  "nfiq": 4,
  "attempt_number": 1,
  "timestamp": "2026-03-02T09:28:22Z"
}
```

**Resposta:**
```json
{
  "success": true,
  "finger_id": 1,
  "quality_score": 85,
  "nfiq": 4
}
```

### 2. **Completar Atividade**
```http
POST /api/activities/biometric/completion
Authorization: Bearer {JWT_TOKEN}

Body:
{
  "user_id": 1,
  "activity_id": 4,
  "course_id": 1,
  "total_fingers_captured": 10,
  "average_quality": 82,
  "success_rate": 95,
  "total_time": 45.5,
  "completion_date": "2026-03-02T09:28:22Z"
}
```

---

## 🎯 Fluxo de Funcionamento

```
┌─────────────────────────────────────────────────────┐
│  PÁGINA: etan-captura-biometrica.html               │
│  (127.0.0.1:5001)                                   │
└────────────────────┬────────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
  ┌──────────────────┐  ┌──────────────────┐
  │ ETANSimulator    │  │ WebSocket        │
  │ (simulação local)│  │ (comunicação      │
  │                  │  │  real-time)      │
  └────────┬─────────┘  └────────┬─────────┘
           │                     │
           └──────────┬──────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  BACKEND Flask              │
        │  (5001)                     │
        │                             │
        │ /api/activities/biometric   │
        │ /api/activities/completion  │
        └─────────────┬───────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  Database                   │
        │  (armazena capturas)        │
        └─────────────────────────────┘
```

---

## 🐛 Debugging

### **Console mostra erros CORS?**
```javascript
// Abra: http://localhost:5001 (não :5000!)
// Verifique no DevTools (F12) → Console
```

**Erro esperado ANTES:**
```
❌ Access to XMLHttpRequest at 'https://infant.akiyama.com.br'
   from origin 'http://localhost' has been blocked by CORS policy
```

**Agora (DEPOIS da correção):**
```
✅ [ETAN] Gerenciador inicializado
✅ [ETAN] Iniciando captura: Direita - Polegar (1/10)
✅ [ETAN] ✅ Captura salva no servidor
```

### **WebSocket Offline?**
```javascript
// Verifique health check:
curl http://localhost:5001/health

// Esperado:
{
  "status": "ok",
  "services": {
    "flask": "ok",
    "websocket": "ok"
  }
}
```

---

## 📊 Métricas de Captura

Após capturar um dedo, o sistema registra:

| Métrica | Exemplo | Descrição |
|---------|---------|-----------|
| `quality` | 85 | Qualidade percentual (0-100) |
| `nfiq` | 4 | NFIQ Score (1-5, sendo 5 a melhor) |
| `attempt_number` | 1 | Qual tentativa foi (1, 2, 3...) |
| `hand` | "Direita" | Mão (Direita/Esquerda) |
| `finger_name` | "Polegar" | Nome do dedo |

---

## ✨ Integrações Ativas

### Socket.IO (Port 5001)
```javascript
// Conecta automaticamente via etan-websocket.js
window.etanWebSocket.emit('biometric_capture', {
  activityId: 4,
  type: 'fingerprint',
  quality: 0.95
});
```

### Config URLs (Centralizado)
```javascript
// Todos acessam via window.CONFIG_URLS
const apiUrl = window.CONFIG_URLS.API_BASE;    // http://localhost:5001
const deviceUrl = window.CONFIG_URLS.DEVICE_URL; // http://localhost:5000
```

---

## 🔒 Autenticação

### Obtém token do localStorage
```javascript
const token = localStorage.getItem('authToken');
// Se não tiver, usa vazio (sem autenticação para testes)
```

### Para testes com autenticação:
```powershell
# 1. Acesse página de login
http://localhost:5001/pages/login.html

# 2. Faça login
# Token salvo automaticamente em localStorage

# 3. Acesse captura biométrica
http://localhost:5001/frontend/activities/etan-captura-biometrica.html
```

---

## 🎓 Próximos Passos

### Fase 1: ✅ Captura Simulada (Completa)
- Simulação de captura funcionando
- Interface responsiva
- Salvamento no backend

### Fase 2: Device Service Real
Para captura real com dispositivo biométrico:
```javascript
// Modificar etan-simulator-manager.js para chamar:
// POST http://localhost:5000/api/fingerprint/capture

const response = await fetch('http://localhost:5000/api/fingerprint/capture', {
  method: 'POST',
  body: JSON.stringify({
    deviceId: 'default',
    finger: 'thumb_left',
    timeoutMs: 5000
  })
});
```

### Fase 3: Integração Completa
- Teste com câmera real
- Validação de qualidade real-time
- Sincronização com banco de dados

---

## 📝 Checklist de Resolução

- ✅ **Problema**: Iframe externo bloqueado
- ✅ **Solução**: Removido iframe, ativado sistema local
- ✅ **Scripts**: Carregados em ordem correta
- ✅ **Backend**: Endpoints disponíveis e testados
- ✅ **WebSocket**: Configurado e operacional
- ✅ **Autenticação**: Suporte a JWT (com fallback)
- ⏳ **Próximo**: Testes com dispositivo real (Fase 2)

---

## 📞 Suporte Rápido

| Problema | Solução |
|----------|---------|
| Página em branco | Abra DevTools (F12), veja erros na console |
| "Cannot find ETANSimulatorManager" | Aguarde carregamento de `/etan-simulator-manager.js` |
| CORS ainda bloqueado | Limpe cache (Ctrl+Shift+Delete), recarregue |
| Toque no dedo não detecta | Use o simulador (clique "Iniciar") |
| Token inválido | Use `/pages/login.html` para obter novo token |

