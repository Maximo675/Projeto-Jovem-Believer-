from flask import Blueprint, jsonify, request
from app import db
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.user import User
from app.models.certificate import Certificate
from datetime import datetime

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
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'erro': 'Curso não encontrado'}), 404
        
        # Retornar curso com todas as aulas
        return jsonify({
            'curso': course.to_dict(),
            'aulas': [a.to_dict() for a in course.aulas]
        }), 200
        
    except Exception as e:
        print(f'[ERROR] Erro ao obter curso: {str(e)}')
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


@bp.route('/<int:course_id>/progress', methods=['POST'])
def save_course_progress(course_id):
    """Salvar progresso do curso do usuário"""
    try:
        data = request.get_json()
        percentual = data.get('percentual', 100)
        concluido = data.get('concluido', False)
        tempo_gasto = data.get('tempo_gasto', 0)
        
        # 🔐 IMPORTANTE: Extrair usuario_id do Authorization header (do token)
        # Não confiar no frontend para evitar fraude
        auth_header = request.headers.get('Authorization', '')
        usuario_id = None
        
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]  # Remove "Bearer "
            import base64
            import json
            try:
                parts = token.split('.')
                if len(parts) == 3:
                    decoded = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
                    usuario_id = decoded.get('sub') or decoded.get('usuario_id') or decoded.get('user_id') or decoded.get('id')
                    print(f'[AUTH] Usuario extraído do token: {usuario_id}')
            except Exception as e:
                print(f'[AUTH] Erro ao decodificar token: {e}')
        
        # Fallback: se não conseguiu extrair do token, usar do frontend (mas com log)
        if not usuario_id:
            usuario_id = data.get('usuario_id')
            if usuario_id:
                print(f'[AUTH] ⚠️  Usando usuario_id do frontend: {usuario_id}')
        
        if not usuario_id:
            return jsonify({'erro': 'usuario_id obrigatório'}), 400
        
        # Verificar se usuário existe
        usuario = User.query.get(usuario_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        # Verificar se curso existe
        curso = Course.query.get(course_id)
        if not curso:
            return jsonify({'erro': 'Curso não encontrado'}), 404
        
        # Buscar ou criar progresso
        progresso = Progress.query.filter_by(
            usuario_id=usuario_id,
            curso_id=course_id
        ).first()
        
        if progresso:
            # Atualizar progresso existente
            progresso.percentual = percentual
            progresso.concluido = concluido
            progresso.tempo_gasto = tempo_gasto
            
            if concluido and not progresso.data_conclusao:
                progresso.data_conclusao = datetime.utcnow()
            
            progresso.data_atualizacao = datetime.utcnow()
        else:
            # Criar novo progresso
            progresso = Progress(
                usuario_id=usuario_id,
                curso_id=course_id,
                percentual=percentual,
                concluido=concluido,
                tempo_gasto=tempo_gasto
            )
            
            if concluido:
                progresso.data_conclusao = datetime.utcnow()
        
        db.session.add(progresso)
        db.session.commit()
        
        # 🎓 NOVO: Gerar certificado se curso foi concluído
        certificado = None
        if concluido:
            # Verificar se certificado já existe
            cert_existe = Certificate.query.filter_by(
                usuario_id=usuario_id,
                curso_id=course_id
            ).first()
            
            if not cert_existe:
                # Criar novo certificado
                certificado = Certificate(
                    usuario_id=usuario_id,
                    curso_id=course_id,
                    validade=365  # Válido por 1 ano
                )
                db.session.add(certificado)
                db.session.commit()
                print(f'[CERTIFICATE] Certificado gerado: Usuario {usuario_id}, Curso {course_id}, Numero: {certificado.numero_certificado}')
            else:
                certificado = cert_existe
        
        return jsonify({
            'mensagem': 'Progresso salvo com sucesso',
            'progresso': progresso.to_dict(),
            'certificado': certificado.to_dict() if certificado else None
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f'[ERROR] Erro ao salvar progresso: {str(e)}')
        return jsonify({'erro': str(e)}), 500



@bp.route('/<int:course_id>/progress/<int:user_id>', methods=['GET'])
def get_course_progress(course_id, user_id):
    """Obter progresso do usuário em um curso específico"""
    try:
        progresso = Progress.query.filter_by(
            usuario_id=user_id,
            curso_id=course_id
        ).first()
        
        if not progresso:
            return jsonify({
                'progresso': {
                    'percentual': 0,
                    'concluido': False,
                    'tempo_gasto': 0
                }
            }), 200
        
        return jsonify({
            'progresso': progresso.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@bp.route('/certificates', methods=['GET'])
def get_user_certificates():
    """Obter certificados do usuário logado"""
    try:
        # Extrair user_id do token
        from flask import request as flask_request
        auth_header = flask_request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'erro': 'Token não fornecido'}), 401
        
        token = auth_header[7:]  # Remove "Bearer "
        
        # Decodificar token (simplificado, sem verificação)
        import base64
        import json
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return jsonify({'erro': 'Token inválido'}), 401
            
            decoded = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
            usuario_id = decoded.get('sub') or decoded.get('usuario_id') or decoded.get('user_id') or decoded.get('id')
            
            if not usuario_id:
                return jsonify({'erro': 'User ID não encontrado no token'}), 401
            
        except Exception as e:
            return jsonify({'erro': f'Erro ao decodificar token: {str(e)}'}), 401
        
        # Buscar certificados do usuário
        certificados = Certificate.query.filter_by(usuario_id=usuario_id).all()
        
        # Enriquecer com dados do curso
        certs_enriquecidos = []
        for cert in certificados:
            curso = Course.query.get(cert.curso_id)
            cert_dict = cert.to_dict()
            cert_dict['curso'] = {
                'id': curso.id,
                'titulo': curso.titulo,
                'descricao': curso.descricao
            } if curso else None
            certs_enriquecidos.append(cert_dict)
        
        print(f'[CERTIFICATES] Buscando certificados para usuario {usuario_id}: {len(certs_enriquecidos)} encontrados')
        
        return jsonify({
            'certificados': certs_enriquecidos,
            'total': len(certs_enriquecidos)
        }), 200
        
    except Exception as e:
        print(f'[ERROR] Erro ao buscar certificados: {str(e)}')
        return jsonify({'erro': str(e)}), 500


@bp.route('/certificates/<cert_number>/download', methods=['GET'])
def download_certificate(cert_number):
    """Fazer download de certificado"""
    try:
        # Buscar certificado
        certificado = Certificate.query.filter_by(numero_certificado=cert_number).first()
        if not certificado:
            return jsonify({'erro': 'Certificado não encontrado'}), 404
        
        # Buscar usuário e curso
        usuario = User.query.get(certificado.usuario_id)
        curso = Course.query.get(certificado.curso_id)
        
        if not usuario or not curso:
            return jsonify({'erro': 'Dados do certificado incompletos'}), 404
        
        # Gerar HTML do certificado
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Certificado - {curso.titulo}</title>
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background: #f5f5f5;
                    font-family: 'Georgia', serif;
                }}
                .certificate {{
                    width: 100%;
                    max-width: 900px;
                    margin: 0 auto;
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    border: 8px solid #1a472c;
                    border-radius: 20px;
                    padding: 60px 80px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    text-align: center;
                    page-break-after: always;
                    min-height: 600px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                }}
                .header {{
                    margin-bottom: 40px;
                }}
                .logo {{
                    font-size: 2.5rem;
                    margin-bottom: 20px;
                }}
                .header h1 {{
                    color: #1a472c;
                    font-size: 2.5rem;
                    margin: 10px 0;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                }}
                .header p {{
                    color: #666;
                    font-size: 1.1rem;
                    margin: 5px 0;
                }}
                .content {{
                    margin: 50px 0;
                }}
                .content p {{
                    margin: 20px 0;
                    color: #333;
                    font-size: 1rem;
                    line-height: 1.6;
                }}
                .highlighted {{
                    color: #1a472c;
                    font-size: 1.3rem;
                    font-weight: bold;
                    margin: 30px 0;
                }}
                .course-name {{
                    background: linear-gradient(90deg, #1a472c 0%, #2d6e4d 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    font-size: 1.5rem;
                    font-weight: bold;
                }}
                .footer {{
                    margin-top: 60px;
                    border-top: 2px solid #1a472c;
                    padding-top: 30px;
                }}
                .cert-details {{
                    display: flex;
                    justify-content: space-around;
                    margin-top: 30px;
                    color: #666;
                    font-size: 0.9rem;
                }}
                .detail {{
                    flex: 1;
                }}
                @media print {{
                    body {{
                        background: white;
                    }}
                    .certificate {{
                        box-shadow: none;
                        margin: 0;
                        padding: 40px 60px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="certificate">
                <div class="header">
                    <div class="logo">🏆</div>
                    <h1>Certificado de Conclusão</h1>
                    <p>INFANTID - Plataforma de Aprendizado</p>
                </div>
                
                <div class="content">
                    <p><strong>Certificamos que</strong></p>
                    
                    <div class="highlighted">
                        {usuario.nome if usuario else 'Aluno'}
                    </div>
                    
                    <p>Completou com sucesso o curso:</p>
                    
                    <div class="course-name">
                        {curso.titulo if curso else 'Curso'}
                    </div>
                    
                    <p>Demonstrando conhecimento e compreensão dos conceitos apresentados durante o treinamento.</p>
                </div>
                
                <div class="footer">
                    <p><strong>Este certificado é válido por 1 (um) ano.</strong></p>
                    
                    <div class="cert-details">
                        <div class="detail">
                            <strong>Certificado #</strong><br/>
                            {cert_number}
                        </div>
                        <div class="detail">
                            <strong>Data de Emissão</strong><br/>
                            {certificado.data_emissao.strftime('%d/%m/%Y') if certificado.data_emissao else 'N/A'}
                        </div>
                        <div class="detail">
                            <strong>Válido até</strong><br/>
                            {(certificado.data_emissao.replace(year=certificado.data_emissao.year + certificado.validade // 365)).strftime('%d/%m/%Y') if certificado.data_emissao else 'N/A'}
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        from flask import send_file
        from io import BytesIO
        
        # Enviar como HTML/PDF
        response = send_file(
            BytesIO(html.encode('utf-8')),
            mimetype='text/html',
            as_attachment=True,
            download_name=f'Certificado_{cert_number}.html'
        )
        
        return response
        
    except Exception as e:
        print(f'[ERROR] Erro ao fazer download de certificado: {str(e)}')
        return jsonify({'erro': str(e)}), 500
