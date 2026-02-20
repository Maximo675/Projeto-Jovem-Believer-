/**
 * Dashboard.js - Sistema de Aprendizado Interativo
 * Gerencia cursos, progresso, IA e funcionalidades do dashboard
 */

const Dashboard = {
    user: null,
    courses: [],
    userProgress: {},
    
    async init() {
        console.log('[DASHBOARD] Inicializando...');
        
        // Verificar autenticação
        const token = this.checkAuth();
        if (!token) return;
        
        // Carregar dados do usuário
        this.loadUserInfo(token);
        
        // Carregar cursos
        await this.loadCourses();
        
        // Carregar progresso
        await this.loadUserProgress();
        
        // Carregar certificados
        await this.loadCertificates();
        
        // Setup de eventos
        this.setupEventListeners();
        
        console.log('[DASHBOARD] Inicializado com sucesso!');
    },
    
    checkAuth() {
        const token = localStorage.getItem('authToken');
        if (!token) {
            console.warn('[DASHBOARD] Token não encontrado, redirecionando para login');
            window.location.href = '/pages/login.html';
            return null;
        }
        return token;
    },
    
    loadUserInfo(token) {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(
                atob(base64).split('').map((c) => {
                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                }).join('')
            );
            
            this.user = JSON.parse(jsonPayload);
            
            // Atualizar UI
            const userName = document.getElementById('userName');
            if (userName) userName.textContent = `${this.user.email}`;
            
            const userAvatar = document.getElementById('userAvatar');
            if (userAvatar) userAvatar.textContent = (this.user.email?.charAt(0) || 'U').toUpperCase();
            
            console.log('[DASHBOARD] Usuário carregado:', this.user);
        } catch (error) {
            console.error('[DASHBOARD] Erro ao decodificar token:', error);
        }
    },
    
    async loadCourses() {
        try {
            console.log('[DASHBOARD] Carregando cursos...');
            
            const response = await fetch('/api/courses');
            const data = await response.json();
            
            this.courses = data.cursos || [];
            console.log('[DASHBOARD] Cursos carregados:', this.courses.length);
            
            this.renderCourses();
            this.updateStats();
        } catch (error) {
            console.error('[DASHBOARD] Erro ao carregar cursos:', error);
            document.getElementById('coursesContainer').innerHTML = 
                '<div class="loading" style="color: #d32f2f;">Erro ao carregar cursos. Tente novamente.</div>';
        }
    },
    
    async loadUserProgress() {
        try {
            console.log('[DASHBOARD] Carregando progresso do usuário...');
            
            const response = await fetch(`/api/users/progress`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                this.userProgress = data.progresso || [];
                console.log('[DASHBOARD] Progresso carregado:', this.userProgress.length);
                this.renderProgress();
            } else {
                console.warn('[DASHBOARD] Erro ao carregar progresso:', response.status);
                this.renderProgressEmpty();
            }
        } catch (error) {
            console.warn('[DASHBOARD] Não foi possível carregar progresso:', error);
            this.renderProgressEmpty();
        }
    },
    
    renderCourses() {
        const container = document.getElementById('coursesContainer');
        
        if (!this.courses || this.courses.length === 0) {
            container.innerHTML = '<div class="loading">Nenhum curso disponível no momento</div>';
            return;
        }
        
        container.innerHTML = this.courses.map(course => `
            <div class="course-card">
                <div class="course-header">
                    <div class="course-icon">${this.getIconForLevel(course.nivel)}</div>
                    <span class="course-level">${course.nivel || 'Básico'}</span>
                </div>
                
                <h3 class="course-title">${course.titulo}</h3>
                <p class="course-description">${course.descricao || 'Curso estruturado para seu aprendizado'}</p>
                
                <div class="course-footer">
                    <div class="course-progress">
                        <div class="progress-label">
                            ${this.getProgressForCourse(course.id)}% completo
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${this.getProgressForCourse(course.id)}%"></div>
                        </div>
                    </div>
                    <div class="course-action">
                        <button class="btn" onclick="Dashboard.startCourse(${course.id}, '${course.titulo}')">
                            ${this.getProgressForCourse(course.id) > 0 ? 'Continuar' : 'Começar'}
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    },
    
    getIconForLevel(level) {
        const icons = {
            'basico': '🌱',
            'intermediario': '📚',
            'avancado': '🚀'
        };
        return icons[level?.toLowerCase()] || '📖';
    },
    
    getProgressForCourse(courseId) {
        return Math.round((Math.random() * 100)); // TODO: Conectar com API real
    },
    
    renderProgress() {
        const container = document.getElementById('progressContainer');
        
        if (!this.userProgress || this.userProgress.length === 0) {
            container.innerHTML = `
                <div style="background: white; padding: 40px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                    <p style="color: #999; font-size: 1.1rem;">Você ainda não iniciou nenhum curso</p>
                    <a href="#" onclick="Dashboard.showTab('courses')" style="color: var(--primary-blue); text-decoration: none; font-weight: 600;">
                        Explorar Cursos →
                    </a>
                </div>
            `;
            return;
        }
        
        container.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
                ${this.userProgress.map(p => `
                    <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                        <h3 style="margin: 0 0 12px 0; color: #1a1a1a;">Curso ${p.curso_id || '?'}</h3>
                        <div style="margin-bottom: 12px;">
                            <div style="height: 8px; background: #e0e0e0; border-radius: 4px; overflow: hidden;">
                                <div style="height: 100%; background: linear-gradient(90deg, var(--primary-blue), var(--success-green)); width: ${p.percentual_completo || 0}%;"></div>
                            </div>
                            <p style="margin: 8px 0 0 0; font-weight: 600; color: var(--primary-blue);">${p.percentual_completo || 0}% Completo</p>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    },
    
    renderProgressEmpty() {
        const container = document.getElementById('progressContainer');
        container.innerHTML = `
            <div style="background: white; padding: 40px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <p style="color: #999; font-size: 1.1rem;">Você ainda não iniciou nenhum curso</p>
                <a href="#" onclick="Dashboard.showTab('courses')" style="color: var(--primary-blue); text-decoration: none; font-weight: 600;">
                    Explorar Cursos →
                </a>
            </div>
        `;
    },
    
    async loadCertificates() {
        try {
            console.log('[DASHBOARD] Carregando certificados...');
            
            const response = await fetch(`/api/users/certificates`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                this.renderCertificates(data.certificados || []);
            } else {
                this.renderCertificatesEmpty();
            }
        } catch (error) {
            console.warn('[DASHBOARD] Não foi possível carregar certificados:', error);
            this.renderCertificatesEmpty();
        }
    },
    
    renderCertificates(certificates) {
        const container = document.getElementById('certificatesContainer');
        
        if (!certificates || certificates.length === 0) {
            container.innerHTML = `
                <div style="background: white; padding: 40px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                    <p style="color: #999; font-size: 1.1rem;">Você ainda não tem certificados</p>
                    <p style="color: #999; margin-top: 8px;">Complete cursos para obter certificados</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
                ${certificates.map(c => `
                    <div style="background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); border-top: 4px solid var(--primary-blue);">
                        <div style="text-align: center; margin-bottom: 16px; font-size: 2.5rem;">🏆</div>
                        <h3 style="margin: 0 0 8px 0; color: #1a1a1a; text-align: center;">Certificado</h3>
                        <p style="margin: 0 0 12px 0; color: #666; text-align: center;">${c.titulo || 'Conclusão de Curso'}</p>
                        <p style="margin: 0; color: #999; font-size: 0.85rem; text-align: center;">
                            ${c.data_emissao ? new Date(c.data_emissao).toLocaleDateString('pt-BR') : 'Data'}
                        </p>
                    </div>
                `).join('')}
            </div>
        `;
    },
    
    renderCertificatesEmpty() {
        const container = document.getElementById('certificatesContainer');
        container.innerHTML = `
            <div style="background: white; padding: 40px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <p style="color: #999; font-size: 1.1rem;">Você ainda não tem certificados</p>
                <p style="color: #999; margin-top: 8px;">Complete cursos para obter certificados</p>
            </div>
        `;
    },
    
    updateStats() {
        document.getElementById('totalCourses').textContent = this.courses.length;
        document.getElementById('enrolledCourses').textContent = Math.ceil(this.courses.length * 0.7);
        document.getElementById('completedCourses').textContent = Math.floor(this.courses.length * 0.3);
        
        const overallProgress = Math.round(
            this.courses.reduce((sum, c) => sum + this.getProgressForCourse(c.id), 0) / this.courses.length
        );
        document.getElementById('overallProgress').textContent = overallProgress + '%';
    },
    
    startCourse(courseId, courseTitle) {
        console.log('[DASHBOARD] Iniciando curso:', courseId, courseTitle);
        
        // Salvar curso atual
        sessionStorage.setItem('currentCourse', JSON.stringify({
            id: courseId,
            title: courseTitle
        }));
        
        // Redirecionar para página do curso
        window.location.href = `/pages/course.html?id=${courseId}`;
    },
    
    setupEventListeners() {
        // Menu de navegação (sidebar)
        const menuItems = document.querySelectorAll('.menu-item');
        menuItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Remover active de todos
                menuItems.forEach(m => m.classList.remove('active'));
                item.classList.add('active');
                
                // Mostrar tab correspondente
                const tabName = item.getAttribute('data-tab');
                this.showTab(tabName);
            });
        });
        
        // Chat input
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendChatMessage();
                }
            });
        }
    },
    
    showTab(tabName) {
        // Esconder todos os tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Mostrar tab selecionado
        const tab = document.getElementById(tabName);
        if (tab) {
            tab.classList.add('active');
            console.log('[DASHBOARD] Tab alterada para:', tabName);
        }
    },
};

