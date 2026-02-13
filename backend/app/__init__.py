# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Arquivo __init__ para testes
"""
from flask import Flask
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
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000,http://127.0.0.1:8000').split(',')
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
    
    # Rota raiz - serve a página de login
    @app.route('/')
    def index():
        from flask import redirect
        return redirect('/pages/login.html')

    # Servir arquivos estáticos (fora da pasta backend)
    @app.route('/pages/<filename>')
    def serve_pages(filename):
        from flask import send_from_directory
        pages_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'pages')
        return send_from_directory(pages_path, filename)

    @app.route('/css/<filename>')
    def serve_css(filename):
        from flask import send_from_directory
        css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'css')
        return send_from_directory(css_path, filename)

    @app.route('/js/<filename>')
    def serve_js(filename):
        from flask import send_from_directory
        js_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'js')
        return send_from_directory(js_path, filename)

    @app.route('/images/<filename>')
    def serve_images(filename):
        from flask import send_from_directory
        images_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'images')
        return send_from_directory(images_path, filename)

    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        from flask import send_from_directory
        assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
        return send_from_directory(assets_path, filename)
    
    # Tabelas já foram criadas no DBeaver via create_tables.sql
    # Não precisa criar novamente aqui
    
    return app
