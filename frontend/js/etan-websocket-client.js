/*
JavaScript WebSocket Client para Atividades ETAN
Comunica com servidor Flask-SocketIO
*/

class ETANWebSocketClient {
    constructor(activityId, userId, options = {}) {
        this.activityId = activityId;
        this.userId = userId;
        this.socket = null;
        this.options = {
            autoConnect: true,
            reconnection: true,
            reconnectionAttempts: 5,
            reconnectionDelay: 1000,
            ...options
        };
        
        this.listeners = new Map();
        this.pendingMessages = [];
        
        if (this.options.autoConnect) {
            this.connect();
        }
    }
    
    /**
     * Conectar ao servidor WebSocket
     */
    connect() {
        try {
            // Socket.IO client
            this.socket = io({
                reconnection: this.options.reconnection,
                reconnectionAttempts: this.options.reconnectionAttempts,
                reconnectionDelay: this.options.reconnectionDelay
            });
            
            // Eventos de conexão
            this.socket.on('connect', () => this.handleConnect());
            this.socket.on('disconnect', () => this.handleDisconnect());
            this.socket.on('connection_response', (data) => this.emit('connection', data));
            this.socket.on('error', (error) => this.handleError(error));
            
            // Eventos de atividade
            this.socket.on('activity_joined', (data) => this.emit('activity_joined', data));
            this.socket.on('activity_started', (data) => this.emit('activity_started', data));
            this.socket.on('progress_update', (data) => this.emit('progress', data));
            this.socket.on('activity_completed', (data) => this.emit('completed', data));
            
            // Eventos de captura
            this.socket.on('preview_received', (data) => this.emit('preview', data));
            this.socket.on('capture_processed', (data) => this.emit('capture', data));
            this.socket.on('capture_error_handled', (data) => this.emit('capture_error', data));
            
            // Eventos de simulador
            this.socket.on('simulator_open', (data) => this.emit('simulator_open', data));
            this.socket.on('simulator_closed', (data) => this.emit('simulator_closed', data));
            
            // Eventos de instrutor
            this.socket.on('instructor_feedback', (data) => this.emit('instructor_feedback', data));
            
            console.log('✅ WebSocket client pronto');
        } catch (error) {
            console.error('❌ Erro ao conectar WebSocket:', error);
            this.handleConnectionError(error);
        }
    }
    
    /**
     * Desconectar do servidor
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            console.log('🔌 Desconectado do servidor');
        }
    }
    
    /**
     * =================================================
     * VIDA DA ATIVIDADE
     * =================================================
     */
    
    /**
     * Entrar em uma atividade
     */
    joinActivity() {
        this.emit_server('activity_join', {
            activity_id: this.activityId,
            user_id: this.userId,
            lesson_id: this.getLessonId()
        });
    }
    
    /**
     * Iniciar atividade
     */
    startActivity(type = 'practice') {
        this.emit_server('activity_start', {
            activity_id: this.activityId,
            user_id: this.userId,
            activity_type: type
        });
    }
    
    /**
     * Atualizar progresso em tempo real
     */
    updateProgress(fase, score, tempo_gasto) {
        this.emit_server('activity_progress', {
            activity_id: this.activityId,
            user_id: this.userId,
            fase: fase,
            score: score,
            tempo_gasto: tempo_gasto
        });
    }
    
    /**
     * Completar atividade
     */
    completeActivity(score, timeTotal, attempts, responses = {}) {
        this.emit_server('activity_complete', {
            activity_id: this.activityId,
            user_id: this.userId,
            score: score,
            time_total: timeTotal,
            attempts: attempts,
            responses: responses
        });
    }
    
    /**
     * Sair da atividade
     */
    leaveActivity() {
        this.emit_server('activity_leave', {
            activity_id: this.activityId,
            user_id: this.userId
        });
    }
    
    /**
     * =================================================
     * CAPTURA BIOMÉTRICA
     * =================================================
     */
    
    /**
     * Enviar preview de captura
     */
    sendPreview(imageData, nfiqScore, roiDetected = false) {
        this.emit_server('capture_preview', {
            activity_id: this.activityId,
            image_data: imageData,
            nfiq_score: nfiqScore,
            roi_detected: roiDetected
        });
    }
    
