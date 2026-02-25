/**
 * Dashboard.js - Sistema de Aprendizado Interativo
 * Gerencia cursos, progresso, IA e funcionalidades do dashboard
 */

const Dashboard = {
    user: null,
    courses: [],
    userProgress: {},
    
    // Cache com timestamp
    cache: {
        courses: { data: null, timestamp: 0, ttl: 5 * 60 * 1000 }, // 5 minutos
        progress: { data: null, timestamp: 0, ttl: 2 * 60 * 1000 },  // 2 minutos
        certificates: { data: null, timestamp: 0, ttl: 1 * 60 * 1000 }  // 1 minuto (mais frequente)
    },
    
    // Verificar se cache está válido
    isCacheValid(cacheKey) {
        const cache = this.cache[cacheKey];
        if (!cache || !cache.data) return false;
        return (Date.now() - cache.timestamp) < cache.ttl;
    },
    
    async init() {
        console.log('[DASHBOARD] Inicializando...');
        
        // Verificar autenticação
        const token = this.checkAuth();
        if (!token) return;
        
        // Carregar dados do usuário
        this.loadUserInfo(token);
        
        // Carregar cursos (com cache)
        await this.loadCourses();
        
        // Carregar progresso (com cache) - DEPOIS dos cursos
        await this.loadUserProgress();
        
        // RE-RENDERIZAR CURSOS AGORA COM PROGRESSO CARREGADO
        this.renderCourses();
        this.updateStats();
        
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
            // Verificar cache
            if (this.isCacheValid('courses')) {
                console.log('[DASHBOARD] Usando cache de cursos');
                this.courses = this.cache.courses.data;
                // NÃO renderizar aqui - será renderizado no init() após progresso ser carregado
                return;
            }
            
            console.log('[DASHBOARD] Carregando cursos...');
            
            const response = await fetch('/api/courses');
            const data = await response.json();
            
            this.courses = data.cursos || [];
            
            // Guardar em cache
            this.cache.courses.data = this.courses;
            this.cache.courses.timestamp = Date.now();
            
            console.log('[DASHBOARD] Cursos carregados:', this.courses.length);
            // NÃO renderizar aqui - será renderizado no init() após progresso ser carregado
        } catch (error) {
            console.error('[DASHBOARD] Erro ao carregar cursos:', error);
            document.getElementById('coursesContainer').innerHTML = 
                '<div class="loading" style="color: #d32f2f;">Erro ao carregar cursos. Tente novamente.</div>';
        }
    },
    
    async loadUserProgress() {
        try {
            // Verificar cache
            if (this.isCacheValid('progress')) {
                console.log('[DASHBOARD] Usando cache de progresso');
                this.userProgress = this.cache.progress.data;
                this.renderProgress();
                return;
            }
            
            console.log('[DASHBOARD] Carregando progresso do usuário...');
            
            const response = await fetch(`/api/users/progress`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                this.userProgress = data.progresso || [];
                
                // Guardar em cache
                this.cache.progress.data = this.userProgress;
                this.cache.progress.timestamp = Date.now();
                
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
        
        container.innerHTML = this.courses.map(course => {
            const progress = this.getProgressForCourse(course.id);
            const isCompleted = this.isCourseCompleted(course.id);
            
            return `
            <div class="course-card" style="${isCompleted ? 'border-top: 4px solid #388e3c; background: linear-gradient(135deg, rgba(56, 142, 60, 0.05) 0%, transparent 100%);' : ''}">
                <div class="course-header">
                    <div class="course-icon">${this.getIconForLevel(course.nivel)}</div>
                    <span class="course-level">${course.nivel || 'Básico'}</span>
                    ${isCompleted ? '<span style="background: #388e3c; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-left: auto;">✓ Concluído</span>' : ''}
                </div>
                
                <h3 class="course-title">${course.titulo}</h3>
                <p class="course-description">${course.descricao || 'Curso estruturado para seu aprendizado'}</p>
                
                <div class="course-footer">
                    <div class="course-progress">
                        <div class="progress-label">
                            ${progress}% completo
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress}%; background: ${progress === 100 ? 'linear-gradient(90deg, #388e3c 0%, #2e7d32 100%)' : 'linear-gradient(90deg, var(--primary-blue), #00a8e8)'}"></div>
                        </div>
                    </div>
                    <div class="course-action">
                        <button class="btn" onclick="Dashboard.startCourse(${course.id}, '${course.titulo}')" style="${isCompleted ? 'background: #388e3c;' : ''}">
                            ${progress === 0 ? 'Começar' : progress === 100 ? 'Revisar' : 'Continuar'}
                        </button>
                    </div>
                </div>
            </div>
        `}).join('');
    },
    
    getIconForLevel(level) {
        const icons = {
            'basico': '⭐',
            'intermediario': '⭐⭐',
            'avancado': '⭐⭐⭐'
        };
        return icons[level?.toLowerCase()] || '⭐';
    },
    
    getProgressForCourse(courseId) {
        // Buscar progresso real do usuário para este curso
        if (this.userProgress && Array.isArray(this.userProgress)) {
            const progress = this.userProgress.find(p => p.curso_id === courseId);
            if (progress) {
                return Math.round(progress.percentual || 0);
            }
        }
        // Se não temos dados de progresso específicos, tentar via API
        if (this.user && this.user.sub) {
            fetch(`/api/courses/${courseId}/progress/${this.user.sub}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.progresso) {
                    // Atualizar em cache local
                    const index = this.userProgress.findIndex(p => p.curso_id === courseId);
                    if (index >= 0) {
                        this.userProgress[index].percentual = data.progresso.percentual;
                        this.userProgress[index].concluido = data.progresso.concluido;
                    } else {
                        this.userProgress.push({
                            curso_id: courseId,
                            percentual: data.progresso.percentual,
                            concluido: data.progresso.concluido
                        });
                    }
                    // Re-renderizar cursos
                    this.renderCourses();
                }
            })
            .catch(err => console.log('[PROGRESS] Erro ao carregar progresso:', err));
        }
        return 0;
    },
    
    isCourseCompleted(courseId) {
        if (this.userProgress && Array.isArray(this.userProgress)) {
            const progress = this.userProgress.find(p => p.curso_id === courseId);
            if (progress && progress.concluido) {
                return true;
            }
        }
        return false;
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
                    <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); border-left: 5px solid ${p.percentual === 100 ? '#388e3c' : 'var(--primary-blue)'};">
                        <h3 style="margin: 0 0 12px 0; color: #1a1a1a;">Curso ${p.curso_id || '?'}</h3>
                        <div style="margin-bottom: 12px;">
                            <div style="height: 8px; background: #e0e0e0; border-radius: 4px; overflow: hidden;">
                                <div style="height: 100%; background: ${p.percentual === 100 ? 'linear-gradient(90deg, #388e3c, #2e7d32)' : 'linear-gradient(90deg, var(--primary-blue), var(--success-green))'}; width: ${p.percentual || 0}%;"></div>
                            </div>
                            <p style="margin: 8px 0 0 0; font-weight: 600; color: ${p.percentual === 100 ? '#388e3c' : 'var(--primary-blue)'};>${p.percentual || 0}%  ${p.percentual === 100 ? '✓ Concluído' : 'Completo'}</p>
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
            // Verificar cache
            if (this.isCacheValid('certificates')) {
                console.log('[DASHBOARD] Usando cache de certificados');
                this.renderCertificates(this.cache.certificates.data || []);
                return;
            }
            
            console.log('[DASHBOARD] Carregando certificados...');
            
            // Tentar novo endpoint primeiro, depois fallback
            let response = await fetch(`/api/courses/certificates`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                }
            });
            
            // Se não existir, tentar endpoint antigo
            if (response.status === 404) {
                response = await fetch(`/api/users/certificates`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                    }
                });
            }
            
            if (response.ok) {
                const data = await response.json();
                console.log('[DASHBOARD] Certificados carregados:', data.certificados?.length || 0);
                
                // Guardar em cache
                this.cache.certificates.data = data.certificados || [];
                this.cache.certificates.timestamp = Date.now();
                
                this.renderCertificates(data.certificados || []);
            } else {
                console.warn('[DASHBOARD] Status:', response.status);
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
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px;">
                ${certificates.map(c => `
                    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); padding: 24px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); border-left: 5px solid #388e3c; position: relative; overflow: hidden;">
                        <div style="position: absolute; top: 10px; right: 10px; font-size: 3rem; opacity: 0.1;">🏆</div>
                        
                        <div style="text-align: center; margin-bottom: 16px; font-size: 2.5rem;">🎓</div>
                        
                        <h3 style="margin: 0 0 8px 0; color: #1a1a1a; text-align: center; font-size: 1.1rem;">
                            ${c.curso?.titulo || 'Conclusão de Curso'}
                        </h3>
                        
                        <p style="margin: 8px 0; color: #666; text-align: center; font-size: 0.9rem;">
                            Certificado # ${c.numero_certificado}
                        </p>
                        
                        <p style="margin: 8px 0 16px 0; color: #999; font-size: 0.85rem; text-align: center;">
                            Emitido em ${c.data_emissao ? new Date(c.data_emissao).toLocaleDateString('pt-BR') : 'N/A'}
                        </p>
                        
                        <div style="border-top: 1px solid #e0e0e0; padding-top: 12px; margin-top: 12px;">
                            <button onclick="Dashboard.downloadCertificate('${c.numero_certificado}')" style="width: 100%; padding: 8px 12px; background: #388e3c; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 0.9rem; transition: background 0.3s;">
                                📥 Baixar Certificado
                            </button>
                        </div>
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
    
    
    downloadCertificate(certNumber) {
        console.log('[DASHBOARD] Baixando certificado:', certNumber);
        
        const token = localStorage.getItem('authToken');
        if (!token) {
            alert('Você não está autenticado');
            return;
        }
        
        // Fazer download via fetch
        fetch(`/api/courses/certificates/${certNumber}/download`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(res => {
            if (!res.ok) throw new Error(`Erro ${res.status}`);
            return res.blob();
        })
        .then(blob => {
            // Criar URL para download
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `Certificado_${certNumber}.html`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
            console.log('[DASHBOARD] ✓ Certificado baixado:', certNumber);
        })
        .catch(err => {
            console.error('[DASHBOARD] Erro ao baixar certificado:', err);
            alert('Erro ao baixar certificado: ' + err.message);
        });
    },
    
    updateStats() {
        const totalCourses = this.courses.length;
        const completedCourses = this.courses.filter(c => this.isCourseCompleted(c.id)).length;
        const enrolledCourses = this.courses.filter(c => {
            const progress = this.getProgressForCourse(c.id);
            return progress > 0; // Iniciado mas não concluído
        }).length;
        
        document.getElementById('totalCourses').textContent = totalCourses;
        document.getElementById('enrolledCourses').textContent = enrolledCourses;
        document.getElementById('completedCourses').textContent = completedCourses;
        
        const overallProgress = totalCourses > 0
            ? Math.round(this.courses.reduce((sum, c) => sum + this.getProgressForCourse(c.id), 0) / totalCourses)
            : 0;
        document.getElementById('overallProgress').textContent = overallProgress + '%';
    },
    
    startCourse(courseId, courseTitle) {
        console.log('[DASHBOARD] Iniciando curso:', courseId, courseTitle);
        
        // Verificar se curso já foi concluído
        const isCompleted = this.isCourseCompleted(courseId);
        
        // Salvar curso atual
        const courseData = {
            id: courseId,
            title: courseTitle,
            isReview: isCompleted  // Adicionar flag para saber se é revisão
        };
        
        sessionStorage.setItem('currentCourse', JSON.stringify(courseData));
        
        // Se curso foi concluído, mostrar mensagem
        if (isCompleted) {
            console.log('[DASHBOARD] Reabrindo curso concluído:', courseTitle);
            // Adicionar flag de revisão ao sessionStorage
            sessionStorage.setItem('courseReview', 'true');
        }
        
        // Redirecionar para página do curso
        window.location.href = `/pages/course.html?id=${courseId}&review=${isCompleted ? 'true' : 'false'}`;
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
