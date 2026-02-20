# 📡 API ROUTES DOCUMENTATION - Alura Jovem Believer

## Base URL
```
http://localhost:5001/api
```

---

## 🔐 AUTENTICAÇÃO - `/api/auth`

### 1. Registrar Novo Usuário
```
POST /api/auth/register
Content-Type: application/json

Request:
{
  "email": "usuario@example.com",
  "nome": "João Silva",
  "senha": "senha_segura_123",
  "hospital_id": 1
}

Response (201 Created):
{
  "mensagem": "Usuário registrado com sucesso",
  "usuario": {
    "id": 1,
    "email": "usuario@example.com",
    "nome": "João Silva",
    "hospital_id": 1,
    "funcao": "usuario",
    "ativo": true,
    "data_criacao": "2026-02-20T10:00:00"
  }
}

Error (400 Bad Request):
{
  "erro": "Campos obrigatórios faltando"
  // ou "Email já cadastrado"
}
```

### 2. Login
```
POST /api/auth/login
Content-Type: application/json

Request:
{
  "email": "usuario@example.com",
  "senha": "senha_segura_123"
}

Response (200 OK):
{
  "mensagem": "Login realizado com sucesso",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": 1,
    "email": "usuario@example.com",
    "nome": "João Silva",
    ...
  }
}

Error (401 Unauthorized):
{
  "erro": "Email ou senha inválidos"
}

Error (403 Forbidden):
{
  "erro": "Usuário desativado"
}
```

### 3. Logout
```
POST /api/auth/logout
Authorization: Bearer {token}

Response (200 OK):
{
  "mensagem": "Logout realizado com sucesso"
}
```

---

## 👥 USUÁRIOS - `/api/users`

### 1. Obter Dados do Usuário
```
GET /api/users/{user_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  "email": "usuario@example.com",
  "nome": "João Silva",
  "hospital_id": 1,
  "funcao": "usuario",
  "ativo": true,
  "data_criacao": "2026-02-20T10:00:00"
}

Error (404 Not Found):
{
  "erro": "Usuário não encontrado"
}
```

### 2. Atualizar Dados do Usuário
```
PUT /api/users/{user_id}
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "nome": "João Silva Atualizado",
  "email": "novo_email@example.com"
}

Response (200 OK):
{
  "mensagem": "Usuário atualizado com sucesso",
  "usuario": { ... }
}

Error (404 Not Found):
{
  "erro": "Usuário não encontrado"
}

Error (400 Bad Request):
{
  "erro": "Email já cadastrado"
}
```

---

## 📚 CURSOS - `/api/courses`

### 1. Listar Todos os Cursos
```
GET /api/courses?page=1&per_page=20
Authorization: Bearer {token}

Response (200 OK):
{
  "total": 5,
  "paginas": 1,
  "cursos": [
    {
      "id": 1,
      "titulo": "Introdução ao SUS",
      "descricao": "...",
      "instrutor_id": 1,
      "ativo": true,
      "data_criacao": "2026-02-20T10:00:00"
    }
    ...
  ]
}
```

### 2. Obter Detalhes de um Curso
```
GET /api/courses/{course_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  "titulo": "Introdução ao SUS",
  "descricao": "...",
  "instrutor_id": 1,
  "ativo": true,
  "aulas": [
    {
      "id": 1,
      "titulo": "Aula 1: Histórico",
      "conteudo": "...",
      "ordem": 1,
      "curso_id": 1
    }
    ...
  ]
}

Error (404 Not Found):
{
  "erro": "Curso não encontrado"
}
```

### 3. Criar Novo Curso (Admin/Instrutor)
```
POST /api/courses
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "titulo": "Novo Curso",
  "descricao": "Descrição do curso",
  "instrutor_id": 1
}

Response (201 Created):
{
  "mensagem": "Curso criado com sucesso",
  "curso": { ... }
}

Error (400 Bad Request):
{
  "erro": "Campos obrigatórios faltando"
}
```

---

## 🏥 HOSPITAIS - `/api/hospitals`

### 1. Listar Todos os Hospitais
```
GET /api/hospitals
Authorization: Bearer {token}

Response (200 OK):
{
  "hospitais": [
    {
      "id": 1,
      "nome": "Hospital X",
      "local": "São Paulo",
      "municipio": "São Paulo",
      "estado": "SP",
      "ativo": true
    }
    ...
  ]
}
```

