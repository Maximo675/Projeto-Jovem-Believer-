# 🔧 Solução de Problemas - Câmera ETAN no Simulador

## 🚨 Erros Comuns e Soluções

### Erro 1: "Câmera não encontrada" / "getUserMedia failed"

**Mensagem Exata:**
```
❌ Não foi possível acessar a câmera do ETAN. Verifique as permissões.
```

**Causas Possíveis:**
```
1. ETAN não conectado
2. ETAN não reconhecido pelo Windows
3. Driver desatualizado
4. Permissão negada no navegador
5. Câmera em uso por outro programa
```

**Soluções (em ordem):**

#### ✅ Solução 1: Verificar Conexão Física
```
1. Desconecte o ETAN
2. Aguarde 3 segundos
3. Reconecte o ETAN (use porta USB diferente se possível)
4. Aguarde LED acender
5. Recarregue página (F5)
```

#### ✅ Solução 2: Verificar Gerenciador de Dispositivos
```
1. Abra: Gerenciador de Dispositivos
   - Clique direito em Iniciar > Gerenciador de Dispositivos
   
2. Procure por "Câmeras" ou "Imaging Devices"
   
3. Você deve ver:
   ✓ "ETAN Scanner" ou "Unknown Device"
   
4. Se estiver com ⚠️ (atenção):
   - Clique direito > Desinstalar dispositivo > Reconecte
   
5. Se não aparece em nenhuma categoria:
   - Driver não instalado
   - Conecte ao computador que tem drivers instalados
```

#### ✅ Solução 3: Atualizar Drivers
```
Opção A - Windows Update (Automático):
1. Gerenciador de Dispositivos
2. Clique direito em ETAN
3. Atualizar Driver
4. "Pesquisar automaticamente"

Opção B - Site do Fabricante:
1. Visite site do ETAN
2. Baixe driver mais recente
3. Execute instalador
4. Reinicie computador

Opção C - Device Manager (Avançado):
1. Gerenciador de Dispositivos
2. Ver > Mostrar dispositivos ocultos
3. Procure por ETAN ou "USB Composite Device"
4. Clique direito > Atualizar Driver
```

#### ✅ Solução 4: Verificar Permissões do Navegador

**Chrome / Edge:**
```
1. Abra a página do simulador
2. Clique no 🔒 Cadeado (esquerda da URL)
3. "Permissões do Site" ou "Privacidade"
4. Procure por "Câmera"
5. Se marcado como ❌ "Bloquear":
   - Clique em "Permitir"
   - Recarregue página (F5)
```

**Firefox:**
```
1. Digite na barra: about:preferences#privacy
2. Scroll até "Permissões"
3. Procure por "Câmera"
4. Procure por seu domínio
5. Se marcado ❌ Bloquear:
   - Clique no X para remover
   - Recarregue página (F5)
```

#### ✅ Solução 5: Fechar Outros Programas

Muitos programas usam câmera:
- ✗ Zoom, Teams, Discord, Skype
- ✗ OBS Studio, Streamlabs
- ✗ Outros apps de câmera

```
Passos:
1. Feche Zoom/Teams/Discord completamente
2. Procure na taskbar (canto inferior)
3. Feche apps de câmera na bandeja
4. Abra Task Manager (Ctrl+Shift+Esc)
5. Procure por câmera/imaging
6. Se achar, finalize processo
7. Recarregue página (F5)
```

---

### Erro 2: "Permissão Negada" / NotAllowedError

**Mensagem Exata:**
```
NotAllowedError: Permission denied
```

**Causa:**
```
Você clicou "Bloquear" quando o navegador perguntou
```

**Solução:**

**Chrome / Edge:**
```
1. Clique no 🔒 Cadeado na URL
2. "Permissões do Site"
3. Câmera:
   - Se "Bloquear" → clique X para remover
   - Se "Permitir" → skip para passo 5

4. Recarregue página (F5)
5. Navegador perguntará novamente
6. Clique "Permitir"
```

**Firefox - Solução Completa:**
```
1. Menu (≡) > Configurações > Privacidade
2. "Permissões"
3. Câmera > Configurações...
4. Procure por seu site
5. Remova ou mude para "Permitir"
6. Ok > Recarregue (F5)
```

**Safari (se usar):**
```
1. Menu > Preferências > Websites
2. Câmera (coluna esquerda)
3. Procure seu domínio
4. Mude para "Permitir"
```

---

### Erro 3: "Qualidade Sempre Baixa"

**Sintomas:**
```
- Barra sempre vermelha (< 40%)
- Sistema pede repetidamente para recontentar
- Qualidade nunca sobe de 35-45%
```

**Causas:**

1️⃣ **Sensor Sujo**
```
Solução:
- Use pano macio seco
- Esfregue gently em movimentos circulares
- Não use álcool (danifica sensor óptico)
- Teste novamente
```

