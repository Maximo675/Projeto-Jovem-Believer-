# ✅ CHECKLIST DE TESTES

## 📋 Antes de Começar

- [ ] Python 3.8+ instalado
- [ ] Ollama instalado (https://ollama.ai)
- [ ] Arquivo `.env` existe na raiz
- [ ] Terminal PowerShell disponível

---

## 🧪 Teste 1: Validação Rápida

Abra um PowerShell e execute:
```powershell
cd "C:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer"
python backend\test_quick.py
```

Você deve ver:
```
[1/5] Verificando Python... ✅ Python X.X.X
[2/5] Verificando Flask... ✅ Flask X.X.X
[3/5] Verificando SQLAlchemy... ✅ SQLAlchemy X.X.X
[4/5] Verificando arquivo .env... ✅ Arquivo encontrado
[5/5] Testando importação da aplicação... ✅ Aplicação carregada

✅ TODOS OS TESTES PASSARAM!
```

**Status:** ✅ / ❌

---

## 🌐 Teste 2: Ollama

Abra um PowerShell e execute:
```powershell
powershell -ExecutionPolicy Bypass -File start_ollama.ps1
```

Você deve ver após alguns segundos:
```
The Ollama API is now available at http://localhost:11434
```

Deixe rodando neste terminal.

**Status:** ✅ / ❌

---

## 🔧 Teste 3: Backend

Abra OUTRO PowerShell (manter Ollama rodando) e execute:
```powershell
powershell -ExecutionPolicy Bypass -File start_backend.ps1
```

Você deve ver:
```
✅ TODOS OS TESTES PASSARAM!
Servidor rodando em:
  http://localhost:5000
Running on http://127.0.0.1:5000
```

Deixe rodando neste terminal.

**Status:** ✅ / ❌

---

## 4️⃣ Teste 4: Conexão Backend

Abra um TERCEIRO PowerShell e execute:
```powershell
curl http://localhost:5000/
```

Você deve ver:
```html
<!DOCTYPE html>
... (código HTML da página de login)
```

**Status:** ✅ / ❌

---

## 🌍 Teste 5: Frontend

Abra seu navegador e vá para:
```
http://localhost
```

Você deve ver:
- ✅ Página de login ou dashboard
- ✅ Sem erro ERR_CONNECTION_REFUSED
- ✅ Logo Jade aparecendo
- ✅ Temas funcionando

**Status:** ✅ / ❌

---

## 💬 Teste 6: Chat com IA (Opcional)

Se logou no dashboard:
1. Clique em "Chat com IA" ou "Assistente IA"
2. Digite uma pergunta: "Oi"
3. Deve receber resposta da IA

**Status:** ✅ / ❌

---

## 🎨 Teste 7: Temas (Opcional)

1. Se o seletor de tema aparecer, clique nos botões
2. Logo deve mudar de cor
3. Página deve mudar para o novo tema

**Status:** ✅ / ❌

---

## 📝 Possíveis Problemas e Soluções

### "Teste 1 falha: Python não encontrado"
```powershell
# Instale Python em:
https://python.org
```

### "Teste 2 falha: Ollama não inicia"
```powershell
# Verifique instalação
ollama version

# Se não funcionar, instale em:
https://ollama.ai
```

### "Teste 3 falha: Porta 5000 em uso"
```powershell
# Encontre o processo
netstat -ano | findstr :5000

# Mate o processo
taskkill /PID <PID> /F
```

### "Teste 5 falha: Página branca"
```powershell
# Verifique backend rodando
curl http://localhost:5000
```

### "Teste 5: ERR_CONNECTION_REFUSED"
- Certifique-se que start_backend.ps1 está rodando
- Verifique se mostra "Running on http://127.0.0.1:5000"
- Não confunda Terminal de Ollama com Terminal de Backend

---

## ✨ Se Todos os Testes Passarem

Parabéns! 🎉 O projeto está 100% funcional!

Agora você pode:
- ✅ Fazer login/registrar
- ✅ Acessar dashboard
- ✅ Conversar com IA
- ✅ Usar temas
- ✅ Carregar cursos

---

## 📊 Status Final

```
Teste 1 (Python): ___
Teste 2 (Ollama): ___
Teste 3 (Backend): ___
Teste 4 (Conexão): ___
Teste 5 (Frontend): ___
Teste 6 (Chat): ___
Teste 7 (Temas): ___

Resultado: ___ / 7 testes passou
```

---

## 📞 Próximas Ações

Se algum teste falhar:
1. Veja a seção "Possíveis Problemas"
2. Execute novamente o teste
3. Se persistir, verifique `CORRECOES_IMPLEMENTADAS.md`

---

**Pronto para testar!** 🚀
