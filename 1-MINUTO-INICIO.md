# ⏩ INÍCIO RÁPIDO - 1 MINUTO

## Seu Problema
❌ Site dava erro: `ERR_CONNECTION_REFUSED`
❌ CSS dos temas dava erro

## A Solução
✅ Porta mudada de 8000 → **5000**
✅ CSS simplificado (sem seletores problemáticos)
✅ JavaScript com try-catch (seguro)
✅ Tudo pronto para usar

---

## ⚡ Comece AGORA (3 passos)

### Passo 1
Abra PowerShell #1 e execute:
```powershell
powershell -ExecutionPolicy Bypass -File start_ollama.ps1
```
Deixe rodando. Espera aparecer algo como:
```
The Ollama API is now available at http://localhost:11434
```

### Passo 2
Abra PowerShell #2 e execute:
```powershell
powershell -ExecutionPolicy Bypass -File start_backend.ps1
```
Deixe rodando. Espera aparecer:
```
Running on http://127.0.0.1:5000
```

### Passo 3
Abra seu navegador em:
```
http://localhost
```

**Pronto!** 🎉

---

## ✅ Tudo Funcionando?

✅ Site abriu sem erro `ERR_CONNECTION_REFUSED`?
✅ Vê a página de login/dashboard?
✅ Temas (logos) funcionando?

Se sim, você está **100% pronto**! 🚀

---

## ❌ Algo deu erro?

### "Diz que conexão foi recusada"
- Certifique-se que PowerShell #2 (backend) está rodando
- Veja se mostra "Running on http://127.0.0.1:5000"

### "Porta 5000 já em uso"
Mate outras aplicações:
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "Teste rápido falhou"
```powershell
python backend\test_quick.py
```
Veja qual dependência está faltando.

---

## 📚 Quer Saber Mais?

- **Veja as mudanças específicas:** `MUDANCAS_ESPECIFICAS.md`
- **Teste completo:** `CHECKLIST_TESTES.md`
- **Resolvendo problemas:** `CORRECOES_IMPLEMENTADAS.md`

---

## 📌 Resumo das Mudanças

| O que | De | Para | Por quê |
|------|---|------|--------|
| **Porta** | 8000 | 5000 | Padrão correto |
| **CSS** | Seletor complexo | Simples | Sem erros |
| **JS** | Sem proteção | Com try-catch | Seguro |

---

**É isso! Tudo funcionando agora!** ✨
