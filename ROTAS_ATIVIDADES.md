# 📋 Rotas de Atividades - Documentação Completa

## 🚀 Como Acessar as Atividades

### 1. **Listar Todas as Atividades Disponíveis**
```
GET http://127.0.0.1:5001/api/activities/list
```
**Resposta:**
```json
{
  "success": true,
  "total": 6,
  "activities": [
    {
      "id": 1,
      "filename": "biometric-capture-simulator.html",
      "name": "biometric-capture-simulator",
      "title": "Biometric Capture Simulator",
      "description": "Simulador de captura de impressões digitais ETAN",
      "category": "Captura Biométrica",
      "icon": "👆",
      "type": "interactive",
      "url": "/activities/biometric-capture-simulator.html",
      "api_url": "/api/activities/biometric-capture-simulator/access"
    },
    // ... mais atividades
  ]
}
```

### 2. **Agrupar Atividades por Categoria**
```
GET http://127.0.0.1:5001/api/activities/categories
```
**Resposta:**
```json
{
  "success": true,
  "categories": {
    "Captura Biométrica": [
      {
        "filename": "etan-captura-biometrica.html",
        "name": "etan-captura-biometrica",
        "title": "Etan Captura Biometrica",
        "url": "/activities/etan-captura-biometrica.html"
      }
    ],
    "Simulador": [
      {
        "filename": "etan_protocol_simulator.html",
        "name": "etan_protocol_simulator",
        "title": "Etan Protocol Simulator",
        "url": "/activities/etan_protocol_simulator.html"
      },
      // ... mais simuladores
    ],
    // ... mais categorias
  },
  "total_activities": 6
}
```

### 3. **Acessar uma Atividade Específica**
```
GET http://127.0.0.1:5001/api/activities/etan-captura-biometrica/access
```
**Resposta:**
```json
{
  "success": true,
  "activity": "etan-captura-biometrica",
  "filename": "etan-captura-biometrica.html",
  "url": "/activities/etan-captura-biometrica.html",
  "message": "Acesse a atividade em: /activities/etan-captura-biometrica.html"
}
```

### 4. **Pesquisar Atividades por Palavra-chave**
```
GET http://127.0.0.1:5001/api/activities/search?q=biometric
```
**Resposta:**
```json
{
  "success": true,
  "query": "biometric",
  "results": [
    {
      "filename": "biometric-capture-simulator.html",
      "name": "biometric-capture-simulator",
      "title": "Biometric Capture Simulator",
      "url": "/activities/biometric-capture-simulator.html"
    },
    {
      "filename": "etan-captura-biometrica.html",
      "name": "etan-captura-biometrica",
      "title": "Etan Captura Biometrica",
      "url": "/activities/etan-captura-biometrica.html"
    }
  ],
  "count": 2
}
```

## 📁 Atividades Disponíveis

| Nome | URL de Acesso | Categoria |
|------|-----------------|-----------|
| Biometric Capture Simulator | `/activities/biometric-capture-simulator.html` | 👆 Captura Biométrica |
| ETAN Captura Biométrica | `/activities/etan-captura-biometrica.html` | 👆 Captura Biométrica |
| ETAN Protocol Simulator | `/activities/etan_protocol_simulator.html` | 🎮 Simulador |
| ETAN Special Cases | `/activities/etan_special_cases.html` | ⚠️ Casos Especiais |
| ETAN Troubleshooting | `/activities/etan_troubleshooting.html` | 🔧 Solução de Problemas |
| Live Biometric Capture | `/activities/live-biometric-capture.html` | 👆 Captura Biométrica |

## 🔗 URLs Diretas para Atividades

### Abrir no Navegador
```
http://127.0.0.1:5001/activities/etan-captura-biometrica.html
http://127.0.0.1:5001/activities/biometric-capture-simulator.html
http://127.0.0.1:5001/activities/etan_protocol_simulator.html
http://127.0.0.1:5001/activities/etan_special_cases.html
http://127.0.0.1:5001/activities/etan_troubleshooting.html
http://127.0.0.1:5001/activities/live-biometric-capture.html
```

## 🎯 Endpoints de Registro de Atividades

