/**
 * Script de Registro - INFANT.ID
 */

// Carregar hospitais ao iniciar
document.addEventListener('DOMContentLoaded', async () => {
    console.log('[REGISTER] Page loaded');
    await loadHospitals();
});

async function loadHospitals() {
    console.log('[REGISTER] Loading hospitals...');
    try {
        const hospitals = await ApiClient.get('/hospitals');
        console.log('[REGISTER] Hospitals response:', hospitals);
        
        const select = document.getElementById('hospital');
        console.log('[REGISTER] Select element:', select);
        
        if (hospitals && hospitals.hospitais) {
            console.log('[REGISTER] Adding', hospitals.hospitais.length, 'hospitals to select');
            hospitals.hospitais.forEach(hospital => {
                const option = document.createElement('option');
                option.value = hospital.id;
                option.textContent = `${hospital.nome} - ${hospital.estado}`;
                select.appendChild(option);
            });
            console.log('[REGISTER] Hospitals loaded successfully');
        }
    } catch (error) {
        console.error('[REGISTER] Error loading hospitals:', error);
    }
}

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    console.log('[REGISTER] Form submitted');

    const nome = document.getElementById('nome').value.trim();
    const email = document.getElementById('email').value.trim();
    const hospitalId = document.getElementById('hospital').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const terms = document.getElementById('terms').checked;

    console.log('[REGISTER] Valores coletados:', { nome, email, hospitalId, password: '***', confirmPassword: '***', terms });

    // Validações
    if (!nome || !email || !hospitalId || !password || !confirmPassword) {
        console.log('[REGISTER] Validação 1 falhou: campos vazios');
        UI.showError('Por favor, preencha todos os campos');
        return;
    }

    if (password.length < 8) {
        console.log('[REGISTER] Validação 2 falhou: senha muito curta');
        UI.showError('A senha deve ter no mínimo 8 caracteres');
        return;
    }

    if (password !== confirmPassword) {
        console.log('[REGISTER] Validação 3 falhou: senhas não correspondem');
        UI.showError('As senhas não correspondem');
        return;
    }

    if (!terms) {
        console.log('[REGISTER] Validação 4 falhou: termos não aceitos');
        UI.showError('Você deve concordar com os Termos de Uso');
        return;
    }

    // Validar email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        console.log('[REGISTER] Validação 5 falhou: email inválido');
        UI.showError('Email inválido');
        return;
    }

    console.log('[REGISTER] Todas as validações passaram. Tentando registrar...');

    try {
        UI.loading(true);
        console.log('[REGISTER] Loading iniciado');

        const result = await Auth.register(email, nome, password, parseInt(hospitalId));
        
        console.log('[REGISTER] Resposta recebida:', result);

        if (result && result.usuario) {
            console.log('[REGISTER] Sucesso! Usuario ID:', result.usuario.id);
            UI.showSuccess('Conta criada com sucesso! Redirecionando para login...');
            
            console.log('[REGISTER] Aguardando 1.5s antes de redirecionar...');
            setTimeout(() => {
                console.log('[REGISTER] Redirecionando para /pages/login.html');
                window.location.href = '/pages/login.html';
            }, 1500);
        } else {
            console.log('[REGISTER] Resposta inválida:', result);
            UI.showError('Resposta inválida do servidor');
        }
    } catch (error) {
        console.error('[REGISTER] ERRO:', error);
        console.error('[REGISTER] Error message:', error.message);
        console.error('[REGISTER] Error stack:', error.stack);
        
        let mensagem = 'Erro ao criar conta: ' + error.message;
        if (error.message.includes('Email já cadastrado')) {
            mensagem = 'Este email já está registrado. Tente fazer login.';
        }
        
        UI.showError(mensagem);
    } finally {
        UI.loading(false);
        console.log('[REGISTER] Loading finalizado');
    }
});
