# 🧪 GUIA DE TESTE - SISTEMA DE PROGRESSO

## ⚡ Quick Test (5 minutos)

### Pré-requisitos:
- [ ] Aplicação rodando (`start_backend.bat`)
- [ ] Dashboard acessível (`http://localhost:5000`)
- [ ] Usuário logado

### Passos:

1. **Abra o DevTools**
   - Pressione `F12`
   - Vá para `Console`

2. **Inicie um curso**
   - Clique "Começar" em qualquer curso
   - Aguarde carregar

3. **Vá para a última aula**
   - Navegue pelos conteúdos (use botões "Próximo")
   - Chegue na última aula da course (ex: "Aula 5")

4. **Clique "Finalizar Curso"**
   - Deve aparecer um modal com:
     - Título: "Avalie este curso"
     - Campo de rating (⭐⭐⭐⭐⭐)
     - Campo de dificuldade
     - Textarea de comentários
     - Botão "Enviar Avaliação"

5. **Preencha o formulário**
   - Clique em ⭐ para dar uma nota (ex: 4 estrelas)
   - Escolha dificuldade: "Médio"
   - Escreva: "Muito bom!"
   - Clique "Enviar Avaliação"

6. **Verifique no Console:**
   Procure por mensagens como:
   ```
   [PROGRESS] Progresso salvo: {percentual: 100, concluido: true}
   [API] POST /api/courses/1/progress respondeu: 200
   ```

7. **Verifique no Network:**
   - Abra aba "Network"
   - Procure por requisição POST para `/api/courses/*/progress`
   - Status deve ser `200`
   - Response deve conter `data_conclusao`

8. **Volta ao Dashboard:**
   - Deve redirecionar automaticamente
   - Verifique mudanças no curso:
     - [ ] Badge "✓ Concluído" aparece?
     - [ ] Barra está verde (100%)?
     - [ ] Botão mudou para "Revisar"?
     - [ ] Fundo do card está sutilmente verde?

9. **Verifique Estatísticas:**
   - "Cursos Concluídos" aumentou?
   - "Progresso Geral" recalculou?

---

## 🔍 Teste Detalhado (15 minutos)

### Cenário 1: Primeira conclusão
```
1. Dashboard vazio (0% em tudo)
2. Inicia Curso 1
3. Navega até final
4. Finaliza
5. Dashboard mostra: 1 concluído, 33% progresso geral
```

**Verificações:**
- [ ] Progresso antes: 0%
- [ ] Progresso depois: 100%
- [ ] `data_conclusao` preenchido no BD
- [ ] Tempo gasto calculado corretamente

---

### Cenário 2: Segunda conclusão
```
1. Dashboard mostra 1 concluído
2. Inicia Curso 2
3. Navega até final
4. Finaliza
5. Dashboard mostra: 2 concluídos, 67% progresso geral
```

**Verificações:**
- [ ] Primeiro curso permanece "Concluído"
- [ ] Segundo curso agora "Concluído"
- [ ] Estatísticas atualizadas corretamente

---

### Cenário 3: Revisão de curso concluído
```
1. Dashboard mostra curso com "Revisar"
2. Clica em "Revisar"
3. Abre no primeiro conteúdo
4. Pode navegar sem trazer modal de conclusão
5. Volta sem salvar novo progresso
```

**Verificações:**
- [ ] Botão diz "Revisar"
- [ ] Modal não aparece ao voltar
- [ ] Progresso continua 100%

---

## 🛠️ Verificação de Backend

### Teste via curl/Postman:

**1. Salvar progresso:**
```bash
curl -X POST "http://localhost:5000/api/courses/1/progress" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 1,
    "percentual": 100,
    "concluido": true,
    "tempo_gasto": 3600
  }'
```

**Resposta esperada:**
```json
{
  "mensagem": "Progresso salvo com sucesso",
  "progresso": {
    "id": 1,
    "curso_id": 1,
    "usuario_id": 1,
    "percentual": 100,
    "concluido": true,
    "data_conclusao": "2026-02-23T15:30:00",
    "tempo_gasto": 3600
  }
}
```

**2. Obter progresso:**
```bash
curl -X GET "http://localhost:5000/api/courses/1/progress/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Resposta esperada:**
```json
{
  "progresso": {
    "percentual": 100,
    "concluido": true,
    "tempo_gasto": 3600,
    "data_conclusao": "2026-02-23T15:30:00"
  }
}
```

---

## 📊 Verificação de Banco de Dados

### SQLite:
```sql
-- Conectar ao banco
sqlite3 backend/app/database/database.db

-- Ver todos os progressos
SELECT usuario_id, curso_id, percentual, concluido, data_conclusao 
FROM progress;

