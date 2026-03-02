# 🔧 Estrutura Interna do Simulador - Para Desenvolvedores

## Arquitetura

```javascript
┌─────────────────────────────────────────────────────────┐
│         BiometricCaptureSimulator Class                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Properties:                                             │
│  - captureMode: 'child' | 'adult'                      │
│  - isCapturing: boolean                                 │
│  - captureStartTime: timestamp                         │
│  - quality: 0-100                                      │
│  - frameCount: number (0-120)                          │
│  - currentState: 'idle' | 'waiting' | 'detecting'...  │
│  - qualityParams: {                                    │
│      wetness: 0-100                                    │
│      cleanliness: 0-100                               │
│      positioning: 0-100                               │
│      pressure: 0-100                                  │
│    }                                                   │
│  - feedbackHistory: array                             │
│                                                        │
│ Methods:                                               │
│  + constructor()                                      │
│  + init()                                             │
│  + cacheDom()                                         │
│  + bindEvents()                                       │
│  + startCapture()                                     │
│  + stopCapture()                                      │
│  + simulateCapture()                                  │
│  + simulateQualityAnalysis()                         │
│  + simulateQualityImprovement()                      │
│  + finishCapture()                                    │
│  + calculateNFIQ()                                    │
│  + showResults(nfiq, time, minutiae)                 │
│  + addFeedback(msg, type)                            │
│  + updateStatus(text)                                │
│  + updateQualityDisplay()                            │
│  + cleanupUI()                                        │
│  + logMessage(msg)                                    │
│                                                        │
└─────────────────────────────────────────────────────────┘
```

---

## Fluxo de Execução

```
┌────────────────────────────────────────────────────────┐
│ 1. DOMContentLoaded Event                               │
│    └─ Instantiate BiometricCaptureSimulator             │
└────────────────────┬─────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│ 2. constructor()                                       │
│    ├─ Initialize properties                            │
│    └─ Call init()                                      │
└────────────────────┬─────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│ 3. init()                                              │
│    ├─ cacheDom() - Armazena referências de elementos  │
│    ├─ bindEvents() - Conecta event listeners          │
│    └─ logMessage('Simulador inicializado')            │
└────────────────────┬─────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│ 4. User Interaction - Clica em \"Iniciar Captura\"    │
│    └─ Dispara startCapture()                          │
└────────────────────┬─────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│ 5. startCapture()                                      │
│    ├─ Set isCapturing = true                          │
│    ├─ Record startTime                                │
│    ├─ Reset frameCount = 0                            │
│    ├─ Clear feedbackHistory                           │
│    ├─ Set currentState = 'waiting'                    │
│    ├─ Update UI (hide/show buttons)                   │
│    ├─ Add feedback: \"Captura iniciada\"              │
│    └─ Schedule simulateCapture()                      │
└────────────────────┬─────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│ 6. simulateCapture() - RequestAnimationFrame Loop      │
│                                                        │
│    A cada frame (60fps):                              │
│                                                        │
│    ├─ Increment frameCount                            │
│    ├─ Calculate elapsedTime                           │
│    │                                                  │
│    ├─ IF frameCount < 30 (Fase 1)                     │
│    │  ├─ State = 'waiting'                            │
│    │  └─ IF frameCount == 15                          │
│    │      ├─ State = 'detecting'                      │
│    │      ├─ fingerDetected = true                    │
│    │      └─ addFeedback(\"Dedo detectado\")          │
│    │                                                  │
│    ├─ IF frameCount 30-70 (Fase 2)                    │
│    │  ├─ State = 'positioning'                        │
│    │  ├─ simulateQualityAnalysis()                    │
│    │  └─ Check conditions for feedback:               │
│    │      ├─ IF positioning < 50 → warn              │
│    │      ├─ IF wetness > 70 → warn                  │
│    │      ├─ IF cleanliness < 40 → warn              │
│    │      └─ IF pressure < 40 → warn                 │
│    │                                                  │
│    ├─ IF frameCount 70-120 (Fase 3)                   │
│    │  ├─ State = 'capturing'                          │
│    │  ├─ simulateQualityImprovement()                │
│    │  └─ Check for pressure feedback                  │
│    │                                                  │
│    ├─ Update timer display                            │
│    ├─ Update quality bar                              │
│    │                                                  │
│    ├─ Check finish conditions:                        │
│    │  ├─ frameCount >= 120 → finishCapture()         │
│    │  ├─ OR quality >= 80% → finishCapture()         │
│    │  └─ Otherwise → requestAnimationFrame()         │
│    │                                                  │
│    └─ Continue loop                                   │
│                                                        │
└────────────────────┬─────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐    ┌────────▼─────────┐
│ User clicks      │    │ Loop finishes    │
│ \"Parar\"       │    │ (120 frames or   │
│                 │    │  80% quality)     │
└───────┬──────────┘    └────────┬─────────┘
        │                       │
        ├───────────┬───────────┤
        │           │           │
        └─────┬─────┘           │
              │                 │
        ┌─────▼──────────────────▼────────┐
        │ finishCapture()                   │
        │                                  │
        ├─ Set isCapturing = false         │
        ├─ State = 'completed'             │
        ├─ Calculate NFIQ (1-5)            │
        │   └─ Based on quality %          │
        ├─ Count minutiae (random 100-200) │
        ├─ Calculate total time            │
        ├─ showResults()                   │
        ├─ addFeedback(\"✅ Sucesso!\")    │
        ├─ cleanupUI()                     │
        └─ Display results panel           │
        │                                  │
        └─────────────────────────────────┘
```

