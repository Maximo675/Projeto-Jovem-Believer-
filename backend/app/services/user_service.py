"""
Serviço de Usuários.
Lógica de negócio relacionada a usuários.
"""

from app import db
from app.models.user import User
from flask import current_app

class UserService:
    """Serviço para gerenciar usuários."""
    
    @staticmethod
    def registrar_usuario(email, nome, senha, hospital_id, funcao='usuario'):
        """
        Registra um novo usuário.
        
        Args:
            email (str): Email do usuário
            nome (str): Nome completo
            senha (str): Senha em texto plano (será hashada)
            hospital_id (int): ID do hospital
            funcao (str): Função do usuário (admin, instrutor, usuario)
        
        Returns:
            User: Usuário criado
            
        Raises:
            ValueError: Se email já existe
        """
        if User.query.filter_by(email=email).first():
            raise ValueError(f"Email {email} já cadastrado")
        
        usuario = User(
            email=email,
            nome=nome,
            senha=senha,
            hospital_id=hospital_id,
            funcao=funcao
        )
        usuario.set_password(senha)
        
        db.session.add(usuario)
        db.session.commit()
        
        return usuario
    
    @staticmethod
    def autenticar_usuario(email, senha):
        """
        Autentica um usuário.
        
        Args:
            email (str): Email
            senha (str): Senha em texto plano
        
        Returns:
            User: Usuário autenticado ou None
        """
        usuario = User.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(senha) and usuario.ativo:
            return usuario
        
        return None
    
    @staticmethod
    def obter_usuario(usuario_id):
        """Obtém um usuário pelo ID."""
        return User.query.get(usuario_id)
    
    @staticmethod
    def atualizar_usuario(usuario_id, **kwargs):
        """
        Atualiza dados do usuário.
        
        Args:
            usuario_id (int): ID do usuário
            **kwargs: Campos a atualizar
        
        Returns:
            User: Usuário atualizado
        """
        usuario = User.query.get(usuario_id)
        if not usuario:
            raise ValueError(f"Usuário {usuario_id} não encontrado")
        
        campos_permitidos = ['nome', 'email', 'funcao']
        
        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                setattr(usuario, campo, valor)
        
        db.session.commit()
        return usuario
    
    @staticmethod
    def listar_usuarios_hospital(hospital_id, pagina=1, por_pagina=20):
        """
        Lista usuários de um hospital específico.
        
        Args:
            hospital_id (int): ID do hospital
            pagina (int): Número da página
            por_pagina (int): Itens por página
        
        Returns:
            list: Usuários do hospital
        """
        return User.query.filter_by(hospital_id=hospital_id).paginate(
            page=pagina,
            per_page=por_pagina
        )
