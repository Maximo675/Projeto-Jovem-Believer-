"""
API de Atividades Práticas
Endpoints para iniciar, registrar tentativas e completar atividades
"""

from flask import Blueprint, request, jsonify
from flask_login import current_user
from app import db
from app.models.activity import UserActivity, ActivityAttempt, ActivityBadge
from app.models.user import User
from datetime import datetime
import json

activities_bp = Blueprint('activities', __name__, url_prefix='/api/activities')


@activities_bp.route('/<int:lesson_id>/start', methods=['POST'])
def start_activity(lesson_id):
    """Iniciar uma nova atividade para uma aula"""
    try:
        if not current_user:
            return jsonify({'error': 'Não autenticado'}), 401
        
        data = request.get_json()
        activity_type = data.get('activity_type', 'practice')  # 'practice', 'quiz', 'challenge'
        course_id = data.get('course_id')
        
        # Criar nova atividade
        activity = UserActivity(
            user_id=current_user.id,
            course_id=course_id,
            lesson_id=lesson_id,
            activity_type=activity_type,
            status='ongoing'
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'activity_id': activity.id,
            'lesson_id': lesson_id,
            'activity_type': activity_type,
            'status': 'ongoing'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@activities_bp.route('/<int:activity_id>/attempt', methods=['POST'])
def record_attempt(activity_id):
    """Registrar uma tentativa em uma atividade"""
    try:
        if not current_user:
            return jsonify({'error': 'Não autenticado'}), 401
        
        activity = UserActivity.query.get(activity_id)
        if not activity or activity.user_id != current_user.id:
            return jsonify({'error': 'Atividade não encontrada'}), 404
        
        data = request.get_json()
        responses = data.get('responses', {})
        score = data.get('score', 0)
        time_taken = data.get('time_taken', 0)
        
        # Atualizar tentativas
        activity.attempts += 1
        activity.score = max(activity.score, score)  # Manter melhor score
        activity.time_spent += time_taken
        
        # Criar registro de tentativa
        attempt = ActivityAttempt(
            activity_id=activity_id,
            user_id=current_user.id,
            attempt_number=activity.attempts,
            score=score,
            time_taken=time_taken
        )
        attempt.set_responses(responses)
        
        # Gerar feedback
        feedback = gerar_feedback(activity_type=activity.activity_type, score=score)
        attempt.set_result(feedback)
        
        db.session.add(attempt)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'attempt_id': attempt.id,
            'attempt_number': activity.attempts,
            'score': score,
            'feedback': feedback,
            'can_continue': True
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@activities_bp.route('/<int:activity_id>/complete', methods=['POST'])
def complete_activity(activity_id):
    """Completar uma atividade"""
    try:
        if not current_user:
            return jsonify({'error': 'Não autenticado'}), 401
        
        activity = UserActivity.query.get(activity_id)
        if not activity or activity.user_id != current_user.id:
            return jsonify({'error': 'Atividade não encontrada'}), 404
        
        data = request.get_json()
        final_score = data.get('score', activity.score)
        total_time = data.get('time_total', activity.time_spent)
        
        # Atualizar atividade
        activity.status = 'completed'
        activity.score = final_score
        activity.time_spent = total_time
        activity.completed_at = datetime.utcnow()
        
        # Verificar e atribuir badges
        badges_earned = []
        if final_score >= 95:
            badge = criar_ou_obter_badge(current_user.id, 'perfect_score', 'Pontuação Perfeita ✨', 'Conquistou 95+ em uma atividade', '🌟')
            badges_earned.append(badge.to_dict())
        
        if activity.attempts == 1:
            badge = criar_ou_obter_badge(current_user.id, 'first_try', 'Acertou de Primeira! 💥', 'Completou com sucesso na primeira tentativa', '⚡')
            badges_earned.append(badge.to_dict())
        
        if total_time < 600:  # Menos de 10 minutos
            badge = criar_ou_obter_badge(current_user.id, 'speed_runner', 'Rápido 🚀', 'Completou em menos de 10 minutos', '🚀')
            badges_earned.append(badge.to_dict())
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'activity_id': activity_id,
            'status': 'completed',
            'score': final_score,
            'time_total': total_time,
            'badges_earned': badges_earned,
            'message': f'Parabéns! Você completou com {final_score}/100 pontos!'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@activities_bp.route('/user/progress', methods=['GET'])
def get_user_progress():
    """Obter progresso geral das atividades do usuário"""
    try:
        if not current_user:
            return jsonify({'error': 'Não autenticado'}), 401
        
        activities = UserActivity.query.filter_by(user_id=current_user.id).all()
        badges = ActivityBadge.query.filter_by(user_id=current_user.id).all()
        
        completed = sum(1 for a in activities if a.status == 'completed')
        ongoing = sum(1 for a in activities if a.status == 'ongoing')
        average_score = sum(a.score for a in activities if a.status == 'completed') / completed if completed > 0 else 0
        
        return jsonify({
            'total_activities': len(activities),
            'completed': completed,
            'ongoing': ongoing,
            'average_score': round(average_score, 1),
            'badges': [b.to_dict() for b in badges],
            'activities': [a.to_dict() for a in activities[:10]]  # Últimas 10
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@activities_bp.route('/<int:activity_id>/details', methods=['GET'])
def get_activity_details(activity_id):
    """Obter detalhes de uma atividade específica"""
    try:
        if not current_user:
            return jsonify({'error': 'Não autenticado'}), 401
        
        activity = UserActivity.query.get(activity_id)
        if not activity or activity.user_id != current_user.id:
            return jsonify({'error': 'Atividade não encontrada'}), 404
        
        attempts = ActivityAttempt.query.filter_by(activity_id=activity_id).all()
        
        return jsonify({
            'activity': activity.to_dict(),
            'attempts': [a.to_dict() for a in attempts],
            'last_attempt': attempts[-1].to_dict() if attempts else None
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@activities_bp.route('/lesson/<int:lesson_id>/status', methods=['GET'])
def get_lesson_activity_status(lesson_id):
    """Obter status das atividades de uma aula"""
    try:
        if not current_user:
            return jsonify({'error': 'Não autenticado'}), 401
        
        activities = UserActivity.query.filter_by(
            user_id=current_user.id,
            lesson_id=lesson_id
        ).all()
        
        return jsonify({
            'lesson_id': lesson_id,
            'activities': [a.to_dict() for a in activities],
            'has_activities': len(activities) > 0,
            'completed_count': sum(1 for a in activities if a.status == 'completed')
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@activities_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Obter ranking de usuários por score de atividades"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Agregação: top usuários por score médio
        top_users = db.session.query(
            User.id,
            User.nome,
            db.func.round(db.func.avg(UserActivity.score), 1).label('avg_score'),
            db.func.count(UserActivity.id).label('total_activities'),
            db.func.max(UserActivity.score).label('best_score')
        ).join(
            UserActivity, User.id == UserActivity.user_id
        ).filter(
            UserActivity.status == 'completed'
        ).group_by(
            User.id, User.nome
        ).order_by(
            db.desc('avg_score')
        ).limit(limit).all()
        
        leaderboard = [{
            'rank': idx + 1,
            'user_id': u[0],
            'nome': u[1],
            'avg_score': float(u[2]) if u[2] else 0,
            'total_activities': u[3],
            'best_score': u[4]
        } for idx, u in enumerate(top_users)]
        
        return jsonify(leaderboard), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def gerar_feedback(activity_type, score):
    """Gerar feedback personalizado baseado no tipo de atividade e score"""
    
    if score >= 90:
        feedback = {
            'level': 'excelente',
            'message': '🌟 Excelente! Você dominou completamente este conceito!',
            'tips': []
        }
    elif score >= 70:
        feedback = {
            'level': 'bom',
            'message': '👍 Muito bem! Mas há espaço para melhorar.',
            'tips': ['Revise as áreas com menos acerto', 'Pratique novamente para consolidar']
        }
    elif score >= 50:
        feedback = {
            'level': 'aceitavel',
            'message': '📚 Aceitável, mas você pode fazer melhor.',
            'tips': ['Estude o material novamente', 'Tente outra vez']
        }
    else:
        feedback = {
            'level': 'precisa_melhorar',
            'message': '⚠️ Você precisa melhorar neste conceito.',
            'tips': ['Releia a explicação teórica', 'Pratique mais uma vez', 'Não hesite em buscar ajuda']
        }
    
    return feedback


def criar_ou_obter_badge(user_id, badge_type, badge_name, description, icon):
    """Criar ou obter um badge existente"""
    badge = ActivityBadge.query.filter_by(
        user_id=user_id,
        badge_type=badge_type
    ).first()
    
    if not badge:
        badge = ActivityBadge(
            user_id=user_id,
            badge_type=badge_type,
            badge_name=badge_name,
            badge_description=description,
            badge_icon=icon
        )
        db.session.add(badge)
        db.session.flush()  # Flush para obter ID
    
    return badge
