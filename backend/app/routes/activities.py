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
# ENDPOINTS PARA LISTAR E ACESSAR ATIVIDADES
# ============================================

@activities_bp.route('/list', methods=['GET'])
def list_available_activities():
    """Listar todas as atividades disponíveis no sistema"""
    import os
    try:
        activities_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'frontend', 'activities'
        )
        
        if not os.path.exists(activities_path):
            return jsonify({'error': 'Diretório de atividades não encontrado'}), 404
        
        # Listar todos os arquivos HTML
        html_files = [f for f in os.listdir(activities_path) if f.endswith('.html')]
        
        # Criar lista com metadados
        activities = []
        for html_file in sorted(html_files):
            name = html_file.replace('.html', '')
            title = name.replace('-', ' ').title()
            
            # Determinar categoria e descrição baseado no nome
            category = 'Simulador'
            description = 'Atividade prática'
            icon = '📋'
            
            if 'biometrica' in name:
                category = 'Captura Biométrica'
                description = 'Simulador de captura de impressões digitais ETAN'
                icon = '👆'
            elif 'simulator' in name or 'simulador' in name:
                category = 'Simulador'
                description = 'Simulador de protocolo ETAN'
                icon = '🎮'
            elif 'troubleshooting' in name:
                category = 'Solução de Problemas'
                description = 'Guia de troubleshooting ETAN'
                icon = '🔧'
            elif 'special_cases' in name:
                category = 'Casos Especiais'
                description = 'Tratamento de casos especiais'
                icon = '⚠️'
            
            activities.append({
                'id': len(activities) + 1,
                'filename': html_file,
                'name': name,
                'title': title,
                'description': description,
                'category': category,
                'icon': icon,
                'type': 'interactive',
                'url': f'/activities/{html_file}',
                'api_url': f'/api/activities/{name}/access'
            })
        
        return jsonify({
            'success': True,
            'total': len(activities),
            'activities': activities
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@activities_bp.route('/<activity_name>/access', methods=['GET'])
def access_activity(activity_name):
    """Acessar uma atividade específica pelo nome"""
    import os
    try:
        activities_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'frontend', 'activities'
        )
        
        # Tentar com .html
        html_file = f'{activity_name}.html'
        file_path = os.path.join(activities_path, html_file)
        
        if not os.path.exists(file_path):
            # Tentar alternativas
            alternatives = [
                f'{activity_name}.html',
                f'{activity_name.replace("_", "-")}.html',
                f'{activity_name.replace("-", "_")}.html'
            ]
            
            found = False
            for alt in alternatives:
                alt_path = os.path.join(activities_path, alt)
                if os.path.exists(alt_path):
                    file_path = alt_path
                    html_file = alt
                    found = True
                    break
            
            if not found:
                return jsonify({
                    'error': f'Atividade "{activity_name}" não encontrada',
                    'available': [f.replace('.html', '') for f in os.listdir(activities_path) if f.endswith('.html')]
                }), 404
        
        return jsonify({
            'success': True,
            'activity': activity_name,
            'filename': html_file,
            'url': f'/activities/{html_file}',
            'message': f'Acesse a atividade em: /activities/{html_file}'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@activities_bp.route('/categories', methods=['GET'])
def get_activity_categories():
    """Obter atividades agrupadas por categoria"""
    import os
    try:
        activities_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'frontend', 'activities'
        )
        
        categories = {
            'Captura Biométrica': [],
            'Simulador': [],
            'Solução de Problemas': [],
            'Casos Especiais': [],
            'Outros': []
        }
        
        html_files = [f for f in os.listdir(activities_path) if f.endswith('.html')]
        
        for html_file in sorted(html_files):
            name = html_file.replace('.html', '')
            title = name.replace('-', ' ').title()
            
            activity = {
                'filename': html_file,
                'name': name,
                'title': title,
                'url': f'/activities/{html_file}'
            }
            
            if 'biometrica' in name:
                categories['Captura Biométrica'].append(activity)
            elif 'simulator' in name or 'simulador' in name:
                categories['Simulador'].append(activity)
            elif 'troubleshooting' in name:
                categories['Solução de Problemas'].append(activity)
            elif 'special_cases' in name:
                categories['Casos Especiais'].append(activity)
            else:
                categories['Outros'].append(activity)
        
        # Remover categorias vazias
        categories = {k: v for k, v in categories.items() if v}
        
        return jsonify({
            'success': True,
            'categories': categories,
            'total_activities': sum(len(v) for v in categories.values())
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@activities_bp.route('/search', methods=['GET'])
def search_activities():
    """Pesquisar atividades por palavra-chave"""
    import os
    try:
        query = request.args.get('q', '').lower()
        
        if not query:
            return jsonify({'error': 'Parâmetro \"q\" é obrigatório'}), 400
        
        activities_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'frontend', 'activities'
        )
        
        html_files = [f for f in os.listdir(activities_path) if f.endswith('.html')]
        results = []
        
        for html_file in sorted(html_files):
            name = html_file.replace('.html', '').lower()
            if query in name:
                results.append({
                    'filename': html_file,
                    'name': html_file.replace('.html', ''),
                    'title': html_file.replace('.html', '').replace('-', ' ').title(),
                    'url': f'/activities/{html_file}'
                })
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'count': len(results)
        }), 200
    
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


# ============================================
# ENDPOINTS PARA CAPTURA BIOMÉTRICA ETAN
# ============================================

@activities_bp.route('/biometric/session/start', methods=['POST'])
def start_biometric_session():
    """Iniciar uma sessão de captura biométrica ETAN"""
    try:
        # Aceitar sem autenticação para testes, mas registrar user_id se disponível
        data = request.get_json()
        user_id = data.get('user_id', 1)
        activity_id = data.get('activity_id', 4)
        course_id = data.get('course_id', 1)
        
        # Criar nova atividade de captura biométrica
        activity = UserActivity(
            user_id=user_id,
            course_id=course_id,
            lesson_id=4,  # Aula do ETAN
            activity_type='biometric',
            status='ongoing',
            metadata=json.dumps({
                'session_type': 'etan_biometric',
                'fingerprint_count': 0,
                'start_time': datetime.utcnow().isoformat()
            })
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'session_id': activity.id,
            'user_id': user_id,
            'activity_id': activity_id,
            'message': 'Sessão de captura biométrica iniciada'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@activities_bp.route('/biometric/capture', methods=['POST'])
def record_biometric_capture():
    """Registrar captura de uma digital com qualidade NFIQ"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 1)
        activity_id = data.get('activity_id', 4)
        finger_id = data.get('finger_id')
        finger_name = data.get('finger_name', 'Unknown')
        hand = data.get('hand', 'Unknown')
        quality = data.get('quality', 0)
        nfiq = data.get('nfiq', 0)
        attempt_number = data.get('attempt_number', 1)
        
        # Registrar tentativa
        attempt = ActivityAttempt(
            activity_id=activity_id,
            user_id=user_id,
            attempt_number=attempt_number,
            score=quality,  # Usar qualidade como score
            time_taken=0
        )
        
        # Armazenar dados biométricos no metadata
        biometric_data = {
            'finger_id': finger_id,
            'finger_name': finger_name,
            'hand': hand,
            'quality': quality,
            'nfiq': nfiq,
            'captured_at': datetime.utcnow().isoformat(),
            'attempt_number': attempt_number
        }
        attempt.set_result(biometric_data)
        attempt.set_responses({'biometric': biometric_data})
        
        db.session.add(attempt)
        
        # Atualizar atividade
        activity = UserActivity.query.get(activity_id)
        if activity:
            activity.attempts += 1
            activity.score = max(activity.score, quality)
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'attempt_id': attempt.id,
            'finger_captured': f"{hand} - {finger_name}",
            'quality': quality,
            'nfiq': nfiq,
            'message': 'Digital capturada com sucesso'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500


@activities_bp.route('/biometric/completion', methods=['POST'])
def complete_biometric_session():
    """Completar sessão de captura biométrica e gerar relatório"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 1)
        activity_id = data.get('activity_id', 4)
        total_fingers = data.get('total_fingers_captured', 0)
        average_quality = data.get('average_quality', 0)
        success_rate = data.get('success_rate', 0)
        captured_fingers = data.get('captured_fingers', [])
        total_time = data.get('total_time', 0)
        
        # Obter atividade
        activity = UserActivity.query.get(activity_id)
        if not activity:
            return jsonify({'error': 'Atividade não encontrada'}), 404
        
        # Calcular score final (baseado na qualidade média e dedos capturados)
        final_score = (total_fingers / 10) * 100 * (average_quality / 100)
        
        # Atualizar atividade
        activity.status = 'completed'
        activity.score = final_score
        activity.time_spent = total_time
        activity.completed_at = datetime.utcnow()
        
        # Atualizar metadata
        metadata = json.loads(activity.metadata) if activity.metadata else {}
        metadata.update({
            'total_fingers_captured': total_fingers,
            'average_quality': average_quality,
            'success_rate': success_rate,
            'captured_fingers': captured_fingers,
            'final_score': final_score,
            'completion_time': datetime.utcnow().isoformat()
        })
        activity.metadata = json.dumps(metadata)
        
        # Gerar badge se 100% de digitalização
        if total_fingers == 10 and average_quality >= 70:
            badge = criar_ou_obter_badge(
                user_id,
                'etan_master',
                'Mestre em ETAN',
                'Completou a captura biométrica com 100% de sucesso',
                '🏆'
            )
            db.session.add(badge)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'activity_id': activity_id,
            'final_score': final_score,
            'status': 'completed',
            'total_fingers_captured': total_fingers,
            'average_quality': average_quality,
            'success_rate': success_rate,
            'message': 'Sessão de captura biométrica concluída com sucesso'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500
