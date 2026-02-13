/**
 * Script de Login - INFANT.ID
 */

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const remember = document.getElementById('remember').checked;

    if (!email || !password) {
        UI.showError('Por favor, preencha todos os campos');
        return;
    }

    try {
        UI.loading(true);

        const result = await Auth.login(email, password);

        if (result && result.token) {
            if (remember) {
                localStorage.setItem('rememberEmail', email);
            }

            UI.showSuccess('Login realizado com sucesso! Redirecionando...');
            
            setTimeout(() => {
                window.location.href = '../pages/dashboard.html';
            }, 1500);
        }
    } catch (error) {
        console.error('Erro no login:', error);
        UI.showError(error.message || 'Erro ao fazer login. Verifique suas credenciais.');
    } finally {
        UI.loading(false);
    }
});

// Preenchimento automático se lembrou do email
window.addEventListener('DOMContentLoaded', () => {
    const rememberedEmail = localStorage.getItem('rememberEmail');
    if (rememberedEmail) {
        document.getElementById('email').value = rememberedEmail;
        document.getElementById('remember').checked = true;
    }
});
