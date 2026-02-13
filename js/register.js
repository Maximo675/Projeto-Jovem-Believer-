/**
 * Script de Registro - INFANT.ID
 */

// Carregar hospitais ao iniciar
document.addEventListener('DOMContentLoaded', async () => {
    await loadHospitals();
});

async function loadHospitals() {
    try {
        const hospitals = await ApiClient.get('/hospitals');
        const select = document.getElementById('hospital');
        
        if (hospitals && hospitals.hospitais) {
            hospitals.hospitais.forEach(hospital => {
                const option = document.createElement('option');
                option.value = hospital.id;
                option.textContent = `${hospital.nome} - ${hospital.estado}`;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Erro ao carregar hospitais:', error);
    }
}

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const nome = document.getElementById('nome').value.trim();
    const email = document.getElementById('email').value.trim();
    const hospitalId = document.getElementById('hospital').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const terms = document.getElementById('terms').checked;

    // Validações
    if (!nome || !email || !hospitalId || !password || !confirmPassword) {
        UI.showError('Por favor, preencha todos os campos');
        return;
    }

    if (password.length < 8) {
        UI.showError('A senha deve ter no mínimo 8 caracteres');
        return;
    }

    if (password !== confirmPassword) {
        UI.showError('As senhas não correspondem');
        return;
    }

    if (!terms) {
        UI.showError('Você deve concordar com os Termos de Uso');
        return;
    }

    // Validar email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        UI.showError('Email inválido');
        return;
    }

    try {
        UI.loading(true);

        const result = await Auth.register(email, nome, password, parseInt(hospitalId));

        if (result && result.usuario) {
            UI.showSuccess('Conta criada com sucesso! Redirecionando para login...');
            
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        }
    } catch (error) {
        console.error('Erro no registro:', error);
        
        let mensagem = 'Erro ao criar conta';
        if (error.message.includes('Email já cadastrado')) {
            mensagem = 'Este email já está registrado. Tente fazer login.';
        }
        
        UI.showError(mensagem);
    } finally {
        UI.loading(false);
    }
});
