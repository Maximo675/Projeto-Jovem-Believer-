from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User
from app.models.hospital import Hospital
from app.models.progress import Progress
from app.models.certificate import Certificate

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Obter dados do usuário"""
    try:
        usuario = User.query.get(user_id)
        
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        return jsonify(usuario.to_dict()), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Atualizar dados do usuário"""
    try:
        usuario = User.query.get(user_id)
        
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualizar apenas campos permitidos
        if 'nome' in data:
            usuario.nome = data['nome']
        if 'email' in data and data['email'] != usuario.email:
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'erro': 'Email já cadastrado'}), 400
            usuario.email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Usuário atualizado com sucesso',
            'usuario': usuario.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@bp.route('', methods=['GET'])
def list_users():
    """Listar todos os usuários (apenas para admin)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        usuarios = User.query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'total': usuarios.total,
            'paginas': usuarios.pages,
            'usuarios': [u.to_dict() for u in usuarios.items]
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/progress', methods=['GET'])
def get_user_progress():
    """Obter progresso do usuário autenticado"""
    try:
        # Para simplificar, vamos retornar dados fictícios
        # Em produção, decodificar JWT e obter usuario_id
        
        progresso = Progress.query.limit(5).all()
        
        return jsonify({
            'progresso': [p.to_dict() for p in progresso] if progresso else []
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/certificates', methods=['GET'])
def get_user_certificates():
    """Obter certificados do usuário autenticado"""
    try:
        certificados = Certificate.query.limit(5).all()
        
        return jsonify({
            'certificados': [c.to_dict() for c in certificados] if certificados else []
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

