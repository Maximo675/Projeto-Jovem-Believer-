# 🔄 GUIA PRÁTICO: REFATORANDO ROTAS PARA PADRÃO MVC

## Objetivo
Transformar rotas desorganizadas em um padrão MVC limpo, com erros padronizados e lógica em controllers.

---

## 📝 COMPARAÇÃO: ANTES vs. DEPOIS

### ❌ ANTES (Desorganizado)
```python
# routes/auth.py - MISTURA LÓGICA COM ROTAS
@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validação manual
        required_fields = ['email', 'nome', 'senha', 'hospital_id']
        if not all(field in data for field in required_fields):
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
        
        # Verificar se usuário já existe
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'Email já cadastrado'}), 400
        
        # Criar usuário
        usuario = User(...)
        usuario.set_password(data['senha'])
        db.session.add(usuario)
        db.session.commit()
        
        # Resposta inconsistente
        return jsonify({
            'mensagem': 'Usuário registrado com sucesso',
            'usuario': usuario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
```

**Problemas:**
- ❌ Lógica misturada com rota
- ❌ Validação manual e repetida
- ❌ Respostas inconsistentes
- ❌ Difícil de testar
- ❌ Código repetido


### ✅ DEPOIS (Padrão MVC)
```python
# controllers/auth_controller.py - LÓGICA CENTRALIZADA
class AuthController:
    @staticmethod
    def register(email, nome, senha, hospital_id=None):
        # Validação centralizada
        Validator.validate_required({'email': email, 'nome': nome, 'senha': senha})
        Validator.validate_email(email)
        Validator.validate_length(senha, min_len=8)
        
        # Verificar duplicata
        if User.query.filter_by(email=email).first():
            raise ConflictError(f"Email '{email}' já cadastrado")
        
        # Criar usuário
        usuario = User(...)
        # ... resto da lógica
        return {...}


# routes/auth.py - APENAS ROTA E RESPOSTA
@bp.route('/register', methods=['POST'])
@handle_errors
def register():
    data = request.get_json()
    resultado = AuthController.register(
        email=data.get('email'),
        nome=data.get('nome'),
        senha=data.get('senha'),
        hospital_id=data.get('hospital_id')
    )
    return APIResponse.created(resultado, "Usuário registrado com sucesso")
```

**Benefícios:**
- ✅ Código limpo e organizado
- ✅ Lógica testável
- ✅ Respostas padronizadas
- ✅ Erros consistentes
- ✅ Fácil de manter


---

## 🛠️ PASSO-A-PASSO PARA REFATORAR

### Passo 1: Criar o Controller
**Arquivo:** `backend/app/controllers/nome_controller.py`

```python
from app import db
from app.models.seu_modelo import SeuModelo
from app.utils.responses import Validator, BadRequestError, NotFoundError, ConflictError

class SeuController:
    @staticmethod
    def metodo(parametro1, parametro2):
        """
        Descrição do método
        
        Args:
            parametro1: Descrição
            parametro2: Descrição
        
        Returns:
            dict: Dados retornados
        
        Raises:
            BadRequestError: Se dados inválidos
        """
        
        # 1. VALIDAR ENTRADA
        Validator.validate_required({'param1': parametro1}, ['param1'])
        
        # 2. LÓGICA DE NEGÓCIO
        modelo = SeuModelo.query.get(parametro1)
        if not modelo:
            raise NotFoundError("Modelo não encontrado")
        
        # 3. PROCESSAR
        # ... código aqui ...
        
        # 4. RETORNAR DADOS
        return {
            'id': modelo.id,
            'nome': modelo.nome,
        }
```


### Passo 2: Refatorar a Rota
**Arquivo:** `backend/app/routes/seu_arquivo.py`

```python
from flask import Blueprint, request
from app.controllers.seu_controller import SeuController
from app.utils.responses import APIResponse, handle_errors

bp = Blueprint('seu_blueprint', __name__, url_prefix='/api/seu_endpoint')

@bp.route('/<int:id>', methods=['GET'])
@handle_errors
def get_something(id):
    """GET /api/seu_endpoint/{id}"""
    resultado = SeuController.get_something(id)
    return APIResponse.success(resultado)

@bp.route('', methods=['POST'])
@handle_errors
def create_something():
    """POST /api/seu_endpoint"""
    data = request.get_json()
    resultado = SeuController.create_something(
        param1=data.get('param1'),
        param2=data.get('param2')
    )
    return APIResponse.created(resultado, "Recurso criado com sucesso")
```


### Passo 3: Adicionar Importações no `__init__.py`
**Arquivo:** `backend/app/controllers/__init__.py`

