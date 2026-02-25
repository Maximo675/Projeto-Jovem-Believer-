/* ==========================================
   SISTEMA DE TEMAS SIMPLES - Jade Logos
   ========================================== */

const ThemeManager = {
    // Temas disponíveis
    THEMES: {
        LIGHT: 'light',
        DARK: 'dark',
        ALTERNATIVE: 'alternative'
    },

    // Logos mapeadas por tema
    LOGOS: {
        light: '/assets/logo/Winged mind_versãoAzul.jpg',
        dark: '/assets/logo/Winged mind_versãoBranco.jpg',
        alternative: '/assets/logo/Winged mind_versãoAzul.jpg'
    },

    // Favicons mapeados por tema
    FAVICONS: {
        light: '/public/icon-blue.ico',
        dark: '/public/icon-white.ico',
        alternative: '/public/icon-blue.ico'
    },

    // Tema atual
    currentTheme: 'dark',

    /**
     * Inicializa o gerenciador de temas
     */
    init() {
        try {
            // Detectar preferência de tema salva
            const savedTheme = localStorage.getItem('app-theme');
            
            if (savedTheme && Object.values(this.THEMES).includes(savedTheme)) {
                this.currentTheme = savedTheme;
            } else {
                // Detectar preferência do sistema
                this.currentTheme = this.detectSystemTheme();
            }
            
            // Aplicar tema
            this.applyTheme(this.currentTheme);
        } catch (e) {
            console.warn('Erro ao inicializar temas:', e);
        }
    },

    /**
     * Detecta a preferência de tema do sistema
     */
    detectSystemTheme() {
        try {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                return this.THEMES.DARK;
            }
        } catch (e) {
            console.warn('Erro ao detectar tema do sistema:', e);
        }
        return this.THEMES.LIGHT;
    },

    /**
     * Atualiza o favicon baseado no tema
     */
    updateFavicon() {
        try {
            const faviconPath = this.FAVICONS[this.currentTheme];
            let faviconLink = document.querySelector('link[rel="icon"]');
            
            if (!faviconLink) {
                faviconLink = document.createElement('link');
                faviconLink.rel = 'icon';
                faviconLink.type = 'image/x-icon';
                document.head.appendChild(faviconLink);
            }
            
            faviconLink.href = faviconPath;
        } catch (e) {
            console.warn('Erro ao atualizar favicon:', e);
        }
    },

    /**
     * Aplica o tema selecionado
     */
    applyTheme(theme) {
        try {
            if (!Object.values(this.THEMES).includes(theme)) {
                console.warn(`Tema inválido: ${theme}`);
                return;
            }

            this.currentTheme = theme;
            
            // Salvar preferência
            localStorage.setItem('app-theme', theme);
            
            // Aplicar classe ao corpo do documento
            document.documentElement.setAttribute('data-theme', theme);
            
            // Atualizar todas as logos na página
            this.updateAllLogos();
            
            // Atualizar favicon
            this.updateFavicon();
            
            // Disparar evento customizado
            try {
                window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
            } catch (e) {
                console.warn('Erro ao disparar evento de tema:', e);
            }
        } catch (e) {
            console.error('Erro ao aplicar tema:', e);
        }
    },

    /**
     * Atualiza todas as imagens de logo na página
     */
    updateAllLogos() {
        try {
            const logoImages = document.querySelectorAll('[data-logo], .logo-img');
            const logoPath = this.LOGOS[this.currentTheme];
            
            logoImages.forEach(img => {
                try {
                    // Atualizar se tem atributo data-logo ou já contém assets/logo no src
                    if (img.hasAttribute('data-logo') || (img.src && img.src.includes('assets/logo/'))) {
                        img.src = logoPath;
                    }
                } catch (e) {
                    console.warn('Erro ao atualizar logo:', e);
                }
            });
        } catch (e) {
            console.error('Erro ao atualizar logos:', e);
        }
    },

    /**
     * Alterna entre light e dark
     */
    toggleLightDark() {
        const nextTheme = this.currentTheme === this.THEMES.DARK 
            ? this.THEMES.LIGHT 
            : this.THEMES.DARK;
        this.applyTheme(nextTheme);
        return this.currentTheme;
    },

    /**
     * Define o tema manualmente
     */
    setTheme(theme) {
        this.applyTheme(theme);
    },

    /**
     * Retorna o tema atual
     */
    getTheme() {
        return this.currentTheme;
    },

    /**
     * Retorna o caminho da logo do tema atual
     */
    getCurrentLogePath() {
        return this.LOGOS[this.currentTheme];
    }
};

// Inicializar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => ThemeManager.init(), 100);
    });
} else {
    setTimeout(() => ThemeManager.init(), 100);
}
