#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test para isolar qual blueprint causa erro 426
"""
from flask import Flask  
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# Inicializar banco de dados
db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///infant_id_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

# Test 1: Sem blueprints
@app.route('/test1')
def test1():
    from flask import jsonify
    return jsonify({'test': '1 - Sem blueprints'})

print("Tentando registrar blueprints...")

try:
    print("1. Importando auth...")
    from app.routes import auth
    app.register_blueprint(auth.bp)
    print("   ✅ auth registrado")
except Exception as e:
    print(f"   ❌ Erro em auth: {e}")

try:
    print("2. Importando hospitals...")
    from app.routes import hospitals
    app.register_blueprint(hospitals.bp)
    print("   ✅ hospitals registrado")
except Exception as e:
    print(f"   ❌ Erro em hospitals: {e}")

try:
    print("3. Importando courses...")
    from app.routes import courses
    app.register_blueprint(courses.bp)
    print("   ✅ courses registrado")
except Exception as e:
    print(f"   ❌ Erro em courses: {e}")

try:
    print("4. Importando users...")
    from app.routes import users
    app.register_blueprint(users.bp)
    print("   ✅ users registrado")
except Exception as e:
    print(f"   ❌ Erro em users: {e}")

try:
    print("5. Importando ai...")
    from app.routes import ai
    app.register_blueprint(ai.bp)
    print("   ✅ ai registrado")
except Exception as e:
    print(f"   ❌ Erro em ai: {e}")

try:
    print("6. Importando documents...")
    from app.routes import documents
    app.register_blueprint(documents.bp)
    print("   ✅ documents registrado")
except Exception as e:
    print(f"   ❌ Erro em documents: {e}")

print("\n✅ Iniciando Flask na porta 5003...")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=False)