    /**
     * Enviar imagem capturada
     */
    sendCapturedImage(imageData, nfiqScore, quality = 'good') {
        this.emit_server('capture_image', {
            activity_id: this.activityId,
            user_id: this.userId,
            image_data: imageData,
            nfiq_score: nfiqScore,
            image_quality: quality
        });
    }
    
    /**
     * Reportar erro de captura
     */
    reportCaptureError(errorCode, errorMessage) {
        this.emit_server('capture_error', {
            activity_id: this.activityId,
            error_code: errorCode,
            error_message: errorMessage
        });
    }
    
    /**
     * =================================================
     * SIMULADOR
     * =================================================
     */
    
    /**
     * Requisitar abertura de simulador
     */
    requestSimulator(type = 'practice', fase = 4) {
        this.emit_server('simulator_request', {
            activity_id: this.activityId,
            type: type,
            fase: fase
        });
    }
    
    /**
     * Notificar que simulador foi fechado
     */
    closeSimulator(resultado = {}) {
        this.emit_server('simulator_close', {
            activity_id: this.activityId,
            resultado: resultado
        });
    }
    
    /**
     * =================================================
     * EVENT LISTENERS
     * =================================================
     */
    
    /**
     * Registrar listener para evento
     */
    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);
    }
    
    /**
     * Remover listener
     */
    off(event, callback) {
        if (this.listeners.has(event)) {
            const callbacks = this.listeners.get(event);
            const index = callbacks.indexOf(callback);
            if (index > -1) callbacks.splice(index, 1);
        }
    }
    
    /**
     * Disparar evento local
     */
    emit(event, data) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`❌ Erro em listener ${event}:`, error);
                }
            });
        }
    }
    
    /**
     * =================================================
     * INTERNO
     * =================================================
     */
    
    /**
     * Enviar evento ao servidor
     */
    emit_server(event, data) {
        if (this.socket && this.socket.connected) {
            this.socket.emit(event, data);
            console.log(`📤 Enviado: ${event}`, data);
        } else {
            console.warn(`⚠️ WebSocket não conectado. Enfileirando: ${event}`);
            this.pendingMessages.push({ event, data });
        }
    }
    
    /**
     * Handler de conexão
     */
    handleConnect() {
        console.log('🔗 Conectado ao servidor WebSocket');
        this.emit('connected', { status: 'online' });
        
        // Enviar mensagens enfileiradas
        while (this.pendingMessages.length > 0) {
            const { event, data } = this.pendingMessages.shift();
            this.emit_server(event, data);
        }
    }
    
    /**
     * Handler de desconexão
     */
    handleDisconnect() {
        console.log('🔌 Desconectado do servidor');
        this.emit('disconnected', { status: 'offline' });
    }
    
    /**
     * Handler de erro
     */
    handleError(error) {
        console.error('❌ Erro WebSocket:', error);
        this.emit('error', { error });
    }
    
    /**
     * Handler de erro de conexão
     */
    handleConnectionError(error) {
        console.error('❌ Erro de conexão:', error);
        if (this.socket) {
            setTimeout(() => this.socket.connect(), this.options.reconnectionDelay);
        }
    }
    
    /**
     * Obter lesson_id da página
     */
    getLessonId() {
        // Pode vir de atributo data-* ou variável global
        return window.lessonId || document.documentElement.getAttribute('data-lesson-id') || null;
    }
    
    /**
     * Verificar se está conectado
     */
    isConnected() {
        return this.socket && this.socket.connected;
    }
    
    /**
     * Get conexão info
     */
    getConnectionInfo() {
        return {
            connected: this.isConnected(),
            activityId: this.activityId,
            userId: this.userId,
            socketId: this.socket?.id
        };
    }
}

// =======================================================
// INICIALIZAR CLIENTE GLOBALMENTE
// =======================================================

window.etanWebSocket = null;

function initializeETANWebSocket(activityId, userId, options = {}) {
    if (!window.etanWebSocket) {
        window.etanWebSocket = new ETANWebSocketClient(activityId, userId, options);
    }
    return window.etanWebSocket;
}

// Permitir uso em iframes
if (window.self === window.top) {
    console.log('🌐 ETAN WebSocket disponível como window.etanWebSocket');
}
