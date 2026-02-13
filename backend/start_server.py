#!/usr/bin/env python
"""
Script para iniciar o servidor Flask.
Testa importações e inicia na porta 5000.
"""

import sys
import os

# Adicionar o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("✅ Importando Flask...")
    from flask import Flask
    print(f"✅ Flask importado com sucesso")
    
    print("✅ Importando create_app...")
    from app import create_app
    print("✅ create_app importado com sucesso")
    
    print("✅ Criando aplicação...")
    app = create_app()
    print("✅ Aplicação criada com sucesso!")
    
    print("\n" + "="*50)
    print("🎉 SERVIDOR PRONTO PARA RODAR")
    print("="*50)
    print(f"Acesse: http://localhost:5000")
    print(f"Login: http://localhost:5000/pages/login.html")
    print("="*50 + "\n")
    
    # Rodar servidor
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000,
        use_reloader=False
    )
    
except ImportError as e:
    print(f"\n❌ ERRO DE IMPORTAÇÃO: {e}")
    print("\nTentando diagnóstico...")
    print(f"Python: {sys.version}")
    print(f"Path: {sys.path}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
