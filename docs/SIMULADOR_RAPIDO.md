# 🎥 Guia Rápido - Simulador com Câmera ETAN em Tempo Real

## 🚀 Como Usar

### 1️⃣ Abrir o Simulador
```
Arquivo: /pages/infant-capture-simulator.html
```

### 2️⃣ Conectar Câmera ETAN
- Conecte o dispositivo ETAN via USB
- Aguarde o Windows reconhecer (deve aparecer em `Gerenciador de Dispositivos > Câmeras`)

### 3️⃣ Permitir Acesso à Câmera
Primeira execução → O navegador pedirá permissão:

```
🔔 Deseja permitir que este site acesse sua câmera?
[Permitir] [Bloquear] [Não perguntar novamente]
```

✅ Clique em **"Permitir"**

### 4️⃣ Iniciar Prática
1. Página carrega com interface do simulador
2. Clique em **"Iniciar Prática"** (ou aguarde 5 segundos)
3. **Câmera abre automaticamente**
4. Posicione seu **dedo no sensor ETAN**
5. Sistema captura automaticamente (5 segundos por dedo)

### 5️⃣ Feedback Visual em Tempo Real

#### Indicadores que você verá:

```
📊 Qualidade: 78% | Detecção: 95%
├─ Barra verde = Qualidade boa
├─ Percentual de detecção = Taxa de acertos
└─ Pressão: 95 mmHg = Feedback de contato

✓ Dedo detectado = Sistema vendo seu dedo
✗ Dedo não detectado = Reposicione o dedo
```

#### Cores da Barra de Qualidade:
```
🔴 Vermelho  (0-33%)  = Qualidade baixa
🟡 Amarelo   (34-66%) = Qualidade média
🟢 Verde     (67-100%)= Qualidade ótima
```

---

## 📋 O Que Mudou (vs. Versão Anterior)

| Recurso | Antes | Agora |
|---------|-------|-------|
| Imagens | Pré-programadas (PNG/JPEG) | **Feed ao vivo da câmera** |
| Qualidade | Simulada aleatoriamente | **Análise real da imagem** |
| Dedo | Desenho genérico | **Próprio dedo da pessoa** |
| Processamento | Nenhum | **Análise avançada de imagem** |
| Realismo | Baixo | **Alto** |

---

## 🎯 Fluxo Completo por Dedo

```
Dedo 1: Polegar Esquerdo
├─ Câmera liga (00:05)
├─ Processamento em tempo real (00:01-00:04)
├─ Qualidade = 78%
├─ Análise = Detecção: 95%
└─ ✅ CAPTURADO

Dedo 2: Indicador Esquerdo
├─ Câmera continua ligada
├─ Novo frame processado
├─ Qualidade = 65%
└─ ✅ CAPTURADO
...
```

---

## 💡 Dicas para Melhor Qualidade

### 1. **Posicionamento do Dedo**
```
✅ Correto
┌─────────────┐
│             │
│      👆     │  Dedo centralizado
│             │  Cobrindo ~50% da área
└─────────────┘

❌ Incorreto
┌─────────────┐
│  👆         │  Muito para lado
│             │  Muito perto
└─────────────┘
```

### 2. **Iluminação**
- Boa iluminação frontal
- Evite contraluz
- Sem sombras no dedo

### 3. **Contato com Sensor**
- Pressão firme (90-120 mmHg ideal)
- Mantenha contato consistente
- Não mova o dedo durante captura

### 4. **Limpeza**
- Limpe o sensor ETAN com pano macio
- Sem álcool (pode danificar)
- Sem umidade excessiva

---

## 🔍 Dados Técnicos Capturados

```json
{
  "finger": "Index Left",
  "capture_data": {
    "quality_nfiq": 78,
    "detection_rate": 95,
    "contrast": 145,
    "brightness": 128,
    "roi_area": 0.35,
    "estimated_pressure": 95,
    "frame_count": 15,
    "processing_time_ms": 1500,
    "timestamp": "2024-02-25T14:32:10Z"
  },
  "status": "SUCCESS"
}
```

---

## ⚙️ Configuração Avançada

### Alterar Limiar de Qualidade

No arquivo `infant-capture-simulator.html`, linha ~800:

```javascript
// Padrão: 60/100
if (finalQuality >= 60) {  // ← Alterar este valor
    // Aceitar captura
}

// Sugestões:
// 50 = Mais tolerante (mais rápido)
// 60 = Padrão (balanceado)
// 70 = Rigoroso (melhor qualidade)
```

### Tempo de Captura

Padrão: **5 segundos** por dedo

Para alterar, no arquivo:

```javascript
// Linha ~280 (startCountdown)
let countdown = 5;  // ← Alterar para tempo desejado

// Opções:
// 3 = Captura rápida
// 5 = Padrão
// 10 = Mais tempo para posicionar
```

---

## ❌ Troubleshooting

### Problema: Câmera não abre
```
Solução:
1. Verifique se ETAN está conectado
2. Verifique em Gerenciador de Dispositivos
3. Recarregue a página (F5)
4. Tente em incógnito (sem extensões interferindo)
```

### Problema: Qualidade sempre baixa
```
Solução:
1. Limpez o sensor ETAN
2. Melhore iluminação da sala
3. Certifique-se do contato com sensor
4. Tente dedo em posição diferente
```

### Problema: Browser não pede permissão
```
Solução Chrome/Edge:
1. Abra DevTools (F12)
2. Application > Cookies > Seu site
3. Delete permissão anterior
4. Recarregue página (F5)
5. Clique "Permitir"
```

### Problema: Console mostra erros de câmera
```
Solução:
1. Verifique console (F12 > Console)
2. Se vir "NotAllowedError": revogue permissão e relogue
3. Se vir "NotFoundError": ETAN não está conectado
4. Se vir "NotSupportedError": Browser não suporta WebRTC
```

---

## 📊 Monitoramento de Desenvolvimento

Para **verificar dados de debug** enquanto está capturando:

```javascript
// Abra Console (F12 > Console)
// Você verá logs como:

📊 Frame 1: {
  quality: 45,
  nfiq: 45.2,
  fingerDetected: false,
  detectionRate: 0,
  pressure: 25,
  roiArea: 0.05
}

📊 Frame 2: {
  quality: 62,
  nfiq: 62.1,
  fingerDetected: true,
  detectionRate: 50,
  pressure: 85,
  roiArea: 0.35
}
```

---

## 🎓 Conceitos Técnicos

### NFIQ Score (Fingerprint Quality)
- **0-20**: Qualidade muito baixa (rejeitar)
- **20-40**: Qualidade baixa (rejeitar)
- **40-60**: Qualidade aceitável (tentar novamente)
- **60-80**: Qualidade boa (aceitar)
- **80-100**: Qualidade excelente (perfeito)

### ROI (Region of Interest)
- Região onde o dedo foi detectado
- Quanto maior, melhor o contato
- Ideal: 30-50% da área de captura

### Pressão (mmHg)
- Indicador de contato
- Ideal: 70-120 mmHg
- Muito baixo (<50): Dedo não conectado
- Muito alto (>150): Pressão excessiva

---

## 📞 Contato para Suporte

Se encontrar problemas:
1. Verifique console (F12)
2. Copie mensagem de erro
3. Verifique se ETAN está reconhecido no Windows
4. Teste em navegador diferente

---

**Versão**: 2.0 (Com Câmera em Tempo Real)  
**Data**: 25 de Fevereiro de 2026  
**Status**: ✅ Pronto para Uso