---

## Estados da Máquina (State Machine)

```
┌──────────────────────────────────────────────────────────┐
│          States: idle, waiting, detecting, ...            │
│          positioning, capturing, completed               │
└──────────────────────────────────────────────────────────┘

                      ┌─────────────┐
                      │    IDLE     │
                      │ (Repouso)   │
                      └──────┬──────┘
                             │ User clicks Start
                             ▼
                      ┌─────────────┐
                      │   WAITING   │ 0-2s
                      │(Aguardando) │
                      └──────┬──────┘
                             │ frameCount == 15
                             ▼
                      ┌─────────────┐
                      │  DETECTING  │
                      │ (Detectado) │
                      └──────┬──────┘
                             │ frameCount == 30
                             ▼
                      ┌─────────────┐
                      │ POSITIONING │ 2-3.5s
                      │ (Posicion.) │
                      └──────┬──────┘
                             │ frameCount == 70
                             ▼
                      ┌─────────────┐
                      │ CAPTURING   │ 3-5s
                      │ (Capturando)│
                      └──────┬──────┘
                             │ frameCount >= 120
                             │ OR quality >= 80%
                             ▼
                      ┌─────────────┐
                      │ COMPLETED   │
                      │ (Concluído) │
                      └─────────────┘

        User can STOP at any point and return to IDLE
```

---

## Cálculo de Qualidade

```javascript
// Simulação de parâmetros em cada frame:

function simulateQualityAnalysis() {
    // Umidade: Aumenta/diminui aleatoriamente
    this.qualityParams.wetness = Math.max(0, Math.min(100,
        this.qualityParams.wetness - 5 + Math.random() * 10
    ));

    // Limpeza: Melhora com tempo
    this.qualityParams.cleanliness = Math.min(100,
        this.qualityParams.cleanliness + 3 + Math.random() * 5
    );

    // Posição: Melhora lentamente
    this.qualityParams.positioning = Math.min(100,
        this.qualityParams.positioning + 4 + Math.random() * 6
    );

    // Pressão: Melhora muito lentamente
    this.qualityParams.pressure = Math.min(100,
        this.qualityParams.pressure + 2 + Math.random() * 4
    );

    // Qualidade Global (média ponderada 25% cada)
    const avgQuality = (
        (100 - this.qualityParams.wetness)    * 0.25 +
        this.qualityParams.cleanliness        * 0.25 +
        this.qualityParams.positioning        * 0.25 +
        this.qualityParams.pressure           * 0.25
    );

    this.quality = Math.min(100, avgQuality);
}

// Durante captura, melhora se tudo ok:
function simulateQualityImprovement() {
    if (this.qualityParams.positioning > 70 &&
        this.qualityParams.cleanliness > 60 &&
        this.qualityParams.wetness < 40) {
        // Condições boas = melhora mais rápido
        this.quality = Math.min(100,
            this.quality + 5 + Math.random() * 5
        );
    } else {
        // Condições ruins = melhora mais lento
        this.quality = Math.max(0,
            this.quality - 2 + Math.random() * 3
        );
    }
}
```

