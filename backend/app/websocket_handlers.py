"""
WebSocket Server para Atividades Práticas ETAN
Comunicação em tempo real entre frontend, backend e dispositivos de captura
"""

from flask import request
from flask_socketio import emit, join_room, leave_room, rooms
from app import socketio, db
from app.models.activity import UserActivity, ActivityAttempt
from app.models.user import User
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

# =======================================================
# EVENTOS DE CONEXÃO/DESCONEXÃO
# =======================================================

@socketio.on('connect')
def handle_connect():
    """Cliente conectou ao WebSocket"""
    user_id = request.sid
    logger.info(f'🔗 Cliente conectado: {user_id}')
    emit('connection_response', {
        'status': 'conectado',
        'message': 'Conectado ao servidor de atividades'
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Cliente desconectou do WebSocket"""
    user_id = request.sid
    logger.info(f'🔌 Cliente desconectado: {user_id}')


# =======================================================
# EVENTOS DE ATIVIDADES
# =======================================================

@socketio.on('activity_join')
def handle_activity_join(data):
    """Usuário entra em uma atividade"""
    activity_id = data.get('activity_id')
    user_id = data.get('user_id')
    lesson_id = data.get('lesson_id')
    
    room = f'activity-{activity_id}'
    join_room(room)
    
    logger.info(f'✅ Usuário {user_id} entrou atividade {activity_id}')
    
    emit('activity_joined', {
        'activity_id': activity_id,
        'room': room,
        'status': 'pronto',
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)


@socketio.on('activity_start')
def handle_activity_start(data):
    """Atividade iniciada"""
    activity_id = data.get('activity_id')
    user_id = data.get('user_id')
    activity_type = data.get('activity_type', 'practice')
    
    room = f'activity-{activity_id}'
    
    logger.info(f'🎮 Atividade {activity_id} iniciada por usuário {user_id}')
    
    emit('activity_started', {
        'activity_id': activity_id,
        'status': 'em_progresso',
        'tipo': activity_type,
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)


@socketio.on('activity_progress')
def handle_activity_progress(data):
    """Progresso da atividade em tempo real"""
    activity_id = data.get('activity_id')
    user_id = data.get('user_id')
    fase = data.get('fase')
    score = data.get('score', 0)
    tempo_gasto = data.get('tempo_gasto', 0)
    
    room = f'activity-{activity_id}'
    
    logger.debug(f'📊 Progresso: fase {fase}, score {score}, tempo {tempo_gasto}s')
    
    # Atualizar progresso em tempo real
    emit('progress_update', {
        'activity_id': activity_id,
        'fase': fase,
        'score': score,
        'tempo_gasto': tempo_gasto,
        'percentual': min((fase / 5) * 100, 100),  # Assumindo 5 fases
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)


@socketio.on('activity_complete')
def handle_activity_complete(data):
    """Atividade completada"""
    activity_id = data.get('activity_id')
    user_id = data.get('user_id')
    score = data.get('score', 0)
    time_total = data.get('time_total', 0)
    attempts = data.get('attempts', 1)
    responses = data.get('responses', {})
    
    room = f'activity-{activity_id}'
    
    logger.info(f'🏁 Atividade {activity_id} completada - Score: {score}/100')
    
    # Atualizar banco de dados
    try:
        activity = UserActivity.query.get(activity_id)
        if activity and activity.user_id == user_id:
            activity.status = 'completed'
            activity.score = score
            activity.time_spent = time_total
            activity.completed_at = datetime.utcnow()
            db.session.commit()
            
            badges = []
            if score >= 95:
                badges.append('perfect_score')
            if attempts == 1:
                badges.append('first_try')
            if time_total < 600:
                badges.append('speed_runner')
            
            emit('activity_completed', {
                'activity_id': activity_id,
                'status': 'completo',
                'score': score,
                'time_total': time_total,
                'attempts': attempts,
                'badges': badges,
                'timestamp': datetime.utcnow().isoformat()
            }, room=room)
        else:
            logger.error(f'❌ Atividade {activity_id} não encontrada')
    except Exception as e:
        logger.error(f'❌ Erro ao completar atividade: {e}')
        emit('error', {'message': str(e)}, room=room)


@socketio.on('activity_leave')
def handle_activity_leave(data):
    """Usuário sai da atividade"""
    activity_id = data.get('activity_id')
    user_id = data.get('user_id')
    room = f'activity-{activity_id}'
    
    leave_room(room)
    logger.info(f'❌ Usuário {user_id} saiu da atividade {activity_id}')


# =======================================================
# EVENTOS DE CAPTURA BIOMÉTRICA (OpenbioEnroll)
# =======================================================

@socketio.on('capture_preview')
def handle_capture_preview(data):
    """Recebe preview de captura em tempo real"""
    activity_id = data.get('activity_id')
    image_data = data.get('image_data')
    nfiq_score = data.get('nfiq_score', 0)
    roi_detected = data.get('roi_detected', False)
    
    room = f'activity-{activity_id}'
    
    # Broadcast do preview para instrutores/monitores
    emit('preview_received', {
        'activity_id': activity_id,
        'nfiq_score': nfiq_score,
        'roi_detected': roi_detected,
        'image_available': bool(image_data),
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)


@socketio.on('capture_image')
def handle_capture_image(data):
    """Captura de imagem finalizada"""
    activity_id = data.get('activity_id')
    user_id = data.get('user_id')
    image_data = data.get('image_data')
    nfiq_score = data.get('nfiq_score', 0)
    image_quality = data.get('image_quality', 'unknown')  # 'excellent', 'good', 'fair', 'poor'
    
    room = f'activity-{activity_id}'
    
    logger.info(f'📸 Captura recebida: NFIQ={nfiq_score}, Qualidade={image_quality}')
    
    feedback = evaluateImageQuality(nfiq_score)
    
    emit('capture_processed', {
        'activity_id': activity_id,
        'nfiq_score': nfiq_score,
        'quality': image_quality,
        'feedback': feedback,
        'can_proceed': nfiq_score >= 40,  # NFIQ mínimo
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)


@socketio.on('capture_error')
def handle_capture_error(data):
    """Erro durante captura"""
    activity_id = data.get('activity_id')
    error_code = data.get('error_code', 'UNKNOWN')
    error_message = data.get('error_message', 'Erro desconhecido')
    
    room = f'activity-{activity_id}'
    
    logger.error(f'❌ Erro de captura: {error_code} - {error_message}')
    
    # Mapear códigos de erro para mensagens amigáveis
    user_message = mapErrorToUserMessage(error_code, error_message)
    
    emit('capture_error_handled', {
        'activity_id': activity_id,
        'error_code': error_code,
        'user_message': user_message,
        'retry_allowed': True,
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)


# =======================================================
# EVENTOS DE SIMULADOR (Para atividade de treino)
# =======================================================

@socketio.on('simulator_request')
def handle_simulator_request(data):
    """Requisição para abrir simulador ou captura real"""
    activity_id = data.get('activity_id')
    simulator_type = data.get('type', 'practice')  # 'practice' ou 'real'
    fase = data.get('fase', 4)  # Assumindo fase 4 = simulador
    
    room = f'activity-{activity_id}'
    
    logger.info(f'🖥️ Simulador requisitado: tipo={simulator_type}, fase={fase}')
    
    emit('simulator_open', {
        'activity_id': activity_id,
        'type': simulator_type,
        'fase': fase,
        'url': get_simulator_url(simulator_type),
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)


@socketio.on('simulator_close')
def handle_simulator_close(data):
    """Simulador fechado"""
    activity_id = data.get('activity_id')
    resultado = data.get('resultado', {})
    
    room = f'activity-{activity_id}'
    
    logger.info(f'✅ Simulador fechado para atividade {activity_id}')
    
    emit('simulator_closed', {
        'activity_id': activity_id,
        'resultado': resultado,
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)


# =======================================================
# EVENTOS DE INSTRUTOR/MONITOR
# =======================================================

@socketio.on('instructor_monitor')
def handle_instructor_monitor(data):
    """Instrutor começa a monitorar uma atividade"""
    instructor_id = data.get('instructor_id')
    activity_id = data.get('activity_id')
    
    room = f'activity-monitor-{activity_id}'
    join_room(room)
    
    logger.info(f'👁️ Instrutor {instructor_id} começou a monitorar atividade {activity_id}')
    
    emit('monitoring_started', {
        'instructor_id': instructor_id,
        'activity_id': activity_id,
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)


@socketio.on('instructor_message')
def handle_instructor_message(data):
    """Instrutor envia mensagem/feedback em tempo real"""
    instructor_id = data.get('instructor_id')
    activity_id = data.get('activity_id')
    message = data.get('message')
    user_id = data.get('target_user_id')
    
    room = f'activity-{activity_id}'
    
    logger.info(f'💬 Mensagem do instrutor: {message}')
    
    emit('instructor_feedback', {
        'instructor_id': instructor_id,
        'message': message,
        'target_user': user_id,
        'timestamp': datetime.utcnow().isoformat()
    }, room=room)


# =======================================================
# FUNÇÕES AUXILIARES
# =======================================================

def evaluateImageQuality(nfiq_score):
    """Avaliar qualidade da imagem baseado em NFIQ"""
    if nfiq_score >= 80:
        return {
            'level': 'excelente',
            'emoji': '⭐',
            'message': 'Qualidade excelente! Imagem pronta para uso.',
            'feedback': 'Perfeito!'
        }
    elif nfiq_score >= 60:
        return {
            'level': 'boa',
            'emoji': '👍',
            'message': 'Qualidade boa. Pode prosseguir com cuidado.',
            'feedback': 'Aceitável'
        }
    elif nfiq_score >= 40:
        return {
            'level': 'aceitavel',
            'emoji': '⚠️',
            'message': 'Qualidade aceitável, mas não ideal. Tente melhorar.',
            'feedback': 'Aceita, mas repita se possível'
        }
    else:
        return {
            'level': 'insuficiente',
            'emoji': '❌',
            'message': 'Qualidade insuficiente. Tente novamente.',
            'feedback': 'Rejeitada'
        }


def mapErrorToUserMessage(error_code, error_message):
    """Mapear código de erro para mensagem amigável ao usuário"""
    error_map = {
        'DEVICE_NOT_FOUND': 'Dispositivo biométrico não encontrado. Verifique a conexão.',
        'DEVICE_BUSY': 'Dispositivo ocupado por outro usuário. Aguarde...',
        'NO_FINGER_DETECTED': 'Nenhum dedo detectado. Posicione melhor.',
        'POOR_CONTACT': 'Contato insuficiente. Pressione mais firme.',
        'MOISTURE_HIGH': 'Dedo muito úmido. Seque e tente novamente.',
        'TIMEOUT': 'Tempo limite excedido. Tente novamente.',
        'SENSOR_ERROR': 'Erro no sensor. Contacte o suporte.',
        'FIRMWARE_ERROR': 'Erro no firmware do sensor. Reinicie o dispositivo.',
    }
    
    return error_map.get(error_code, error_message or 'Erro desconhecido')


def get_simulator_url(simulator_type):
    """Gerar URL appropriada para simulador ou captura real"""
    if simulator_type == 'practice':
        return '/activities/etan_simulador_pratica.html'
    elif simulator_type == 'real':
        return 'https://infant.akiyama.com.br/#/infant-capture'  # URL do site real
    else:
        return '/activities/etan_protocol_simulator.html'


# =======================================================
# ENDPOINTS HTTP PARA INICIALIZAR WEBSOCKET
# =======================================================

def register_websocket_routes(app):
    """Registrar rotas HTTP que inicializam conexões WebSocket"""
    
    @app.route('/api/activities/ws-init/<int:activity_id>', methods=['POST'])
    def init_websocket_activity(activity_id):
        """Inicializar conexão WebSocket para uma atividade"""
        from flask_login import current_user
        from flask import jsonify
        
        if not current_user:
            return jsonify({'error': 'Não autenticado'}), 401
        
        try:
            activity = UserActivity.query.get(activity_id)
            if not activity or activity.user_id != current_user.id:
                return jsonify({'error': 'Atividade não encontrada'}), 404
            
            return jsonify({
                'status': 'websocket_ready',
                'activity_id': activity_id,
                'user_id': current_user.id,
                'ws_url': request.host_url.replace('http', 'ws')[:-1] + '/socket.io',
                'message': 'Conecte via WebSocket usando o Socket.IO client'
            }), 200
        
        except Exception as e:
            logger.error(f'❌ Erro ao inicializar WebSocket: {e}')
            return jsonify({'error': str(e)}), 500
