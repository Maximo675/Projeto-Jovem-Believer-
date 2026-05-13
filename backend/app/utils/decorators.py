"""
Decoradores customizados para rotas.

Hierarquia de papéis (do mais ao menos privilegiado):
  super_admin → admin → instrutor → usuario
"""

from functools import wraps
from flask import request, jsonify, g
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import os
from app.models.user import User

# Papéis válidos em ordem de privilégio
ROLES_ORDER = ['super_admin', 'admin', 'instrutor', 'usuario']


def _role_gte(usuario_funcao: str, minimo: str) -> bool:
    """Retorna True se o papel do usuário é >= ao mínimo exigido."""
    try:
        return ROLES_ORDER.index(usuario_funcao) <= ROLES_ORDER.index(minimo)
    except ValueError:
        return False


def token_requerido(f):
    """
    Decorador que requer um token JWT válido.
    O token deve ser enviado no header: Authorization: Bearer <token>
    """
    @wraps(f)
    def decorada(*args, **kwargs):
        token = None
        
        # Verificar if token está no header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'erro': 'Token malformado'}), 401
        
        if not token:
            return jsonify({'erro': 'Token não fornecido'}), 401
        
        try:
            # Decodificar token — fallback igual ao auth.py para evitar assimetria
            _secret = os.getenv('JWT_SECRET', 'secret-dev-inseguro-troque-em-producao')
            data = jwt.decode(token, _secret, algorithms=['HS256'])
            usuario = User.query.get(data['usuario_id'])

            if not usuario:
                return jsonify({'erro': 'Não autorizado'}), 401

            # Conta desativada: nega acesso mesmo com token ainda válido
            if not usuario.ativo:
                return jsonify({'erro': 'Não autorizado'}), 401

            # Adicionar usuário ao contexto global Flask
            g.usuario = usuario
            
        except ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    
    return decorada


def requer_papel(papel_minimo: str):
    """Fábrica de decoradores de papel.

    Uso::
        @token_requerido
        @requer_papel('admin')
        def minha_rota(): ...
    """
    def decorator(f):
        @wraps(f)
        def decorada(*args, **kwargs):
            if not hasattr(g, 'usuario'):
                return jsonify({'erro': 'Não autorizado'}), 401
            if not _role_gte(g.usuario.funcao, papel_minimo):
                # Não revelar o papel mínimo exigido — informação desnecessria ao atacante
                return jsonify({'erro': 'Acesso negado'}), 403
            return f(*args, **kwargs)
        return decorada
    return decorator


# Atalhos para os papéis mais usados
def super_admin_requerido(f):
    """Apenas super_admin."""
    return token_requerido(requer_papel('super_admin')(f))


def admin_requerido(f):
    """admin ou superior (super_admin)."""
    @wraps(f)
    def decorada(*args, **kwargs):
        if not hasattr(g, 'usuario') or not _role_gte(g.usuario.funcao, 'admin'):
            return jsonify({'erro': 'Acesso negado'}), 403
        return f(*args, **kwargs)
    return decorada


def instrutor_requerido(f):
    """instrutor ou superior."""
    @wraps(f)
    def decorada(*args, **kwargs):
        if not hasattr(g, 'usuario') or not _role_gte(g.usuario.funcao, 'instrutor'):
            return jsonify({'erro': 'Acesso negado. Instrutor requerido'}), 403
        return f(*args, **kwargs)
    return decorada
