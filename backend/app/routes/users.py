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
        # 🔐 Extrair usuario_id do JWT
        auth_header = request.headers.get('Authorization', '')
        usuario_id = None
        
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            import base64
            import json
            try:
                parts = token.split('.')
                if len(parts) == 3:
                    decoded = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
                    usuario_id = decoded.get('sub') or decoded.get('usuario_id') or decoded.get('user_id') or decoded.get('id')
            except Exception as e:
                print(f'[AUTH] Erro ao decodificar: {e}')
        
        if not usuario_id:
            return jsonify({'erro': 'Não autenticado'}), 401
        
        # Retornar progressos do usuário
        progresso = Progress.query.filter_by(usuario_id=usuario_id).all()
        print(f'[PROGRESS] Retornando {len(progresso)} progressos para usuario {usuario_id}')
        
        return jsonify({
            'progresso': [p.to_dict() for p in progresso] if progresso else []
        }), 200
        
    except Exception as e:
        print(f'[ERROR] Erro em get_user_progress: {e}')
        return jsonify({'erro': str(e)}), 500


@bp.route('/certificates', methods=['GET'])
def get_user_certificates():
    """Obter certificados do usuário autenticado"""
    try:
        # 🔐 Extrair usuario_id do JWT
        auth_header = request.headers.get('Authorization', '')
        usuario_id = None
        
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            import base64
            import json
            try:
                parts = token.split('.')
                if len(parts) == 3:
                    decoded = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
                    usuario_id = decoded.get('sub') or decoded.get('usuario_id') or decoded.get('user_id') or decoded.get('id')
            except Exception as e:
                print(f'[AUTH] Erro ao decodificar: {e}')
        
        if not usuario_id:
            return jsonify({'erro': 'Não autenticado'}), 401
        
        # Retornar certificados do usuário
        certificados = Certificate.query.filter_by(usuario_id=usuario_id).all()
        print(f'[CERTIFICATES] Retornando {len(certificados)} certificados para usuario {usuario_id}')
        
        return jsonify({
            'certificados': [c.to_dict() for c in certificados] if certificados else []
        }), 200
        
    except Exception as e:
        print(f'[ERROR] Erro em get_user_certificates: {e}')
        return jsonify({'erro': str(e)}), 500

