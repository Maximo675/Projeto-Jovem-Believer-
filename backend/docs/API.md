# Documentação da API - INFANT.ID

## Visão Geral

API RESTful para a plataforma de onboarding educacional INFANT.ID.

## Base URL

```
http://localhost:5000/api
```

## Autenticação

Todas as rotas protegidas requerem um token JWT no header:

```
Authorization: Bearer <token>
```

## Endpoints

### Autenticação

#### POST /auth/register
Registrar novo usuário

**Request:**
```json
{
  "email": "user@hospital.com",
  "nome": "João Silva",
  "senha": "senha_segura",
  "hospital_id": 1
}
```

**Response (201):**
```json
{
  "mensagem": "Usuário registrado com sucesso",
  "usuario": {
    "id": 1,
    "email": "user@hospital.com",
    "nome": "João Silva",
    "funcao": "usuario"
  }
}
```

#### POST /auth/login
Fazer login

**Request:**
```json
{
  "email": "user@hospital.com",
  "senha": "senha_segura"
}
```

**Response (200):**
```json
{
  "mensagem": "Login realizado com sucesso",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "usuario": {
    "id": 1,
    "email": "user@hospital.com",
    "nome": "João Silva"
  }
}
```

### Cursos

#### GET /courses
Listar todos os cursos

**Query Parameters:**
- `page` (int): Número da página (padrão: 1)
- `per_page` (int): Itens por página (padrão: 20)

**Response (200):**
```json
{
  "total": 15,
  "paginas": 1,
  "cursos": [
    {
      "id": 1,
      "titulo": "Onboarding Básico",
      "descricao": "...",
      "nivel": "basico",
      "autor": "Group Akiyama",
      "quantidade_aulas": 5
    }
  ]
}
```

#### GET /courses/<id>
Obter detalhes de um curso

**Response (200):**
```json
{
  "id": 1,
  "titulo": "Onboarding Básico",
  "descricao": "...",
  "aulas": [
    {
      "id": 1,
      "titulo": "Introdução",
      "ordem": 1,
      "duracao": 30
    }
  ]
}
```

#### GET /courses/<id>/aulas
Obter aulas de um curso

**Response (200):**
```json
{
  "curso_id": 1,
  "aulas": [
    {
      "id": 1,
      "titulo": "Aula 1",
      "descricao": "...",
      "ordem": 1
    }
  ]
}
```

### IA

#### POST /ia/consult
Consultar IA para dúvidas

**Request:**
```json
{
  "usuario_id": 1,
  "curso_id": 1,
  "pergunta": "O que é onboarding?"
}
```

**Response (200):**
```json
{
  "id": 1,
  "pergunta": "O que é onboarding?",
  "resposta": "Onboarding é o processo...",
  "tokens": 150
}
```

#### GET /ia/historico/<usuario_id>
Obter histórico de conversas com IA

**Response (200):**
```json
{
  "total": 5,
  "conversas": [
    {
      "id": 1,
      "pergunta": "...",
      "resposta": "...",
      "data_criacao": "2024-01-15T10:30:00"
    }
  ]
}
```

### Usuários

#### GET /users/<id>
Obter dados do usuário

**Response (200):**
```json
{
  "id": 1,
  "email": "user@hospital.com",
  "nome": "João Silva",
  "funcao": "usuario",
  "ativo": true
}
```

#### PUT /users/<id>
Atualizar dados do usuário

**Request:**
```json
{
  "nome": "João Silva Updated",
  "email": "newemail@hospital.com"
}
```

**Response (200):**
```json
{
  "mensagem": "Usuário atualizado com sucesso",
  "usuario": { ... }
}
```

## Códigos de Status

| Código | Significado |
|--------|------------|
| 200 | OK |
| 201 | Criado |
| 400 | Requisição inválida |
| 401 | Não autenticado |
| 403 | Não autorizado |
| 404 | Não encontrado |
| 500 | Erro do servidor |

## Erros

Respostas de erro seguem o formato:

```json
{
  "erro": "Descrição do erro"
}
```

## Rate Limiting

Por padrão, sem limitação. Pode ser configurado em produção.

## Versionamento

API versão: 1.0
