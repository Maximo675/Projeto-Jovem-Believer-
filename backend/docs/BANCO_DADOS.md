# Documentação do Banco de Dados - INFANT.ID

## Visão Geral

Banco de dados relacional para armazenar informações de usuários, cursos, progresso e conversas com IA.

## Diagrama de Entidades

```
Hospitals (1) ──── (N) Users
                      │
                      ├─── (N) Progress ──── (N) Courses
                      │                         │
                      ├─── (N) IAConversation   └─── (N) Lessons
                      │
                      └─── (N) Certificates
```

## Tabelas

### hospitals
Informações dos hospitais clientes.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT PK | ID único |
| nome | VARCHAR(255) | Nome do hospital |
| estado | VARCHAR(2) | Sigla do estado (SP, RJ, etc) |
| cidade | VARCHAR(120) | Cidade |
| endereco | VARCHAR(255) | Endereço |
| telefone | VARCHAR(20) | Telefone |
| email | VARCHAR(120) | Email |
| cnpj | VARCHAR(18) | CNPJ |
| ativo | BOOLEAN | Status |
| data_criacao | DATETIME | Data de criação |
| data_atualizacao | DATETIME | Data de atualização |

### users
Usuários da plataforma.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT PK | ID único |
| email | VARCHAR(120) | Email (único) |
| nome | VARCHAR(120) | Nome completo |
| senha_hash | VARCHAR(255) | Senha hasheada |
| hospital_id | INT FK | Referência a hospital |
| funcao | VARCHAR(50) | admin, instrutor, usuario |
| ativo | BOOLEAN | Status |
| data_criacao | DATETIME | Data de criação |
| data_atualizacao | DATETIME | Data de atualização |

### courses
Cursos disponíveis.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT PK | ID único |
| titulo | VARCHAR(255) | Título do curso |
| descricao | TEXT | Descrição |
| nivel | VARCHAR(20) | basico, intermediario, avancado |
| tempo_estimado | INT | Duração em minutos |
| autor | VARCHAR(120) | Autor |
| imagem_url | VARCHAR(255) | URL da imagem |
| ativo | BOOLEAN | Status |
| data_criacao | DATETIME | Data de criação |
| data_atualizacao | DATETIME | Data de atualização |

### lessons
Aulas dentro dos cursos.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT PK | ID único |
| curso_id | INT FK | Referência a course |
| titulo | VARCHAR(255) | Título da aula |
| descricao | TEXT | Descrição |
| conteudo | LONGTEXT | Conteúdo HTML |
| ordem | INT | Ordem na sequência |
| duracao | INT | Duração em minutos |
| video_url | VARCHAR(255) | URL do vídeo |
| material_complementar | TEXT | Links de material |
| ativo | BOOLEAN | Status |
| data_criacao | DATETIME | Data de criação |
| data_atualizacao | DATETIME | Data de atualização |

### progress
Progresso dos usuários em cursos.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT PK | ID único |
| usuario_id | INT FK | Referência a user |
| curso_id | INT FK | Referência a course |
| aula_id | INT FK | Referência a lesson |
| percentual | INT | Percentual de conclusão (0-100) |
| concluido | BOOLEAN | Se foi concluído |
| data_inicio | DATETIME | Quando iniciou |
| data_conclusao | DATETIME | Quando concluiu |
| tempo_gasto | INT | Tempo gasto em segundos |
| data_atualizacao | DATETIME | Data de atualização |

### ia_conversations
Histórico de conversas com IA.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT PK | ID único |
| usuario_id | INT FK | Referência a user |
| curso_id | INT FK | Referência a course |
| pergunta | TEXT | Pergunta do usuário |
| resposta | TEXT | Resposta da IA |
| modelo_ia | VARCHAR(50) | Modelo utilizado |
| tokens_usados | INT | Tokens gastos |
| avaliacao | INT | Avaliação do usuário (1-5) |
| data_criacao | DATETIME | Data de criação |

### certificates
Certificados emitidos.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT PK | ID único |
| usuario_id | INT FK | Referência a user |
| curso_id | INT FK | Referência a course |
| numero_certificado | VARCHAR(50) | Número único |
| data_emissao | DATETIME | Data de emissão |
| validade | INT | Validade em dias |
| arquivo_url | VARCHAR(255) | URL do PDF |

## Índices

Para melhor performance, as seguintes índices foram criadas:

- `idx_email` em users
- `idx_hospital` em users
- `idx_estado` em hospitals
- `idx_ativo` em courses
- `idx_nivel` em courses
- `idx_curso` em lessons
- `idx_ordem` em lessons
- `idx_usuario_concluido` em progress (composto)
- `idx_data` em ia_conversations

## Relacionamentos

### One-to-Many
- Hospital → Users
- Hospital → Documents
- Course → Lessons
- Course → Progress
- User → Progress
- User → IAConversations
- User → Certificates

### Many-to-Many (implícito)
- Users (via Progress) ↔ Courses
- Users (via IAConversation) ↔ Courses

## Constraints

- **UNIQUE**: email em users, email em hospitals, titulo em courses
- **FOREIGN KEYS**: Com ON DELETE CASCADE ou SET NULL conforme apropriado
- **CHECK**: status fields (ativo) com valores booleanos
- **DEFAULT**: CURRENT_TIMESTAMP para data_criacao

## Backup e Manutenção

### Backup
```bash
mysqldump -u root -p infant_id_platform > backup.sql
```

### Restauração
```bash
mysql -u root -p infant_id_platform < backup.sql
```

## Performance

### Queries frequentes otimizadas:

1. Listar cursos ativos:
```sql
SELECT * FROM courses WHERE ativo = TRUE ORDER BY data_criacao DESC;
```

2. Progresso do usuário:
```sql
SELECT * FROM progress WHERE usuario_id = ? AND concluido = FALSE;
```

3. Histórico de conversas:
```sql
SELECT * FROM ia_conversations WHERE usuario_id = ? ORDER BY data_criacao DESC LIMIT 20;
```

## Notas

- Todas as senhas devem ser armazenadas como hash bcrypt
- Datas usam UTC
- Charset: UTF8MB4 para suportar emojis e caracteres especiais
- Collation: utf8mb4_unicode_ci para melhor compatibilidade
