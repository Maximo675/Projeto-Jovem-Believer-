"""
Prova de cada curso — parte da trilha sequencial (cada curso só libera o
próximo depois de uma prova aprovada, nota mínima em Quiz.nota_minima).

A correção é sempre feita aqui no servidor: GET /quiz nunca inclui o campo
`correto` das opções, e POST /quiz/submit ignora qualquer nota vinda do
cliente — calcula a nota comparando as respostas com o gabarito no banco.
Isso fecha a mesma classe de bug que existia em save_course_progress(),
onde um `concluido: true` mandado pelo frontend era aceito sem verificação.
"""

from flask import Blueprint, jsonify, request, g
from app import db
from app.models.course import Course
from app.models.progress import Progress
from app.models.certificate import Certificate
from app.models.quiz import Quiz, QuizQuestion, QuizOption
from app.utils.decorators import token_requerido
from datetime import datetime

bp = Blueprint('quizzes', __name__, url_prefix='/api/courses')


@bp.route('/<int:course_id>/quiz', methods=['GET'])
@token_requerido
def get_quiz(course_id):
    """Devolve as perguntas da prova do curso, sem o gabarito."""
    try:
        quiz = Quiz.query.filter_by(curso_id=course_id).first()
        if not quiz:
            return jsonify({'erro': 'Este curso ainda não tem prova cadastrada'}), 404

        return jsonify({'quiz': quiz.to_dict(incluir_gabarito=False)}), 200

    except Exception as e:
        print(f'[ERROR] Erro ao obter quiz: {str(e)}')
        return jsonify({'erro': str(e)}), 500


@bp.route('/<int:course_id>/quiz/submit', methods=['POST'])
@token_requerido
def submit_quiz(course_id):
    """
    Corrige a prova no servidor e grava Progress.nota/aprovado.
    Body esperado: { respostas: [{question_id, option_id}, ...] }
    Tentativas ilimitadas — pode ser chamado de novo a qualquer momento.
    """
    try:
        quiz = Quiz.query.filter_by(curso_id=course_id).first()
        if not quiz:
            return jsonify({'erro': 'Este curso ainda não tem prova cadastrada'}), 404

        data = request.get_json(silent=True) or {}
        respostas = data.get('respostas', [])
        respostas_por_pergunta = {r.get('question_id'): r.get('option_id') for r in respostas}

        total_perguntas = len(quiz.perguntas)
        if total_perguntas == 0:
            return jsonify({'erro': 'Prova sem perguntas cadastradas'}), 400

        acertos = 0
        detalhe = []
        for pergunta in quiz.perguntas:
            opcao_marcada_id = respostas_por_pergunta.get(pergunta.id)
            opcao_correta = next((o for o in pergunta.opcoes if o.correto), None)
            acertou = bool(opcao_marcada_id) and opcao_correta is not None and int(opcao_marcada_id) == opcao_correta.id
            if acertou:
                acertos += 1
            detalhe.append({
                'question_id': pergunta.id,
                'acertou': acertou,
                'opcao_correta_id': opcao_correta.id if opcao_correta else None,
            })

        nota = round((acertos / total_perguntas) * 100)
        aprovado = nota >= quiz.nota_minima

        usuario_id = g.usuario.id

        progresso = Progress.query.filter_by(usuario_id=usuario_id, curso_id=course_id).first()
        if not progresso:
            progresso = Progress(usuario_id=usuario_id, curso_id=course_id, percentual=100, concluido=True)
            db.session.add(progresso)

        progresso.nota = nota
        progresso.aprovado = aprovado
        if aprovado and not progresso.data_conclusao:
            progresso.data_conclusao = datetime.utcnow()
        progresso.data_atualizacao = datetime.utcnow()

        db.session.commit()

        certificado = None
        if aprovado:
            certificado = Certificate.query.filter_by(usuario_id=usuario_id, curso_id=course_id).first()
            if not certificado:
                certificado = Certificate(usuario_id=usuario_id, curso_id=course_id, validade=365)
                db.session.add(certificado)
                db.session.commit()
                print(f'[CERTIFICATE] Certificado gerado (prova aprovada): Usuario {usuario_id}, Curso {course_id}, Numero: {certificado.numero_certificado}')

        return jsonify({
            'nota': nota,
            'nota_minima': quiz.nota_minima,
            'aprovado': aprovado,
            'acertos': acertos,
            'total_perguntas': total_perguntas,
            'detalhe': detalhe,
            'certificado': certificado.to_dict() if certificado else None,
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f'[ERROR] Erro ao corrigir quiz: {str(e)}')
        return jsonify({'erro': str(e)}), 500