### Iniciar Sessão de Captura Biométrica
```bash
POST http://127.0.0.1:5001/api/activities/biometric/session/start
Content-Type: application/json

{
  "user_id": 1,
  "activity_id": 4,
  "course_id": 1
}
```

### Registrar Captura de Digital
```bash
POST http://127.0.0.1:5001/api/activities/biometric/capture
Content-Type: application/json

{
  "user_id": 1,
  "activity_id": 4,
  "finger_id": 1,
  "finger_name": "Polegar Direito",
  "hand": "Direita",
  "quality": 85,
  "nfiq": 50,
  "attempt_number": 1
}
```

### Completar Sessão de Captura
```bash
POST http://127.0.0.1:5001/api/activities/biometric/completion
Content-Type: application/json

{
  "user_id": 1,
  "activity_id": 4,
  "total_fingers_captured": 10,
  "average_quality": 85,
  "success_rate": 100,
  "captured_fingers": ["Polegar D.", "Índice D.", ...],
  "total_time": 300
}
```

## 📊 Endpoints de Progresso

### Obter Progresso do Usuário
```
GET http://127.0.0.1:5001/api/activities/user/progress
(Requer autenticação)
```

### Obter Status de Atividades de uma Aula
```
GET http://127.0.0.1:5001/api/activities/lesson/4/status
(Requer autenticação)
```

### Obter Ranking (Leaderboard)
```
GET http://127.0.0.1:5001/api/activities/leaderboard?limit=10
```

## 🛠️ Exemplos com cURL

### Listar Atividades
```bash
curl http://127.0.0.1:5001/api/activities/list
```

### Obter Categorias
```bash
curl http://127.0.0.1:5001/api/activities/categories
```

### Pesquisar Atividades
```bash
curl "http://127.0.0.1:5001/api/activities/search?q=simulator"
```

### Acessar Atividade Específica
```bash
curl http://127.0.0.1:5001/api/activities/etan-captura-biometrica/access
```

## 📱 Exemplos com JavaScript/Fetch

```javascript
// Listar todas as atividades
fetch('http://127.0.0.1:5001/api/activities/list')
  .then(r => r.json())
  .then(data => console.log(data.activities))

// Pesquisar atividades
fetch('http://127.0.0.1:5001/api/activities/search?q=biometric')
  .then(r => r.json())
  .then(data => console.log(data.results))

// Iniciar sessão biométrica
fetch('http://127.0.0.1:5001/api/activities/biometric/session/start', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    user_id: 1,
    activity_id: 4,
    course_id: 1
  })
})
  .then(r => r.json())
  .then(data => console.log('Session ID:', data.session_id))
```

## ⚠️ Notas Importantes

1. **URL Correta**: Use `/activities/<filename>` para servir os arquivos HTML
   - ❌ ERRADO: `/frontend/activities/etan-captura-biometrica.html`
   - ✅ CORRETO: `/activities/etan-captura-biometrica.html`

2. **API vs Arquivos Estáticos**:
   - `/api/activities/list` → Endpoint API JSON
   - `/api/activities/<name>/access` → Informações sobre a atividade
   - `/activities/<filename>` → Arquivo HTML estático

3. **Sem Autenticação**: Os endpoints de listar e servir atividades não requerem autenticação
   - Registro de atividades também aceita sem autenticação (para desenvolvimento)
   - Endpoints de progresso do usuário requerem autenticação

4. **Nomes de Arquivos**: 
   - Use hífens (`-`) nos nomes de arquivo
   - A API aceita beide hífens e underscores (`_`)

## 🎓 Fluxo de Uso Recomendado

1. **Descoberta**: `GET /api/activities/list` ou `GET /api/activities/categories`
2. **Pesquisa**: `GET /api/activities/search?q=termo`
3. **Verificação**: `GET /api/activities/<name>/access`
4. **Acesso**: Abrir a atividade em `/activities/<filename>`
5. **Registro**: Usar endpoints de captura biométrica conforme necessário

## 📝 Próximos Passos

- [ ] Integrar formulários de atividades com backend
- [ ] Implementar sistema de badges
- [ ] Criar página de dashboard com progresso
- [ ] Adicionar notificações de conclusão
