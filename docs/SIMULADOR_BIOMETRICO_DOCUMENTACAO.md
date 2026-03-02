# 🖐️ Simulador de Captura Biométrica - Documentação Técnica

## 📋 Visão Geral

O simulador de captura biométrica foi desenvolvido para treinar técnicos de coleta de dados biométricos infantil e adulto com feedback ao vivo profissional. Ele replica o fluxo completo do SDK de captura biométrica com detecção de problemas em tempo real.

---

## 🚀 Arquitetura do Simulador

### Fluxo de Captura Sequencial

O simulador segue uma sequência bem definida baseada no SDK infantil:

```
1. FASE AGUARDANDO (0-2s)
   └─ Aguarda detecção do dedo no scanner
   └─ Fornece feedback: "Aguardando dedo..."

2. FASE DETECTANDO (2-3.5s)
   └─ Dedo foi detectado
   └─ Inicia análise de posicionamento
   └─ Feedback: Detectado, aguarde análise
   └─ Verifica:
      ├─ Umidade (wetness)
      ├─ Limpeza (cleanliness)
      ├─ Posicionamento (positioning)
      └─ Pressão (pressure)

3. FASE POSICIONANDO (3-5s)
   └─ Refina análise de qualidade
   └─ Feedbacks contextuais:
      ├─ "Digital está molhada" (wetness > 70%)
      ├─ "Dedo mal posicionado" (positioning < 50%)
      ├─ "Digital está suja" (cleanliness < 40%)
      └─ "Aumentar pressão" (pressure < 40%)

4. FASE CAPTURANDO (5-5s)
   └─ Captura ativa
   └─ Melhora contínua de qualidade
   └─ Feedback: "Capturando... Mantenha fixo"

5. FASE COMPLETA
   └─ Captura termina por:
      ├─ ≥120 frames (5 segundos)
      └─ OU qualidade ≥ 80%
   └─ Exibe resultados finais
```

---

## 🎯 Sistema de Qualidade

### Parâmetros de Qualidade

Cada parâmetro é avaliado de 0 a 100%:

| Parâmetro | Descrição | Impacto | Feedback |
|-----------|-----------|---------|----------|
| **Umidade (Wetness)** | Digital molhada | -25% qualidade | "Digital está molhada" |
| **Limpeza (Cleanliness)** | Sujeira/resíduos | -25% qualidade | "Digital está suja" |
| **Posicionamento** | Centralização | -25% qualidade | "Dedo mal posicionado" |
| **Pressão** | Força aplicada | -25% qualidade | "Aumentar/diminuir pressão" |

### Cálculo do Score

```javascript
qualidade_global = (
  (100 - wetness) * 0.25 +
  cleanliness * 0.25 +
  positioning * 0.25 +
  pressure * 0.25
);

nfiq_score = {
  90-100%: 5 (Excelente),
  80-89%:  4 (Bom),
  70-79%:  3 (Regular),
  50-69%:  2 (Pobre),
  < 50%:   1 (Ruim)
};
```

---

## 🔄 Feedback ao Vivo

### Tipos de Mensagens

#### ✅ Sucesso (Verde)
```
✅ Dedo detectado!
✅ Capturando... Mantenha o dedo fixo.
✅ Captura concluída com sucesso!
```

#### ⚠️ Aviso (Amarelo)
```
⚠️ Dedo muito molhado. Seque com papel limpo.
⚠️ Digital está suja ou marcada. Limpe a mão.
⚠️ Dedo mal posicionado. Centralize melhor.
⚠️ Aumentar pressão ligeiramente. Dedo muito leve.
```

#### ❌ Erro (Vermelho)
```
❌ Captura cancelada pelo usuário
❌ Tempo limite excedido
```

### Visualização de Feedback

- **Histórico Visual**: Últimas 5 mensagens exibidas
- **Animação**: Slide-in desde o topo
- **Cor-coded**: Verde, Amarelo, Vermelho
- **Atualização em Tempo Real**: Conforme fase avança

---

## 📊 Resultados Finais

### Métricas Oferecidas

```
┌─────────────────────────────────────┐
│  ✅ CAPTURA REALIZADA COM SUCESSO   │
├─────────────────────────────────────┤
│ Qualidade Final (NFIQ): 5 (Excelente)
│ Score de Qualidade: 85%
│ Tempo Total: 3.5s
│ Minúcias Detectadas: 147
└─────────────────────────────────────┘
```

### Interpretação de Resultados

**NFIQ Score:**
- **5**: Excelente - Pronto para uso em sistemas de identificação
- **4**: Bom - Adequado para a maioria das aplicações
- **3**: Regular - Aceitável com reservas
- **2**: Pobre - Limite mínimo aceitável
- **1**: Ruim - Falha de captura