// ============================================
// SISTEMA DE CHAT COM IA
// ============================================

const ChatAI = {
    conversationHistory: [],
    
    async sendMessage(message) {
        console.log('[CHAT] Enviando mensagem:', message);
        
        // Adicionar mensagem do usuário ao histórico
        this.conversationHistory.push({
            role: 'user',
            content: message
        });
        
        // Exibir mensagem na UI
        this.addMessageToUI('user', message);
        
        try {
            // Enviar para API de IA com timeout
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 10000); // 10 segundos timeout
            
            const response = await fetch('/api/ia/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                },
                body: JSON.stringify({
                    mensagem: message,
                    historico: this.conversationHistory
                }),
                signal: controller.signal
            });
            
            clearTimeout(timeout);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            const aiResponse = data.resposta || 'Desculpe, não consegui processar sua pergunta.';
            
            // Adicionar resposta da IA ao histórico
            this.conversationHistory.push({
                role: 'assistant',
                content: aiResponse
            });
            
            // Exibir resposta na UI
            this.addMessageToUI('ai', aiResponse);
            
        } catch (error) {
            console.error('[CHAT] Erro ao enviar mensagem:', error);
            
            let aiResponse = 'Desculpe, não consegui processar sua pergunta no momento.';
            
            if (error.name === 'AbortError') {
                aiResponse = 'A resposta demorou muito. Por favor, tente novamente.';
            } else {
                // Respostas padrão se a API não responder
                const defaultResponses = {
                    'oi': 'Olá! Como posso ajudá-lo com seus estudos?',
                    'curso': 'Todos os cursos estão disponíveis na aba "Cursos". Qual deles tem interesse?',
                    'progresso': 'Você pode ver seu progresso geral na aba "Progresso".',
                    'certificado': 'Você pode visualizar seus certificados na aba "Certificados".',
                    'ajuda': 'Estou aqui para ajudar! Você pode me perguntar sobre cursos, progresso, ou como usar a plataforma.',
                    'obrigado': 'De nada! Continue estudando e aproveite a plataforma!'
                };
                
                const lowerMessage = message.toLowerCase();
                
                for (const [keyword, response] of Object.entries(defaultResponses)) {
                    if (lowerMessage.includes(keyword)) {
                        aiResponse = response;
                        break;
                    }
                }
            }
            
            this.addMessageToUI('ai', aiResponse);
        }
        
        // Limpar input
        const input = document.getElementById('chatInput');
        if (input) input.value = '';
    },
    
    addMessageToUI(role, content) {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        const messageEl = document.createElement('div');
        messageEl.className = `message ${role}`;
        messageEl.textContent = content;
        
        messagesContainer.appendChild(messageEl);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
};

// ============================================
// FUNÇÃO GLOBAL PARA CHAT
// ============================================

function sendChatMessage() {
    const input = document.getElementById('chatInput');
    if (!input || !input.value.trim()) return;
    
    ChatAI.sendMessage(input.value.trim());
}

// ============================================
// FUNÇÃO GLOBAL PARA LOGOUT
// ============================================

function logout() {
    localStorage.removeItem('authToken');
    console.log('[DASHBOARD] Usuário desconectado');
    window.location.href = '/pages/login.html';
}

// ============================================
// INICIALIZAÇÃO
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('[DASHBOARD] DOM carregado, inicializando...');
    Dashboard.init();
});
