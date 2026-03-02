/**
 * Chatbot Flutuante - Sistema de IA disponível em qualquer página
 * Aparece como widget fixo no canto inferior direito
 */

const ChatbotFlutuante = {
    isOpen: false,
    conversationHistory: [],
    
    init() {
        console.log('[CHATBOT] Inicializando chatbot flutuante...');
        this.createChatbotHTML();
        this.setupEventListeners();
        this.loadConversationHistory();
    },
    
    createChatbotHTML() {
        const chatbotHTML = `
        <div id="chatbot-container" class="chatbot-container">
            <!-- Botão flutuante com Jade -->
            <button id="chatbot-toggle" class="chatbot-toggle" title="Assistente IA - Jade">
                <img src="/assets/logo/Jade.jpg" alt="Jade - Assistente IA" class="chatbot-avatar-btn">
                <span class="chatbot-badge">1</span>
            </button>
            
            <!-- Janela do chat -->
            <div id="chatbot-window" class="chatbot-window hidden">
                <!-- Header com Jade -->
                <div class="chatbot-header">
                    <div class="chatbot-jade-container">
                        <img src="/assets/logo/Jade.jpg" alt="Jade" class="chatbot-jade-image">
                    </div>
                    <div class="chatbot-title">
                        <h3>Jade</h3>
                        <span class="chatbot-status">Online</span>
                    </div>
                    <button id="chatbot-close" class="chatbot-close" title="Fechar chat">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                </div>
                
                <!-- Mensagens -->
                <div id="chatbot-messages" class="chatbot-messages">
                    <div class="message ai">
                        Olá! 👋 Sou a Jade, sua assistente de IA da Winged Mind. Como posso ajudá-lo(a)?
                        <div style="font-size: 0.85rem; margin-top: 8px; opacity: 0.9;">
                            📚 Dúvidas sobre cursos?<br>
                            🎓 Dúvidas sobre progresso?<br>
                            ❓ Perguntas gerais?
                        </div>
                    </div>
                </div>
                
                <!-- Input -->
                <div class="chatbot-input-group">
                    <input 
                        type="text" 
                        id="chatbot-input" 
                        placeholder="Digite sua pergunta para Jade..." 
                        autocomplete="off"
                    >
                    <button id="chatbot-send" class="chatbot-send-btn" title="Enviar">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        `;
        
        // Inserir no final do body
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
        
        // Adicionar estilos
        this.injectStyles();
    },
    
    injectStyles() {
        if (document.getElementById('chatbot-styles')) return;
        
        const styles = `
        <style id="chatbot-styles">
            .chatbot-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                z-index: 9999;
            }
            
            .chatbot-toggle {
                width: 70px;
                height: 70px;
                border-radius: 50%;
                background: linear-gradient(135deg, #20b7c9 0%, #1a99ac 100%);
                border: 3px solid #fff;
                cursor: pointer;
                box-shadow: 0 4px 16px rgba(32, 183, 201, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                position: relative;
                padding: 0;
                overflow: hidden;
            }
            
            .chatbot-avatar-btn {
                width: 100%;
                height: 100%;
                object-fit: cover;
                border-radius: 50%;
                animation: jadeFloat 3s ease-in-out infinite;
            }
            
            @keyframes jadeFloat {
                0%, 100% {
                    transform: translateY(0px);
                }
                50% {
                    transform: translateY(-8px);
                }
            }
            
            .chatbot-toggle:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 20px rgba(32, 183, 201, 0.7);
            }
            
            .chatbot-toggle:active {
                transform: scale(0.95);
            }
            
            .chatbot-badge {
                position: absolute;
                top: -8px;
                right: -8px;
                background: #d32f2f;
                color: white;
                border-radius: 50%;
                width: 28px;
                height: 28px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.8rem;
                font-weight: 700;
                border: 2px solid white;
                animation: badgePulse 1.5s ease-in-out infinite;
            }
            
            @keyframes badgePulse {
                0%, 100% {
                    transform: scale(1);
                }
                50% {
                    transform: scale(1.2);
                }
            }
            
            .chatbot-window {
                position: absolute;
                bottom: 90px;
                right: 0;
                width: 400px;
                height: 550px;
                background: white;
                border-radius: 16px;
                box-shadow: 0 5px 50px rgba(0, 0, 0, 0.2);
                display: flex;
                flex-direction: column;
                animation: slideUp 0.4s ease;
                overflow: hidden;
            }
            
            .chatbot-window.hidden {
                display: none;
            }
            
            @keyframes slideUp {
                from {
                    transform: translateY(30px) scale(0.9);
                    opacity: 0;
                }
                to {
                    transform: translateY(0) scale(1);
                    opacity: 1;
                }
            }
            
            .chatbot-header {
                background: linear-gradient(135deg, #20b7c9 0%, #1a99ac 100%);
                color: white;
                padding: 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .chatbot-jade-container {
                flex-shrink: 0;
            }
            
            .chatbot-jade-image {
                width: 56px;
                height: 56px;
                border-radius: 50%;
                border: 2px solid white;
                object-fit: cover;
                animation: jadeWave 3s ease-in-out infinite;
            }
            
            @keyframes jadeWave {
                0%, 100% {
                    transform: scale(1) rotate(0deg);
                }
                25% {
                    transform: scale(1.05) rotate(-3deg);
                }
                50% {
                    transform: scale(1.08) rotate(3deg);
                }
                75% {
                    transform: scale(1.05) rotate(-2deg);
                }
            }
            
            .chatbot-title {
                flex: 1;
            }
            
            .chatbot-title h3 {
                margin: 0 0 4px 0;
                font-size: 1.1rem;
                font-weight: 600;
            }
            
            .chatbot-status {
                font-size: 0.8rem;
                opacity: 0.95;
                display: flex;
                align-items: center;
            }
            
            .chatbot-status::before {
                content: '';
                width: 8px;
                height: 8px;
                background: #4caf50;
                border-radius: 50%;
                margin-right: 6px;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.4; }
            }
            
            .chatbot-close {
                background: none;
                border: none;
                color: white;
                cursor: pointer;
                padding: 4px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: opacity 0.2s;
                flex-shrink: 0;
            }
            
            .chatbot-close:hover {
                opacity: 0.8;
            }
            
            .chatbot-messages {
                flex: 1;
                overflow-y: auto;
                padding: 16px;
                display: flex;
                flex-direction: column;
                gap: 12px;
                background: #f8f9fa;
            }
            
            .chatbot-messages::-webkit-scrollbar {
                width: 6px;
            }
            
            .chatbot-messages::-webkit-scrollbar-track {
                background: transparent;
            }
            
            .chatbot-messages::-webkit-scrollbar-thumb {
                background: #ccc;
                border-radius: 3px;
            }
            
            .chatbot-messages::-webkit-scrollbar-thumb:hover {
                background: #999;
            }
            
            .message {
                padding: 12px 16px;
                border-radius: 12px;
                max-width: 85%;
                word-wrap: break-word;
                font-size: 0.9rem;
                line-height: 1.5;
                animation: messageSlide 0.3s ease;
            }
            
            @keyframes messageSlide {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .message.user {
                background: linear-gradient(135deg, #20b7c9 0%, #1a99ac 100%);
                color: white;
                align-self: flex-end;
                border-radius: 12px 0px 12px 12px;
                box-shadow: 0 2px 8px rgba(32, 183, 201, 0.3);
            }
            
            .message.ai {
                background: white;
                color: #1a1a1a;
                align-self: flex-start;
                border-radius: 0px 12px 12px 12px;
                border: 1px solid #e0e0e0;
            }
            
            .chatbot-input-group {
                display: flex;
                gap: 8px;
                padding: 12px;
                border-top: 1px solid #e0e0e0;
                background: white;
            }
            
            .chatbot-input-group input {
                flex: 1;
                padding: 10px 14px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                font-size: 0.9rem;
                font-family: inherit;
                transition: all 0.2s;
            }
            
            .chatbot-input-group input:focus {
                outline: none;
                border-color: #20b7c9;
                box-shadow: 0 0 0 3px rgba(32, 183, 201, 0.1);
            }
            
            .chatbot-input-group input::placeholder {
                color: #ccc;
            }
            
            .chatbot-send-btn {
                background: linear-gradient(135deg, #20b7c9 0%, #1a99ac 100%);
                color: white;
                border: none;
                padding: 10px 14px;
                border-radius: 8px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
                box-shadow: 0 2px 8px rgba(32, 183, 201, 0.2);
            }
            
            .chatbot-send-btn:hover {
                background: linear-gradient(135deg, #1a99ac 0%, #157a8a 100%);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(32, 183, 201, 0.3);
            }
            
            .chatbot-send-btn:active {
                transform: scale(0.98);
            }
            
            /* Responsivo */
            @media (max-width: 600px) {
                .chatbot-window {
                    width: calc(100vw - 40px);
                    height: 65vh;
                    max-height: 500px;
                    bottom: 80px;
                    right: 20px;
                }
                
                .chatbot-toggle {
                    width: 64px;
                    height: 64px;
                }
                
                .message {
                    max-width: 90%;
                }
            }
        </style>
        `;
        
        document.head.insertAdjacentHTML('beforeend', styles);
    },
    
    setupEventListeners() {
        const toggleBtn = document.getElementById('chatbot-toggle');
        const closeBtn = document.getElementById('chatbot-close');
        const sendBtn = document.getElementById('chatbot-send');
        const input = document.getElementById('chatbot-input');
        
        // Abrir/fechar chat
        toggleBtn?.addEventListener('click', () => this.toggleChat());
        closeBtn?.addEventListener('click', () => this.closeChat());
        
        // Enviar mensagem
        sendBtn?.addEventListener('click', () => this.sendMessage());
        input?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    },
    
    toggleChat() {
        const window = document.getElementById('chatbot-window');
        if (window.classList.contains('hidden')) {
            this.openChat();
        } else {
            this.closeChat();
        }
    },
    
    openChat() {
        const window = document.getElementById('chatbot-window');
        const input = document.getElementById('chatbot-input');
        window.classList.remove('hidden');
        input?.focus();
        this.hideBadge();
    },
    
    closeChat() {
        const window = document.getElementById('chatbot-window');
        window.classList.add('hidden');
    },
    
    hideBadge() {
        const badge = document.querySelector('.chatbot-badge');
        if (badge) badge.style.display = 'none';
    },
    
    async sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input?.value.trim();
        
        if (!message) return;
        
        console.log('[CHATBOT] Enviando mensagem:', message);
        
        // Adicionar mensagem do usuário
        this.conversationHistory.push({ role: 'user', content: message });
        this.addMessageToUI('user', message);
        input.value = '';
        
        try {
            // Enviar para API
            const token = localStorage.getItem('authToken');
            const response = await fetch('/api/ia/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(token && { 'Authorization': `Bearer ${token}` })
                },
                body: JSON.stringify({
                    mensagem: message,
                    historico: this.conversationHistory
                })
            });
            
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const data = await response.json();
            const aiResponse = data.resposta || 'Desculpe, não consegui processar sua pergunta.';
            
            // Adicionar resposta da IA
            this.conversationHistory.push({ role: 'assistant', content: aiResponse });
            this.addMessageToUI('ai', aiResponse);
            
        } catch (error) {
            console.error('[CHATBOT] Erro:', error);
            
            let response = 'Desculpe, não consegui processar sua pergunta no momento.';
            
            // Respostas padrão
            const defaultResponses = {
                'oi': 'Olá! Como posso ajudá-lo com seus estudos?',
                'curso': 'Todos os cursos estão disponíveis na aba "Cursos". Qual deles tem interesse?',
                'progresso': 'Você pode ver seu progresso geral na aba "Progresso".',
                'certificado': 'Você pode visualizar seus certificados na aba "Certificados".',
                'ajuda': 'Estou aqui para ajudar! Você pode me perguntar sobre cursos, progresso, ou como usar a plataforma.',
            };
            
            const lowerMessage = message.toLowerCase();
            for (const [keyword, resp] of Object.entries(defaultResponses)) {
                if (lowerMessage.includes(keyword)) {
                    response = resp;
                    break;
                }
            }
            
            this.conversationHistory.push({ role: 'assistant', content: response });
            this.addMessageToUI('ai', response);
        }
        
        this.saveConversationHistory();
    },
    
    addMessageToUI(role, content) {
        const messagesContainer = document.getElementById('chatbot-messages');
        if (!messagesContainer) return;
        
        const messageEl = document.createElement('div');
        messageEl.className = `message ${role}`;
        messageEl.textContent = content;
        
        messagesContainer.appendChild(messageEl);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    },
    
    saveConversationHistory() {
        sessionStorage.setItem('chatbotHistory', JSON.stringify(this.conversationHistory));
    },
    
    loadConversationHistory() {
        const saved = sessionStorage.getItem('chatbotHistory');
        if (saved) {
            this.conversationHistory = JSON.parse(saved);
            // Recarregar mensagens na UI
            const container = document.getElementById('chatbot-messages');
            if (container && this.conversationHistory.length > 0) {
                const messages = container.querySelectorAll('.message');
                if (messages.length <= 1) { // Se só tiver a mensagem inicial
                    this.conversationHistory.forEach(msg => {
                        if (msg.role !== 'system') {
                            this.addMessageToUI(msg.role, msg.content);
                        }
                    });
                }
            }
        }
    }
};

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    ChatbotFlutuante.init();
});
