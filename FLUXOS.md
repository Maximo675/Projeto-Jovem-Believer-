# 🎯 Fluxos da Plataforma INFANT.ID

## 1️⃣ Fluxo de Autenticação

```
┌─────────────────────────────────────────────────────────┐
│ FASE 1: NOVO USUÁRIO                                    │
└─────────────────────────────────────────────────────────┘

    Browser                         Backend
       │                               │
       ├─→ Abre register.html          │
       │   (pages/register.html)       │
       │                               │
       ├─→ Preenche formulário         │
       │   (email, senha, hospital)    │
       │                               │
       ├─→ Clica "Registrar"           │
       │                               │
       ├─→ Envia POST /api/auth/reg... │
       │─────────────────────────────→│
       │                               ├─→ Valida email
       │                               ├─→ Hash da senha
       │                               ├─→ Salva no banco
       │                               │
       │←───────── Resposta 201 ───────│
       │   (usuário criado)            │
       │                               │
       ├─→ Redireciona para login      │
       │                               │

┌─────────────────────────────────────────────────────────┐
│ FASE 2: LOGIN                                           │
└─────────────────────────────────────────────────────────┘

    Browser                         Backend
       │                               │
       ├─→ Abre login.html             │
       │   (pages/login.html)          │
       │                               │
       ├─→ Preenche credentials        │
       │   (email, senha)              │
       │                               │
       ├─→ Clica "Entrar"              │
       │                               │
       ├─→ Envia POST /api/auth/login  │
       │─────────────────────────────→│
       │                               ├─→ Encontra usuário
       │                               ├─→ Valida senha
       │                               ├─→ Gera JWT token
       │                               │
       │←────── Token JWT 200 ─────────│
       │   (autenticação aceita)       │
       │                               │
       ├─→ Salva token (localStorage)  │
       │                               │
       ├─→ Redireciona para dashboard  │
       │                               │

┌─────────────────────────────────────────────────────────┐
│ FASE 3: DASHBOARD (Autenticado)                        │
└─────────────────────────────────────────────────────────┘

    Browser                         Backend
       │                               │
       ├─→ Abre dashboard.html         │
       │   (pages/dashboard.html)      │
       │                               │
       ├─→ Envia GET /api/documents    │
       │   + TOKEN                     │
       │─────────────────────────────→│
       │                               ├─→ Valida token
       │                               ├─→ Busca documentos
       │                               │
       │←────── Lista docs 200 ────────│
       │   (3 documentos)              │
       │                               │
       ├─→ Exibe documentos na página  │
       │                               │
```

---

## 2️⃣ Fluxo de Documentos

```
┌─────────────────────────────────────────────────────────┐
│ COMO DOCUMENTOS FUNCIONAM                               │
└─────────────────────────────────────────────────────────┘

    User Interface          API              File System
       │                    │                    │
       ├─ Clica em Docs ────│                    │
       │                    │                    │
       │                    ├─ GET /documents ──→│
       │                    │                    ├─ Lê: assets/documents/
       │                    │                    │   • Informativo Etan.docx
       │                    │                    │   • Procedimento de Coleta.docx
       │                    │                    │   • Protocolo Passo a Passo.docx
       │                    │                    │
       │                    │←─ Lista documentos─│
       │←─ Mostra lista ────│                    │
       │                    │                    │
       ├─ Clica documento ──│                    │
       │                    │                    │
       │                    ├─ GET /documents/[ID] │
       │                    │                    │
       │                    ├─ DocumentService ─→│
       │                    │   extrair_conteudo()
       │                    │                    ├─ python-docx
       │                    │                    ├─ Extrai texto
       │                    │←─ Conteúdo ───────│
       │                    │                    │
       │←─ Mostra conteúdo ─│                    │
       │                    │                    │
       ├─ Clica Download ───│                    │
       │                    ├─ GET /documents/[ID]/download
       │                    │                    │
       │                    │←─ Arquivo binário ─│
       │                    │    (.docx)         │
       │←─ Faz download ────│                    │
       │                    │                    │
```

---

## 3️⃣ Arquitetura Técnica

