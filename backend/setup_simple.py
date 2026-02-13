# -*- coding: utf-8 -*-
"""
Script de teste simples - criar tabelas PostgreSQL
"""
import os
import sys

# Definir encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from pathlib import Path
import importlib

# Carregar .env
try:
    _dotenv = importlib.import_module("dotenv")
    load_dotenv = getattr(_dotenv, "load_dotenv")
except Exception:
    def load_dotenv(*args, **kwargs):
        return False

load_dotenv()

print("\n" + "="*70)
print("🗄️  TESTE DE CONEXÃO POSTGRESQL")
print("="*70 + "\n")

# Dados de conexão
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', '')
db_name = os.getenv('DB_NAME', 'infant_id_platform')

print(f"Host: {db_host}")
print(f"Port: {db_port}")
print(f"User: {db_user}")
print(f"Database: {db_name}\n")

try:
    print("📦 Importando Flask e SQLAlchemy...")
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy import text
    print("✅ Flask e SQLAlchemy importados!\n")
    
    print("🔧 Criando app Flask...")
    app = Flask(__name__)
    
    # URL do banco
    database_uri = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    print(f"URI: {database_uri}\n")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    print("✅ App criado!\n")
    
    print("🔗 Testando conexão...")
    with app.app_context():
        # Teste de conexão simples
        result = db.session.execute(text("SELECT 1"))
        print("✅ Conexão com PostgreSQL OK!\n")
        
        print("📝 Criando tabelas...")
        db.create_all()
        print("✅ Tabelas criadas com sucesso!\n")
        
    print("="*70)
    print("✅ DATABASE SETUP CONCLUÍDO COM SUCESSO!")
    print("="*70)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print(f"Tipo: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