---

## Sistema de Feedback

```javascript
/*
 * Tipos de Feedback:
 * - 'success': Verde, ✅
 * - 'warning': Amarelo, ⚠️
 * - 'error': Vermelho, ❌
 * - 'info': Azul, ℹ️
 */

// Adicionar feedback (anima e organiza)
addFeedback(message, type = 'info') {
    const div = document.createElement('div');
    div.className = `feedback-item feedback-${type}`;
    
    // Renderizar com icone
    div.innerHTML = `
        <span class="feedback-icon">${icons[type]}</span>
        <span>${message}</span>
    `;
    
    // Adicionar ao topo do container
    this.feedbackContainer.prepend(div);
    
    // Manter apenas últimas 5 mensagens
    while (this.feedbackContainer.children.length > 5) {
        this.feedbackContainer.removeChild(
            this.feedbackContainer.lastChild
        );
    }
    
    // Registrar no histórico
    this.feedbackHistory.push({
        message,
        type,
        time: new Date()
    });
}

// Feedback condicional nas fases:
if (frameCount === 35 && this.qualityParams.positioning < 50) {
    this.addFeedback('⚠️ Dedo mal posicionado', 'warning');
}

if (frameCount === 45 && this.qualityParams.wetness > 70) {
    this.addFeedback('💧 Digital está molhada', 'warning');
}

if (frameCount === 55 && this.qualityParams.cleanliness < 40) {
    this.addFeedback('🧼 Digital está suja', 'warning');
}

if (frameCount === 90 && this.qualityParams.pressure < 40) {
    this.addFeedback('👉 Aumentar pressão', 'warning');
}
```

---

## DOM Caching

```javascript
cacheDom() {
    // Buttons
    this.startBtn = document.getElementById('start-capture-btn');
    this.stopBtn = document.getElementById('stop-capture-btn');
    
    // Display Elements
    this.timerEl = document.getElementById('timer');
    this.statusEl = document.getElementById('status');
    
    // Feedback
    this.feedbackContainer = document.getElementById('feedback-container');
    
    // Quality Display
    this.qualityFill = document.querySelector('.quality-fill');
    this.qualityScore = document.querySelector('.quality-score');
    
    // Visual Feedback
    this.fingerPreview = document.querySelector('.finger-preview');
    
    // Results
    this.resultsPanel = document.getElementById('results-panel');
    
    // Mode Selection
    this.modeBtns = document.querySelectorAll('.mode-btn');
}
```

---

## Event Binding

```javascript
bindEvents() {
    // Start/Stop buttons
    this.startBtn.addEventListener('click', () => this.startCapture());
    this.stopBtn.addEventListener('click', () => this.stopCapture());
    
    // Mode selection
    this.modeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Desselecionar todos
            this.modeBtns.forEach(b => b.classList.remove('active'));
            
            // Selecionar clicado
            e.target.classList.add('active');
            
            // Atualizar modo
            this.captureMode = e.target.dataset.mode;
            this.logMessage(`Modo alterado para: ${this.captureMode}`);
        });
    });
}
```

---

## NFIQ Score Calculation

