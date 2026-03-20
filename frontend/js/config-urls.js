/**
 * CONFIG_URLS.JS
 * ===============================================
 * Configuração centralizada de todas as URLs e portas
 * Este arquivo é compartilhado entre frontend e iframe
 * ===============================================
 */

class ConfigURLs {
    constructor() {
        // Detectar ambiente baseado na URL
        const hostname = window.location.hostname;
        const protocol = window.location.protocol;
        
        // Configurar portas baseado no ambiente
        this.isDevelopment = hostname === 'localhost' || hostname === '127.0.0.1';
        
        // SERVIDOR FLASK - Dinâmico: usa localhost:5001 em dev, mesma origem em produção
        this.FLASK_HOST = this.isDevelopment ? 'localhost' : hostname;
        this.FLASK_PORT = this.isDevelopment ? 5001 : (window.location.port || '');
        this.FLASK_URL = this.isDevelopment
            ? `${protocol}//${this.FLASK_HOST}:5001`
            : window.location.origin;
        
        // DEVICE SERVICE - Captura Biométrica (sempre local, porta 5000)
        this.DEVICE_PORT = 5000;
        this.DEVICE_URL = `http://localhost:${this.DEVICE_PORT}`;
        
        // PROXY BRIDGE - Intermediário Node (Openbio Bridge - sempre local, porta 3333 - HTTPS)
        this.PROXY_PORT = 3333;
        this.PROXY_URL = `https://localhost:${this.PROXY_PORT}`;
        
        // WEBSOCKET CONFIGURATION - Dinâmico
        this.WEBSOCKET_NAMESPACE = this.isDevelopment
            ? 'http://localhost:5001/socket.io'
            : window.location.origin + '/socket.io';
        this.WEBSOCKET_OPTIONS = {
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            reconnectionAttempts: 5,
            transports: ['websocket', 'polling']
        };
    }
    
    /**
     * API Endpoints - Plataforma de Ensino
     */
    get API_BASE() {
        return `${this.FLASK_URL}/api`;
    }
    
    get API_ACTIVITIES() {
        return `${this.API_BASE}/activities`;
    }
    
    get API_USERS() {
        return `${this.API_BASE}/users`;
    }
    
    get API_COURSES() {
        return `${this.API_BASE}/courses`;
    }
    
    /**
     * Device Service Endpoints - Captura Biométrica
     */
    get DEVICE_CAPTURE() {
        return `${this.DEVICE_URL}/capture`;
    }
    
    get DEVICE_STATUS() {
        return `${this.DEVICE_URL}/status`;
    }
    
    /**
     * Proxy Endpoints - Intermediário
     */
    get PROXY_BIOMETRIC() {
        return `${this.PROXY_URL}/api/biometric`;
    }
    
    /**
     * Verificar disponibilidade do serviço
     */
    async checkService(url, timeout = 5000) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), timeout);
            
            const response = await fetch(url, {
                method: 'GET',
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            return response.ok;
        } catch (error) {
            console.warn(`⚠️ Serviço indisponível: ${url}`, error);
            return false;
        }
    }
    
    /**
     * Obter status de todos os serviços
     */
    async getServicesStatus() {
        return {
            flask: await this.checkService(`${this.FLASK_URL}/health`),
            device: await this.checkService(`${this.DEVICE_URL}/status`),
            proxy: await this.checkService(`${this.PROXY_URL}/health`)
        };
    }
    
    /**
     * Log die configuração (apenas em desenvolvimento)
     */
    logConfig() {
        if (this.isDevelopment) {
            console.group('🔧 CONFIG URLs');
            console.log('Flask:', this.FLASK_URL);
            console.log('Device:', this.DEVICE_URL);
            console.log('Proxy:', this.PROXY_URL);
            console.log('WebSocket:', this.WEBSOCKET_NAMESPACE);
            console.groupEnd();
        }
    }
}

// Inicializar globalmente
window.CONFIG_URLS = new ConfigURLs();

// Log no console
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.CONFIG_URLS.logConfig();
}
