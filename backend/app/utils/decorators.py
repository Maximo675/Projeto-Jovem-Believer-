"""
Decoradores customizados para rotas.
"""

from functools import wraps
from flask import request, jsonify, g
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import os
from app.models.user import User

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
            # Decodificar token
            data = jwt.decode(token, os.getenv('JWT_SECRET', 'secret'), algorithms=['HS256'])
            usuario = User.query.get(data['usuario_id'])
            
            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
            
            # Adicionar usuário ao contexto global Flask
            g.usuario = usuario
            
        except ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    
    return decorada


def admin_requerido(f):
    """
    Decorador que requer que o usuário seja admin.
    Deve ser usado com @token_requerido.
    """
    @wraps(f)
    def decorada(*args, **kwargs):
        if not hasattr(g, 'usuario') or g.usuario.funcao != 'admin':
            return jsonify({'erro': 'Acesso negado. Admin requerido'}), 403
        
        return f(*args, **kwargs)
    
    return decorada


def instrutor_requerido(f):
    """
    Decorador que requer que o usuário seja instrutor ou admin.
    Deve ser usado com @token_requerido.
    """
    @wraps(f)
    def decorada(*args, **kwargs):
        if not hasattr(g, 'usuario') or g.usuario.funcao not in ['instrutor', 'admin']:
            return jsonify({'erro': 'Acesso negado. Instrutor requerido'}), 403
        
        return f(*args, **kwargs)
    
    return decorada
