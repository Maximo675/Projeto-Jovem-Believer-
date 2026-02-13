from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User
from app.models.hospital import Hospital
from datetime import datetime, timedelta
import jwt
import os

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Registrar novo usuário"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['email', 'nome', 'senha', 'hospital_id']
        if not all(field in data for field in required_fields):
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
        
        # Verificar se usuário já existe
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'Email já cadastrado'}), 400
        
        # Criar novo usuário
        usuario = User(
            email=data['email'],
            nome=data['nome'],
            senha=data['senha'],
            hospital_id=data.get('hospital_id'),
            funcao='usuario'
        )
        usuario.set_password(data['senha'])
        
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Usuário registrado com sucesso',
            'usuario': usuario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """Fazer login"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('senha'):
            return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
        
        usuario = User.query.filter_by(email=data['email']).first()
        
        if not usuario or not usuario.check_password(data['senha']):
            return jsonify({'erro': 'Email ou senha inválidos'}), 401
        
        if not usuario.ativo:
            return jsonify({'erro': 'Usuário desativado'}), 403
        
        # Gerar token JWT
        payload = {
            'usuario_id': usuario.id,
            'email': usuario.email,
            'funcao': usuario.funcao,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(payload, os.getenv('JWT_SECRET', 'secret'), algorithm='HS256')
        
        return jsonify({
            'mensagem': 'Login realizado com sucesso',
            'token': token,
            'usuario': usuario.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/logout', methods=['POST'])
def logout():
    """Logout (client-side, apenas para confirmação)"""
    return jsonify({'mensagem': 'Logout realizado com sucesso'}), 200
