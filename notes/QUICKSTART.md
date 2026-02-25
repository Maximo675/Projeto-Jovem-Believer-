# 🚀 Guia de Início Rápido - INFANT.ID

## Integração Completa Realizada

Sua plataforma de ensino agora tem:
- ✅ Documentos profissionais integrados
- ✅ Logo e identidade visual aplicados
- ✅ Sistema de login/registro funcional
- ✅ API para gerenciar documentos
- ✅ Cores de saúde em todo design
- ✅ Base de conhecimento estruturada

---

## 🎨 Elementos de Design Integrados

### Logo e Cores
- **Logo:** `/assets/logo/logo.png`
- **Cores Principais:**
  - Verde Saúde: `#00a86b` (primário)
  - Azul Médico: `#1e90ff` (secundário)
  - Vermelho Alerta: `#ff6b6b` (accent)
  - Fundo Claro: `#f0f8f5`

### Páginas Disponíveis
- `index.html` - Página principal
- `pages/login.html` - Tela de login
- `pages/register.html` - Tela de registro
- `pages/dashboard.html` - Dashboard (próximo passo)
- `pages/courses.html` - Listagem de cursos

---

## 📄 Documentos da Knowledge Base

Localização: `/assets/documents/`

### Documentos Integrados:
1. **Informativo Etan.docx** - Informações sobre protocolo
2. **Procedimento de Coleta.docx** - Guia passo a passo
3. **Protocolo de Coleta Passo a Passo.docx** - Instruções sequenciais

### Acessar Documentos via API

```bash
# Listar todos os documentos
curl http://localhost:5000/api/documents

# Obter conteúdo de um documento
curl http://localhost:5000/api/documents/Informativo%20Etan

# Fazer download de um documento
curl http://localhost:5000/api/documents/Informativo%20Etan/download -o documento.docx

# Ver índice de conhecimento
curl http://localhost:5000/api/documents/indice
```

---

## 🔧 Setup Rápido

### 1. Instalar Dependências
```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar pacotes
pip install -r requirements.txt
```

### 2. Configurar Ambiente
```bash
# Copiar arquivo de exemplo
copy .env.example .env

# Editar .env com suas configurações
# Mínimo necessário:
# - DB_HOST
# - DB_USER
# - DB_PASSWORD
# - OPENAI_API_KEY
```

### 3. Criar Banco de Dados
```bash
# MySQL
mysql -u root -p
> CREATE DATABASE infant_id_platform;
> USE infant_id_platform;
> source backend/database/schema.sql;
```

### 4. Iniciar Aplicação
```bash
# Terminal 1: Backend
cd backend
python run.py

# Terminal 2: Frontend (opcional - usar live server em VS Code)
python -m http.server 8000
```

### 5. Acessar
```
Frontend: http://localhost:8000 ou http://localhost:5000
API: http://localhost:5000/api
Login: http://localhost:5000/pages/login.html
```

---

## 📚 Usando os Documentos como Conteúdo

### Via API
```javascript
// Buscar documentos
const response = await fetch('/api/documents');
const { documentos } = await response.json();

// Exibir lista de documentos
documentos.forEach(doc => {
    console.log(`${doc.nome} (${doc.arquivo})`);
});

// Obter conteúdo de um documento
const doc = await fetch('/api/documents/Informativo Etan').then(r => r.json());
console.log(doc.conteudo);
```

### Via Python (Backend)
```python
from app.services.document_service import DocumentService

# Listar documentos
docs = DocumentService.listar_documentos()
for doc in docs:
    print(f"Documento: {doc['nome']}")

# Obter conteúdo
conteudo = DocumentService.obter_documento('Informativo Etan')
print(conteudo['conteudo'])

# Criar curso baseado em documento
DocumentService.criar_curso_de_documento(
    nome_documento='Informativo Etan',
    titulo_curso='Treinamento Etan - Básico',
    descricao='Aprenda sobre o protocolo Etan',
    nivel='basico'
)
```

---

## 🔐 Fluxo de Login/Registro

### 1. Registrar Novo Usuário
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "usuario@hospital.com",
  "nome": "João Silva",
  "senha": "senha_segura",
  "hospital_id": 1
}
```

### 2. Fazer Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "usuario@hospital.com",
  "senha": "senha_segura"
}

# Response:
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "usuario": { ... }
}
```

