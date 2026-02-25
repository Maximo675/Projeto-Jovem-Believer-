# 🎥 Integração de Câmera ETAN no Simulador

## 📋 O que foi alterado?

O simulador de captura foi atualizado para usar o feed de vídeo **em tempo real** da câmera ETAN, ao invés de imagens pré-programadas.

## ✨ Recursos Implementados

### 1. **Captura de Vídeo em Tempo Real**
- ✅ Acesso à câmera ETAN via WebRTC (`getUserMedia`)
- ✅ Stream contínuo de vídeo no canvas (250x250px)
- ✅ Processamento de frames em tempo real (10 fps)

### 2. **Análise Inteligente de Qualidade**
O sistem agora analisa:
- **Contraste** - Diferença entre cores para detectar bordas do dedo
- **Brilho** - Análise de pixels para identificar características da pele
- **Detecção de Dedo** - Baseada em análise de cores RGB
- **Pressão Simulada** - Varia conforme qualidade detectada

### 3. **Feedback Visual em Tempo Real**
- 📊 Barra de qualidade atualizada a cada frame
- ✓/✗ Indicador se o dedo foi detectado
- 📈 Média móvel de qualidade (últimos 5 frames)
- 💾 Dados em tempo real do NFIQ e pressão

## 🚀 Como Usar

### Pré-requisitos
1. **Câmera ETAN conectada** e reconhecida como dispositivo de câmera do Windows
2. **Permissões de câmera** habilitadas no navegador
3. **HTTPS ou localhost** (getUserMedia requer contexto seguro)

### Permissões do Navegador
Na primeira execução, o navegador pedirá permissão para acessar a câmera:

```
🔔 infantcapture-site.com deseja acessar sua câmera
[Permitir] [Bloquear]
```

**Clique em "Permitir"** para que o simulador funcione.

### Fluxo de Uso

1. **Abra o simulador** → `infant-capture-simulator.html`
2. **Aguarde 5 segundos** → Câmera abre automaticamente
3. **Posicione o dedo** → No centro da área de captura
4. **Frame capturado** → Qualidade é calculada
5. **Dedo aceito** → Se qualidade ≥ 60/100

---

## 🔧 Configuração Técnica

### Constraints de Câmera
```javascript
{
    video: {
        width: { ideal: 500 },
        height: { ideal: 500 },
        facingMode: 'environment'  // Câmera traseira/externa
    },
    audio: false
}
```

### Algoritmo de Detecção de Qualidade

```
Qualidade = (Contraste / 3) + (Detecção de Dedo / 3)

Onde:
- Contraste = |ΔR| + |ΔG| + |ΔB|
- Detecção = (Pixels Escuros × 1.5)
```

### Análise de Frames

| Parâmetro | Descrição | Intervalo |
|-----------|-----------|-----------|
| Contraste | Diferença média de cores | 0-255 |
| Brilho | Intensidade do pixel | 0-255 |
| Qualidade | Score final NFIQ | 0-100 |
| Pressão | Pressão simulada | 0-150 mmHg |

---

## 🎯 Melhorias Futuras

### Fase 2: Processamento Avançado
- [ ] **Detecção de Bordas** - Canny Edge Detection
- [ ] **Análise de Textura** - LBP (Local Binary Patterns)
- [ ] **Normalize ROI** - Extrair apenas a região do dedo
- [ ] **Estimativa de Pressão** - Baseada em análise de contato

### Fase 3: Integração Backend
- [ ] Enviar frames ao servidor para análise NFIQ real (se houver SDK)
- [ ] Armazenar imagens capturadas para análise pós-prática
- [ ] Integração com sistema de biometria real

### Fase 4: Otimizações UX
- [ ] Guia visual em tempo real ("mexa para cima", "pressione mais")
- [ ] Sons de confirmação/erro
- [ ] Histórico de qualidade em gráfico
- [ ] Modo dark/light automático

---

## 🐛 Troubleshooting

### ❌ "Câmera não encontrada"
```
Sistema: Verifique no Gerenciador de Dispositivos
- Dispositivos > Câmeras > ETAN Scanner
- Se não aparecer: instale drivers do ETAN
```

### ❌ "Permissão negada"
```
Navegador Chrome/Edge:
1. Clique no cadeado 🔒 na URL
2. Permissões > Câmera > Permitir
3. Recarregue a página
```

### ❌ "Qualidade sempre baixa"
```
Verificações:
- Limpeza LED do ETAN (dedão com álcool)
- Iluminação suficiente na sala
- ETAN posicionado corretamente
- Driver da câmera atualizado
```

### ❌ "Vídeo congela após alguns segundos"
```
Possíveis causas:
- Falta de permissão persistente (relogin necessário)
- Câmera em uso por outro programa
- Aquecimento do sensor (descanse 1 minuto)
```

---

## 📊 Dados Capturados

Quando um dedo é capturado com sucesso, o sistema armazena:

```json
{
  "finger_id": "index_l",
  "finger_name": "Indicador Esquerdo",
  "quality": 78,
  "pressure": 95,
  "detection_confidence": 85,
  "frame_count": 15,
  "capture_time": "2024-02-25T14:32:10Z"
}
```

---

## 🔐 Segurança e Privacidade

- ✅ Câmera acessa **apenas durante captura** (5 segundos)
- ✅ Imagens **não são transmitidas** (processadas localmente)
- ✅ Streams **encerrados automaticamente** após conclusão
- ✅ Sem armazenamento persistente no navegador

---

## 📞 Suporte

Para problemas com:
- **Câmera ETAN**: Consulte manual do dispositivo
- **Navegador**: Verifique console (F12 > Console)
- **Sistema**: Verifique logs em `C:\Users\maximo.silva\...\browser_logs`

---

## 📝 Histórico de Alterações

| Data | Versão | Alterações |
|------|--------|-----------|
| 2024-02-25 | 2.0 | ✨ Integração de câmera em tempo real |
| 2024-02-24 | 1.0 | Versão com imagens simuladas |

---

**Última atualização**: 25 de fevereiro de 2026
**Compatibilidade**: Chrome 90+, Edge 90+, Firefox 88+