**Minúcias:**
- Padrões únicos da digital detectados
- Mínimo recomendado: 30-40
- Típico: 100-200 dependendo do dedo

---

## 🎓 Modos de Captura

### 👶 Modo Infantil
- Timeout: 5 segundos (maior flexibilidade)
- Qualidade mínima: 30% (menos exigente)
- Sensibilidade: Média
- Tipicamente: RNs, bebês, crianças até 12 anos

### 👨 Modo Adulto  
- Timeout: 5 segundos
- Qualidade mínima: 50% (mais exigente)
- Sensibilidade: Alta
- Tipicamente: Adultos, profissionais de saúde

---

## 🛠️ Integração com Outros Componentes

### WebSocket Integration

O simulador se comunica com o servidor via WebSocket:

```javascript
// Evento enviado ao completar captura
{
  type: 'capture_completed',
  data: {
    nfiq_score: 5,
    quality_percentage: 85,
    total_time: 3.5,
    minutiae_count: 147,
    capture_mode: 'child'
  }
}
```

### IFrame Bridge

Se embutido em iframe:

```javascript
// Enviar para página pai
window.parent.postMessage({
  type: 'CAPTURE_COMPLETED',
  data: { ... }
}, '*');
```

### API Endpoints

```javascript
POST /api/activity/complete
{
  lesson_id: 4,
  course_id: 1,
  user_id: 123,
  activity_type: 'biometric_practice',
  score: 100,
  completed: true
}
```

---

## 📱 Responsividade

### Desktop (> 1024px)
- Layout lado a lado
- Scanner: 350px × 350px
- Instruções: 350px coluna lateral

### Tablet (768px - 1024px)
- Layout flexível
- Scanner responsivo

### Mobile (< 768px)
- Layout empilhado verticalmente
- Scanner: 100vw - 40px
- Instruções: scrollable

---

## 🔍 Debugging & Logs

O simulador registra todas as ações no console:

```javascript
[BiometricSimulator] Simulador inicializado
[BiometricSimulator] Modo alterado para: child
[BiometricSimulator] Captura iniciada
[BiometricSimulator] Dedo detectado
[BiometricSimulator] Qualidade: 45%
...
```

---

## 🎮 Casos de Uso de Treinamento

### Cenário 1: Digital Molhada
```
⚠️ Dedo detectado
⚠️ Digital está muito molhada. Seque com papel limpo.
-> Qualidade cai para 35%
-> Usuário seca o dedo
-> Qualidade volta para 75%
```

### Cenário 2: Posicionamento Ruim
```
✅ Dedo detectado
⚠️ Dedo mal posicionado. Centralize melhor.
-> Qualidade em 40%
-> Usuário reposiciona
-> Qualidade sobe para 85%
```

### Cenário 3: Captura Bem-Sucedida
```
✅ Dedo detectado!
✅ Capturando... Mantenha o dedo fixo.
(3 segundos se Modo Infantil OU 2.5s em Modo Adulto)
✅ Captura concluída!
Result: NFIQ 5, 88%, 147 minúcias
```

---

## 🔐 Segurança

- **Sem dados reais**: Simulador não armazena dados biométricos
- **Sem comunicação externa**: Tudo é processado localmente
- **Sem rastreamento**: Apenas logs locais de console
- **GDPR Compliant**: Nenhum dado pessoal coletado

---

## 📌 Referências Técnicas

### Atributos Data

```html
<button data-mode="child">Modo Infantil</button>
<button data-mode="adult">Modo Adulto</button>
```

### Classes CSS

```css
.scanner-display    /* Container do scanner */
.camera-feed        /* Área de câmera */
.quality-meter      /* Barra de qualidade */
.feedback-area      /* Container de feedback */
.results-panel      /* Painel de resultados */
```

### JavaScript

```javascript
window.simulator = new BiometricCaptureSimulator()
simulator.startCapture()
simulator.stopCapture()
simulator.addFeedback(message, type)
```

---

## 🚯 Troubleshooting

| Problema | Solução |
|----------|---------|
| Simulador não carrega | Verificar console para erros |
| Feedback não aparece | Limpar cache, recarregar página |
| Qualidade não melhora | Digital pode estar muito suja |
| Timeout excedido | Modo infantil permite mais tempo |

---

## 📞 Suporte

Para dúvidas sobre o simulador:
- Consulte a documentação técnica acima
- Abra console (F12) para ver logs
- Verifique se um dedo foi corretamente detectado

---

**Versão:** 1.0  
**Data:** 26 de Fevereiro, 2026  
**Autor:** Sistema de Treinamento ETAN  
**Status:** ✅ Produção
