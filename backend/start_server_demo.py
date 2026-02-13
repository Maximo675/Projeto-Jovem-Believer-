#!/usr/bin/env python
"""
Script para iniciar o servidor Flask em modo DEBUG (sem banco de dados).
Perfeito para testes iniciais da API.
"""

import sys
import os

# Adicionar o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("✅ Importando Flask...")
    from flask import Flask
    print("✅ Flask importado com sucesso")
    
    print("✅ Criando aplicação simples (sem banco de dados)...")
    
    # App simples para testes
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        """Homepage"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>INFANT.ID - Online</title>
            <style>
                body { font-family: Arial; margin: 40px; }
                h1 { color: #00a86b; }
                .status { background: #f0f8f5; padding: 20px; border-radius: 8px; }
                .success { color: #00a86b; }
                a { color: #1e90ff; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>✅ INFANT.ID Servidor Rodando!</h1>
            <div class="status">
                <p><strong>Status: Ativo</strong></p>
                <p>Servidor Flask está funcionando na porta 5000</p>
                <br>
                <p>Links disponíveis:</p>
                <ul>
                    <li><a href="/pages/login.html">📱 Ir para Login</a></li>
                    <li><a href="/pages/register.html">📝 Ir para Registro</a></li>
                    <li><a href="/docs">📚 Documentação API</a></li>
                </ul>
                <br>
                <p style="color: #ff9800;">
                    ⚠️ <strong>MODO DEBUG:</strong> Servidor rodando sem banco de dados<br>
                    Para usar com banco de dados, configure MySQL primeiro.
                </p>
            </div>
        </body>
        </html>
        ''', 200
    
    @app.route('/api/health')
    def health():
        """Health check"""
        return {
            "status": "OK",
            "message": "INFANT.ID server is running",
            "version": "1.0.0"
        }, 200
    
    print("✅ Aplicação criada com sucesso!")
    
    # Servir arquivos estáticos (HTML, CSS, JS)
    print("✅ Configurando arquivos estáticos...")
    @app.route('/pages/<path:filename>')
    def pages(filename):
        """ Servir páginas HTML """
        import os
        file_path = os.path.join(os.path.dirname(__file__), '..', 'pages', filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read(), 200, {'Content-Type': 'text/html'}
        return "Página não encontrada", 404
    
    @app.route('/css/<path:filename>')
    def css(filename):
        """Servir CSS"""
        import os
        file_path = os.path.join(os.path.dirname(__file__), '..', 'css', filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read(), 200, {'Content-Type': 'text/css'}
        return "CSS não encontrado", 404
    
    @app.route('/js/<path:filename>')
    def js(filename):
        """Servir JavaScript"""
        import os
        file_path = os.path.join(os.path.dirname(__file__), '..', 'js', filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read(), 200, {'Content-Type': 'application/javascript'}
        return "JS não encontrado", 404
    
    print("\n" + "="*60)
    print("🎉 SERVIDOR PRONTO PARA USAR")
    print("="*60)
    print("✅ Acesse: http://localhost:8000")
    print("✅ Login: http://localhost:8000/pages/login.html")
    print("✅ Register: http://localhost:8000/pages/register.html")
    print("="*60 + "\n")
    
    # Rodar servidor
    app.run(
        debug=False,
        host='0.0.0.0',
        port=8000,
        use_reloader=False
    )
    
except ImportError as e:
    print(f"\n❌ ERRO DE IMPORTAÇÃO: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
