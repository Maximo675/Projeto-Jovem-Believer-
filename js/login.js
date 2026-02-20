/**
 * Script de Login - INFANT.ID
 */

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    console.log('[LOGIN] Form submitted');

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const remember = document.getElementById('remember')?.checked || false;

    console.log('[LOGIN] Valores coletados:', { email, password: '***', remember });

    if (!email || !password) {
        console.log('[LOGIN] Validação falhou: email ou password vazio');
        UI.showError('Por favor, preencha todos os campos');
        return;
    }

    console.log('[LOGIN] Validações passaram. Tentando fazer login...');

    try {
        UI.loading(true);
        console.log('[LOGIN] Loading iniciado');

        console.log('[LOGIN] Chamando Auth.login com:', { email, password: '***' });
        const result = await Auth.login(email, password);
        
        console.log('[LOGIN] Resposta recebida:', result);

        if (result && result.token) {
            console.log('[LOGIN] Token recebido:', result.token.substring(0, 20) + '...');
            
            if (remember) {
                localStorage.setItem('rememberEmail', email);
                console.log('[LOGIN] Email lembrado em localStorage');
            }

            UI.showSuccess('Login realizado com sucesso! Redirecionando...');
            
            console.log('[LOGIN] Aguardando 1.5s antes de redirecionar...');
            setTimeout(() => {
                console.log('[LOGIN] Redirecionando para dashboard');
                window.location.href = '../pages/dashboard.html';
            }, 1500);
        } else {
            console.log('[LOGIN] Resposta inválida:', result);
            UI.showError('Resposta inválida do servidor');
        }
    } catch (error) {
        console.error('[LOGIN] ERRO CAPTURADO:', error);
        console.error('[LOGIN] Error message:', error.message);
        console.error('[LOGIN] Error stack:', error.stack);
        
        let mensagem = 'Erro: ' + (error.message || 'Erro desconhecido ao fazer login');
        if (error.message.includes('Email ou senha inválidos')) {
            mensagem = 'Email ou senha incorretos. Tente novamente.';
        } else if (error.message.includes('Usuário desativado')) {
            mensagem = 'Sua conta foi desativada. Contate o administrador.';
        }
        
        UI.showError(mensagem);
    } finally {
        UI.loading(false);
        console.log('[LOGIN] Loading finalizado');
    }
});

// Preenchimento automático se lembrou do email
window.addEventListener('DOMContentLoaded', () => {
    console.log('[LOGIN] Page loaded');
    const rememberCheckbox = document.getElementById('remember');
    
    if (rememberCheckbox) {
        const rememberedEmail = localStorage.getItem('rememberEmail');
        if (rememberedEmail) {
            document.getElementById('email').value = rememberedEmail;
            rememberCheckbox.checked = true;
            console.log('[LOGIN] Email lembrado restaurado');
        }
    }
});
