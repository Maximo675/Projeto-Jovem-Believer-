"""
Guia de Integração de Atividades Práticas nas Aulas
Exemplos de como embutir atividades nas páginas de lições
"""

# ============================================
# 1. INCORPORAR ATIVIDADE NA PÁGINA HTML
# ============================================

ATIVIDADE_HTML_TEMPLATE = """
<!-- Aula 2: Protocolo ETAN - As 5 Fases Completas -->
<div class="aula-container">
    <h1>📚 Aula 2: Protocolo ETAN - As 5 Fases Completas</h1>
    
    <!-- Conteúdo teórico -->
    <section class="conteudo-teorico">
        <h2>Conceitos Fundamentais</h2>
        <p>O protocolo ETAN possui 5 fases fundamentais que devem ser executadas na ordem correta...</p>
        <!-- outros conteúdos -->
    </section>
    
    <!-- Atividade prática embutida -->
    <section class="atividade-pratica">
        <h2>🎮 Atividade Prática: Simulador ETAN</h2>
        <p>Pratique o protocolo interativamente no simulador abaixo:</p>
        
        <div class="iframe-container">
            <iframe 
                id="activity-frame"
                src="/activities/etan_protocol_simulator.html"
                class="activity-iframe"
                style="width: 100%; height: 900px; border: none;">
            </iframe>
        </div>
    </section>
</div>

<style>
.iframe-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 20px;
    margin: 30px 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.activity-iframe {
    border-radius: 8px;
    background: white;
}

.atividade-pratica {
    background: #f8f9ff;
    padding: 30px;
    border-radius: 12px;
    border-left: 4px solid #667eea;
}
</style>
"""


# ============================================
# 2. COMPONENTE JAVASCRIPT PARA COMUNICAÇÃO
# ============================================

ACTIVITY_COMMUNICATION_JS = """
/**
 * Activity Communication Handler
 * Gerencia a comunicação entre a atividade (iframe) e a página da aula
 */

class ActivityHandler {
    constructor(activityType = 'protocol', lessonId = null, courseId = null) {
        this.activityType = activityType;
        this.lessonId = lessonId;
        this.courseId = courseId;
        this.activityId = null;
        this.isIframe = window.self !== window.top;
        
        this.setupMessageListener();
        this.initializeActivity();
    }
    
    /**
     * Escutar mensagens da atividade (iframe)
     */
    setupMessageListener() {
        window.addEventListener('message', (event) => {
            // Verificar origem por segurança
            if (event.origin !== window.location.origin) return;
            
            const data = event.data;
            console.log('📨 Mensagem recebida:', data);
            
            switch(data.action) {
                case 'ACTIVITY_STARTED':
                    this.handleActivityStarted(data.payload);
                    break;
                case 'ATTEMPT_RECORDED':
                    this.handleAttemptRecorded(data.payload);
                    break;
                case 'ACTIVITY_COMPLETED':
                    this.handleActivityCompleted(data.payload);
                    break;
                case 'ACTIVITY_ERROR':
                    this.handleActivityError(data.payload);
                    break;
            }
        });
    }
    
    /**
     * Inicializar atividade no servidor
     */
    async initializeActivity() {
        try {
            const response = await fetch(`/api/activities/${this.lessonId}/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content
                },
                body: JSON.stringify({
                    activity_type: this.activityType,
                    course_id: this.courseId,
                    lesson_id: this.lessonId
                })
            });
            
            const data = await response.json();
            if (data.success) {
                this.activityId = data.activity_id;
                console.log('✅ Atividade inicializada:', this.activityId);
                
                // Enviar ID da atividade para o iframe
                this.sendMessageToIframe({
                    action: 'SET_ACTIVITY_ID',
                    payload: { activityId: this.activityId }
                });
            }
        } catch (error) {
            console.error('❌ Erro ao inicializar atividade:', error);
        }
    }
    
    /**
     * Enviar mensagem para a atividade (iframe)
     */
    sendMessageToIframe(message) {
        const iframe = document.getElementById('activity-frame');
        if (iframe && iframe.contentWindow) {
            iframe.contentWindow.postMessage(message, window.location.origin);
        }
    }
    
    /**
     * Manejar: Atividade iniciada na atividade
     */
    handleActivityStarted(payload) {
        console.log('🎮 Atividade iniciada pelo usuário');
        // Mostrar indicador visual
        const badge = document.querySelector('[data-activity-badge]');
        if (badge) badge.classList.add('active');
    }
    
    /**
     * Manejar: Tentativa registrada
     */
    async handleAttemptRecorded(payload) {
        try {
            const response = await fetch(`/api/activities/${this.activityId}/attempt`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content
                },
                body: JSON.stringify({
                    responses: payload.responses,
                    score: payload.score,
                    time_taken: payload.time_taken
                })
            });
            
            const result = await response.json();
            if (result.success) {
                console.log('✅ Tentativa registrada:', result.attempt_id);
                
                // Enviar feedback para o iframe
                this.sendMessageToIframe({
                    action: 'ATTEMPT_ACK',
                    payload: { feedback: result.feedback }
                });
            }
        } catch (error) {
            console.error('❌ Erro ao registrar tentativa:', error);
        }
    }
    
    /**
     * Manejar: Atividade completada
     */
    async handleActivityCompleted(payload) {
        try {
            const response = await fetch(`/api/activities/${this.activityId}/complete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content
                },
                body: JSON.stringify({
                    score: payload.score,
                    time_total: payload.time_total,
                    attempts: payload.attempts
                })
            });
            
            const result = await response.json();
            if (result.success) {
                console.log('🎉 Atividade completada!', result);
                
                // Mostrar notificação ao usuário
                this.showCompletionNotification(result);
                
                // Atualizar progresso da aula
                this.updateLessonProgress();
            }
        } catch (error) {
            console.error('❌ Erro ao completar atividade:', error);
        }
    }
    
    /**
     * Manejar: Erro na atividade
     */
    handleActivityError(payload) {
        console.error('❌ Erro na atividade:', payload.message);
        // Mostrar mensagem de erro ao usuário
    }
    
    /**
     * Mostrar notificação de conclusão
     */
    showCompletionNotification(result) {
        const notification = document.createElement('div');
        notification.className = 'activity-completion-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <h3>🎉 Parabéns!</h3>
                <p>Você completou a atividade com <strong>${result.score}/100</strong> pontos!</p>
                ${result.badges_earned && result.badges_earned.length > 0 ? `
                    <div class="badges-earned">
                        <p>Badges conquistados:</p>
                        ${result.badges_earned.map(b => `<span class="badge">${b.badge_icon} ${b.badge_name}</span>`).join('')}
                    </div>
                ` : ''}
                <button onclick="this.parentElement.parentElement.remove()">Fechar</button>
            </div>
        `;
        document.body.appendChild(notification);
    }
    
    /**
     * Atualizar progresso da aula
     */
    async updateLessonProgress() {
        try {
            const response = await fetch(`/api/activities/lesson/${this.lessonId}/status`);
            const data = await response.json();
            
            // Atualizar UI com progresso
            const progressBar = document.querySelector('[data-lesson-progress]');
            if (progressBar) {
                const progress = (data.completed_count / data.activities.length) * 100;
                progressBar.style.width = progress + '%';
            }
        } catch (error) {
            console.error('Erro ao atualizar progresso:', error);
        }
    }
}

// Inicializar ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    window.activityHandler = new ActivityHandler('protocol', lessonId, courseId);
});
"""


