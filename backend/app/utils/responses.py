"""
Utilitários para respostas padronizadas da API
"""

from flask import jsonify
import traceback
from functools import wraps
import os

# ============================================
# PADRÃO DE RESPOSTA
# ============================================

class APIResponse:
    """Classe para padronizar respostas da API"""
    
    @staticmethod
    def success(data=None, message="Operação realizada com sucesso", status_code=200):
        """Resposta de sucesso"""
        response = {
            "sucesso": True,
            "mensagem": message,
            "data": data if data is not None else {}
        }
        return jsonify(response), status_code
    
    @staticmethod
    def created(data=None, message="Recurso criado com sucesso", status_code=201):
        """Resposta para criação de recurso"""
        response = {
            "sucesso": True,
            "mensagem": message,
            "data": data if data is not None else {}
        }
        return jsonify(response), status_code
    
    @staticmethod
    def error(message="Erro ao processar requisição", status_code=400, error_code=None):
        """Resposta de erro"""
        response = {
            "sucesso": False,
            "mensagem": message,
            "erro": error_code or f"ERROR_{status_code}"
        }
        return jsonify(response), status_code
    
    @staticmethod
    def bad_request(message="Requisição inválida", error_code=None):
        """400 - Requisição inválida"""
        return APIResponse.error(message, 400, error_code or "BAD_REQUEST")
    
    @staticmethod
    def unauthorized(message="Não autorizado", error_code=None):
        """401 - Não autenticado"""
        return APIResponse.error(message, 401, error_code or "UNAUTHORIZED")
    
    @staticmethod
    def forbidden(message="Acesso proibido", error_code=None):
        """403 - Acesso proibido"""
        return APIResponse.error(message, 403, error_code or "FORBIDDEN")
    
    @staticmethod
    def not_found(message="Recurso não encontrado", error_code=None):
        """404 - Não encontrado"""
        return APIResponse.error(message, 404, error_code or "NOT_FOUND")
    
    @staticmethod
    def conflict(message="Conflito ao processar requisição", error_code=None):
        """409 - Conflito (ex: email já existe)"""
        return APIResponse.error(message, 409, error_code or "CONFLICT")
    
    @staticmethod
    def internal_error(message="Erro interno do servidor", error_code=None):
        """500 - Erro interno"""
        return APIResponse.error(message, 500, error_code or "INTERNAL_ERROR")
    
    @staticmethod
    def unprocessable_entity(message="Dados inválidos", error_code=None):
        """422 - Entidade não processável"""
        return APIResponse.error(message, 422, error_code or "UNPROCESSABLE_ENTITY")


# ============================================
# DECORATORS PARA TRATAMENTO DE ERROS
# ============================================

def handle_errors(f):
    """
    Decorator que envolve rotas para tratamento automático de erros
    
    Uso:
    @bp.route('/users/<int:user_id>')
    @handle_errors
    def get_user(user_id):
        usuario = User.query.get(user_id)
        if not usuario:
            raise NotFoundError("Usuário não encontrado")
        return APIResponse.success(usuario.to_dict())
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except NotFoundError as e:
            return APIResponse.not_found(str(e))
        except UnauthorizedError as e:
            return APIResponse.unauthorized(str(e))
        except ForbiddenError as e:
            return APIResponse.forbidden(str(e))
        except BadRequestError as e:
            return APIResponse.bad_request(str(e))
        except ConflictError as e:
            return APIResponse.conflict(str(e))
        except Exception as e:
            # Em produção, não retornar detalhes do erro
            error_msg = str(e)
            if os.getenv('FLASK_ENV') == 'production':
                error_msg = "Erro interno ao processar requisição"
            
            # Log do erro
            print(f"❌ ERRO NÃO TRATADO: {str(e)}")
            traceback.print_exc()
            
            return APIResponse.internal_error(error_msg)
    
    return wrapper


# ============================================
# EXCEÇÕES CUSTOMIZADAS
# ============================================

class APIException(Exception):
    """Exceção base para API"""
    def __init__(self, message, status_code=400, error_code=None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or f"ERROR_{status_code}"
        super().__init__(self.message)


class BadRequestError(APIException):
    """400 - Requisição inválida"""
    def __init__(self, message):
        super().__init__(message, 400, "BAD_REQUEST")


class UnauthorizedError(APIException):
    """401 - Não autenticado"""
    def __init__(self, message):
        super().__init__(message, 401, "UNAUTHORIZED")


class ForbiddenError(APIException):
    """403 - Acesso proibido"""
    def __init__(self, message):
        super().__init__(message, 403, "FORBIDDEN")


class NotFoundError(APIException):
    """404 - Não encontrado"""
    def __init__(self, message):
        super().__init__(message, 404, "NOT_FOUND")


class ConflictError(APIException):
    """409 - Conflito"""
    def __init__(self, message):
        super().__init__(message, 409, "CONFLICT")


class ValidationError(APIException):
    """422 - Dados inválidos"""
    def __init__(self, message):
        super().__init__(message, 422, "VALIDATION_ERROR")


# ============================================
# VALIDADORES
# ============================================

class Validator:
    """Classe para validação de dados"""
    
    @staticmethod
    def validate_required(data, fields):
        """
        Valida se os campos obrigatórios estão presentes
        
        Uso:
        Validator.validate_required(data, ['email', 'senha'])
        """
        missing = [f for f in fields if f not in data or not data[f]]
        if missing:
            raise BadRequestError(f"Campos obrigatórios faltando: {', '.join(missing)}")
        return True
    
    @staticmethod
    def validate_email(email):
        """Valida se email é válido"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise BadRequestError(f"Email inválido: {email}")
        return True
    
    @staticmethod
    def validate_length(value, min_len=None, max_len=None, field_name="Campo"):
        """Valida comprimento de string"""
        if min_len and len(value) < min_len:
            raise BadRequestError(f"{field_name} deve ter pelo menos {min_len} caracteres")
        if max_len and len(value) > max_len:
            raise BadRequestError(f"{field_name} não pode ter mais de {max_len} caracteres")
        return True
    
    @staticmethod
    def validate_type(value, expected_type, field_name="Campo"):
        """Valida tipo de dado"""
        if not isinstance(value, expected_type):
            raise BadRequestError(f"{field_name} deve ser do tipo {expected_type.__name__}")
        return True
    
    @staticmethod
    def validate_choices(value, choices, field_name="Campo"):
        """Valida se valor está entre as opções permitidas"""
        if value not in choices:
            raise BadRequestError(f"{field_name} deve ser um dos: {', '.join(choices)}")
        return True


# ============================================
# EXEMPLO DE USO
# ============================================

"""
Exemplo de como usar no seu código:

from app.utils.responses import APIResponse, handle_errors, BadRequestError, NotFoundError, Validator
from flask import request

@bp.route('/users', methods=['POST'])
@handle_errors
def create_user():
    data = request.get_json()
    
    # Validar entrada
    Validator.validate_required(data, ['email', 'nome', 'senha'])
    Validator.validate_email(data['email'])
    Validator.validate_length(data['senha'], min_len=8, field_name="Senha")
    
    # Lógica de criação
    user = User(email=data['email'], nome=data['nome'])
    user.set_password(data['senha'])
    
    db.session.add(user)
    db.session.commit()
    
    # Resposta padronizada
    return APIResponse.created(user.to_dict(), "Usuário criado com sucesso")


@bp.route('/users/<int:user_id>', methods=['GET'])
@handle_errors
def get_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        raise NotFoundError("Usuário não encontrado")
    
    return APIResponse.success(user.to_dict())
"""