```
┌─────────────────────────────────────────────────────────┐
│ CAMADAS DA APLICAÇÃO                                    │
└─────────────────────────────────────────────────────────┘

FRONTEND (Navegador)
├── index.html (Homepage)
├── pages/
│   ├── login.html -------→ js/login.js ------→ main.js (ApiClient)
│   ├── register.html ----→ js/register.js ----→ main.js
│   └── dashboard.html ---→ [JavaScript] ------→ main.js
├── css/
│   ├── style.css (cores, layout)
│   └── login.css (formulários)
└── assets/
    ├── logo/logo.png
    └── documents/ (3 Word files)


│
│ HTTP/REST API
│ (JSON via fetch)
│


BACKEND (Python/Flask)
└── app/
    ├── routes/ (API Endpoints)
    │   ├── auth.py (POST /login, /register)
    │   ├── users.py (GET /users)
    │   ├── courses.py (GET/POST /courses)
    │   ├── hospitals.py (GET/POST /hospitals)
    │   ├── documents.py (GET /documents)
    │   └── ia.py (POST /consult)
    │
    ├── models/ (ORM SQLAlchemy)
    │   ├── User.py
    │   ├── Hospital.py
    │   ├── Course.py
    │   ├── Lesson.py
    │   ├── Progress.py
    │   ├── IAConversation.py
    │   └── Certificate.py
    │
    └── services/ (Lógica de Negócio)
        ├── auth_service.py
        ├── user_service.py
        ├── course_service.py
        └── document_service.py
                └── python-docx (extrair .docx)


│
│ SQL
│


DATABASE (MySQL/PostgreSQL)
├── hospitals (Hospitais)
├── users (Usuários)
├── courses (Cursos)
├── lessons (Aulas)
├── progress (Progresso)
├── ia_conversations (Chat)
└── certificates (Certificados)
```

---

## 4️⃣ Fluxo Completo de Uso

```
NOVO USUÁRIO
│
├─→ Abre: localhost:5000/
│   └─→ Vê homepage com info
│
├─→ Clica "Criar Conta"
│   └─→ Vai para /pages/register.html
│
├─→ Preenche:
│   ├─ Nome: João Silva
│   ├─ Email: joao@hospital.com
│   ├─ Hospital: Seleciona da lista (via API)
│   └─ Senha: SenhaTest123
│
├─→ Backend armazena no banco:
│   ├─ Hash na senha com bcrypt
│   ├─ Salva em MySQL/PostgreSQL
│   └─ Retorna sucesso
│
├─→ Redireciona para login
│   └─→ Vai para /pages/login.html
│
├─→ Faz login:
│   ├─ Email: joao@hospital.com
│   ├─ Senha: SenhaTest123
│   └─ Backend gera JWT token
│
├─→ Token salvo no localStorage
│   └─→ Identificado em futuras requisições
│
├─→ Redireciona para dashboard
│   └─→ Vai para /pages/dashboard.html
│
├─→ Dashboard carrega:
│   ├─ Seu nome (João Silva)
│   ├─ Hospital (aquele que escolheu)
│   ├─ Cards com:
│   │   ├─ Meus Cursos (3)
│   │   ├─ Documentos (3 Word files)
│   │   └─ Meu Progresso (45%)
│   └─  Botões para ver detalhes
│
├─→ Ao clicar "Ver Docs"
│   ├─ API busca /api/documents
│   ├─ python-docx extrai conteúdo
│   └─ Mostra na página
│
├─→ Ao clicar "Download"
│   ├─ Navegador faz GET /api/documents/[ID]/download
│   └─ Download do .docx original
│
└─→ Uso contínuo
    ├─ Enroll em cursos
    ├─ Ver aulas
    ├─ Track progresso
    ├─ Chat com IA
    └─ Ganhar certificados
```

---

## 5️⃣ Ciclo de Requisição HTTP

```
CLIENT REQUEST                      SERVER RESPONSE

GET /api/documents
├─ Headers:
│  ├─ Authorization: Bearer [JWT]
│  └─ Content-Type: application/json
│
├─ Body: (vazio para GET)
│
└─→ Chega ao backend:
      │
      ├─→ Flask router recebe em documents.py
      ├─→ Valida JWT token
      ├─→ Busca em document_service.py
      ├─→ Document service chama python-docx
      ├─→ Consulta banco de dados se preciso
      │
      └─→ Retorna resposta:
          ├─ Status: 200 OK
          ├─ Headers:
          │  └─ Content-Type: application/json
          │
          └─ Body:
             {
               "documentos": [
                 {
                   "id": 1,
                   "nome": "Informativo Etan",
                   "tipo": "docx",
                   "tamanho": "250KB"
                 },
                 ...
               ],
               "total": 3
             }

Client recebe e:
├─→ Parse JSON
├─→ Renderiza na página
└─→ Botões funcionam normalmente
```