# ============================================
# 3. CÓDIGO DENTRO DA ATIVIDADE (iframe)
# ============================================

ACTIVITY_INTERNAL_JS = """
/**
 * Activity Internal Handler
 * Código que roda DENTRO da atividade (iframe)
 */

class InternalActivityHandler {
    constructor() {
        this.activityId = null;
        this.startTime = Date.now();
        this.setupParentListener();
    }
    
    /**
     * Escutar mensagens do pai (página da aula)
     */
    setupParentListener() {
        window.addEventListener('message', (event) => {
            if (event.origin !== window.location.origin) return;
            
            const data = event.data;
            console.log('📨 Mensagem do pai:', data);
            
            switch(data.action) {
                case 'SET_ACTIVITY_ID':
                    this.activityId = data.payload.activityId;
                    console.log('✅ Activity ID recebido:', this.activityId);
                    break;
                case 'ATTEMPT_ACK':
                    this.handleAttemptAck(data.payload);
                    break;
            }
        });
    }
    
    /**
     * Notificar pai: Atividade iniciada
     */
    notifyActivityStarted() {
        window.parent.postMessage({
            action: 'ACTIVITY_STARTED',
            payload: { startTime: this.startTime }
        }, window.location.origin);
    }
    
    /**
     * Notificar pai: Tentativa registrada
     */
    notifyAttemptRecorded(responses, score, timeTaken) {
        window.parent.postMessage({
            action: 'ATTEMPT_RECORDED',
            payload: { 
                responses, 
                score, 
                time_taken: timeTaken 
            }
        }, window.location.origin);
    }
    
    /**
     * Notificar pai: Atividade completada
     */
    notifyActivityCompleted(score, totalTime, attempts) {
        window.parent.postMessage({
            action: 'ACTIVITY_COMPLETED',
            payload: {
                score,
                time_total: totalTime,
                attempts
            }
        }, window.location.origin);
    }
    
    /**
     * Notificar pai: Erro na atividade
     */
    notifyError(message) {
        window.parent.postMessage({
            action: 'ACTIVITY_ERROR',
            payload: { message }
        }, window.location.origin);
    }
    
    /**
     * Manejar resposta da tentativa
     */
    handleAttemptAck(payload) {
        console.log('✅ Tentativa reconhecida pelo servidor');
        // Mostrar feedback ao usuário
        const feedback = payload.feedback;
        this.displayFeedback(feedback);
    }
    
    /**
     * Mostrar feedback na tela
     */
    displayFeedback(feedback) {
        const feedbackEl = document.getElementById('feedback');
        if (feedbackEl) {
            feedbackEl.innerHTML = `
                <div class="feedback ${feedback.level}">
                    <p>${feedback.message}</p>
                    ${feedback.tips && feedback.tips.length > 0 ? `
                        <ul>
                            ${feedback.tips.map(tip => `<li>${tip}</li>`).join('')}
                        </ul>
                    ` : ''}
                </div>
            `;
        }
    }
}

// Inicializar handler interno
const internalHandler = new InternalActivityHandler();

// IMPORTANTE: Usar internalHandler em vez de fazer requisições diretas a /api
// Exemplo:
// internalHandler.notifyAttemptRecorded(respostas, score, tempoGasto);
"""


