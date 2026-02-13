from flask import Blueprint, jsonify, request
from app import db
from app.models.hospital import Hospital

bp = Blueprint('hospitals', __name__, url_prefix='/api/hospitals')

@bp.route('', methods=['GET'])
def list_hospitals():
    """Listar todos os hospitais"""
    try:
        hospitais = Hospital.query.filter_by(ativo=True).all()
        
        return jsonify({
            'total': len(hospitais),
            'hospitais': [h.to_dict() for h in hospitais]
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/<int:hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    """Obter detalhes de um hospital"""
    try:
        hospital = Hospital.query.get(hospital_id)
        
        if not hospital:
            return jsonify({'erro': 'Hospital não encontrado'}), 404
        
        return jsonify(hospital.to_dict()), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('', methods=['POST'])
def create_hospital():
    """Criar novo hospital (apenas admin)"""
    try:
        data = request.get_json()
        
        required_fields = ['nome', 'estado', 'cidade', 'endereco', 'telefone', 'email']
        if not all(field in data for field in required_fields):
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
        
        # Verificar se já existe
        if Hospital.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'Hospital com esse email já existe'}), 400
        
        hospital = Hospital(
            nome=data['nome'],
            estado=data['estado'],
            cidade=data['cidade'],
            endereco=data['endereco'],
            telefone=data['telefone'],
            email=data['email'],
            cnpj=data.get('cnpj')
        )
        
        db.session.add(hospital)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Hospital criado com sucesso',
            'hospital': hospital.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@bp.route('/<int:hospital_id>', methods=['PUT'])
def update_hospital(hospital_id):
    """Atualizar hospital (apenas admin)"""
    try:
        hospital = Hospital.query.get(hospital_id)
        
        if not hospital:
            return jsonify({'erro': 'Hospital não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualizar campos permitidos
        if 'nome' in data:
            hospital.nome = data['nome']
        if 'cidade' in data:
            hospital.cidade = data['cidade']
        if 'endereco' in data:
            hospital.endereco = data['endereco']
        if 'telefone' in data:
            hospital.telefone = data['telefone']
        if 'ativo' in data:
            hospital.ativo = data['ativo']
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Hospital atualizado com sucesso',
            'hospital': hospital.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
