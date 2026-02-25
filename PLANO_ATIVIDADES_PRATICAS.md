# 📋 Plano de Implementação: Atividades Práticas Interativas

## 🎯 Objetivo
Integrar atividades práticas nas aulas usando o SDK ETAN, WebSockets e o sistema de captura biométrica para que enfermeiras possam praticar sem scanner físico.

---

## 🏗️ Arquitetura

### 1. **Componentes Base**

```
Aula (HTML)
├── Explicação Teórica
├── Atividade Prática (iframe)
│   └── Sistema de Captura Simulado
└── Validação & Feedback
```

### 2. **Tecnologias Envolvidas**

| Componente | Tecnologia | Propósito |
|-----------|-----------|----------|
| Interface | Vue.js / HTML | Renderizar atividades nas aulas |
| Captura | SDK ETAN (OpenbioEnroll) | Simulador de captura real |
| Comunicação | WebSockets | Tempo real interativo |
| Backend | Flask + SQLAlchemy | Rastrear progresso |
| Embed | iframes | Integração segura |

---

## 📦 Tipos de Atividades Práticas

### Tipo 1: **Simulador de Protocolo ETAN**
**Objetivo:** Praticar os 5 passos do protocolo

```
Fase 1: Preparação → Quiz: "Qual é o sinal vital normal?"
        ✓ RESPOSTA CORRETA → avança
        ✗ RESPOSTA ERRADA → explicação + tenta novamente

Fase 2: Limpeza → Vídeo + Botões (Limpe, Seque, Verifique)
        Sequência correta desbloqueia próxima fase

Fase 3: Captura da Progenitora → Simulador visual
        Clique nos dedos na ordem correta (1-10)

Fase 4: Captura do RN → Simulador ETAN real
        Use iframe apontando para https://infant.akiyama.com.br/#/infant-capture

Fase 5: Verificação → Quiz final sobre qualidade
```

### Tipo 2: **Casos Especiais - Decisão**
**Objetivo:** Praticar como responder a cenários

```
Cenário: "Bebê prematuro, 32 semanas, muito agitado"

Perguntas:
□ Qual é o primeiro passo? (Verificar estabilidade)
□ Que tipo de pressão usar? (MÍNIMA)
□ Se chorar, o que fazer? (PARAR)

Feedback: "Correto! Você fez todas as decisões certas! ✓"
```

### Tipo 3: **Troubleshooting - Diagnóstico**
**Objetivo:** Diagnosticar problema na imagem

```
Mostra: Imagem capturada (borrada/escura/etc)

Perunta: "Qual é o problema?"
Opções:
○ Scanner sujo
○ Dedo muito seco
○ Dedo muito úmido
○ Posicionamento errado

Resposta Corerta: "Excelente! Agora clique para limpar o scanner"
Mostra: Simulação de limpeza (3 vezes com gaze)
Feedback: "Qualidade agora: EXCELENTE ✓"
```

### Tipo 4: **Prática Guiada em Tempo Real**
**Objetivo:** Praticar captura com feedback imediato

```
1. Abre iframe do OpenbioEnroll
2. Usuário faz captura de verdade (se tiver scanner)
3. Sistema retorna NFIQ score
4. Feedback:
   - NFIQ > 70: "Excelente qualidade! ✓"
   - NFIQ 50-70: "Aceitável, mas melhore a limpeza"
   - NFIQ < 50: "Rejeitado, tente novamente"
```

---

## 🔧 Implementação Técnica

### Estrutura de Pastas

```
backend/
├── app/
│   ├── services/
│   │   └── activity_service.py ✨ NOVO
│   ├── models/
│   │   └── activity.py ✨ NOVO
│   └── routes/
│       └── activities.py ✨ NOVO
│
frontend/ (HTML/JS)
├── <templates/>
│   └── activities/
│       ├── etan_protocol_simulator.html ✨ NOVO
│       ├── special_cases.html ✨ NOVO
│       ├── troubleshooting.html ✨ NOVO
│       └── live_capture.html ✨ NOVO
```

### Banco de Dados

