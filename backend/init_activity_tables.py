#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple database initialization script for activity tracking tables
No Alembic migration required - direct SQLAlchemy table creation
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models.activity import UserActivity, ActivityAttempt, ActivityBadge

def init_activity_tables():
    """Create activity tracking tables directly"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Inicializando tabelas de atividades...")
        
        try:
            # Create all tables from models
            db.create_all()
            
            print("✅ Tabelas criadas com sucesso:")
            print("  - user_activities (rastreamento de progresso)")
            print("  - activity_attempt (detalhes de cada tentativa)")
            print("  - activity_badge (sistema de badges)")
            
            # Verify tables were created
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print("\n📊 Tabelas no banco de dados:")
            for table in sorted(tables):
                print(f"  ✓ {table}")
            
            print("\n✨ Banco de dados pronto para atividades!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            return False


if __name__ == '__main__':
    success = init_activity_tables()
    sys.exit(0 if success else 1)
