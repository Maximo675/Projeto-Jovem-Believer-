#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup PostgreSQL Database Script
Cria o banco de dados PostgreSQL e as tabelas automaticamente
"""

import os
import sys
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

class Config:
    """Configuração base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    # JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key')
    JWT_EXPIRATION = int(os.getenv('JWT_EXPIRATION', 86400))

    # IA
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', 5432)}/{os.getenv('DB_NAME', 'infant_id_platform')}?client_encoding=utf8"

class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    """Configuração de testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Adicionar backend ao path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

def setup_database():
    """Criar database e tabelas no PostgreSQL"""
    print("\n" + "="*70)
    print("🗄️  INFANT.ID - PostgreSQL DATABASE SETUP")
    print("="*70 + "\n")
    
    # Verificar configurações
    print("📋 Verificando configurações...")
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_user = os.getenv('DB_USER', 'postgres')
    db_name = os.getenv('DB_NAME', 'infant_id_platform')
    
    print(f"   Host: {db_host}")
    print(f"   Port: {db_port}")
    print(f"   User: {db_user}")
    print(f"   Database: {db_name}")
    print()
    
    try:
        print("📦 Importando dependências...")
        from app import create_app, db
        from app.models.user import User
        from app.models.hospital import Hospital
        from app.models.course import Course
        from app.models.lesson import Lesson
        from app.models.document import Document
        
        print("✅ Dependências importadas com sucesso!")
        
        # Criar app context
        print("\n🔧 Criando contexto da aplicação...")
        app = create_app()
        
        with app.app_context():
            print("✅ Contexto criado!")
            
            # Testar conexão
            print("\n🔗 Testando conexão com PostgreSQL...")
            try:
                db.session.execute(text("SELECT 1"))
                print("✅ Conexão com PostgreSQL estabelecida!")
            except Exception as e:
                print(f"❌ Erro ao conectar: {e}")
                return False
            
            # Criar tabelas
            print("\n📝 Criando tabelas no banco de dados...")
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
            
            # Listar tabelas criadas
            print("\n📊 Tabelas criadas:")
            tables = [
                ('users', 'Usuários do sistema'),
                ('hospitals', 'Hospitais'),
                ('courses', 'Cursos'),
                ('lessons', 'Aulas'),
                ('documents', 'Documentos'),
            ]
            
            for table, description in tables:
                print(f"   ✓ {table:<20} ({description})")
            
            # Estatísticas
            print("\n📈 Registros no banco:")
            stats = [
                (User, 'Users'),
                (Hospital, 'Hospitals'),
                (Course, 'Courses'),
                (Lesson, 'Lessons'),
                (Document, 'Documents'),
            ]
            
            for model, name in stats:
                count = model.query.count()
                print(f"   {name:<20} {count} registros")
            
        print("\n" + "="*70)
        print("✅ DATABASE SETUP CONCLUÍDO COM SUCESSO!")
        print("="*70)
        print("\n🎯 Próximos passos:")
        print("   1. Abra o DBeaver")
        print("   2. Conecte ao PostgreSQL")
        print("   3. Expanda 'infant_id_platform' → 'Schemas' → 'public' → 'Tables'")
        print("   4. Você verá todas as tabelas criadas!")
        print("\n🚀 Agora rode o servidor:")
        print("   python run.py")
        print("\n🔗 Acesse em:")
        print("   http://localhost:5000")
        print("="*70 + "\n")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ ERRO DE IMPORTAÇÃO: {e}")
        print("\n💡 Solução: Instale as dependências:")
        print("   C:\\Python314\\python.exe -m pip install --user Flask Flask-SQLAlchemy")
        return False
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print(f"\n💡 Verifique:")
        print("   1. PostgreSQL está rodando?")
        print("   2. Senha do usuário 'postgres' está correta em .env?")
        print("   3. Database 'infant_id_platform' foi criado?")
        print("\n   Execute no DBeaver para criar o database:")
        print("   CREATE DATABASE infant_id_platform;")
        return False

if __name__ == '__main__':
    success = setup_database()
    sys.exit(0 if success else 1)