```sql
CREATE TABLE user_activities (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT,
  course_id INT,
  lesson_id INT,
  activity_type VARCHAR(50), -- 'protocol', 'cases', 'troubleshooting', 'live'
  status VARCHAR(20), -- 'ongoing', 'completed', 'failed'
  score INT, -- 0-100
  attempts INT,
  completed_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (course_id) REFERENCES courses(id),
  FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

CREATE TABLE activity_attempts (
  id INT PRIMARY KEY AUTO_INCREMENT,
  activity_id INT,
  user_id INT,
  response JSON, -- Respostas do usuário
  result JSON, -- Feedback/resultado
  timestamp TIMESTAMP,
  FOREIGN KEY (activity_id) REFERENCES user_activities(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 📝 Estrutura das Aulas Modificadas

### Exemplo: Aula 2 (Protocolo ETAN)

```html
<div class="aula-container">
  <h1>Protocolo ETAN - As 5 Fases Completas</h1>
  
  <h2>📚 Explicação Teórica</h2>
  <!-- Conteúdo existente aqui -->
  
  <h2>🎯 Atividade Prática</h2>
  
  <div class="atividade-modulo">
    <h3>Praticar: Executar Protocolo ETAN Completo</h3>
    
    <!-- FASE 1: Preparação -->
    <div class="fase-atividade" data-fase="1">
      <h4>✓ Fase 1: Preparação</h4>
      <p>Você estão em uma maternidade. Um RN de 3000g acabou de nascer.</p>
      
      <div class="quiz-atividade">
        <p><strong>Qual é o primeiro passo?</strong></p>
        <input type="radio" name="prep"> Coletar biometria imediatamente
        <input type="radio" name="prep"> Verificar sinais vitais primeiro ✓
        <input type="radio" name="prep"> Chamar a mãe para coleta
      </div>
      
      <button onclick="validarFase1()">VERIFICAR RESPOSTA</button>
      <div id="feedback1" class="feedback"></div>
    </div>
    
    <!-- FASE 2: Limpeza -->
    <div class="fase-atividade" data-fase="2" hidden>
      <h4>✓ Fase 2: Limpeza</h4>
      <p>Os dedos têm vernix espesso. Qual é a sequência correta?</p>
      
      <div class="atividade-sequencia">
        <div class="passo" data-passo="1">Aplicar solução ETAN</div>
        <div class="passo" data-passo="2">Esperar 30 segundos</div>
        <div class="passo" data-passo="3">Secar com gaze</div>
        <div class="passo" data-passo="4">Verificar limpeza</div>
      </div>
      
      <p>Arraste os passos na ordem correta:</p>
      <div class="drop-zone"></div>
      
      <button onclick="validarFase2()">VERIFICAR SEQUÊNCIA</button>
    </div>
    
    <!-- FASE 3: Captura Progenitora -->
    <div class="fase-atividade" data-fase="3" hidden>
      <h4>✓ Fase 3: Captura da Progenitora</h4>
      <p>Digite na ordem correta (1-10) os dedos a capturar:</p>
      
      <div class="digitos-grid">
        <div class="digito" data-digito="5">👍 Polegar D</div>
        <div class="digito" data-digito="1">👆 Indicador D</div>
        <!-- mais dedos -->
      </div>
      
      <ol id="ordem-captura"></ol>
      
      <button onclick="validarFase3()">VERIFICAR ORDEM</button>
    </div>
    
    <!-- FASE 4: Captura RN (iframe) -->
    <div class="fase-atividade" data-fase="4" hidden>
      <h4>✓ Fase 4: Captura do RN</h4>
      <p>Agora pratique a captura real ou simulada:</p>
      
      <iframe 
        src="https://infant.akiyama.com.br/#/infant-capture?mode=practice&lesson=2"
        style="width:100%; height:600px; border:none; border-radius:8px;"
      ></iframe>
      
      <p id="feedback-captura"></p>
      <button onclick="validarFase4()">CONFIRMAR CAPTURA</button>
    </div>
    
    <!-- FASE 5: Verificação -->
    <div class="fase-atividade" data-fase="5" hidden>
      <h4>✓ Fase 5: Verificação Final</h4>
      
      <div class="quiz-atividade">
        <p><strong>Qual é a pontuação NFIQ aceitável?</strong></p>
        <input type="radio" name="nfiq"> Maior que 50 ✓
        <input type="radio" name="nfiq"> Maior que 70 (ideal)
        <input type="radio" name="nfiq"> Qualquer coisa
      </div>
      
      <button onclick="completarAtividade()">FINALIZAR ATIVIDADE</button>
    </div>
    
    <!-- Resultado Final -->
    <div class="resultado-atividade" hidden>
      <h3>✨ Parabéns!</h3>
      <p>Você completou a atividade com <strong>95/100</strong> pontos!</p>
      <p>Tempo: 12 minutos e 30 segundos</p>
      
      <ul>
        <li>✓ Fase 1: Preparação correta</li>
        <li>✓ Fase 2: Limpeza executada bem</li>
        <li>✓ Fase 3: Ordem de captura perfeita</li>
        <li>✓ Fase 4: Qualidade NFIQ=78 (Excelente)</li>
        <li>✓ Fase 5: Verificação correta</li>
      </ul>
      
      <button onclick="proximaAula()">PRÓXIMA AULA →</button>
    </div>
  </div>
</div>

<script>
  // JavaScript para gerenciar progressão
  let progressoAtual = 1;
  
  function validarFase1() {
    // Verifica resposta
    progressoAtual = 2;
    mostrarFase(2);
  }
  
  function mostrarFase(numero) {
    document.querySelectorAll('.fase-atividade').forEach(el => el.hidden = true);
    document.querySelector(`[data-fase="${numero}"]`).hidden = false;
  }
  
  // Mais funções...