```python
from .seu_controller import SeuController

__all__ = ['SeuController']
```


### Passo 4: Testar com cURL
```bash
# GET
curl -X GET "http://localhost:5001/api/seu_endpoint/1" \
  -H "Authorization: Bearer seu_token"

# POST
curl -X POST "http://localhost:5001/api/seu_endpoint" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer seu_token" \
  -d '{
    "param1": "valor1",
    "param2": "valor2"
  }'
```


---

## 📋 CHECKLIST DE REFATORAÇÃO

Quando refatorar uma rota, verifique:

- [ ] **Controller criado** com toda a lógica
- [ ] **Validação de entrada** usando `Validator`
- [ ] **Exceções customizadas** para erros (BadRequestError, NotFoundError, etc)
- [ ] **Resposta padronizada** usando `APIResponse`
- [ ] **@handle_errors decorator** na rota
- [ ] **Documentação** no docstring
- [ ] **Teste com cURL** funcionando
- [ ] **Integração com frontend** testada


---

## 🚀 EXEMPLO COMPLETO: Refatorar Auth

### ✅ PASSO 1: Criar AuthController (JÁ FEITO)
✓ Arquivo criado: `backend/app/controllers/auth_controller.py`


### ✅ PASSO 2: Refatorar routes/auth.py
```python
# ============ ANTES ============
@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        # ... 50 linhas de lógica ...
        return jsonify({'usuario': ...}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ============ DEPOIS ============
from app.controllers.auth_controller import AuthController

@bp.route('/register', methods=['POST'])
@handle_errors
def register():
    """POST /api/auth/register - Registrar novo usuário"""
    data = request.get_json()
    resultado = AuthController.register(
        email=data.get('email'),
        nome=data.get('nome'),
        senha=data.get('senha'),
        hospital_id=data.get('hospital_id')
    )
    return APIResponse.created(resultado, "Usuário registrado com sucesso")
```


---

## 🧪 TESTE DO NOVO PADRÃO

### 1. Teste com cURL
```bash
# Post de registro
curl -X POST "http://localhost:5001/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "novo@exemplo.com",
    "nome": "João Silva",
    "senha": "senha_segura_123",
    "hospital_id": 1
  }'

# Resposta esperada (201 Created):
{
  "sucesso": true,
  "mensagem": "Usuário registrado com sucesso",
  "data": {
    "id": 1,
    "email": "novo@exemplo.com",
    "nome": "João Silva",
    ...
  }
}

# Erro esperado (409 Conflict):
{
  "sucesso": false,
  "mensagem": "Email 'novo@exemplo.com' já cadastrado",
  "erro": "CONFLICT"
}
```


### 2. Verificar Padrão de Erro
```bash
# Request inválido (sem campos obrigatórios)
curl -X POST "http://localhost:5001/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "teste@exemplo.com"}'

# Resposta (400 Bad Request):
{
  "sucesso": false,
  "mensagem": "Campos obrigatórios faltando: nome, senha",
  "erro": "BAD_REQUEST"
}
```


---

## 📊 ORDEM DE REFATORAÇÃO RECOMENDADA

1. **ALTA PRIORIDADE (Esta semana)**
   - [ ] Refatorar `/api/auth/register`
   - [ ] Refatorar `/api/auth/login`
   - [ ] Refatorar `/api/users/{id}`

2. **MÉDIA PRIORIDADE (Próxima semana)**
   - [ ] Refatorar `/api/courses`
   - [ ] Refatorar `/api/hospitals`

3. **BAIXA PRIORIDADE (Após estável)**
   - [ ] Refatorar `/api/ai`
   - [ ] Refatorar `/api/documents`


---

## ⚠️ CUIDADOS IMPORTANTES

1. **NÃO quebre a retrocompatibilidade** - Mude uma rota por vez
2. **Faça commits após cada rota** - Para poder voltar se necessário
3. **Documente os erros** - Use mensagens claras
4. **Teste cada mudança** - Com o frontend realmente
5. **Mantenha os modelos atualizados** - Certifique-se dos relacionamentos


---

## 📞 DÚVIDAS COMUNS

**P: Posso deixar rotas antigas e criar novas?**
R: Não, refatore gradualmente. Uma rota por vez.

**P: E se o frontend usar endpoint diferente?**
R: Atualize o frontend ao mesmo tempo. Mantenha sincronizado.

**P: Como faço rollback?**
R: Use git: `git diff` para ver mudanças, `git checkout` para reverter.

**P: Preciso reescrever os testes?**
R: Sim, mas agora é mais fácil testar controllers separado de rotas.