```javascript
calculateNFIQ() {
    /*
     * NFIQ: National Fingerprint Image Quality
     * Escala 1-5 onde 5 é excelente
     * Baseado em qualidade percentual
     */
    
    if (this.quality >= 90)      return 5;  // Excelente
    if (this.quality >= 80)      return 4;  // Bom
    if (this.quality >= 70)      return 3;  // Regular
    if (this.quality >= 50)      return 2;  // Pobre
    return 1;                               // Ruim
}

// Usar em resultado final:
const nfiqScore = this.calculateNFIQ();
const nfiqText = ['Ruim', 'Pobre', 'Regular', 'Bom', 'Excelente'][nfiqScore - 1];
document.getElementById('final-nfiq').textContent = `${nfiqScore} (${nfiqText})`;
```

---

## Personalização

### Ajustar Tempo de Fases

```javascript
// No método simulateCapture():

// Fase 1: Aguardando (frames 0-30)
if (this.frameCount < 30) {
    // Aumentar para 40 frames = 2.5s (invés de 2s)
    // Diminuir para 20 frames = 1.3s
}

// Fase 2: Posicionamento (frames 30-70)
if (this.frameCount >= 30 && this.frameCount < 70) {
    // Range: 40 frames = 2.6s
    // Aumentar para 80 para 5.3s de posicionamento
}

// Fase 3: Captura (frames 70-120)
if (this.frameCount >= 70 && this.frameCount < 120) {
    // Range: 50 frames = 3.3s
    // Esta é a fase final de captura
}

// Total máximo: 120 frames = 2 segundos @ 60fps
// Para aumentar total: 180 frames = 3 segundos
```

### Ajustar Sensibilidade de Feedback

```javascript
// Fazer feedback aparecer mais cedo/tarde:

// ANTES (apareça no frame 35):
if (frameCount === 35 && this.qualityParams.positioning < 50) {

// DEPOIS (apareça no frame 30):
if (frameCount === 30 && this.qualityParams.positioning < 50) {

// DEPOIS (apareça no frame 45):
if (frameCount === 45 && this.qualityParams.positioning < 50) {
```

### Alterar Thresholds

```javascript
// ANTES (70% umidade = molhado):
if (this.qualityParams.wetness > 70) {

// DEPOIS (80% umidade = molhado):
if (this.qualityParams.wetness > 80) {

// DEPOIS (60% = mais sensível):
if (this.qualityParams.wetness > 60) {
```

---

## Debug Tips

```javascript
// Ver no console o progresso:
console.log('[BiometricSimulator] frameCount:', this.frameCount);
console.log('[BiometricSimulator] quality:', this.quality);
console.log('[BiometricSimulator] state:', this.currentState);
console.log('[BiometricSimulator] params:', this.qualityParams);

// Ou passe para a página:
window.simulator.frameCount           // Número de frames
window.simulator.quality              // Qualidade 0-100
window.simulator.currentState         // Estado atual
window.simulator.qualityParams        // Todos os 4 parâmetros
window.simulator.captureMode          // 'child' ou 'adult'
window.simulator.feedbackHistory      // Histórico de mensagens

// Forçar finalização:
window.simulator.finishCapture();

// Adicionar feedback customizado:
window.simulator.addFeedback('Teste!', 'success');
```

---

## Performance

```javascript
/*
 * RequestAnimationFrame vs SetInterval:
 * 
 * Usamos requestAnimationFrame porque:
 * - Sincroniza com refresh rate da tela (60fps)
 * - Pausa quando tab não está ativa
 * - Melhor performance
 * - Menos consumo de bateria
 */

requestAnimationFrame(() => this.simulateCapture());

// Se precisar de timing exato:
const targetFPS = 30;  // invés de 60
const frameDelay = 1000 / targetFPS;
setTimeout(() => this.simulateCapture(), frameDelay);
```

---

**Versão:** 1.0  
**Data:** 26/02/2026  
**Para Desenvolvedores:** Use este guia para estender/personalizar o simulador
