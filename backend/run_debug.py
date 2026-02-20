#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Server com logging detalhado para debugar erro 426
"""
import os
import sys
import logging

# Configurar path
sys.path.insert(0, os.path.dirname(__file__))

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from app import create_app, db

print("\n" + "=" * 60)
print("DEBUG SERVER - LOGGING DETALHADO")
print("=" * 60 + "\n")

try:
    print("[1] Criando app...")
    app = create_app()
    print("[✅] App criada com sucesso")
    
    # Adicionar before_request e after_request hooks para logging
    @app.before_request()
    def before_req():
        from flask import request
        print(f"[REQ] {request.method} {request.path}")
    
    @app.after_request
    def after_req(response):
        from flask import request
        print(f"[RES] {request.method} {request.path} -> {response.status_code}")
        return response
    
    print("[2] Adicionando hooks de logging...")
    @app.before_request
    def before_req():
        from flask import request
        print(f"[REQ] {request.method} {request.path}")
    
    @app.after_request
    def after_req(response):
        from flask import request
        print(f"[RES] {request.method} {request.path} -> {response.status_code}")
        return response
    
    print("[3] Iniciando servidor na porta 5001...")
    port = int(os.getenv('FLASK_PORT', 5001))
    app.run(
        host='127.0.0.1', 
        port=port, 
        debug=True,
        use_reloader=False,
        use_debugger=True,
        threaded=True
    )
    
except Exception as e:
    print(f"[❌] Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
