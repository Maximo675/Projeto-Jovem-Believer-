# 🧪 GUIA DE TESTE - PLATAFORMA INFANT.ID COM IA

Servidor está rodando agora em: **http://localhost:5001**

---

## 🔑 LOGIN

**Credenciais:**
```
Email: usuario.teste@infantid.com.br
Senha: user_seguro_123456
```

---

## ✅ TESTE 1: Cursos Populados (O PROBLEMA PRINCIPAL)

### Passo 1: Ir ao Dashboard
1. Abra: http://localhost:5001/pages/dashboard.html
2. Faça login com credenciais acima
3. Clique em **"Cursos"** (primeira aba, já está selecionada)

### Passo 2: Verificar Cursos
Você deverá ver 3 cursos com cards mostrando:
- Onboarding INFANT.ID (6 aulas, básico, 2 horas)
- Integração Hospitalar (4 aulas, intermediário, 1.5 horas)
- Gerenciamento de Usuários (3 aulas,avançado, 1 hora)

### Passo 3: Abrir Cada Curso

#### Curso 1: Onboarding INFANT.ID
1. Clique "Começar" no card do Onboarding
2. Será aberto: http://localhost:5001/pages/course.html?id=1
3. **Lado Esquerdo:** Sidebar com lista de 6 aulas ✅
4. **Centro:** Conteúdo da primeira aula "Bem-vindo ao INFANT.ID"
5. **Navegação:** Clique em cada aula no sidebar para ver:
   - Aula 1: Bem-vindo (video + apresentação)
   - Aula 2: Biometria (tabela comparando 4 modalidades)
   - Aula 3: Equipamentos (especificações scanner/câmera/leitor)
   - Aula 4: Coleta (protocolo 5 fases + checklist)
   - Aula 5: Segurança (criptografia + LGPD detalhado)
   - Aula 6: Troubleshooting (problemas comuns + soluções)

**✅ RESULTADO ESPERADO:** Todas as 6 aulas carregam com conteúdo HTML profissional

#### Curso 2: Integração Hospitalar
1. Voltar ao Dashboard (clique "Voltar" no course page)
2. Clique "Começar" no card de Integração Hospitalar
3. Opens: http://localhost:5001/pages/course.html?id=2
4. Ver 4 aulas:
   - Aula 1: Arquitetura (diagrama, API, segurança)
   - Aula 2: Implementação Técnica (SDK Python e Node.js)
   - Aula 3: Workflow Clínico (5 etapas do paciente)
   - Aula 4: Troubleshooting (problemas de integração)

**✅ Antes:** "Este curso não possuiaulas ainda" ❌
**✅ Depois:** 4 aulas com conteúdo técnico profissional ✅

#### Curso 3: Gerenciamento de Usuários
1. Voltar ao Dashboard
2. Clique "Começar" em Gerenciamento de Usuários
3. Opens: http://localhost:5001/pages/course.html?id=3
4. Ver 3 aulas:
   - Aula 1: Papéis (admin, médico, técnico, recepcionista, auditor)
   - Aula 2: Multi-institucional (onboarding hospitais, custos)
   - Aula 3: Auditoria (logs, alertas, relatórios compliance)

**✅ Antes:** 0 aulas ❌
**✅ Depois:** 3 aulas estruturadas com tabelas ✅

---

## 🤖 TESTE 2: IA com Knowledge Base (O OUTRO PROBLEMA)

### Passo 1: Abrir Chat IA
1. Dashboard → Clique na aba **"Assistente IA"**
2. Será aberto chat com "Assistente Winged Mind"

### Passo 2: Fazer Perguntas (Compare com Antes)

#### Pergunta 1: "Como coletar biometria?"

**Antes:** 
```
IA: "Bem-vindo! Como posso ajudá-lo?"
```

**Depois (NOVO):**
```
IA: "Entendi sua pergunta sobre biometria..."
├─ Protocolo de Coleta com 5 FASES
├─ Tabela com modalidades (impressão, íris, facial, voz)
├─ Instruções passo-a-passo
├─ Dicas práticas
└─ Links para aulas relacionadas
   └─ "Protocolo de Coleta Passo a Passo"
   └─ "Troubleshooting e Melhores Práticas"
```

#### Pergunta 2: "Qual é o protocolo de segurança?"

**Antes:**
```
IA: "A segurança é importante..."
```

**Depois (NOVO):**
```
IA: "Excelente pergunta sobre segurança..."
├─ Encriptação em 3 camadas (trânsito, repouso, hash)
├─ Conformidade LGPD com artigos específicos
├─ Direitos do titular (acesso, retificação, exclusão)
├─ Retenção de dados (cronograma)
├─ Incidente de segurança (5 passos)
└─ Links: "Segurança e Conformidade LGPD"
```

#### Pergunta 3: "Como integrar com HIS?"

**Antes:**
```
IA: "A integração é um processo..."
```

**Depois (NOVO):**
```
IA: "Ótima pergunta sobre integração..."
├─ Arquitetura de 3 componentes
├─ Fluxo de integração (5 etapas)
├─ Protocolo HTTP/REST com exemplo
├─ Segurança na integração (API Keys, TLS 1.3)
└─ Links: 
   └─ "Arquitetura de Integração"
   └─ "Implementação Técnica"
```

#### Pergunta 4: "Quais são os papéis de usuário?"

**Antes:**
```
IA: "Existem diferentes papéis..."
```

**Depois (NOVO):**
```
IA: "Ótima pergunta sobre papéis..."
├─ 5 Papéis definidos com permissões
├─ Tabela: Admin, Médico, Técnico, Recepcionista, Auditor
├─ O que cada um pode fazer
├─ Princípios de segurança (Least Privilege)
└─ Links: "Controle de Acesso e Permissões"
```

