"""
Feedback da enfermeira/instrutor sobre um curso, com inbox e resposta do
super_admin.

Antes, pages/course.html tentava mandar esse feedback para
PUT /api/ia/avaliar/<conversa_id> — rota errada (método e recurso
incompatíveis), então o feedback se perdia silenciosamente. Este blueprint é
o destino correto; a correção do lado do frontend é só trocar a URL/método
em course.html.
"""

from flask import Blueprint, jsonify, request, g
from app import db
from app.models.feedback import Feedback
from app.utils.decorators import token_requerido
from app.decorators import requer_funcao, usuario_atual
from datetime import datetime

bp = Blueprint('feedback', __name__)


@bp.route('/api/courses/<int:course_id>/feedback', methods=['POST'])
@token_requerido
def enviar_feedback(course_id):
    """Enfermeira/instrutor envia feedback sobre um curso."""
    try:
        data = request.get_json(silent=True) or {}

        fb = Feedback(
            usuario_id=g.usuario.id,
            curso_id=course_id,
            avaliacao_conteudo=data.get('content'),
            avaliacao_dificuldade=data.get('difficulty'),
            comentario=data.get('comments'),
        )
        db.session.add(fb)
        db.session.commit()

        return jsonify({'mensagem': 'Feedback enviado com sucesso', 'feedback': fb.to_dict(para_usuario=True)}), 201

    except Exception:
        import logging
        logging.getLogger(__name__).exception('Erro ao salvar feedback')
        db.session.rollback()
        return jsonify({'erro': 'Não foi possível salvar o feedback.'}), 500


@bp.route('/api/users/meus-feedbacks', methods=['GET'])
@token_requerido
def meus_feedbacks():
    """Feedbacks enviados pelo usuário logado, com resposta (se houver) — para o dashboard."""
    try:
        feedbacks = (Feedback.query
                     .filter_by(usuario_id=g.usuario.id)
                     .order_by(Feedback.data_criacao.desc())
                     .all())
        return jsonify({'feedbacks': [f.to_dict(para_usuario=True) for f in feedbacks]}), 200
    except Exception:
        return jsonify({'erro': 'Não foi possível carregar os feedbacks.'}), 500


# ── Inbox do super_admin ───────────────────────────────────────────────────

@bp.route('/api/admin/feedback', methods=['GET'])
@requer_funcao('super_admin')
def listar_feedbacks():
    """Lista todos os feedbacks recebidos (todas as enfermeiras/hospitais)."""
    try:
        apenas_pendentes = request.args.get('pendentes') == 'true'
        query = Feedback.query
        if apenas_pendentes:
            query = query.filter(Feedback.resposta.is_(None))
        feedbacks = query.order_by(Feedback.data_criacao.desc()).all()
        return jsonify({'feedbacks': [f.to_dict(para_usuario=False) for f in feedbacks]}), 200
    except Exception:
        return jsonify({'erro': 'Não foi possível carregar os feedbacks.'}), 500


@bp.route('/api/admin/feedback/<int:feedback_id>/responder', methods=['POST'])
@requer_funcao('super_admin')
def responder_feedback(feedback_id):
    """super_admin responde a um feedback — a resposta aparece depois no dashboard da enfermeira."""
    try:
        eu = usuario_atual()
        fb = Feedback.query.get_or_404(feedback_id)
        data = request.get_json(silent=True) or {}
        resposta = (data.get('resposta') or '').strip()

        if not resposta:
            return jsonify({'erro': 'Resposta não pode ser vazia'}), 400

        fb.resposta = resposta
        fb.respondido_por_id = eu.id
        fb.respondido_em = datetime.utcnow()
        db.session.commit()

        return jsonify({'mensagem': 'Resposta enviada', 'feedback': fb.to_dict(para_usuario=False)}), 200
    except Exception:
        import logging
        logging.getLogger(__name__).exception('Erro ao responder feedback')
        db.session.rollback()
        return jsonify({'erro': 'Não foi possível salvar a resposta.'}), 500
