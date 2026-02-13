# Issues & Correções - INFANT.ID

## ⚠️ Problemas Conhecidos

### 1. Extensão de Arquivo .docx - Parsing de Conteúdo
**Status:** ⚠️ PENDENTE  
**Severidade:** Alta  
**Descrição:** O serviço `document_service.py` ainda não extrai conteúdo real dos arquivos .docx  
**Causa:** Dependência `python-docx` não foi adicionada ao requirements.txt  
**Solução:**
```bash
pip install python-docx
```
**Código Corrigido:**
```python
from docx import Document

@staticmethod
def extrair_conteudo(caminho_arquivo):
    """Extrai conteúdo de um arquivo Word"""
    try:
        doc = Document(caminho_arquivo)
        conteudo = '\n'.join([p.text for p in doc.paragraphs])
        return conteudo
    except Exception as e:
        raise Exception(f"Erro ao extrair conteúdo: {str(e)}")
```

### 2. Rota de Hospitals Faltava no __init__.py
**Status:** ✅ CORRIGIDO  
**Severidade:** Alta  
**Descrição:** Blueprints de hospitals e documents não foram registrados na aplicação  
**Solução:** Atualizou `backend/app/__init__.py` para registrar todas as rotas

### 3. Placeholder de Arquivo no .env.example
**Status:** ⚠️ PENDENTE  
**Severidade:** Média  
**Descrição:** Configuração SQLALCHEMY_DATABASE_URI com valores hardcoded  
**Solução:** Usar variáveis de ambiente completas
```env
# Adicionar ao .env:
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=infant_id_platform
SQLALCHEMY_DATABASE_URI=mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

### 4. Validação de Email no Frontend
**Status:** ⚠️ PARCIAL  
**Severidade:** Baixa  
**Descrição:** Campo de email não possui pattern HTML5 ideal  
**Solução:** Adicionar pattern no input
```html
<input 
    type="email" 
    id="email" 
    name="email" 
    pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    required
>
```

### 5. Tratamento de Erro de Conexão no AI Service
**Status:** ⚠️ PENDENTE  
**Severidade:** Alta  
**Descrição:** Sem retry logic para falhas de API OpenAI  
**Solução:** Implementar retry com backoff exponencial
```python
import time
from functools import wraps

def retry_on_failure(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    time.sleep(delay ** attempts)
        return wrapper
    return decorator
```

### 6. Falta de CORS Configuration
**Status:** ⚠️ PENDENTE  
**Severidade:** Média  
**Descrição:** CORS não está configurado na aplicação Flask  
**Solução:** Adicionar Flask-CORS
```bash
pip install flask-cors
```

**Código:**
```python
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))
    # ... resto do código
```

### 7. Falta de Logging Centralizado
**Status:** ⚠️ PENDENTE  
**Severidade:** Baixa  
**Descrição:** Sem sistema de logging estruturado  
**Solução:** Implementar logging com arquivo

### 8. Documentação Swagger/OpenAPI
**Status:** ⚠️ PENDENTE  
**Severidade:** Baixa  
**Descrição:** API sem documentação interativa  
**Solução:** Adicionar flask-restx ou flasgger
```bash
pip install flasgger
```

### 9. Testes Incompletos
**Status:** ⚠️ PENDENTE  
**Severidade:** Média  
**Descrição:** Apenas teste de autenticação implementado  
**Solução:** Adicionar testes para cursos, documentos e IA

### 10. Validação de Senha Fraca
**Status:** ⚠️ PENDENTE  
**Severidade:** Alta  
**Descrição:** Sem validação de força de senha no backend  
**Solução:** Integrar validador de senha
```python
def validar_senha_forte(senha):
    if len(senha) < 8:
        return False, "Mínimo 8 caracteres"
    if not any(c.isupper() for c in senha):
        return False, "Deve conter letra maiúscula"
    if not any(c.isdigit() for c in senha):
        return False, "Deve conter número"
    return True, "Válida"
```

## ✅ Correções Implementadas Nesta Sessão

- ✅ Criado sistema de login/registro
- ✅ Integrada logo do projeto
- ✅ Atualizado design com cores de saúde
- ✅ Estruturado knowledge base com documentos
- ✅ Criado document_service para gerenciar documentos
- ✅ Adicionadas rotas para hospitals e documents API
- ✅ Registrados todos os blueprints na aplicação

## 🔧 Checklist de Correções Pendentes

- [ ] Instalar `python-docx` e implementar extração de conteúdo real
- [ ] Configurar CORS na aplicação
- [ ] Implementar retry logic no AI service
- [ ] Melhorar validação de senha
- [ ] Adicionar testes completos
- [ ] Implementar logging centralizado
- [ ] Adicionar documentação Swagger
- [ ] Configurar banco de dados MySQL/PostgreSQL
- [ ] Implementar cache Redis (opcional)
- [ ] Setup de CI/CD pipeline

## 🚀 Prioridade de Correção

### ALTA (Fazer agora)
1. Instalar `python-docx` e extrair conteúdo real dos documentos
2. Testar login/registro com banco de dados real
3. Configurar variáveis de ambiente corretamente
4. Implementar retry logic na IA

### MÉDIA (Fazer em breve)
1. Configurar CORS
2. Melhorar validação de senha
3. Adicionar mais testes
4. Implementar logging

### BAIXA (Fazer depois)
1. Documentação Swagger
2. Cache Redis
3. Otimizações de performance
4. UI melhorias adicionais

## 📞 Como Reportar Novos Problemas

Crie um novo arquivo: `bug_report.md` com:
- Descrição do problema
- Passos para reproduzir
- Comportamento esperado
- Comportamento atual
- Logs/erros