---

## 6️⃣ Estado de Dados (LocalStorage)

```
┌─────────────────────────────────────────┐
│ LocalStorage (Cliente)                  │
└─────────────────────────────────────────┘

localStorage = {
  token: "eyJhbGciOiJIUzI1NiIs...",
           │
           └─ JWT que valida requisições
  
  user: {
    id: 1,
    nome: "João Silva",
    email: "joao@hospital.com",
    hospital: "Hospital Exemplo",
    funcao: "usuario"
  }
           │
           └─ Dados do usuário
}

Usado para:
├─ Manter login mesmo após refresh
├─ Saudar usuário no navbar
├─ Enviar em Authorization header
└─ Verificar se está logado
```

---

## 7️⃣ Fluxo de Cores

```
┌─────────────────────────────────┐
│ DESIGN COLORS                   │
└─────────────────────────────────┘

Fonte: Logo.png
└─→ Extraídas cores

Cores Aplicadas:
├── #00a86b (Verde Saúde)
│   └─ Botões, sucesso, principais
│
├── #1e90ff (Azul Médico)
│   └─ Navbar, links, secundário
│
├── #ff6b6b (Vermelho Alerta)
│   └─ Erros, avisos
│
├── #f0f8f5 (Fundo Claro)
│   └─ Background de seções
│
└── #333 (Texto Escuro)
    └─ Legibilidade

Localização:
├─ css/style.css (variáveis CSS)
├─ css/login.css (login específico)
├─ index.html (gradientes)
├─ pages/login.html (formulários)
└─ pages/dashboard.html (cards)
```

---

## 8️⃣ Estrutura de Pastas

```
Raiz/
│
├── 📄 START_HERE.md          ← Comece aqui!
├── 📄 CHECKLIST.md           ← Status visual
├── 📄 INDEX.md               ← Navegação
│
├── 📁 backend/
│   ├── 📄 run.py             ← Inicie aqui
│   ├── 📄 config.py
│   ├── 📄 requirements.txt
│   │
│   ├── 📁 app/
│   │   ├── 📄 __init__.py
│   │   ├── 📁 models/        (7 modelos)
│   │   ├── 📁 routes/        (6 rotas)
│   │   └── 📁 services/      (4 serviços)
│   │
│   ├── 📁 database/
│   │   └── 📄 schema.sql     ← SQL aqui
│   │
│   └── 📁 tests/
│       └── 📄 test_auth.py
│
├── 📁 pages/                 (HTML)
│   ├── 📄 login.html
│   ├── 📄 register.html
│   └── 📄 dashboard.html
│
├── 📁 css/
│   ├── 📄 style.css
│   └── 📄 login.css
│
├── 📁 js/
│   ├── 📄 main.js
│   ├── 📄 login.js
│   └── 📄 register.js
│
├── 📁 assets/
│   ├── 📁 logo/
│   │   └── 📄 logo.png
│   │
│   └── 📁 documents/
│       ├── 📄 Informativo Etan.docx
│       ├── 📄 Procedimento de Coleta.docx
│       └── 📄 Protocolo Passo a Passo.docx
│
├── 📁 docs/
│   ├── 📄 API.md
│   ├── 📄 DATABASE.md
│   └── 📄 IA.md
│
└── 📁 [outros documentos]
    ├── QUICKSTART.md
    ├── TEST_GUIDE.md
    ├── COMANDOS.md
    └── ...
```

---

## 9️⃣ Timing de Desenvolvimento

```
AGORA (0 min)
└─→ python run.py

5 MINUTOS
├─ Server rodando
├─ Testa homepage
└─ Vê cores verdes/azuis

15 MINUTOS
├─ Testa registro
├─ Testa login
└─ Vê dashboard

30 MINUTOS
├─ Teste com curl
├─ Vê documentos
└─ Entende API

1 HORA
├─ Lê QUICKSTART.md
├─ Setup banco de dados
└─ Testa com dados reais

2 HORAS
├─ Lê toda documentação
├─ Entende arquitetura
└─ Pronto para contribuir
```

---

## 🔟 Próximo Passo

### ✅ Tudo está documentado em diagramas visuais!

Para começar:
```
1. Abra START_HERE.md
2. Ou execute: cd backend && python run.py
3. Acesse: http://localhost:5000/pages/login.html
```

---

**Data:** 11 de Fevereiro de 2025
**Versão:** 1.0.0
**Status:** ✅ Completo