</script>
```

---

## 🔌 API Endpoints

### Atividades

```python
# POST /api/activities/start
{
  "lesson_id": 2,
  "activity_type": "protocol"  # 'protocol', 'cases', 'troubleshooting', 'live'
}
→ Response:
{
  "activity_id": 123,
  "lesson_id": 2,
  "type": "protocol",
  "status": "ongoing"
}

# POST /api/activities/123/attempt
{
  "fase": 1,
  "resposta": ["verificar_vitais"],
  "tempo_gasto": 120  # segundos
}
→ Response:
{
  "correto": true,
  "feedback": "Excelente! Você identificou corretamente...",
  "proxima_fase": 2
}

# POST /api/activities/123/complete
{
  "score": 95,
  "tempo_total": 750,  # segundos total
  "tentativas": 1
}
→ Response:
{
  "completed": true,
  "achievement": "Protocolo ETAN Dominado ✓",
  "certificado_url": "..."
}

# GET /api/user/activities/progress
→ Response:
{
  "total_atividades": 15,
  "completadas": 7,
  "em_progresso": 2,
  "score_medio": 88.5,
  "badges": [...]
}
```

---

## 🎯 Funcionalidades WebSocket

```javascript
// Conectar ao WebSocket
const ws = new WebSocket("wss://backend.infant.local/activities/stream");

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === "capture_result") {
    // Resultado de captura em tempo real
    console.log("NFIQ Score:", data.nfiq);
    console.log("Feedback:", data.feedback);
    mostrarFeedback(data);
  }
  
  if (data.type === "activity_progress") {
    // Progresso atualizado
    atualizarBarraProgresso(data.progresso);
  }
};

// Enviar resposta para atividade
ws.send(JSON.stringify({
  type: "activity_response",
  activity_id: 123,
  resposta: ["verificar_vitais"],
  timestamp: Date.now()
}));
```

---

## 🚀 Fases de Implementação

### **Fase 1: Estrutura Base (1-2 dias)**
- [ ] Criar modelos de banco de dados (activity, activity_attempt)
- [ ] Criar endpoints básicos da API
- [ ] Configurar roteamento para atividades

### **Fase 2: Atividades Simples (2-3 dias)**
- [ ] Protocolo ETAN (Fuzes 1-3: Quiz e sequências)
- [ ] Casos Especiais (Quiz de decisão)
- [ ] Troubleshooting (Diagnóstico de imagem)

### **Fase 3: Integração com SDK (2-3 dias)**
- [ ] Iframe embed da captura real
- [ ] WebSocket para feedback em tempo real
- [ ] Validação de NFIQ score

### **Fase 4: Testes & Polish (1-2 dias)**
- [ ] Testar todas as atividades
- [ ] Feedback de UX/UI
- [ ] Deploy em staging

### **Fase 5: Monitoramento (Contínuo)**
- [ ] Rastrear progresso dos usuários
- [ ] Coletar métricas
- [ ] Ajustar baseado em feedback

---

## 📊 Métricas de Sucesso

```
✓ Taxa de conclusão de atividades: >80%
✓ Score médio: >85/100
✓ Tempo médio por atividade: 10-15 min
✓ Taxa de retenção na aula: >90%
✓ Feedback positivo: >4.5/5 ⭐
```

---

## 💡 Exemplos de Atividades por Aula

| Aula | Atividade Tipo | Descrição |
|------|---|---|
| 1 | Quiz | "Qual é a unicidade de impressão digital?" |
| 2 (ETAN) | Protocol Sim | Executar 5 fases com validação |
| 3 (Casos) | Decision Tree | "Bebê chorador → o que fazer?" |
| 4 (Troubleshooting) | Diagnóstico | Ver imagem borrada → identificar problema |
| 5 (Qualidade) | Reflexão | "Por que qualidade > velocidade?" |

---

## 🔐 Segurança & LGPD

- ✅ Dados de atividades criptografados no banco
- ✅ Sem armazenar imagens reais de captura
- ✅ Consentimento implícito no treinamento
- ✅ Logs para auditoria
- ✅ Deletar dados após 1 ano (configurável)

---

## 📱 Responsividade

- ✅ Desktop: 1920x1080 (otimizado)
- ✅ Tablet: 1024x768 (adaptado)
- ✅ Mobile: Não recomendado (muita interação)

---

## 🎓 Próximos Passos

1. **Hoje:** Aprovação do plano
2. **Amanhã:** Começar Fase 1 (modelos DB)
3. **Próxima semana:** Fase 2 & 3 (atividades básicas)
4. **Semana depois:** Teste em staging
5. **Semana depois:** Deploy para usuários reais

