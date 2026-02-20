from flask import Blueprint, jsonify, request
from app import db
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.progress import Progress

bp = Blueprint('courses', __name__, url_prefix='/api/courses')

@bp.route('', methods=['GET'])
def list_courses():
    """Listar todos os cursos"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        cursos = Course.query.filter_by(ativo=True).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'total': cursos.total,
            'paginas': cursos.pages,
            'cursos': [c.to_dict() for c in cursos.items]
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Obter detalhes de um curso"""
    try:
        curso = Course.query.get(course_id)
        
        if not curso:
            return jsonify({'erro': 'Curso não encontrado'}), 404
        
        return jsonify({
            'curso': curso.to_dict(),
            'aulas': [a.to_dict() for a in curso.aulas]
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('', methods=['POST'])
def create_course():
    """Criar novo curso (apenas para admin/instrutor)"""
    try:
        data = request.get_json()
        
        required_fields = ['titulo', 'descricao', 'autor']
        if not all(field in data for field in required_fields):
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
        
        curso = Course(
            titulo=data['titulo'],
            descricao=data['descricao'],
            autor=data['autor'],
            nivel=data.get('nivel', 'basico'),
            tempo_estimado=data.get('tempo_estimado')
        )
        
        db.session.add(curso)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Curso criado com sucesso',
            'curso': curso.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@bp.route('/<int:course_id>/aulas', methods=['GET'])
def get_course_lessons(course_id):
    """Obter aulas de um curso"""
    try:
        curso = Course.query.get(course_id)
        
        if not curso:
            return jsonify({'erro': 'Curso não encontrado'}), 404
        
        aulas = Lesson.query.filter_by(
            curso_id=course_id, ativo=True
        ).order_by('ordem').all()
        
        return jsonify({
            'curso_id': course_id,
            'aulas': [a.to_dict() for a in aulas]
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
