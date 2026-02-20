# -*- coding: utf-8 -*-
"""
Arquivo __init__ para testes
"""
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv
from app.config import config

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar banco de dados
db = SQLAlchemy()

def create_app():
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Usar config de desenvolvimento (SQLite para evitar problemas PostgreSQL)
    app.config.from_object(config['development'])
    
    # Inicializar extensões
    db.init_app(app)
    
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
    from app.routes import auth, courses, users, ai, hospitals, documents
    app.register_blueprint(auth.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(ai.bp)
    app.register_blueprint(hospitals.bp)
    app.register_blueprint(documents.bp)
    
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
    
    # Rota catch-all para JS
    @app.route('/js/<filename>')
    def serve_js(filename):
        js_path = os.path.join(root_path, 'js')
        return send_from_directory(js_path, filename, mimetype='application/javascript')
    
    # Rota catch-all para imagens
    @app.route('/images/<filename>')
    def serve_images(filename):
        images_path = os.path.join(root_path, 'images')
        return send_from_directory(images_path, filename)
    
    # Rota catch-all para assets (logos, documentos, etc)
    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        assets_path = os.path.join(root_path, 'assets')
        return send_from_directory(assets_path, filename)
    
    # Health check
    @app.route('/health')
    def health():
        return {'status': 'ok', 'message': 'Server is running'}
    
    # Criar tabelas se não existirem
    with app.app_context():
        db.create_all()
    
    return app
