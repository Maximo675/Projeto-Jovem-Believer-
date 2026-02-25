# INFANT.ID - Plataforma de Onboarding Educacional

## Sobre o Projeto

Plataforma educacional desenvolvida para melhorar a taxa de sucesso do onboarding da **INFANT.ID** para **95%**, atendendo hospitais em 9 estados. A plataforma integra **IA** para personalização de aprendizado e oferece uma experiência profissional e escalável.

### Objetivos Principais
- ✅ Aumentar taxa de sucesso do onboarding para 95%
- ✅ Criar plataforma educacional robusta e profissional
- ✅ Integrar IA para personalização de conteúdo
- ✅ Atender múltiplas instituições de saúde
- ✅ Facilitar gerenciamento de usuários e progresso

## Estrutura do Projeto

```
.
├── backend/                    # Backend da aplicação (Python/Flask)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/            # Modelos de dados
│   │   ├── routes/            # Rotas da API
│   │   ├── services/          # Lógica de negócio
│   │   ├── ai/                # Integração com IA
│   │   ├── utils/             # Funções utilitárias
│   │   └── config.py          # Configuração
│   ├── migrations/            # Migrações de banco de dados
│   ├── tests/                 # Testes unitários
│   ├── docs/                  # Documentação da API
│   ├── instance/              # Arquivos de instância (DB local)
│   └── run.py                 # Script principal
├── frontend/                  # Frontend (HTML/CSS/JS)
│   ├── css/                   # Estilos
│   ├── js/                    # Scripts JavaScript
│   ├── images/                # Imagens
│   └── pages/                 # Páginas HTML
├── database/                  # Scripts de banco de dados
│   ├── schema.sql             # Schema do banco
│   └── seeds.sql              # Dados iniciais
├── docs/                      # Documentação do projeto
├── .env.example               # Variáveis de ambiente (exemplo)
├── .gitignore                 # Arquivos ignorados pelo Git
├── requirements.txt           # Dependências Python
└── README.md                  # Este arquivo
```

## Pré-requisitos

- Python 3.9+
- MySQL/PostgreSQL
- DBeaver (para gerenciamento do BD)
- Node.js (opcional, para build de assets)

## Instalação

### 1. Clonar o repositório
```bash
git clone <seu_repositorio>
cd "Alura Jovem Believer"
```

### 2. Criar ambiente virtual
```bash
python -m venv .venv
```

### 3. Ativar ambiente virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações locais.

### 6. Criar banco de dados
```bash
# Use DBeaver para executar os scripts em database/
```

### 7. Executar a aplicação
```bash
python backend/run.py
```

A aplicação estará disponível em `http://localhost:5000`

## Tecnologias Utilizadas

### Backend
- **Flask** - Framework Web
- **SQLAlchemy** - ORM para banco de dados
- **OpenAI API** - Integração com IA
- **PyJWT** - Autenticação JWT

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilos
- **JavaScript** - Interatividade

### Banco de Dados
- **MySQL/PostgreSQL** - Dados persistentes
- **DBeaver** - Gerenciamento

## Configuração do Banco de Dados

### MySQL (Recomendado)
```sql
CREATE DATABASE infant_id_platform;
```

### PostgreSQL
```sql
CREATE DATABASE infant_id_platform;
```

## Estrutura de Modelos de Dados

### Entidades Principais
- **Hospital** - Instituições de saúde
- **Usuario** - Usuários da plataforma
- **Curso** - Cursos de onboarding
- **Aula** - Aulas dentro dos cursos
- **Progresso** - Rastreamento do progresso do usuário
- **ConversaIA** - Histórico de conversas com IA
- **Certificado** - Certificados ao completar cursos

## API Endpoints (Exemplo)

```
POST   /api/auth/login              - Login do usuário
POST   /api/auth/register           - Registro de novo usuário
GET    /api/users/<id>              - Obter dados do usuário
GET    /api/courses                 - Listar cursos disponíveis
GET    /api/courses/<id>            - Detalhes do curso
POST   /api/ia/consult              - Consultar IA para dúvidas
GET    /api/progress/<user_id>      - Progresso do usuário
```

## Integração com IA

A plataforma utiliza OpenAI para:
- Responder dúvidas sobre conteúdo
- Personalizar recomendações de aprendizado
- Gerar feedback personalizado
- Sugerir conteúdo complementar

### Configurar OpenAI
1. Obter chave API em https://platform.openai.com/
2. Adicionar em `.env`: `OPENAI_API_KEY=sua_chave`

## Variáveis de Ambiente

Veja `.env.example` para todas as variáveis disponíveis.

## Desenvolvimento

### Rodar em modo debug
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python backend/run.py
```

### Executar testes
```bash
pytest backend/tests/
```

## Deployment

### Produção com Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 backend.run:app
```

### Docker (futuro)
```bash
docker build -t infant-id .
docker run -p 5000:5000 infant-id
```

## Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
2. Commit suas mudanças (`git commit -m 'Add MinhaFeature'`)
3. Push para a branch (`git push origin feature/MinhaFeature`)
4. Abra um Pull Request

## Estrutura de Commits

- `feat:` - Novas features
- `fix:` - Correções de bugs
- `docs:` - Documentação
- `style:` - Formatação de código
- `refactor:` - Refatoração de código
- `test:` - Testes

## Solução de Problemas

### Erro de conexão com banco de dados
- Verifique credenciais em `.env`
- Verifique se MySQL/PostgreSQL está rodando
- Verifique porta do banco de dados

### Erro de chave OpenAI
- Verifique se `OPENAI_API_KEY` está em `.env`
- Verifique se a chave está válida em platform.openai.com

## Contato & Suporte

- **Empresa**: Group Akiyama
- **Projeto**: INFANT.ID Onboarding Platform
- **Status**: Em Desenvolvimento

## Licença

© 2026 Group Akiyama. Todos os direitos reservados.
