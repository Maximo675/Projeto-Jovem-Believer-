# -*- coding: utf-8 -*-
"""
Arquivo __init__ para testes
"""
from flask import Flask, send_from_directory
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
    
    # Rota catch-all para assets (logos, documentos, etc)
    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        assets_path = os.path.join(root_path, 'assets')
        return send_from_directory(assets_path, filename)
    
    # Health check
    @app.route('/health')
    def health():
        return {'status': 'ok', 'message': 'Server is running'}
    
    # Registrar WebSocket handlers
    from . import websocket_handlers
    
    # Criar tabelas se não existirem - dentro do contexto
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"[WARNING] Erro ao criar tabelas: {e}")
    
    return app