### 2. Obter Detalhes de um Hospital
```
GET /api/hospitals/{hospital_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  "nome": "Hospital X",
  "local": "São Paulo",
  "municipio": "São Paulo",
  "estado": "SP",
  "ativo": true,
  "usuarios": [...]
}
```

---

## 🤖 IA - `/api/ai`

### 1. Iniciar Conversa com IA
```
POST /api/ai/chat
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "mensagem": "Qual é o objetivo do SUS?",
  "usuario_id": 1
}

Response (200 OK):
{
  "resposta": "O SUS (Sistema Único de Saúde) é um sistema público de saúde...",
  "conversa_id": 1,
  "mensagem_id": 1,
  "timestamp": "2026-02-20T10:00:00"
}
```

### 2. Obter Histórico de Conversa
```
GET /api/ai/conversations/{conversa_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  "usuario_id": 1,
  "mensagens": [
    {
      "id": 1,
      "usuario": "Qual é o objetivo do SUS?",
      "ia": "O SUS é um sistema público de saúde...",
      "timestamp": "2026-02-20T10:00:00"
    }
  ]
}
```

---

## 📄 DOCUMENTOS - `/api/documents`

### 1. Listar Documentos do Usuário
```
GET /api/documents
Authorization: Bearer {token}

Response (200 OK):
{
  "documentos": [
    {
      "id": 1,
      "titulo": "Documento 1",
      "tipo": "pdf",
      "usuario_id": 1,
      "data_criacao": "2026-02-20T10:00:00"
    }
    ...
  ]
}
```

### 2. Carregar Documento
```
POST /api/documents
Authorization: Bearer {token}
Content-Type: multipart/form-data

Request:
- file: (PDF file)
- titulo: "Meu Documento"

Response (201 Created):
{
  "mensagem": "Documento enviado com sucesso",
  "documento": { ... }
}
```

---

## 🔄 STATUS DE PROGRESSO - `/api/progress`

### 1. Obter Progresso do Usuário em um Curso
```
GET /api/progress/{user_id}/{course_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "usuario_id": 1,
  "curso_id": 1,
  "aulas_completas": 3,
  "total_aulas": 10,
  "percentual": 30,
  "data_inicio": "2026-02-20T10:00:00",
  "ultima_atualizacao": "2026-02-21T10:00:00"
}
```

### 2. Marcar Aula como Completa
```
POST /api/progress
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "usuario_id": 1,
  "aula_id": 1,
  "completada": true
}

Response (201 Created):
{
  "mensagem": "Progresso atualizado com sucesso",
  "progresso": { ... }
}
```

---

## 📋 STATUS DOS ENDPOINTS

| Endpoint | Método | Status | Prioridade |
|----------|--------|--------|-----------|
| /auth/register | POST | ✅ Implementado | ALTA |
| /auth/login | POST | ✅ Implementado | ALTA |
| /auth/logout | POST | ✅ Implementado | MÉDIA |
| /users/{id} | GET | ✅ Implementado | ALTA |
| /users/{id} | PUT | ✅ Implementado | ALTA |
| /courses | GET | ✅ Implementado | ALTA |
| /courses/{id} | GET | ✅ Implementado | ALTA |
| /courses | POST | ✅ Implementado | MÉDIA |
| /hospitals | GET | ✅ Implementado | MÉDIA |
| /hospitals/{id} | GET | ✅ Implementado | MÉDIA |
| /ai/chat | POST | ⚠️ Precisa verificar | ALTA |
| /ai/conversations/{id} | GET | ⚠️ Precisa verificar | ALTA |
| /documents | GET | ✅ Implementado | MÉDIA |
| /documents | POST | ✅ Implementado | BAIXA |
| /progress/{user_id}/{course_id} | GET | ⚠️ Precisa verificar | ALTA |
| /progress | POST | ⚠️ Precisa verificar | ALTA |

---

## ⚠️ PROBLEMAS ENCONTRADOS

1. **Respostas inconsistentes** - Alguns endpoints retornam `erro`, outros `message`
2. **Sem validação clara** - Falta validação de entrada em alguns endpoints
3. **Status HTTP inconsistentes** - 400 vs 404 não seguem RFC
4. **Documentação incompleta** - /ai e /documents não estão claros
5. **Sem paginação em alguns endpoints** - /documents, /hospitals

---

## 📝 PRÓXIMOS PASSOS

Para CADA endpoint, implementar:
1. ✅ Validação da entrada (request)
2. ✅ Lógica de negócio em controller
3. ✅ Resposta padronizada
4. ✅ Tratamento de erros
5. ✅ Teste com curl/Postman