# ============================================
# 4. EXEMPLO DE USO NO HTML DA ATIVIDADE
# ============================================

ACTIVITY_INTEGRATION_EXAMPLE = """
<!-- Dentro de etan_protocol_simulator.html -->

<!-- Ao clicar no botão "Iniciar": -->
<script>
document.getElementById('iniciar-btn').addEventListener('click', function() {
    internalHandler.notifyActivityStarted();
    // ... iniciar simulação
});

// Ao registrar uma tentativa:
document.getElementById('verificar-fase').addEventListener('click', function() {
    const score = calcularScore();
    const respostas = coletarRespostas();
    const tempo = (Date.now() - internalHandler.startTime) / 1000;
    
    internalHandler.notifyAttemptRecorded(respostas, score, tempo);
});

// Ao completar a atividade:
function completarAtividade() {
    const scoreTotal = calcularScoreTotal();
    const tempoTotal = (Date.now() - internalHandler.startTime) / 1000;
    const tentativas = contarTentativas();
    
    internalHandler.notifyActivityCompleted(scoreTotal, tempoTotal, tentativas);
}
</script>
"""


# ============================================
# 5. INICIALIZAR ROTAS NO BACKEND
# ============================================

FLASK_BLUEPRINT_REGISTRATION = """
# Em backend/app/__init__.py ou backend/app/app.py

from app.routes.activities import activities_bp

def create_app():
    app = Flask(__name__)
    
    # ... outras configurações ...
    
    # Registrar blueprint de atividades
    app.register_blueprint(activities_bp)
    
    return app
"""


# ============================================
# 6. EXEMPLO COMPLETO DE INTEGRAÇÃO
# ============================================

COMPLETE_INTEGRATION_EXAMPLE = """
<!-- exemplo_aula_com_atividade.html -->

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="csrf-token" content="{{ csrf_token }}">
    <title>Aula 2: Protocolo ETAN</title>
    <style>
        .activity-completion-notification {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from { transform: translateX(500px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .notification-content {
            padding: 30px;
        }
        
        .badges-earned {
            margin-top: 15px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .badge {
            background: #667eea;
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <main class="container">
        <!-- Conteúdo da aula -->
        <h1>📚 Aula 2: Protocolo ETAN - As 5 Fases Completas</h1>
        
        <section class="conteudo">
            <h2>Conceitos Fundamentais</h2>
            <!-- ... conteúdo teórico ... -->
        </section>
        
        <!-- Atividade Prática -->
        <section class="atividade-pratica">
            <h2>🎮 Atividade Prática</h2>
            <iframe 
                id="activity-frame"
                src="/activities/etan_protocol_simulator.html"
                style="width: 100%; height: 900px; border: none;"
            ></iframe>
        </section>
    </main>
    
    <!-- Script de integração -->
    <script>
        // Configuração da aula
        const lessonId = {{ lesson.id }};
        const courseId = {{ course.id }};
    </script>
    <script src="/static/js/activity-handler.js"></script>
</body>
</html>
"""


if __name__ == '__main__':
    print("📋 Guia de Integração de Atividades Práticas")
    print("\nLinhas principais:")
    print("1. HTML: Usar <iframe> para embutir atividades")
    print("2. JavaScript: ActivityHandler (página) + InternalActivityHandler (iframe)")
    print("3. Comunicação: postMessage() para cross-iframe communication")
    print("4. API: /api/activities/* para persistência")
    print("5. Segurança: CSRF token, origem validada, autenticação obrigatória")