-- Ver progressos de um usuário
SELECT * FROM progress 
WHERE usuario_id = 1
ORDER BY data_atualizacao DESC;

-- Ver cursos concluídos
SELECT curso_id, COUNT(*) as usuarios_concluidos
FROM progress
WHERE concluido = TRUE
GROUP BY curso_id;
```

**Resultado esperado:**
```
usuario_id | curso_id | percentual | concluido | data_conclusao
1          | 1        | 100        | 1         | 2026-02-23 15:30:00
1          | 2        | 100        | 1         | 2026-02-23 16:00:00
2          | 1        | 50         | 0         | NULL
```

---

## 🐛 Troubleshooting

### Problema: Modal não aparece ao finalizar

**Solução:**
1. Verifique se está realmente na última aula
2. Abra DevTools → Console
3. Procure por erros JavaScript
4. Verifique se `course.html` foi atualizado

### Problema: Progresso não salva

**Verificação:**
1. DevTools → Network → veja request POST
2. Status 400: Erro na validação de dados
   - Verifique: usuario_id, percentual, concluido, tempo_gasto
3. Status 401: Problema de autenticação
   - Verifique token JWT no localStorage
   - Faça login novamente
4. Status 500: Erro no servidor
   - Veja logs do Flask `/logs`
   - Verifique conexão com banco de dados

### Problema: Dashboard não mostra "Concluído"

**Verificação:**
1. Recarregue a página (F5) - forçar refresh
2. Verifique em DevTools → Network:
   - Request GET `/api/courses/{id}/progress/{user_id}` deve retornar 200
   - Response deve incluir `"concluido": true`
3. Console deve mostrar: `[DASHBOARD] Progresso carregado: ...`

### Problema: Tempo gasto incorreto

**Verificação:**
1. Verifique JavaScript em `course.html`
2. `startTime` deve ser definido ao carregar a página
3. `tempo_gasto` calcula como: `(Date.now() - startTime) / 1000`
4. Se muito grande: usuário deixou aberta sem interagir

---

## 📈 Métricas de Sucesso

| Métrica | Esperado | Teste |
|---------|----------|-------|
| Progresso salvo | 100% | Clique finalizar, veja 100% no BD |
| Data conclusão | Preenchida | SELECT data_conclusao FROM progress |
| Badge visível | "✓ Concluído" | Veja no dashboard |
| Cor da barra | Verde | Visual na barra de progresso |
| Estatísticas | Somam correto | Total cursos, concluídos, geral% |
| Persistência | Permanece após reload | F5 no dashboard |
| Tempo gasto | > 0 segundos | Verifique no BD |
| JWT decode | Funciona | Sem erros no console |

---

## ✅ Checklist de Testes

### Funcionalidade Principal
- [ ] Posso completar um curso
- [ ] Progresso aparece como 100%
- [ ] Badge "Concluído" aparece
- [ ] Dados salvos no banco
- [ ] Dashbaord mostra corretamente

### Múltiplos Cursos
- [ ] Posso completar 2 cursos
- [ ] Ambos mostram "Concluído"
- [ ] Estatísticas recalculam
- [ ] Progresso geral ≈ média

### Persistência
- [ ] Recarrego a página
- [ ] Progresso permanece
- [ ] Badge permanece
- [ ] Dados no BD intactos

### Validação de Dados
- [ ] Percentual nunca > 100%
- [ ] data_conclusao nunca NULL se concluido=true
- [ ] tempo_gasto sempre positivo
- [ ] usuario_id existe em users

### Edge Cases
- [ ] Abrir mesma page 2x
- [ ] Finalizar sem nota
- [ ] Fechar modal sem salvar
- [ ] Sair da página e voltar
- [ ] Cache do navegador

---

## 🎯 Resultado Esperado Final

Quando usuario completa um curso:

**Na Página:**
- ✅ Modal feedback abre
- ✅ Após enviar, mostra "Parabéns!"
- ✅ Aguarda 1s
- ✅ Redirecion a dashboard
- ✅ Vê curso com badge "✓ Concluído"
- ✅ Barra 100% em verde
- ✅ Botão muda para "Revisar"
- ✅ Estatísticas atualizadas

**No Banco:**
```sql
id | usuario_id | curso_id | percentual | concluido | data_conclusao
1  | 1          | 1        | 100        | true      | 2026-02-23 15:30:00
```

**No Console:**
```
✅ Progresso ✅ Feedback
✅ Salvo no BD
✅ Dashboard atualizado
```

---

**Quando tudo isto funcionar, o sistema de progresso está 100% operacional! 🚀**
