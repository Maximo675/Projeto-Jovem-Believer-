# ✅ CHECKLIST DE VALIDAÇÃO - Sistema de Captura Biométrica

## 🚀 Antes de Começar

Certifique-se de que tem:
- [ ] VS Code aberto com este projeto
- [ ] Terminal PowerShell disponível
- [ ] Python 3.8+ instalado
- [ ] Node.js instalado (opcional para Device Service)

---

## 📋 Passo 1: Iniciar Serviços

### CLI Commands:
```powershell
# Abra um terminal PowerShell na pasta do projeto
cd "C:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer"

# Execute o script de inicialização
.\start_all_services.ps1
```

### Checklist:
- [ ] Script inicia sem erros
- [ ] **3 janelas PowerShell abrem automaticamente:**
  - [ ] Janela 1: Flask Backend (Porta 5001) - deve mostrar "Running on http://localhost:5001"
  - [ ] Janela 2: Device Service (Porta 5000) - opcional, pode aguardar entrada manual
- [ ] Nenhuma mensagem de erro CORS no console

---

## 🧪 Passo 2: Teste Rápido

### URL de Teste:
```
http://localhost:5001/frontend/pages/teste-biometria.html
```

### Validar no Teste:
- [ ] **Scripts Carregados**: todos 5 devem estar ✅
  - [ ] Socket.IO
  - [ ] ConfigURLs
  - [ ] ETANWebSocket
  - [ ] ETANSimulatorManager
  - [ ] IFrameBridge

- [ ] **Configuração URLs**: 3 URLs devem aparecer
  - [ ] API_BASE: http://localhost:5001
  - [ ] DEVICE_URL: http://localhost:5000
  - [ ] WEBSOCKET: http://localhost:5001/socket.io

- [ ] **WebSocket**: deve mostrar ✅ Conectado (ou ⏳ Aguardando)

- [ ] **Endpoints Backend**: 2 requests devem retornar
  - [ ] /health → 200 OK
  - [ ] /api/activities/1 → 200 OK (ou sem erro)

- [ ] **localStorage**: deve mostrar Token (se logado) ou "Token ausente"

- [ ] **ETAN Manager**: deve mostrar ✅ Manager inicializado "0/10"

- [ ] **Status dos Serviços**: tabela abaixo mostrando:
  - [ ] Backend Flask: ONLINE
  - [ ] Device Service: ONLINE (ou offline, não é crítico)
  - [ ] Atividade ETAN: online

---

## 🎯 Passo 3: Atividade Principal

### URL Principal:
```
http://localhost:5001/frontend/activities/etan-captura-biometrica.html
```

### Fluxo de Uso:

#### 3.1 Inicializar
- [ ] Página carrega sem erros (branco → conteúdo)
- [ ] V progress bar aparece "0/10"
- [ ] Texto aparece: "🔐 Protocolo ETAN - Captura Biométrica"

#### 3.2 Começar Captura
- [ ] Clique no botão **"▶️ Iniciar Captura"**
- [ ] Mensagem aparece: "🚀 Captura iniciada. Posicione o dedo..."
- [ ] progress bar muda para a cor da digital (Direita - Polegar)

#### 3.3 Captura Simulada
- [ ] Barra de qualidade começa a preencher (da esquerda para direita)
- [ ] Percentual aumenta: 0% → 100%
- [ ] Tempo: ~2-3 segundos
- [ ] Mensagem aparece quando qualidade ≥ 70%: "✅ ... capturada com XXX% de qualidade!"

#### 3.4 Próximo Dedo
- [ ] Botão "➡️ Próximo Dedo" aparece
- [ ] Clique para avançar
- [ ] Label muda para próximo dedo (ex: "👆 Direita - Índice (2/10)")
- [ ] Qualidade volta a 0%

#### 3.5 Repetir 10 Vezes
- [ ] Repita o processo para todos os 10 dedos:
  - [ ] Mão Direita: Polegar, Índice, Meio, Anular, Mínimo (1-5)
  - [ ] Mão Esquerda: Polegar, Índice, Meio, Anular, Mínimo (6-10)

#### 3.6 Finalizar
Após capturar 10 dedo:
- [ ] Botão "✅ Finalizar" aparece
- [ ] Clique para finalizar
- [ ] Resultados aparecem:
  - [ ] "Digitais Capturadas: 10/10"
  - [ ] "Qualidade Média: ~82%"
  - [ ] "Tempo Total: ~45s"
  - [ ] "Taxa de Sucesso: 100%"