**✅ RESULTADO ESPERADO:**
- Respostas vêm RÁPIDO (<100ms, não infinito)
- Respostas têm estrutura (tópicos numerados, tabelas)
- Respostas incluem links para aulas relevantes
- 100% confiança (a IA "sabe" sobre esses tópicos!)

---

## 📊 TESTE 3: Outras Abas do Dashboard

### Progress (Progresso)
1. Dashboard → Aba **"Progresso"**
2. **Antes:** Carregava infinitamente 🔄
3. **Depois:** 
   - Mostra mensagem amigável: "Você ainda não iniciou nenhum curso"
   - OU mostra lista de cursos em progresso (se houver)
   - Carrega RÁPIDO, não infinito

### Certificados (Certificados)
1. Dashboard → Aba **"Certificados"**
2. **Antes:** Carregava infinitamente 🔄
3. **Depois:**
   - Mostra mensagem: "Você ainda não tem certificados"
   - OU mostra lista de certificados conquistados
   - Carrega RÁPIDO

---

## 📝 CHECKLIST DE VALIDAÇÃO

```
CONTEÚDO DAS AULAS
[ ] Onboarding INFANT.ID: 6 aulas, todas carregam com conteúdo
[ ] Integração Hospitalar: 4 aulas, todas carregam com conteúdo
[ ] Gerenciamento: 3 aulas, todas carregam com conteúdo
[ ] Total: 13 aulas, nenhuma vazia

IA E CONHECIMENTO
[ ] IA responde sobre biometria (100% confiança)
[ ] IA responde sobre segurança (100% confiança)
[ ] IA responde sobre integração (90% confiança)
[ ] IA retorna links para aulas relevantes
[ ] Respostas carregam RÁPIDO (<200ms)

INTERFACE
[ ] Dashboard abra sem erros 404
[ ] Course pages abram sem erros 404
[ ] Progress carrega rápido (não infinito)
[ ] Certificados carregam rápido (não infinito)
[ ] Chat IA responda rápido (não congela)

```

---

## 🐛 Se Encontrar Problemas

### Problema: Page não carrega / 404
**Solução:** Verifique se servidor está rodando:
```bash
cd backend && python run.py
```
Deve dizer: "Running on http://localhost:5001"

### Problema: Login falha
**Solução:** Use credenciais corretas:
```
Email: usuario.teste@infantid.com.br
Senha: user_seguro_123456
```

### Problema: IA não responde / responde genérica
**Solução:** Verifique se knowledge_base foi importado:
```bash
python -c "from app.services.knowledge_base import KNOWLEDGE_BASE; print(len(KNOWLEDGE_BASE))"
# Output: 8 (número de tópicos)
```

---

## 🎯 RESUMO DO TESTOU RÁPIDO (5 minutos)

1. ✅ Login com `usuario.teste@infantid.com.br`
2. ✅ Clique em "Cursos" → Veja 3 cursos com múltiplas aulas
3. ✅ Clique em "Começar" → Abra course.html → Veja 6 aulas do Onboarding
4. ✅ Volte → Abra "Integração Hospitalar" → Veja 4 aulas (ANTES: 404!)
5. ✅ Dashboard → "Assistente IA" → Pergunte "Como coletar biometria?"
6. ✅ Veja resposta estruturada com links (ANTES: "Como posso ajudar?")
7. ✅ Teste "Qual é a segurança?" → Veja tabela LGPD (ANTES: genérica)
8. ✅ Clique "Progresso" → Carregue RÁPIDO (ANTES: infinito)
9. ✅ Clique "Certificados" → Carregue RÁPIDO (ANTES: infinito)

**TEMPO TOTAL: 5-10 minutos para validar tudo! ⚡**

---

## 📸 ANTES vs DEPOIS

### Visualmente:

**ANTES:**
```
[Integração Hospitalar]
"Este curso não possui aulas ainda"
```

**DEPOIS:**
```
[Integração Hospitalar]
├─ 1. Arquitectura de Integração
├─ 2. Implementação Técnica
├─ 3. Workflow Clínico
└─ 4. Troubleshooting
```

**ANTES:**
```
Chat: "Qual é o protocolo de coleta?"
IA: "Bem-vindo! Como posso ajudá-lo?"
```

**DEPOIS:**
```
Chat: "Qual é o protocolo de coleta?"
IA: "📋 Protocolo de Coleta - 5 FASES
     [Tabela] [Links] [Dicas]"
```

---

## ✨ São Práticos - Testes Automáticos

Se quiser rodar testes automáticos:

```bash
cd backend
python -c "
from app.services.knowledge_base import buscar_resposta

# Teste 1: Biometria
r = buscar_resposta('Como coletar biometria?')
print(f'Biometria: {r[\"confianca\"]*100:.0f}% confiança')

# Teste 2: Segurança
r = buscar_resposta('Qual é o protocolo de segurança?')
print(f'Segurança: {r[\"confianca\"]*100:.0f}% confiança')

# Teste 3: Integração
r = buscar_resposta('Como integrar com HIS?')
print(f'Integração: {r[\"confianca\"]*100:.0f}% confiança')
"
```

Output esperado:
```
Biometria: 100% confiança
Segurança: 100% confiança
Integração: 90% confiança
```

---

## 🎉 Pronto para Testar!

A plataforma está **rodando agora** em:
```
http://localhost:5001
```

Acesse, teste, e veja que **todos os problemas foram resolvidos!** 🚀
