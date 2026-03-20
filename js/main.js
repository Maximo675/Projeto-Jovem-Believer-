/* ==========================================
   UTILITÁRIOS JAVASCRIPT
   ========================================== */

// API base URL — dinâmica: funciona em localhost (dev) e em nuvem (prod)
const API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://127.0.0.1:5001/api'
    : window.location.origin + '/api';

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
        console.log(`[API] ${method} ${endpoint}`, data || '');
        
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
            const url = `${API_URL}${endpoint}`;
            console.log(`[API] Fetching: ${url}`);
            
            const response = await fetch(url, options);
            console.log(`[API] Response status: ${response.status}`);
            
            if (response.status === 401) {
                // Token expirado
                TokenManager.remove();
                window.location.href = '/pages/login.html';
                return;
            }

            const result = await response.json();
            console.log(`[API] Response body:`, result);

            if (!response.ok) {
                console.error(`[API] Error response:`, result);
                throw new Error(result.erro || `HTTP ${response.status}: Erro ao fazer requisição`);
            }

            console.log(`[API] Success response`);
            return result;
        } catch (error) {
            console.error(`[API] Catch error:`, error);
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
    async login(email, password) {
        try {
            console.log('[AUTH] Login attempt:', email);
            const result = await ApiClient.post('/auth/login', { email, senha: password });
            TokenManager.set(result.token);
            console.log('[AUTH] Login success');
            return result;
        } catch (error) {
            console.error('[AUTH] Login error:', error);
            throw error;
        }
    },

    async register(email, nome, senha, hospitalId) {
        try {
            console.log('[AUTH] Register attempt:', { email, nome, hospitalId });
            const result = await ApiClient.post('/auth/register', {
                email,
                nome,
                senha,
                hospital_id: hospitalId
            });
            console.log('[AUTH] Register success:', result);
            return result;
        } catch (error) {
            console.error('[AUTH] Register error:', error);
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
// INTERFACE DO USUÁRIO
// ==========================================

const UI = {
    showError: (message) => {
        const container = document.getElementById('alertContainer');
        if (!container) {
            alert(message);
            return;
        }
        
        const alert = document.createElement('div');
        alert.className = 'alert alert-error';
        alert.innerHTML = `
            <div style="background: #f8d7da; color: #721c24; padding: 12px 20px; border-radius: 4px; border-left: 4px solid #dc3545; margin-bottom: 16px;">
                <strong>Erro:</strong> ${message}
            </div>
        `;
        container.innerHTML = '';
        container.appendChild(alert);
        
        setTimeout(() => {
            alert.remove();
        }, 5000);
    },

    showSuccess: (message) => {
        const container = document.getElementById('alertContainer');
        if (!container) {
            alert(message);
            return;
        }
        
        const alert = document.createElement('div');
        alert.className = 'alert alert-success';
        alert.innerHTML = `
            <div style="background: #d4edda; color: #155724; padding: 12px 20px; border-radius: 4px; border-left: 4px solid #28a745; margin-bottom: 16px;">
                <strong>Sucesso:</strong> ${message}
            </div>
        `;
        container.innerHTML = '';
        container.appendChild(alert);
    },

    loading: (show) => {
        const registerForm = document.getElementById('registerForm');
        const submitBtn = registerForm?.querySelector('button[type="submit"]');
        
        if (!submitBtn) return;
        
        if (show) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '⏳ Processando...';
            submitBtn.style.opacity = '0.6';
        } else {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Criar Conta';
            submitBtn.style.opacity = '1';
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
