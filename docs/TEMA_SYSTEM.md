# 🎨 Sistema de Temas - Jade Logos

## Visão Geral

O sistema de temas gerencia automaticamente a exibição das logos Jade em diferentes variações:
- **Logo Branca** (Jade_versão_branco.jpg) - Para tema escuro
- **Logo Preta** (Jade_versão_preto.png) - Para tema claro
- **Logo Azul** (Jade_versão_azul.jpg) - Para tema alternativo

## Como Funciona

### Inicialização Automática

O gerenciador de temas (`theme.js`) detecta automaticamente a preferência de tema do sistema:
- **Sistema em modo escuro** → Usa logo branca
- **Sistema em modo claro** → Usa logo preta
- **Preferência salva** → Mantém a última escolha do usuário

### Integração nos Arquivos HTML

Adicione em cada arquivo HTML no `<head>`:

```html
<script src="../js/theme.js"></script>
```

Marque as imagens de logo com o atributo `data-logo`:

```html
<img src="../assets/logo/Jade_versão_branco.jpg" alt="Logo" class="logo-img" data-logo>
```

## API do Gerenciador de Temas

### Mudar Tema Programaticamente

```javascript
// Definir tema específico
ThemeManager.setTheme('dark');      // Logo branca
ThemeManager.setTheme('light');     // Logo preta
ThemeManager.setTheme('alternative'); // Logo azul

// Alternar entre light/dark
ThemeManager.toggleLightDark();

// Alternar entre todos os temas
ThemeManager.toggleTheme();

// Obter tema atual
const currentTheme = ThemeManager.getTheme();

// Obter caminho da logo do tema atual
const logoPath = ThemeManager.getCurrentLogePath();
```

### Eventos Customizados

Escute quando o tema muda:

```javascript
window.addEventListener('themeChanged', (event) => {
    console.log('Novo tema:', event.detail.theme);
    // Fazer algo quando o tema muda
});
```

## Exemplo: Botão de Alternância de Tema

### No HTML:
```html
<button id="themeToggle" class="theme-toggle-btn">
    🌙 Alternar Tema
</button>
```

### No JavaScript:
```javascript
const themeToggleBtn = document.getElementById('themeToggle');

themeToggleBtn.addEventListener('click', () => {
    const newTheme = ThemeManager.toggleLightDark();
    console.log('Tema alterado para:', newTheme);
});

// Atualizar o ícone baseado no tema
window.addEventListener('themeChanged', (event) => {
    const emoji = event.detail.theme === 'dark' ? '☀️' : '🌙';
    themeToggleBtn.textContent = emoji + ' Alternar Tema';
});
```

### No CSS:
```css
.theme-toggle-btn {
    padding: 8px 16px;
    border: 1px solid var(--primary-blue);
    background: transparent;
    color: var(--white);
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: var(--transition);
}

.theme-toggle-btn:hover {
    background: var(--primary-blue);
}
```

## Estrutura das Logos

```
assets/logo/
├── Jade_versão_branco.jpg  (100x100, para fundos escuros)
├── Jade_versão_preto.png   (100x100, para fundos claros)
├── Jade_versão_azul.jpg    (100x100, tema alternativo)
└── logo.png                (logo original - pode ser removida)
```

## Temas Disponíveis

| Nome | Constante | Logo | Uso |
|------|-----------|------|-----|
| Escuro | `ThemeManager.THEMES.DARK` | Branca | Padrão do sistema escuro |
| Claro | `ThemeManager.THEMES.LIGHT` | Preta | Padrão do sistema claro |
| Alternativo | `ThemeManager.THEMES.ALTERNATIVE` | Azul | Tema customizado |

## Atributos de Dados

- `data-theme="dark|light|alternative"` - Definido no elemento `<html>`
- `data-logo` - Marca elementos de imagem para atualização automática

## Persistência

As preferências do usuário são salvas em `localStorage` sob a chave `app-theme`.

Para limpar a preferência e voltar a usar a detecção automática:
```javascript
localStorage.removeItem('app-theme');
location.reload();
```

## Compatibilidade

- ✅ Todos os navegadores modernos (Chrome, Firefox, Safari, Edge)
- ✅ Detecção de `prefers-color-scheme` para sistemas operacionais
- ✅ Fallback para tema escuro em navegadores antigos

---

**Desenvolvido para o projeto Alura Jovem Believer**
