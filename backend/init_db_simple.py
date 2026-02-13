# -*- coding: utf-8 -*-
"""
Script simples para inicializar banco SQLite
"""
import os
import sys

# Adicionar backend ao path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db

print("🗄️ Inicializando banco SQLite...")
app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database criado com sucesso!")
    print(f"📁 Arquivo: infant_id_platform.db")