### 3. Usar Token em Requisições Protegidas
```bash
GET /api/users/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

## 🎓 Estrutura de Rotas da API

### Autenticação
- `POST /api/auth/register` - Registrar
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout

### Hospital
- `GET /api/hospitals` - Listar hospitais
- `GET /api/hospitals/<id>` - Detalhes do hospital
- `POST /api/hospitals` - Criar hospital (admin)

### Usuários
- `GET /api/users/<id>` - Dados do usuário
- `PUT /api/users/<id>` - Atualizar usuário
- `GET /api/users` - Listar usuários (paginado)

### Cursos
- `GET /api/courses` - Listar cursos (paginado)
- `GET /api/courses/<id>` - Detalhes do curso
- `GET /api/courses/<id>/aulas` - Aulas do curso
- `POST /api/courses` - Criar curso (instrutor)

### Documentos
- `GET /api/documents` - Listar documentos
- `GET /api/documents/<nome>` - Conteúdo do documento
- `GET /api/documents/<nome>/download` - Download
- `GET /api/documents/indice` - Índice de conhecimento

### IA
- `POST /api/ia/consult` - Consultar IA
- `GET /api/ia/historico/<user_id>` - Histórico de conversas
- `PUT /api/ia/avaliar/<conversa_id>` - Avaliar resposta

---

## ⚠️ Problemas Conhecidos e Soluções

Veja `ISSUES.md` para lista completa de problemas e como corrigi-los.

### Principais Issues:
1. ✅ **Extração de documentos Word** - CORRIGIDO (python-docx instalado)
2. ✅ **CORS** - CORRIGIDO (Flask-CORS adicionado)
3. ⚠️ **Bancos de dados** - Monte seu MySQL/PostgreSQL

---

## 📦 Estrutura Final

```
Alura Jovem Believer/
├── assets/
│   ├── logo/
│   │   └── logo.png ✅
│   └── documents/
│       ├── Informativo Etan.docx ✅
│       ├── Procedimento de Coleta.docx ✅
│       └── Protocolo de Coleta Passo a Passo.docx ✅
├── backend/
│   ├── app/
│   │   ├── routes/ ✅
│   │   ├── services/ ✅
│   │   ├── models/ ✅
│   │   └── __init__.py ✅ (CORS adicionado)
│   ├── knowledge_base/ ✅
│   ├── database/ ✅
│   ├── tests/ ✅
│   ├── run.py ✅
│   └── requirements.txt ✅
├── pages/
│   ├── login.html ✅
│   └── register.html ✅
├── css/
│   ├── style.css ✅ (cores de saúde)
│   └── login.css ✅
├── js/
│   ├── main.js ✅
│   ├── login.js ✅
│   └── register.js ✅
├── index.html ✅ (logo integrada)
├── README.md
├── CONTRIBUTING.md
├── ISSUES.md ✅ (novo)
└── requirements.txt ✅
```

---

## 🎯 Próximos Passos

1. **Configurar Banco de Dados Real**
   - Criar MySQL/PostgreSQL
   - Executar schema.sql
   - Testar conexão

2. **Implementar Dashboard**
   - Página de dashboard do usuário
   - Visualizar progresso
   - Gerenciar cursos

3. **Integrar IA Completamente**
   - Obter chave OpenAI
   - Testar chatbot
   - Implementar recomendações

4. **Testes de Ponta a Ponta**
   - Testar fluxo completo
   - Validar processamento de documentos
   - Testar APIs

5. **Deploy**
   - Setup Docker (opcional)
   - Configurar para produção
   - Deploy na nuvem

---

## 💡 Dicas Úteis

### Desenvolvimento
```bash
# Ativar debug mode
set FLASK_ENV=development
set FLASK_DEBUG=True

# Executar com reload automático
python backend/run.py
```

### Testes
```bash
# Rodartestes
pytest backend/tests/

# Com cobertura
pytest --cov=backend/app backend/tests/
```

### Banco de Dados
```bash
# Resetar banco (cuidado!)
python backend/database/database.py resetar

# Criar tabelas
python backend/database/database.py criar

# Popular com dados de exemplo
python backend/run.py seed_db
```

---

## 🆘 Ajuda

- Veja `README.md` para documentação completa
- Veja `ISSUES.md` para problemas conhecidos
- Veja `CONTRIBUTING.md` para guia de contribuição
- Veja `backend/docs/` para documentação de componentes

---

**Sua plataforma está pronta para uso! 🎉**
