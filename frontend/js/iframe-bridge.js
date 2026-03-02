/**
 * Iframe Bridge para Comunicação Entre Atividades e Página Principal
 * Permite que iframes se comuniquem com o servidor via postMessage e WebSocket
 */

class IFrameBridge {
    constructor(parentWindow = window.parent) {
        this.parentWindow = parentWindow;
        this.isIframe = window.self !== window.top;
        this.messageHandlers = new Map();
        this.setupMessageListener();
        this.setupXFrameMessaging();
    }
    
    /**
     * Escutar mensagens de iframes filhos
     */
    setupMessageListener() {
        window.addEventListener('message', (event) => {
            // Validar origem por segurança
            if (!this.isValidOrigin(event.origin)) {
                console.warn(`⚠️ Origem não confiável: ${event.origin}`);
                return;
            }
            
            const data = event.data;
            if (data.type === 'IFRAME_MESSAGE') {
                this.handleIframeMessage(data.payload, event.source);
            }
        });
    }
    
    /**
     * Setup para comunicação cross-frame
     */
    setupXFrameMessaging() {
        // Se for um iframe, pode enviar mensagens para o pai
        if (this.isIframe) {
            window.iframeBridge = {
                send: (action, payload) => this.sendToParent(action, payload),
                connect: (activityId, userId) => this.connectToWebSocket(activityId, userId)
            };
        }
    }
    
    /**
     * =================================================
     * ENVIAR PARA PAI
     * =================================================
     */
    
    /**
     * Enviar mensagem para a página pai
     */
    sendToParent(action, payload = {}) {
        if (!this.isIframe) {
            console.warn('❌ Não é um iframe - não pode enviar para pai');
            return;
        }
        
        const message = {
            type: 'IFRAME_MESSAGE',
            action: action,
            payload: payload,
            source: 'iframe',
            timestamp: Date.now()
        };
        
        this.parentWindow.postMessage(message, '*');
        console.log(`📤 Mensagem enviada ao pai: ${action}`, payload);
    }
    
    /**
     * Atividade iniciada
     */
    notifyActivityStarted(activityId) {
        this.sendToParent('ACTIVITY_STARTED', { activityId });
    }
    
    /**
     * Progresso atualizado
     */
    notifyProgress(activityId, fase, score, tempo) {
        this.sendToParent('ACTIVITY_PROGRESS', {
            activityId,
            fase,
            score,
            tempo_gasto: tempo
        });
    }
    
    /**
     * Atividade completada
     */
    notifyCompletion(activityId, score, timeTotal, attempts, responses = {}) {
        this.sendToParent('ACTIVITY_COMPLETED', {
            activityId,
            score,
            time_total: timeTotal,
            attempts,
            responses
        });
    }
    
    /**
     * Requisitar abertura de simulador
     */
    requestSimulator(activityId, tipo = 'practice', fase = 4) {
        this.sendToParent('SIMULATOR_REQUEST', {
            activityId,
            type: tipo,
            fase
        });
    }
    
    /**
     * Reportar erro
     */
    reportError(activityId, errorCode, errorMessage) {
        this.sendToParent('ERROR_REPORT', {
            activityId,
            error_code: errorCode,
            error_message: errorMessage
        });
    }
    
    /**
     * =================================================
     * RECEBER DO PAI (Se for página pai)
     * =================================================
     */
    
    /**
     * Registrar handler para msg de iframe
     */
    onIframeMessage(action, callback) {
        if (!this.messageHandlers.has(action)) {
            this.messageHandlers.set(action, []);
        }
        this.messageHandlers.get(action).push(callback);
    }
    
    /**
     * Lidar com mensagem de iframe
     */
    handleIframeMessage(payload, source) {
        const action = payload.action;
        
        if (this.messageHandlers.has(action)) {
            this.messageHandlers.get(action).forEach(handler => {
                try {
                    handler(payload, source);
                } catch (error) {
                    console.error(`❌ Erro em handler ${action}:`, error);
                }
            });
        }
    }
    
    /**
     * Enviar mensagem para iframe específico
     */
    sendToIframe(iframeElement, action, payload = {}) {
        const message = {
            type: 'PARENT_MESSAGE',
            action: action,
            payload: payload,
            source: 'parent',
            timestamp: Date.now()
        };
        
        if (iframeElement.contentWindow) {
            iframeElement.contentWindow.postMessage(message, '*');
            console.log(`📤 Mensagem enviada ao iframe: ${action}`, payload);
        }
    }
    
    /**
     * Broadcast para todos os iframes
     */
    broadcastToAllIframes(action, payload = {}) {
        const iframes = document.querySelectorAll('iframe[src*="/activities/"]');
        iframes.forEach(iframe => {
            this.sendToIframe(iframe, action, payload);
        });
    }
    
    /**
     * =================================================
     * CONECTAR WEBSOCKET (Do iframe)
     * =================================================
     */
    
