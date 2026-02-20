from flask import Blueprint, jsonify, request
from app import db
from app.models.ia_conversation import IAConversation
from app.models.user import User
from app.services.ai_service import AiService
import traceback

bp = Blueprint('ai', __name__, url_prefix='/api/ia')

ai_service = AiService()

@bp.route('/chat', methods=['POST'])
def chat_ia():
    """Endpoint de chat com IA (para dashboard)"""
    try:
        data = request.get_json()
        
        if not data or not data.get('mensagem'):
            return jsonify({'erro': 'Mensagem é obrigatória'}), 400
        
        mensagem = data['mensagem']
        
        # Consultar IA
        resposta, tokens = ai_service.responder_pergunta(mensagem)
        
        return jsonify({
            'mensagem': mensagem,
            'resposta': resposta,
            'tokens': tokens
        }), 200
        
    except Exception as e:
        traceback.print_exc()
        print(f"[AI ERROR] {str(e)}")
        return jsonify({'erro': f'Erro ao processar mensagem: {str(e)}'}), 500


@bp.route('/consult', methods=['POST'])
def consult_ia():
    """Consultar IA para dúvidas"""
    try:
        data = request.get_json()
        
        if not data or not data.get('pergunta'):
            return jsonify({'erro': 'Pergunta é obrigatória'}), 400
        
        usuario_id = data.get('usuario_id')
        curso_id = data.get('curso_id')
        pergunta = data['pergunta']
        
        # Validar usuário
        if usuario_id:
            usuario = User.query.get(usuario_id)
            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        # Consultar IA
        resposta, tokens = ai_service.responder_pergunta(pergunta, curso_id)
        
        # Salvar conversação
        conversa = IAConversation(
            usuario_id=usuario_id,
            curso_id=curso_id,
            pergunta=pergunta,
            resposta=resposta,
            tokens_usados=tokens
        )
        
        db.session.add(conversa)
        db.session.commit()
        
        return jsonify({
            'id': conversa.id,
            'pergunta': pergunta,
            'resposta': resposta,
            'tokens': tokens
        }), 200
        
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'erro': f'Erro ao consultao IA: {str(e)}'}), 500


@bp.route('/historico/<int:user_id>', methods=['GET'])
def get_historico(user_id):
    """Obter histórico de conversas"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        conversas = IAConversation.query.filter_by(usuario_id=user_id).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'total': conversas.total,
            'paginas': conversas.pages,
            'conversas': [c.to_dict() for c in conversas.items]
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/avaliar/<int:conversa_id>', methods=['PUT'])
def avaliar_resposta(conversa_id):
    """Avaliar resposta da IA"""
    try:
        conversa = IAConversation.query.get(conversa_id)
        
        if not conversa:
            return jsonify({'erro': 'Conversa não encontrada'}), 404
        
        data = request.get_json()
        if 'avaliacao' not in data:
            return jsonify({'erro': 'Avaliação é obrigatória'}), 400
        
        conversa.avaliacao = data['avaliacao']
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Avaliação registrada',
            'conversa': conversa.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
