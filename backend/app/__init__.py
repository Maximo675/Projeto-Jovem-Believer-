# -*- coding: utf-8 -*-
"""
Arquivo __init__ para testes
"""
from flask import Flask, send_from_directory, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv
from app.config import config

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar banco de dados e SocketIO
db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Usar config de desenvolvimento (SQLite para evitar problemas PostgreSQL)
    app.config.from_object(config['development'])
    
    # Inicializar extensões
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Configurar CORS
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5001,http://127.0.0.1:3000,http://127.0.0.1:5001').split(',')
    # Em desenvolvimento, aceitar qualquer localhost
    cors_origins = [origin.strip() for origin in cors_origins if origin.strip()]
    
    CORS(app, 
         origins=cors_origins, 
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Registrar blueprints
    from app.routes import auth, courses, users, ai, hospitals, documents, activities
    app.register_blueprint(auth.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(ai.bp)
    app.register_blueprint(hospitals.bp)
    app.register_blueprint(documents.bp)
    app.register_blueprint(activities.activities_bp)
    
    # ====== SERVIR ARQUIVOS ESTÁTICOS ======
    # Caminho raiz do projeto (acima de backend)
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Rota raiz - serve index.html
    @app.route('/')
    def index():
        index_path = os.path.join(root_path, 'index.html')
        return send_from_directory(root_path, 'index.html', mimetype='text/html')
    
    # Rota para dashboard de atividades
    @app.route('/atividades')
    def atividades_dashboard():
        pages_path = os.path.join(root_path, 'pages')
        return send_from_directory(pages_path, 'atividades.html', mimetype='text/html')
    
    # Rota catch-all para páginas em /pages/
    @app.route('/pages/<filename>')
    def serve_pages(filename):
        pages_path = os.path.join(root_path, 'pages')
        return send_from_directory(pages_path, filename)
    
    # Rota catch-all para CSS
    @app.route('/css/<filename>')
    def serve_css(filename):
        css_path = os.path.join(root_path, 'css')
        return send_from_directory(css_path, filename, mimetype='text/css')
    
    # Rota catch-all para JS (tenta frontend/js primeiro, depois js)
    @app.route('/js/<filename>')
    def serve_js(filename):
        # Tentar em frontend/js primeiro
        js_path = os.path.join(root_path, 'frontend', 'js')
        if os.path.exists(os.path.join(js_path, filename)):
            return send_from_directory(js_path, filename, mimetype='application/javascript')
        # Fallback para js raiz
        js_path = os.path.join(root_path, 'js')
        return send_from_directory(js_path, filename, mimetype='application/javascript')
    
    # Rota catch-all para imagens (comentada pois pasta foi removida)
    # @app.route('/images/<filename>')
    # def serve_images(filename):
    #     images_path = os.path.join(root_path, 'images')
    #     return send_from_directory(images_path, filename)
    
    # Rota para arquivos públicos (favicons, ícones)
    @app.route('/public/<filename>')
    def serve_public(filename):
        public_path = os.path.join(root_path, 'public')
        return send_from_directory(public_path, filename)
    
    # Rota para atividades práticas
    @app.route('/activities/<filename>')
    def serve_activities(filename):
        activities_path = os.path.join(root_path, 'frontend', 'activities')
        return send_from_directory(activities_path, filename, mimetype='text/html')
    
    # Redirect para evitar confusão (frontend/activities -> activities)
    @app.route('/frontend/activities/<filename>')
    def redirect_activities(filename):
        from flask import redirect
        return redirect(f'/activities/{filename}', code=301)
    
    # Rota catch-all para assets (logos, documentos, etc)
    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        assets_path = os.path.join(root_path, 'assets')
        return send_from_directory(assets_path, filename)
    
    # Health check
    @app.route('/health')
    def health():
        return {'status': 'ok', 'message': 'Server is running'}
    
    # ============================================================
    # Rota de Captura Biométrica (simulador)
    # ============================================================
    @app.route('/api/activity-attempts', methods=['POST'])
    def save_biometric_capture():
        """Salvar captura biométrica do simulador"""
        from app.models.activity import UserActivity, ActivityAttempt
        from datetime import datetime
        
        try:
            data = request.get_json()
            
            user_id = data.get('user_id', 1)
            activity_id = data.get('activity_id', 4)
            attempt_number = data.get('attempt_number', 1)
            score = data.get('score', 0)
            metrics = data.get('metrics', {})
            success = data.get('success', True)
            timestamp = data.get('timestamp', datetime.utcnow().isoformat())
            
            # Buscar ou criar atividade
            activity = UserActivity.query.filter_by(
                user_id=user_id,
                activity_id=activity_id
            ).first()
            
            if not activity:
                activity = UserActivity(
                    user_id=user_id,
                    activity_id=activity_id,
                    activity_type='biometric_capture',
                    status='ongoing'
                )
                db.session.add(activity)
                db.session.flush()
            
            # Criar tentativa
            attempt = ActivityAttempt(
                activity_id=activity.id,
                user_id=user_id,
                attempt_number=attempt_number,
                score=score,
                time_taken=0
            )
            
            # Salvar metrics como JSON
            if metrics:
                attempt.set_responses(metrics)
            
            # Marcar como sucesso
            if success:
                attempt.set_result('success')
                activity.score = max(activity.score or 0, score)
                activity.attempts = attempt_number
            
            db.session.add(attempt)
            db.session.commit()
            
            finger = metrics.get('finger', 'desconhecido')
            print(f"✅ Captura biométrica salva: User={user_id}, Activity={activity_id}, Finger={finger}, NFIQ={score}")
            
            return jsonify({
                'success': True,
                'attempt_id': attempt.id,
                'message': 'Captura salva com sucesso',
                'data': {
                    'user_id': user_id,
                    'activity_id': activity_id,
                    'attempt_number': attempt_number,
                    'score': score,
                    'finger': finger
                }
            }), 201
        
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao salvar captura: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # Registrar WebSocket handlers
    from . import websocket_handlers
    
    # Criar tabelas se não existirem - dentro do contexto
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"[WARNING] Erro ao criar tabelas: {e}")
    
    return app