2️⃣ **Iluminação Ruim**
```
Solução:
- Mude para local com melhor luz
- Idealmente luz frontal (não contraluz)
- Evite sombras sobre o sensor
- Luzes overhead ajudam
```

3️⃣ **Posicionamento Errado**
```
Solução:
- Dedo deve estar CENTRADO no sensor
- Coprir ~30-50% da área
- Não muito perto (distorciona)
- Não muito longe (não detecta)
```

4️⃣ **Contato Insuficiente**
```
Solução:
- Pressione dedo com firmeza
- Mantenha pressão constante (5 segundos)
- Pressão ideal: 80-120 mmHg
- Não levante/mexa durante captura
```

5️⃣ **Sensor Esquentado**
```
Solução:
- Após 20+ capturas, sensor aquece
- Descanse dispositivo 2-3 minutos
- Qualidade voltará ao normal
- Design normal (não é bug)
```

---

### Erro 4: "Vídeo Congela / Frame Preso"

**Sintomas:**
```
- Canvas para de atualizar após alguns segundos
- Barra de qualidade congelada
- Browser fica lento
```

**Causas:**
```
1. Browser sem recursos suficientes
2. Vazamento de memória
3. Câmera congelada
4. Conflito de drivers
```

**Soluções:**

#### ✅ Solução Rápida
```
1. Feche todas abas do navegador
2. Feche outro apps (Zoom, Teams, etc)
3. Recarregue página (Ctrl+Shift+R força refresh)
4. Tente novamente
```

#### ✅ Solução de Drivers
```
1. Gerenciador de Dispositivos
2. Câmeras > ETAN
3. Clique direito > Desinstalar
4. Reconecte o ETAN (desconecte e reconecte)
5. Windows baixará driver padrão
6. Recarregue página do simulador
```

#### ✅ Solução de Memória
```
1. Abra Console (F12 > Console)
2. Digite: 
   imageProcessor.imageHistory.length
   
3. Se valor > 100:
   - Memória vazando
   - Feche página e abra novamente
   
4. Reporte o problema se repetir
```

#### ✅ Solução Avançada (Reiniciar Câmera)
```
1. Abra Console (F12 > Console)
2. Digite: stopCamera()
3. Aguarde 2 segundos
4. Clique "Limpar Tudo e Reiniciar"
5. Tente captura normal

Se problema persiste:
- Use computador diferente
- Teste com outro programa (Zoom)
```

---

### Erro 5: "Detecta Dedo Mas Qualidade Baixa"

**Sintomas:**
```
- ✓ Dedo detectado (detecção = 80%+)
- ✗ Qualidade = 40-50%
- Sistema nega captura
```

**Causa:**
```
Dedo detectado, mas padrão não está claro
(tipo fotografia desfocada)
```

**Soluções:**

1. **Limpeza de Superfície**
```
Pode haver:
- Dedada (gordura)
- Poeira
- Umidade

Solução:
- Use pano levemente úmido (água destilada)
- Seque bem com pano seco
- Teste novamente
```

2. **Ângulo e Posição**
```
✓ Correto:
  └─ Dedo plano, perpendicular ao sensor
  
✗ Incorreto:
  └─ Dedo inclinado (ângulo)
  └─ Dedo muito de ponta (vertical)
  
Solução:
- Alinhe dedo paralelo ao sensor
- Mantenha todo dedo em contato
```

3. **Pressão Inconsistente**
```
✗ Problema:
  └─ Pressão varia durante captura (oscilação)
  
✓ Solução:
  └─ Mantenha pressão ESTÁVEL
  └─ Não levante nem aperte mais a meio
  └─ Pressão ideal: 80-110 mmHg
```

4. **Ajustar Limiar de Qualidade** (Avançado)
```
No arquivo infant-capture-simulator.html:
Linha ~800, procure por:

if (finalQuality >= 60) {

Altere 60 para:
- 50 = Mais tolerante (pode aceitar m qualidade)
- 55 = Um pouco mais tolerante
- 65 = Mais exigente (melhor qualidade)
```

---

### Erro 6: "Captura Muito Rápida / Lenta"

**Se muito rápida** (< 3 segundos):
```
No arquivo infant-capture-simulator.html
Procure por:
  let countdown = 5;

Mude para:
  let countdown = 10;  // ou mais
```

**Se muito lenta** (> 10 segundos):
```
Possível causa:
- Processamento da câmera está lento

Verificar:
1. Abra Console (F12)
2. Procure por "Processing time: Xms"
3. Se > 200ms:
   - Processamento lento
   - Tente fechar outros apps
   - Reinicie browser
```

---

### Erro 7: "Console Mostra Erros de WebRTC"

