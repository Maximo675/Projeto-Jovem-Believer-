# 🔐 Guia do Simulador ETAN Completo - Captura de 10 Dedos

## Visão Geral

O novo simulador ETAN (`etan-captura-biometrica.html`) implementa o fluxo completo de captura biométrica com:

- ✅ **10 Dedos**: Sequência completa (5 dedos mão direita + 5 dedos mão esquerda)
- ✅ **Qualidade em Tempo Real**: Medição contínua de qualidade da digital (0-100%)
- ✅ **Limite de Qualidade**: Mínimo de 70% para aceitar a captura
- ✅ **Tentativas Múltiplas**: Até 3 tentativas por dedo antes de avançar
- ✅ **Relatório Final**: Resumo com métricas de sucesso e qualidade média

## Sequência de Dedos

### Mão Direita (Dedos 1-5)
1. **Polegar** (1/10)
2. **Índice** (2/10)
3. **Meio** (3/10)
4. **Anular** (4/10)
5. **Mínimo** (5/10)

### Mão Esquerda (Dedos 6-10)
6. **Polegar** (6/10)
7. **Índice** (7/10)
8. **Meio** (8/10)
9. **Anular** (9/10)
10. **Mínimo** (10/10)

## Fluxo de Captura

### 1. Iniciar Captura
- Clique no botão **"▶️ Iniciar Captura"**
- A simulação começa automaticamente para o primeiro dedo (Polegar - Direita)
- A barra de qualidade começa a aumentar (2-5 segundos)

### 2. Acompanhar Qualidade
- **Barra Colorida**: Verde = boa qualidade, vermelho = fraca
- **Porcentagem**: Leitura em tempo real
- **Limite**: Precisa atingir **70% ou mais** para aceitar
- **Simulação**: Qualidade aumenta ~15% a cada frame

### 3. Cenários Possíveis

#### ✅ Captura Bem-Sucedida
- Qualidade atinge 70%+ antes de 5 segundos
- Sistema mostra ✅ Mensagem de sucesso
- Oferece opções: **"🔄 Tentar Novamente"** ou **"➡️ Próximo Dedo"**

#### ⚠️ Qualidade Insuficiente
- Passou 5 segundos sem atingir 70%
- Sistema avisa: "⚠️ Qualidade insuficiente"
- Mostra tentativa atual (ex: 1/3)
- Permite retentativas

#### ❌ Máximo de Tentativas
- 3 tentativas falhadas consecutivas
- Sistema avança automaticamente para próximo dedo
- Registra como falha mas continua

### 4. Progresso na Tela
- **Barra de Progresso**: Mostra % de conclusão (0% → 100%)
- **Digitais Capturadas**: Contador (ex: 3/10)
- **Qualidade Média**: Média de todas as capturas
- **Taxa de Sucesso**: % de dedos capturados com sucesso

### 5. Conclusão da Atividade
- Após completar os 10 dedos:
  - Painel verde mostra: "✅ Atividade Concluída!"
  - Resumo com:
    - Total de digitais capturadas
    - Qualidade média
    - Tempo total (segundos)
    - Taxa de sucesso (%)
  - Dados salvos no backend automaticamente

## Integração com Backend

### Endpoints Utilizados

#### 1. Iniciar Sessão (Opcional)
```
POST /api/activities/biometric/session/start
```
**Payload:**
```json
{
  "user_id": 1,
  "activity_id": 4,
  "course_id": 1
}
```

#### 2. Registrar Captura
```
POST /api/activities/biometric/capture
```
**Payload:**
```json
{
  "user_id": 1,
  "activity_id": 4,
  "finger_id": 1,
  "finger_name": "Polegar",
  "hand": "Direita",
  "quality": 85,
  "nfiq": 4,
  "attempt_number": 1
}
```

#### 3. Completar Sessão
```
POST /api/activities/biometric/completion
```
**Payload:**
```json
{
  "user_id": 1,
  "activity_id": 4,
  "total_fingers_captured": 10,
  "average_quality": 78,
  "success_rate": 100,
  "captured_fingers": [...],
  "total_time": 45.3
}
```

