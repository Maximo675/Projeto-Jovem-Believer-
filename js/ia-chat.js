/* ==========================================
   IA CHAT - JavaScript
   ========================================== */

// Estado do Chat
const ChatState = {
    conversas: [],
    usuarioId: null,
    cursoId: null,
    modo: 'carregando',
    modelo: 'desconhecido'
};

/**
 * Inicializar chat ao carregar página
 */
document.addEventListener('DOMContentLoaded', () => {
    initChat();
});

/**
 * Inicializar chat
 */
function initChat() {
    console.log('🤖 Inicializando IA Chat...');
    
    // Obter usuário logado
    const token = TokenManager.get();
    if (!token) {
        window.location.href = '/pages/login.html';
        return;
    }
    
    // Carregar informações de modo
    fetchIAInfo();
    
    // Event listeners
    document.getElementById('messageInput').addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            sendMessage(e);
        }
    });
    
    document.getElementById('showTokens').addEventListener('change', (e) => {
        const tokenCount = document.getElementById('tokenCount');
        tokenCount.style.display = e.target.checked ? 'block' : 'none';
    });
    
    console.log('✅ Chat inicializado');
}

/**
 * Buscar informações sobre modo de IA
 */
async function fetchIAInfo() {
    try {
        // Simulado por enquanto, em produção seria uma API
        ChatState.modo = 'Ollama Local';
        ChatState.modelo = 'llama2';
        
        document.getElementById('modoIA').textContent = ChatState.modo;
        document.getElementById('modeloIA').textContent = ChatState.modelo;
        
        updateStatus('Pronto');
    } catch (error) {
        console.error('Erro ao buscar info:', error);
        document.getElementById('modoIA').textContent = 'Erro';
    }
}

/**
 * Enviar mensagem
 */
async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById('messageInput');
    const pergunta = input.value.trim();
    
    if (!pergunta) return;
    
    // Limpar input
    input.value = '';
    input.style.height = 'auto';
    
    // Adicionar mensagem do usuário
    addMessage(pergunta, 'user');
    
    // Atualizar status
    updateStatus('Enviando...');
    document.getElementById('sendBtn').disabled = true;
    
    try {
        // Chamar API
        const response = await ApiClient.post('/ia/consult', {
            pergunta: pergunta,
            usuario_id: ChatState.usuarioId,
            curso_id: ChatState.cursoId
        });
        
        // Adicionar resposta da IA
        addMessage(response.resposta, 'assistant', response.tokens);
        
        // Adicionar ao histórico
        ChatState.conversas.push({
            id: response.id,
            pergunta: pergunta,
            resposta: response.resposta,
            tokens: response.tokens,
            data: new Date()
        });
        
        updateStatus(`Pronto (${response.tokens} tokens)`);
        
    } catch (error) {
        console.error('Erro ao enviar:', error);
        addMessage(
            `❌ Erro ao processar pergunta: ${error.message}`,
            'error'
        );
        updateStatus('Erro ao processar');
    } finally {
        document.getElementById('sendBtn').disabled = false;
        document.getElementById('messageInput').focus();
    }
}

/**
 * Fazer pergunta rápida
 */
function askQuestion(pergunta) {
    document.getElementById('messageInput').value = pergunta;
    document.getElementById('messageInput').focus();
    sendMessage({ preventDefault: () => {} });
}

/**
 * Adicionar mensagem ao chat
 */
function addMessage(texto, tipo = 'assistant', tokens = 0) {
    const container = document.getElementById('messagesContainer');
    
    // Remover welcome se for primeira mensagem
    const welcome = container.querySelector('.message-welcome');
    if (welcome) {
        welcome.remove();
    }
    
    // Criar elemento da mensagem
    const messageEl = document.createElement('div');
    messageEl.className = `message ${tipo}`;
    
    const contentEl = document.createElement('div');
    contentEl.className = 'message-content';
    
    // Renderizar conteúdo com markdown básico
    if (tipo === 'assistant') {
        contentEl.innerHTML = renderMarkdown(texto);
    } else {
        contentEl.textContent = texto;
    }
    
    messageEl.appendChild(contentEl);
    container.appendChild(messageEl);
    
    // Auto-scroll se habilitado
    if (document.getElementById('autoScroll').checked) {
        container.scrollTop = container.scrollHeight;
    }
    
    // Mostrar tokens se habilitado
    if (tokens > 0 && document.getElementById('showTokens').checked) {
        document.getElementById('tokenValue').textContent = tokens;
        document.getElementById('tokenCount').style.display = 'block';
    }
}

/**
 * Renderizar markdown básico
 */
function renderMarkdown(texto) {
    let html = texto;
    
    // Negrito
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Itálico
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Listas
    html = html.replace(/\n- (.*?)(?=\n|$)/g, '<li>$1</li>');
    html = html.replace(/(<li>.*?<\/li>)/s, '<ul>$1</ul>');
    
    // Links
    html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
    
    // Quebras de linha
    html = html.replace(/\n\n/g, '</p><p>');
    html = `<p>${html}</p>`;
    
    return html;
}

/**
 * Limpar chat
 */
function clearChat() {
    if (!confirm('Tem certeza que deseja limpar todo o histórico de conversa?')) {
        return;
    }
    
    document.getElementById('messagesContainer').innerHTML = `
        <div class="message-welcome">
            <div class="welcome-icon">🤖</div>
            <h2>Chat Limpo</h2>
            <p>A conversa foi resetada. Como posso ajudá-lo?</p>
            <div class="quick-questions">
                <p>Perguntas populares:</p>
                <div class="quick-buttons">
                    <button onclick="askQuestion('Como funciona a coleta biométrica de recém-nascidos?')" class="quick-btn">
                        📋 Coleta Biométrica
                    </button>
                    <button onclick="askQuestion('Quais são os protocolos de segurança?')" class="quick-btn">
                        🔒 Segurança
                    </button>
                    <button onclick="askQuestion('Como usar o sistema ETAN?')" class="quick-btn">
                        ⚙️ Sistema ETAN
                    </button>
                    <button onclick="askQuestion('Qual é o protocolo de onboarding?')" class="quick-btn">
                        📚 Onboarding
                    </button>
                </div>
            </div>
        </div>
    `;
    
    ChatState.conversas = [];
    updateStatus('Pronto');
}

/**
 * Exportar conversa como JSON
 */
function exportChat() {
    if (ChatState.conversas.length === 0) {
        alert('Nenhuma conversa para exportar');
        return;
    }
    
    const data = {
        data: new Date().toISOString(),
        usuario_id: ChatState.usuarioId,
        modo: ChatState.modo,
        modelo: ChatState.modelo,
        conversas: ChatState.conversas
    };
    
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-${new Date().getTime()}.json`;
    a.click();
    
    URL.revokeObjectURL(url);
}

/**
 * Atualizar status
 */
function updateStatus(texto) {
    document.getElementById('statusText').textContent = texto;
}

/**
 * Auto-expand textarea
 */
document.addEventListener('loaded', () => {
    const textarea = document.getElementById('messageInput');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 150) + 'px';
        });
    }
});

// Fallback se DOMContentLoaded já passou
if (document.readyState === 'interactive' || document.readyState === 'complete') {
    initChat();
}
