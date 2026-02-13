/* ==========================================
   UTILITÁRIOS JAVASCRIPT
   ========================================== */

// API base URL
const API_URL = 'http://localhost:8000/api';

// ==========================================
// GERENCIAMENTO DE TOKEN
// ==========================================

const TokenManager = {
    set: (token) => {
        localStorage.setItem('authToken', token);
    },
    
    get: () => {
        return localStorage.getItem('authToken');
    },
    
    remove: () => {
        localStorage.removeItem('authToken');
    },
    
    isAuthenticated: () => {
        return !!localStorage.getItem('authToken');
    }
};

// ==========================================
// REQUISIÇÕES API
// ==========================================

const ApiClient = {
    async request(method, endpoint, data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${TokenManager.get()}`
            }
        };

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${API_URL}${endpoint}`, options);
            
            if (response.status === 401) {
                // Token expirado
                TokenManager.remove();
                window.location.href = '/pages/login.html';
                return;
            }

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.erro || 'Erro ao fazer requisição');
            }

            return result;
        } catch (error) {
            console.error('Erro na requisição:', error);
            throw error;
        }
    },

    get: (endpoint) => ApiClient.request('GET', endpoint),
    post: (endpoint, data) => ApiClient.request('POST', endpoint, data),
    put: (endpoint, data) => ApiClient.request('PUT', endpoint, data),
    delete: (endpoint) => ApiClient.request('DELETE', endpoint)
};

// ==========================================
// AUTENTICAÇÃO
// ==========================================

const Auth = {
    async login(email, senha) {
        try {
            const result = await ApiClient.post('/auth/login', { email, senha });
            TokenManager.set(result.token);
            return result;
        } catch (error) {
            console.error('Erro no login:', error);
            throw error;
        }
    },

    async register(email, nome, senha, hospitalId) {
        try {
            return await ApiClient.post('/auth/register', {
                email,
                nome,
                senha,
                hospital_id: hospitalId
            });
        } catch (error) {
            console.error('Erro no registro:', error);
            throw error;
        }
    },

    logout() {
        TokenManager.remove();
        window.location.href = '/index.html';
    },

    isAuthenticated: () => TokenManager.isAuthenticated()
};

// ==========================================
// UTILITÁRIOS DE UI
// ==========================================

const UI = {
    showMessage: (message, type = 'info') => {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        document.body.insertBefore(alertDiv, document.body.firstChild);

        setTimeout(() => alertDiv.remove(), 5000);
    },

    showError: (message) => UI.showMessage(message, 'danger'),
    showSuccess: (message) => UI.showMessage(message, 'success'),
    showInfo: (message) => UI.showMessage(message, 'info'),

    loading: (show = true) => {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.style.display = show ? 'block' : 'none';
        }
    }
};

// ==========================================
// INICIALIZAR
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    // Adicionar event listeners globais se necessário
    console.log('JavaScript inicializado');
});
