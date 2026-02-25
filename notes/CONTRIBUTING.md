# Contribuindo para INFANT.ID

Obrigado por querer contribuir para o projeto INFANT.ID! Este guia vai ajudá-lo a entender nosso processo de desenvolvimento.

## Como Começar

### 1. Faça um Fork e Clone
```bash
git clone https://github.com/seu-usuario/alura-jovem-believer.git
cd "Alura Jovem Believer"
```

### 2. Crie uma Branch para sua Feature
```bash
git checkout -b feature/minha-feature
```

### 3. Instale Dependências
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

## Padrões de Código

### Python
- Use [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Docstrings em todas as funções e classes
- Type hints quando possível
- Nomes descritivos

```python
def calcular_tempo_aprendizado(usuario_id: int, curso_id: int) -> int:
    """
    Calcula o tempo total gasto em um curso.
    
    Args:
        usuario_id: ID do usuário
        curso_id: ID do curso
    
    Returns:
        Tempo em minutos
    """
    pass
```

### JavaScript
- Use arrow functions
- Const por padrão
- Template literals para strings
- Comments claros

```javascript
const fetchUserProgress = async (userId) => {
    try {
        const response = await fetch(`/api/users/${userId}/progress`);
        return await response.json();
    } catch (error) {
        console.error('Erro ao buscar progresso:', error);
    }
};
```

## Commits

Use o formato convenção emoji:

```
✨ feat: Adicionar nova funcionalidade
🐛 fix: Corrigir bug
📚 docs: Atualizar documentação
🎨 style: Formatar código
♻️  refactor: Refatorar módulo
⚡ perf: Melhorar performance
✅ test: Adicionar testes
🔐 security: Melhorar segurança
```

Exemplo:
```bash
git commit -m "✨ feat: Adicionar autenticação com JWT"
git commit -m "🐛 fix: Corrigir bug no progresso do usuário"
git commit -m "📚 docs: Atualizar README com instruções de setup"
```

## Pull Request (PR)

1. **Descreva sua mudança** - Ser claro sobre o que foi feito
2. **Reference issues** - Se resolve alguma issue, mencione: `Fixes #123`
3. **Testes** - Inclua testes para nova funcionalidade
4. **Documentação** - Atualize docs se necessário

**Exemplo de PR:**
```markdown
## Descrição
Adiciona funcionalidade de recomendação de cursos baseado em IA.

## Tipo de Mudança
- [x] Nova feature
- [ ] Bug fix
- [ ] Documentation update

## Como Testar
1. Faça login como usuário
2. Complete um curso
3. Verifique as recomendações na página inicial

Fixes #42
```

## Testes

Sempre escreva testes para suas mudanças:

```python
# backend/tests/test_courses.py
import pytest
from app import create_app, db
from app.models.course import Course

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_criar_curso(app):
    with app.app_context():
        curso = Course(
            titulo="Test Course",
            descricao="Test",
            autor="Test Author"
        )
        db.session.add(curso)
        db.session.commit()
        
        assert curso.id is not None
        assert curso.titulo == "Test Course"
```

Rodar testes:
```bash
pytest backend/tests/
```

## Documentação

- Documente código complexo
- Atualize o README se adicionar features
- Adicione comentários para lógica não óbvia
- Mantenha docs/API.md atualizado

## Guia de Estilo

### Nomes de Variáveis
```python
# ✅ Bom
usuario_id = 1
nome_completo = "João Silva"
tempo_aprendizado = 120

# ❌ Ruim
uid = 1
nomeCompleto = "João Silva"
t = 120
```

### Funções
```python
# ✅ Bom - Verbo + Objeto
def registrar_usuario(email, nome):
    pass

def obter_progresso_usuario(usuario_id):
    pass

# ❌ Ruim
def usuario_registrar(email, nome):
    pass

def progressoUsuario(usuario_id):
    pass
```

## Reporting Issues

Encontrou um bug? Abra uma issue com:

1. **Descrição clara** do problema
2. **Passos para reproduzir**
3. **Comportamento esperado**
4. **Comportamento atual**
5. **Ambiente** (SO, Python version, etc)

```markdown
## Bug Report

### Descrição
Ao fazer login, recebo erro 500

### Passos para Reproduzir
1. Ir para página de login
2. Inserir email e senha
3. Clicar em "Entrar"

### Erro Esperado
Fazer login com sucesso

### Erro Atual
Erro 500 - Internal Server Error

### Ambiente
- Windows 11
- Python 3.11
- Chrome 120
```

## Perguntas?

- Abra uma issue para discussão
- Revise a documentação em `backend/docs/`
- Pergunte no README

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto.

---

**Obrigado por contribuir para INFANT.ID! 🎉**
