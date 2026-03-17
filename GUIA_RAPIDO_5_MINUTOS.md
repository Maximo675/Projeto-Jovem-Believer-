# 🚀 GUIA RÁPIDO - 5 Minutos para Começar

## 1️⃣ Iniciar Serviços (1 min)

Abra PowerShell na pasta do projeto e execute:
```powershell
.\start_all_services.ps1
```

✅ Abre 3 terminais automaticamente:
- Terminal 1: Flask (5001) ← digita 'y' se pedir
- Terminal 2: Openbio Bridge (3333) ← aguarda
- Terminal 3: Openbio Device (5000) ← aguarda ou pressiona Enter

**Aguarde todas as mensagens "✅ online" aparecerem**

---

## 2️⃣ Verificar Se Funciona (1 min)

Em um **novo terminal** PowerShell, execute:
```powershell
.\test_services_connectivity.ps1
```

Deve mostrar:
```
✅ Flask Backend:                ONLINE
✅ Openbio Bridge (CORS Proxy):  ONLINE
⏳ Openbio Device:               ONLINE/OFFLINE (ok se offline)
```

---

## 3️⃣ Abrir no Navegador (1 min)

Acesse esta URL:
```
http://localhost:5001/frontend/activities/etan-captura-biometrica.html
```

Você deve **VER:**
- 🎯 Página roxa com interface profissional
- 📱 **Iframe visível** do site externo (infant.akiyama.com.br)
- ✅ Nenhum erro CORS

---

## 4️⃣ Testar Captura (2 min)

### Se o iframe está visível:
1. Clique no iframe
2. Procure opção de "Capturar" ou similar
3. Sistema deve comunicar com localhost:5000

### Se há interface local abaixo:
1. Clique em "▶️ Iniciar Captura"
2. Simula captura com qualidade crescente
3. Quando atingir 70%+, marca como capturado

---

## ✅ Sucesso!

Se chegou aqui:
- ✅ Serviços estão rodando
- ✅ Comunicação sem CORS
- ✅ Dois sistemas funcionando juntos
- ✅ **Pronto para demonstração!**

---

## 🐛 Se Algo Não Funcionar

### Erro: "Aplicações usando portas..."
```powershell
# Feche as janelas que aberta e tente de novo
# OU mude as portas em config-urls.js
```

### Erro: "npm not found"
```bash
# Instale Node.js de https://nodejs.org
# Depois tente novamente
```

### Iframe não aparece
```javascript
// Abra DevTools (F12) → Console
// Procure por erros
// Copie erros e compartilhe
```

### "CORS bloqueado" ainda aparece
```javascript
// Console (F12):
fetch('http://localhost:3333/health')
// Se falhar, openbio-bridge não rodou
// Verifique Terminal 2
```

---

## 🎯 Checklist de Uso

- [ ] Executou `start_all_services.ps1`
- [ ] Viu 3 terminais abrirem
- [ ] Todos mostraram "✅ online"
- [ ] Executou `test_services_connectivity.ps1`
- [ ] Acessou a URL da atividade
- [ ] Página carregou sem erros
- [ ] Iframe visível na tela
- [ ] Console (F12) sem erros vermelhos

✅ **Se tudo checked, você está pronto!**

---

## ⏱️ Timeline

- ⏱️ 0:00 - 1:00 → Iniciar serviços
- ⏱️ 1:00 - 2:00 → Testar conectividade
- ⏱️ 2:00 - 3:00 → Abrir navegador
- ⏱️ 3:00 - 5:00 → Testar captura

**Total: ~5 minutos para tudo funcionando!**

---

## 📞 Documentação Completa

Se quiser entender técnico:
👉 Leia: `SOLUCAO_CORS_IFRAME_OPENBIO.md`

Se quiser executivo:
👉 Leia: `RESUMO_SOLUCAO_CORS_FINAL.md`

---

## 🎉 Próxima Apresentação

Você agora tem:
✅ Interface visual profissional (iframe)
✅ Sem erros CORS
✅ Hardware real integrado
✅ Dados salvos no banco

**Isso é game changer para a demo!** 🚀

