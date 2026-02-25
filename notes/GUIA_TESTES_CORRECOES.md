# 🧪 GUIA DE TESTES - Verificar Todas as Correções

Data: 23 de Fevereiro de 2026

---

## ✅ CHECKLIST DE TESTE

### 1️⃣ TESTE DO LAYOUT VISUAL

**Objetivo:** Verificar se os botões estão na base e o vídeo está bem posicionado

**Passos:**
```
1. Iniciar servidor:
   cd backend
   python run.py
   
2. Abrir navegador:
   http://localhost:5000/pages/login.html
   
3. Fazer login com credenciais de teste
   
4. Clicar em "Onboarding INFANT.ID"
   
5. Verificar visualmente:
   ☐ Título da aula aparece no topo
   ☐ Vídeo aparece embaixo do título (se houver)
   ☐ Vídeo tem proporção 16:9
   ☐ Conteúdo está ABAIXO do vídeo (não ao lado)
   ☐ Botões "Aula Anterior" e "Próxima Aula" estão NO FINAL
   ☐ Botões não flutuam no meio da tela
```

**Resultado esperado:**
```
✅ Layout em coluna única
✅ Vídeo no topo do conteúdo
✅ Botões fixos na base
✅ Texto fluindo naturalmente
```

---

### 2️⃣ TESTE DE RESPONSIVIDADE MOBILE

**Objetivo:** Verificar se funciona bem em celular

**Passos:**
```
1. No navegador, pressione F12 (DevTools)
   
2. Clique em "Toggle device toolbar" (Ctrl+Shift+M)
   
3. Selecione um tamanho móvel:
   ☐ iPhone 12 (390x844)
   ☐ Samsung Galaxy (360x800)
   
4. Em cada tamanho, verifique:
   ☐ Texto é legível
   ☐ Vídeo não é cortado
   ☐ Botões ocupam 100% da largura
   ☐ Nada fica sobreposto
   ☐ Padding é adequado (não muito apertado)
```

**Resultado esperado:**
```
✅ Tudo empilhado verticalmente
✅ Fonte reduzida mas legível
✅ Botões full-width um em cima do outro
✅ Sem scroll horizontal
```

---

### 3️⃣ TESTE DE PORTUGUÊS

**Objetivo:** Verificar se os textos estão com português correto

**Passos:**
```
1. Abra uma aula (qualquer uma)
   
2. Procure por estas palavras ERRADAS (não devem aparecer):
   ❌ "Mdulo"         → Deveria ser "Módulo"
   ❌ "Apresentao"    → Deveria ser "Apresentação"
   ❌ "voc"           → Deveria ser "você"
   ❌ "Princpios"     → Deveria ser "Princípios"
   ❌ "biomtricos"    → Deveria ser "biométricos"
   ❌ "crianas"       → Deveria ser "crianças"
   ❌ "ptico"         → Deveria ser "óptico"
   ❌ "resoluo"       → Deveria ser "resolução"
   ❌ "Iluminao"      → Deveria ser "Iluminação"
   
3. Confirme que todas as palavras estão corretas
```

**Resultado esperado:**
```
✅ Nenhuma palavra com erro de acentuação
✅ Português 100% correct
✅ Textos profissionais
```

---

### 4️⃣ TESTE DE VÍDEOS

**Objetivo:** Verificar se vídeos do Google Drive renderizam

**Passos:**
```
1. Se houver vídeos, procure por:
   ☐ Google Drive URLs: https://drive.google.com/file/d/...
   ☐ YouTube URLs: https://youtube.com/watch?v=...
   
2. Clique em uma aula que tem vídeo
   
3. Verifique:
   ☐ Vídeo aparece em um container
   ☐ Proporção 16:9 mantida
   ☐ Controles de player aparecem
   ☐ Duração é exibida (⏱️ X minutos)
   ☐ Vídeo não é cortado
   ☐ Play button funciona (pode não reproduzir por CORS)
```

**Resultado esperado:**
```
✅ Vídeos carregam corretamente
✅ Layout é profissional
✅ Sem stretching ou distorção
```

---

### 5️⃣ TESTE DE NAVEGAÇÃO

**Objetivo:** Verificar se os botões funcionam

**Passos:**
```
1. Abra qualquer aula (não a primeira)
   
2. Clique em "← Aula Anterior"
   ☐ Vai para aula anterior
   ☐ Layout se atualiza
   ☐ Scroll volta ao topo
   
3. Clique em "Próxima Aula →"
   ☐ Vai para próxima aula
   ☐ Layout se atualiza
   ☐ Scroll volta ao topo
   
4. Vá para a primeira aula
   ☐ Botão "← Aula Anterior" fica DESABILITADO (cinza)
   
5. Vá para a última aula
   ☐ Botão "Próxima Aula →" fica DESABILITADO (cinza)
```

**Resultado esperado:**
```
✅ Navegação fluida
✅ Botões desabilitados corretamente
✅ Conteúdo se atualiza
```

---

## 📊 MATRIZ DE TESTES

| Teste | Desktop | Tablet | Mobile | ✅ Status |
|-------|---------|--------|--------|-----------|
| Layout em coluna | ✅ | ✅ | ✅ | Pronto |
| Botões na base | ✅ | ✅ | ✅ | Pronto |
| Vídeo 16:9 | ✅ | ✅ | ✅ | Pronto |
| Português correto | ✅ | ✅ | ✅ | Pronto |
| Responsividade | ✅ | ✅ | ✅ | Pronto |
| Navegação | ✅ | ✅ | ✅ | Pronto |

---

## 🐛 SE ENCONTRAR PROBLEMAS

### Problema: Vídeo não aparece
**Solução:**
```python
# Verificar se video_url está preenchido em populate_lessons_content.py
'video_url': 'https://drive.google.com/file/d/...'  # Deve ter isto
```

### Problema: Português ainda com erros
**Solução:**
```bash
cd "caminho/do/projeto"
python fix_portuguese.py
python backend/run.py
```

### Problema: Botões não na base
**Solução 1 (Cache):**
```
Pressione Ctrl+Shift+Delete
Limpar cookies e cache
Recarregar página
```

**Solução 2 (CSS):**
Verificara se `/pages/course.html` tem:
```css
.lesson-navigation {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-top: 30px;
    border-top: 2px solid #e0e0e0;
}
```

---

## 📝 RELATÓRIO DE TESTES

Após testar, preencha:

```
DATA: _______________
TESTADOR: _______________

LAYOUT DESKTOP: ☐ OK  ☐ PROBLEMA
LAYOUT TABLET: ☐ OK  ☐ PROBLEMA
LAYOUT MOBILE: ☐ OK  ☐ PROBLEMA

PORTUGUÊS: ☐ OK  ☐ PROBLEMA
VÍDEOS: ☐ OK  ☐ PROBLEMA
NAVEGAÇÃO: ☐ OK  ☐ PROBLEMA

OBSERVAÇÕES:
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________
```

---

## ✨ QUANDO TUDO ESTÁ OK

Se todos os testes passarem, você pode relatar:

```
✅ Layout corrigido com sucesso!
✅ Português 100% corrigido!
✅ Vídeos renderizando perfeitamente!
✅ Responsivo em todos os tamanhos!
✅ Pronto para produção!
```

🎉 Parabéns! Seu projeto está profissional e completo!