## Acesso ao Simulador

### Via Dashboard
1. Navegue para `/pages/dashboard.html`
2. Clique no card **"🔐 Captura de 10 Dedos"**
3. O simulador abrirá em nova página

### URL Direto
```
/frontend/activities/etan-captura-biometrica.html
```

## Arquivos Envolvidos

### Frontend
- **`/frontend/activities/etan-captura-biometrica.html`** - Nova página do simulador
- **`/frontend/js/etan-simulator-manager.js`** - Gerenciador lógico completo
- **`/pages/dashboard.html`** - Link para atividades ETAN

### Backend
- **`/backend/app/routes/activities.py`** - Endpoints biométricos:
  - `/api/activities/biometric/session/start`
  - `/api/activities/biometric/capture`
  - `/api/activities/biometric/completion`

## Cálculo de NFIQ

O escore NFIQ (1-5) é calculado baseado na qualidade percentual:

- **NFIQ 1**: Qualidade 0-20% (Muito Pobre)
- **NFIQ 2**: Qualidade 21-40% (Pobre)
- **NFIQ 3**: Qualidade 41-60% (Regular)
- **NFIQ 4**: Qualidade 61-80% (Bom)
- **NFIQ 5**: Qualidade 81-100% (Excelente)

## Score Final da Atividade

O score final é calculado como:
```
Score = (Dedos Capturados / 10) × 100 × (Qualidade Média / 100)
```

**Exemplos:**
- 10/10 dedos com 80% de qualidade média = 80 points
- 8/10 dedos com 75% de qualidade média = 60 points
- 10/10 dedos com 100% de qualidade média = 100 points (Máximo!)

## Badges/Prêmios

### 🏆 Mestre em ETAN
- **Condição**: 10/10 dedos capturados + qualidade média ≥ 70%
- **Automático**: Concedido ao completar com sucesso

## Testes

### Teste Completo
1. Abra o simulador
2. Clique "Iniciar Captura" para cada dedo
3. Aguarde 5 segundos ou até atingir 70%
4. Escolha "Próximo Dedo" para avançar
5. Repita até completar os 10 dedos
6. Verifique se aparece o painel de conclusão

### Teste de Retentativa
1. Comece captura de um dedo
2. Aguarde mais de 5 segundos (vai falhar)
3. Clique "Tentar Novamente"
4. Repita até atingir 3 tentativas
5. Sistema deve avançar automaticamente

### Teste de Backend
```bash
curl -X POST http://localhost:5001/api/activities/biometric/capture \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "activity_id": 4, "finger_id": 1, "finger_name": "Polegar", "hand": "Direita", "quality": 85, "nfiq": 4, "attempt_number": 1}'
```

## Troubleshooting

### Problema: Qualidade não aumenta
**Solução**: Verifique console do navegador (F12) para erros JavaScript

### Problema: Dados não salvam no backend
**Solução**: Confirme que backend está rodando e endpoints estão corretos

### Problema: Simulador não abre
**Solução**: Verifique se arquivo `etan-captura-biometrica.html` existe em `/frontend/activities/`

### Problema: Próximo dedo não aparece
**Solução**: Carregue a página novamente, cache pode estar velho

## Próximos Passos

1. ✅ Simulador implementado
2. ✅ Gerenciador lógico pronto
3. ✅ Endpoints backend criados
4. ⏳ Integrar com câmera real (futuro)
5. ⏳ Adicionar feedback visual melhorado (futuro)
6. ⏳ Implementar histórico de capturas (futuro)

## Suporte

Dúvidas? Verifique:
- Console do navegador (F12)
- Logs do backend em `backend/run.py`
- Arquivo `RELATORIO_SIMULADOR_BIOMETRICO_FINAL.md`

---

**Data de Criação**: 2024
**Status**: ✅ Pronto para Uso
**Versão**: 1.0
