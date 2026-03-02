#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup Database Script
Cria o banco de dados MySQL e as tabelas automaticamente
"""

import os
import sys
from pathlib import Path

# Adicionar backend ao path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

def setup_database():
    """Criar database e tabelas"""
    print("\n" + "="*60)
    print("🗄️  INFANT.ID - DATABASE SETUP")
    print("="*60 + "\n")
    
    try:
        print("📦 Importando Flask app...")
        from app import create_app, db
        from app.models.user import User
        from app.models.hospital import Hospital
        from app.models.course import Course
        from app.models.lesson import Lesson
        from app.models.document import Document
        
        print("✅ App importada com sucesso!")
        
        # Criar app context
        print("\n🔧 Criando contexto da aplicação...")
        app = create_app()
        
        with app.app_context():
            print("✅ Contexto criado!")
            
            # Criar tabelas
            print("\n📝 Criando tabelas no banco de dados...")
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
            
            # Listar tabelas criadas
            print("\n📊 Tabelas criadas:")
            print("   ✓ users")
            print("   ✓ hospitals")
            print("   ✓ courses")
            print("   ✓ lessons")
            print("   ✓ documents")
            
            # Estatísticas
            print("\n📈 Estatísticas:")
            print(f"   Users no banco: {User.query.count()}")
            print(f"   Hospitals no banco: {Hospital.query.count()}")
            print(f"   Courses no banco: {Course.query.count()}")
            print(f"   Lessons no banco: {Lesson.query.count()}")
            print(f"   Documents no banco: {Document.query.count()}")
            
        print("\n" + "="*60)
        print("✅ DATABASE SETUP CONCLUÍDO COM SUCESSO!")
        print("="*60)
        print("\n🚀 Agora você pode rodar o servidor:")
        print("   python run.py")
        print("\n🔗 E acessar em:")
        print("   http://localhost:5001")
        print("="*60 + "\n")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ ERRO DE IMPORTAÇÃO: {e}")
        print("\n💡 Solução: Instale as dependências:")
        print("   C:\\Python314\\python.exe -m pip install --user Flask Flask-SQLAlchemy python-dotenv")
        return False
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("\n💡 Verifique:")
        print("   1. MySQL está rodando? (Services → MySQL80)")
        print("   2. Porta 3306 correta?")
        print("   3. Senha do root está configurada em .env?")
        print("   4. Database 'infant_id_platform' existe?")
        return False

if __name__ == '__main__':
    success = setup_database()
    sys.exit(0 if success else 1)