- [ ] Mensagem verde: "🎉 Atividade concluída!"

---

## 🔍 Passo 4: Validação de Dados

### Abrir DevTools (F12):
```
Windows: F12 ou Ctrl+Shift+I
macOS: Cmd+Option+I
```

### Console > Network:
- [ ] Requisições POST para `/api/activities/biometric/capture` aparecem
- [ ] Status das requisições: **201** (Created) ou **200** (OK)
- [ ] Resposta JSON inclui:
  ```json
  {
    "success": true,
    "finger_id": 1,
    "quality_score": 85,
    "nfiq": 4
  }
  ```

### Console > Application > localStorage:
- [ ] Após completar, verificar se há dados salvos
- [ ] Deve haver token (se logado)

---

## 🐛 Passo 5: Troubleshooting

### Se a página está branca/vazia:
```javascript
// Abra Console (F12) e procure por:
❌ "Cannot find ETANSimulatorManager"
✅ "[ETAN] Gerenciador inicializado"
```

**Solução:** Aguarde 2-3 segundos para scripts carregarem. Se erro persiste, reload (F5).

### Se o CORS ainda aparece:
```
❌ Access to XMLHttpRequest... has been blocked
```

**Solução:**
1. Verifique que está em http://localhost:5001 (não localhost:5000 ou externo)
2. Limpe cache: Ctrl+Shift+Delete
3. Recarregue: Ctrl+F5 (hard refresh)
4. Verifique que Flask está rodando

### Se WebSocket mostra "Aguardando...":
```
⏳ Conectando para WebSocket...
```

**Solução:**
```bash
# Verifique se Flask está rodando
curl http://localhost:5001/health

# Esperado:
# {"status": "ok", "services": {"flask": "ok", "websocket": "ok"}}
```

### Se não consegue logar:
- [ ] Acesse http://localhost:5001/pages/login.html
- [ ] Teste com usuário padrão
- [ ] Verifique se banco de dados existe

---

## 📊 Passo 6: Métricas de Sucesso

Após completar a atividade, você deve ter:

| Métrica | Esperado | Seu Resultado |
|---------|----------|---------------|
| Digitais Capturadas | 10/10 | ___ |
| Qualidade Média | 70%+ | ___ |
| Tempo Total | 40-60s | ___ |
| Taxa de Sucesso | 90%+ | ___ |
| Erro CORS | 0 | ___ |
| Scripts Carregados | 5 | ___ |

---

## 📋 Passo 7: Teste com Autenticação Real (Opcional)

### Com token JWT:
```powershell
# 1. Acesse login
http://localhost:5001/pages/login.html

# 2. Use credenciais (ex: usuario/senha)

# 3. Token será salvo em localStorage

# 4. Acesse captura biométrica
http://localhost:5001/frontend/activities/etan-captura-biometrica.html
```

### Verificar token:
```javascript
// No console (F12):
localStorage.getItem('authToken')
// Deve retornar algo como: eyJhbGciOiJIUzI1NiI...
```

---

## ✅ Checklist Final

- [ ] **Serviços iniciados** sem erros
- [ ] **Página de teste** mostra todos scripts ✅
- [ ] **Atividade carrega** sem CORS
- [ ] **Captura simula** corretamente (qualidade cresce)
- [ ] **10 dedos capturáveis** em sequência
- [ ] **Resultados aparecem** ao finalizar
- [ ] **Dados salves no backend** (verificar Network)
- [ ] **Sem erros no console**
- [ ] **Performance aceitável** (~2s por dedo)

---

## 📞 Próximos Passos

Se tudo passou:
✅ **Sistema Pronto para QA!**

Próximas fases:
1. Teste com dispositivo real (Fase 2)
2. Validação de qualidade real-time (Fase 3)
3. Integração com banco de dados (Fase 4)

---

## 📝 Anotações

Use este espaço para registrar seus testes:

```
Data: _______________
Hora: _______________
Aviador: _______________

Resultado geral: [ ] PASSOU  [ ] FALHOU

Problemas encontrados:
_________________________________
_________________________________
_________________________________

Observações:
_________________________________
_________________________________
```

---

## 🎯 Conclusão

Se todos os checkboxes acima estão marcados ✅, o sistema está **100% funcional**!

A captura biométrica ETAN está pronta para:
- ✅ Treinamento de operadores
- ✅ Coleta de dados biométricos
- ✅ Integração com sistema de gestão
- ✅ Análise de qualidade de imagem

**Parabéns! Sistema operacional!** 🎉