    /**
     * Conectar a WebSocket do servidor
     */
    connectToWebSocket(activityId, userId) {
        if (!window.etanWebSocket) {
            console.log('🔌 Inicializando WebSocket...');
            initializeETANWebSocket(activityId, userId);
        }
        
        const ws = window.etanWebSocket;
        
        // Aguardar conexão
        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
                reject(new Error('Timeout ao conectar WebSocket'));
            }, 5000);
            
            if (ws.isConnected()) {
                clearTimeout(timeout);
                resolve(ws);
            } else {
                // Aguardar evento de conexão
                ws.on('connected', () => {
                    clearTimeout(timeout);
                    resolve(ws);
                });
                
                ws.on('error', (error) => {
                    clearTimeout(timeout);
                    reject(error);
                });
            }
        });
    }
    
    /**
     * =================================================
     * HELPERS
     * =================================================
     */
    
    /**
     * Validar origem da mensagem
     */
    isValidOrigin(origin) {
        // Aceitar localhost, domínio local, e domínios configurados
        const allowedOrigins = [
            window.location.origin,
            'http://localhost:*',
            'http://127.0.0.1:*'
        ];
        
        // Validação simples - em produção, implementar whitelist propriamente
        return origin === window.location.origin || 
               origin.includes('localhost') || 
               origin.includes('127.0.0.1');
    }
    
    /**
     * Get informações de conexão
     */
    getConnectionInfo() {
        return {
            isIframe: this.isIframe,
            hasParent: this.parentWindow !== window,
            webSocketConnected: window.etanWebSocket?.isConnected?.() || false,
            webSocketInfo: window.etanWebSocket?.getConnectionInfo?.()
        };
    }
}

// =======================================================
// INICIALIZAR GLOBALMENTE
// =======================================================

window.iframeBridge = new IFrameBridge();

// Se NÃO é iframe, configurar handlers para atividades
if (window.self === window.top) {
    window.iframeBridge.onIframeMessage('ACTIVITY_STARTED', (payload, source) => {
        console.log('✅ Atividade iniciada no iframe:', payload);
        
        // Registrar no WebSocket se disponível
        if (window.etanWebSocket) {
            window.etanWebSocket.startActivity();
        }
    });
    
    window.iframeBridge.onIframeMessage('ACTIVITY_PROGRESS', (payload, source) => {
        console.log('📊 Progresso da atividade:', payload);
        
        // Atualizar WebSocket
        if (window.etanWebSocket) {
            window.etanWebSocket.updateProgress(payload.fase, payload.score, payload.tempo_gasto);
        }
    });
    
    window.iframeBridge.onIframeMessage('ACTIVITY_COMPLETED', (payload, source) => {
        console.log('🏁 Atividade completada:', payload);
        
        // Salvar no servidor + WebSocket
        if (window.etanWebSocket) {
            window.etanWebSocket.completeActivity(
                payload.score,
                payload.time_total,
                payload.attempts,
                payload.responses
            );
        }
    });
    
    window.iframeBridge.onIframeMessage('SIMULATOR_REQUEST', (payload, source) => {
        console.log('🖥️ Simulador requisitado:', payload);
        
        // Enviar command para WebSocket
        if (window.etanWebSocket) {
            window.etanWebSocket.requestSimulator(payload.type, payload.fase);
        }
        
        // Abrir simulador em novo popup (opcional)
        openSimulatorWindow(payload.type, payload.fase);
    });
    
    window.iframeBridge.onIframeMessage('ERROR_REPORT', (payload, source) => {
        console.error('❌ Erro reportado:', payload);
        
        // Atualizar WebSocket
        if (window.etanWebSocket) {
            window.etanWebSocket.reportCaptureError(
                payload.error_code,
                payload.error_message
            );
        }
    });
}

// =======================================================
// HELPERS DA PÁGINA PRINCIPAL
// =======================================================

/**
 * Abrir janela de simulador
 */
function openSimulatorWindow(simulatorType, fase = 4) {
    const simulatorUrl = '/activities/biometric-capture-simulator.html?mode=' + simulatorType + '&fase=' + fase;
    
    // Abrir em popup
    const popup = window.open(simulatorUrl, 'BiometricSimulator', 'width=1000,height=800');
    
    if (popup) {
        console.log('🖥️ Janela de simulador aberta');
    } else {
        console.error('❌ Bloqueador de pop-up impediu abertura');
    }
}

/**
 * Initializar atividad com WebSocket
 */
async function initializeActivityWithWebSocket(activityId, userId) {
    try {
        // Criar cliente WebSocket
        const ws = initializeETANWebSocket(activityId, userId);
        
        // Aguardar conexão
        await new Promise(resolve => {
            if (ws.isConnected()) {
                resolve();
            } else {
                ws.on('connected', () => resolve());
                setTimeout(() => resolve(), 3000);
            }
        });
        
        // Entrar na atividade
        ws.joinActivity();
        
        console.log('✅ Atividade inicializada com WebSocket');
        return ws;
    } catch (error) {
        console.error('❌ Erro ao inicializar atividade:', error);
        throw error;
    }
}

console.log('🌉 Iframe Bridge carregado');