#### Erro: `NotSupportedError`
```
Significa: Browser não suporta WebRTC

Solução:
- Use versão mais recente
- Chrome 90+ ✓
- Edge 90+ ✓
- Firefox 88+ ✓
- Safari 14.1+ ✓
```

#### Erro: `ConstraintNotSatisfiedError`
```
Significa: Câmera não consegue atender ao constraint
  (ex: resolução pedida)

Solução:
1. ETAN pode ter limitação de resolução
2. Sistema reduz automaticamente para 500x500
3. Se problema persiste, contate suporte ETAN
```

#### Erro: `TypeError: video is null`
```
Significa: Elemento de vídeo não foi criado

Solução:
1. Recarregue página (F5)
2. Feche e reabra browser
3. Teste em incógnito
```

---

## 🔍 Verificação Pré-Captura (Checklist)

```
Antes de começar prática, verifique:

□ ETAN Conectado
  └─ LED aceso? SIM / NÃO

□ Gerenciador de Dispositivos
  └─ ETAN aparece em "Câmeras"? SIM / NÃO

□ Navegador Atualizado
  └─ Chrome 90+? SIM / NÃO

□ Permissão Câmera
  └─ Permitir no navegador? SIM / NÃO

□ Nenhum Outro Programa Usando Câmera
  └─ Zoom/Teams/Discord fechados? SIM / NÃO

□ Iluminação Ambiente
  └─ Boa luz? SIM / NÃO

□ Sensor Limpo
  └─ Sem sujeira? SIM / NÃO

Se todos SIM: Pode começar com confiança! ✓
Se algum NÃO: Corrija antes de começar
```

---

## 📞 Quando Abrir Um Ticket de Suporte

### Abra ticket se:
```
1. Seguiu todos troubleshooting acima
2. Problema persiste
3. Erro aparece no console (F12)
4. Código de erro específico (ex: 0x80000001)
```

### Informações para fornecer:
```
1. Sistema Operacional
   └─ Windows 10 ou 11? Qual versão?

2. Navegador
   └─ Chrome / Edge / Firefox?
   └─ Qual versão? (Menu > Ajuda > Sobre)

3. Dispositivo ETAN
   └─ Modelo? (ex: CrossMatch)
   └─ Firmware versão?

4. Mensagem de Erro Exata
   └─ Copie texto completo

5. Stock de Console
   └─ F12 > Console > Copie vermelho

6. Passos para Reproduzir
   └─ "Quando clico em... acontece..."

7. Screenshots
   └─ Gerenciador de Dispositivos
   └─ Console do browser
   └─ Mensagem de erro
```

### Exemplo de Ticket Bem Preenchido:
```
Título: Camera ETAN não funciona no simulador

Descrição:
Quando abro infant-capture-simulator.html e 
clico em "Iniciar Prática", o sistema pede 
permissão mas depois da "Não foi possível 
acessar a câmera".

Sistema: Windows 11 Home (Build 22621)
Navegador: Chrome 120.0.6099.116
ETAN: Modelo X, Firmware 2.1.5

Console Error:
NotFoundError: Requested device not found

Gerenciador de Dispositivos:
[Screenshot em anexo - mostra ETAN listado]

Passos:
1. Conecte ETAN
2. Abra Windows Chrome
3. Vá para /pages/infant-capture-simulator.html
4. Clique "Iniciar Prática"
5. ERROR (ver console em anexo)
```

---

## 🎯 Performance Debugging

### Monitorar Performance em Tempo Real
```javascript
// Abra Console (F12 > Console)
// Cole este código:

setInterval(() => {
  const mem = performance.memory;
  console.log(`
    Memory: ${Math.round(mem.usedJSHeapSize / 1048576)}MB / ${Math.round(mem.jsHeapSizeLimit / 1048576)}MB
    Image History: ${imageProcessor.imageHistory.length}
    FPS: Check DevTools Performance tab
  `);
}, 1000);
```

### Verificar Performance da Câmera
```javascript
// No Console:
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    const track = stream.getVideoTracks()[0];
    console.log('Camera FPS:', track.getSettings().frameRate);
    console.log('Resolution:', 
      track.getSettings().width + 'x' + 
      track.getSettings().height);
    stream.getTracks().forEach(t => t.stop());
  });
```

---

## 📚 Links Úteis

- **Chrome DevTools**: F12 ou Ctrl+Shift+I
- **Edge DevTools**: F12 ou Ctrl+Shift+I
- **Firefox DevTools**: F12 ou Ctrl+Shift+I
- **Windows Gerenciador de Dispositivos**: Win+X > M
- **Windows Task Manager**: Ctrl+Shift+Esc

---

**Versão**: 2.0  
**Data**: 25 de Fevereiro de 2026  
**Última atualização**: Hoje
