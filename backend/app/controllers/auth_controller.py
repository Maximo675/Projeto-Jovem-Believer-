"""
AuthController - Controlador de autenticação
"""

from app import db
from app.models.user import User
from app.utils.responses import APIResponse, Validator, BadRequestError, UnauthorizedError, ConflictError
from datetime import datetime, timedelta
import jwt
import os


class AuthController:
    """Controller para autenticação"""
    
    @staticmethod
    def register(email, nome, senha, hospital_id=None):
        """
        Registrar novo usuário
        
        Args:
            email (str): Email do usuário
            nome (str): Nome do usuário
            senha (str): Senha do usuário
            hospital_id (int): ID do hospital (opcional)
        
        Returns:
            dict: Dados do usuário criado
        
        Raises:
            BadRequestError: Se dados inválidos
            ConflictError: Se email já existe
        """
        
        # Validar entrada
        Validator.validate_required({'email': email, 'nome': nome, 'senha': senha}, 
                                   ['email', 'nome', 'senha'])
        Validator.validate_email(email)
        Validator.validate_length(senha, min_len=8, field_name="Senha")
        Validator.validate_length(nome, min_len=3, field_name="Nome")
        
        # Verificar se email já existe
        if User.query.filter_by(email=email).first():
            raise ConflictError(f"Email '{email}' já cadastrado")
        
        # Criar novo usuário
        usuario = User(
            email=email,
            nome=nome,
            senha=senha,
            hospital_id=hospital_id,
            funcao='usuario'
        )
        usuario.set_password(senha)
        
        try:
            db.session.add(usuario)
            db.session.commit()
            
            return {
                'id': usuario.id,
                'email': usuario.email,
                'nome': usuario.nome,
                'hospital_id': usuario.hospital_id,
                'funcao': usuario.funcao,
                'ativo': usuario.ativo
            }
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar usuário: {str(e)}")
    
    @staticmethod
    def login(email, senha):
        """
        Fazer login do usuário
        
        Args:
            email (str): Email do usuário
            senha (str): Senha do usuário
        
        Returns:
            dict: Token JWT e dados do usuário
        
        Raises:
            UnauthorizedError: Se email/senha inválidos
        """
        
        # Validar entrada
        Validator.validate_required({'email': email, 'senha': senha}, 
                                   ['email', 'senha'])
        Validator.validate_email(email)
        
        # Buscar usuário
        usuario = User.query.filter_by(email=email).first()
        
        if not usuario or not usuario.check_password(senha):
            raise UnauthorizedError("Email ou senha inválidos")
        
        if not usuario.ativo:
            raise UnauthorizedError("Usuário desativado")
        
        # Gerar token JWT
        payload = {
            'usuario_id': usuario.id,
            'email': usuario.email,
            'funcao': usuario.funcao,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        secret = os.getenv('JWT_SECRET', 'secret')
        token = jwt.encode(payload, secret, algorithm='HS256')
        
        return {
            'token': token,
            'usuario': {
                'id': usuario.id,
                'email': usuario.email,
                'nome': usuario.nome,
                'hospital_id': usuario.hospital_id,
                'funcao': usuario.funcao,
                'ativo': usuario.ativo
            }
        }
    
    @staticmethod
    def logout():
        """
        Logout do usuário (client-side apenas)
        
        Returns:
            dict: Mensagem de confirmação
        """
        return {
            'mensagem': 'Logout realizado com sucesso'
        }
    
    @staticmethod
    def verify_token(token):
        """
        Verificar validade do token JWT
        
        Args:
            token (str): Token JWT
        
        Returns:
            dict: Dados decodificados do token
        
        Raises:
            UnauthorizedError: Se token inválido
        """
        try:
            secret = os.getenv('JWT_SECRET', 'secret')
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token expirado")
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Token inválido")
