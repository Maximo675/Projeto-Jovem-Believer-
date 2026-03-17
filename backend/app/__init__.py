# -*- coding: utf-8 -*-
"""
Arquivo __init__ para testes
"""
from flask import Flask, send_from_directory, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv
from app.config import config

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar banco de dados e SocketIO
db = SQLAlchemy()
socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode='threading',
    ping_timeout=60,
    ping_interval=25,
    engineio_logger=False,
    transports=['websocket', 'polling']  # Allow both WebSocket and HTTP polling
)

def create_app():
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Usar config de desenvolvimento (SQLite para evitar problemas PostgreSQL)
    app.config.from_object(config['development'])
    
    # Inicializar extensões
    db.init_app(app)
    socketio.init_app(
        app, 
        cors_allowed_origins="*",
        async_mode='threading',
        ping_timeout=60,
        ping_interval=25,
        transports=['websocket', 'polling']  # Allow both WebSocket and HTTP polling
    )
    
    # ============================================================
    # CONFIGURAR CORS - OTIMIZADO PARA MÚLTIPLAS PORTAS
    # ============================================================
    
    # Obter origens do arquivo .env (padrão: aceitar localhost)
    cors_origins_str = os.getenv(
        'CORS_ORIGINS', 
        'http://localhost:3000,http://localhost:5001,http://127.0.0.1:3000,http://127.0.0.1:5001,http://localhost:4000,http://127.0.0.1:4000'
    )
    
    cors_origins = [origin.strip() for origin in cors_origins_str.split(',') if origin.strip()]
    
    # Em produção, usar apenas as origens configuradas
    # Em desenvolvimento, aceitar qualquer localhost
    if os.getenv('FLASK_ENV', 'development') == 'development':
        # Aceitar wildcard para localhost em desenvolvimento
        cors_config = {
            'origins': ['http://localhost:*', 'http://127.0.0.1:*'],
            'supports_credentials': True,
            'allow_headers': ['Content-Type', 'Authorization', 'X-Requested-With'],
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
            'max_age': 3600,
            'expose_headers': ['Content-Type', 'X-Total-Count']
        }
    else:
        # Modo produção - apenas origens específicas
        cors_config = {
            'origins': cors_origins,
            'supports_credentials': True,
            'allow_headers': ['Content-Type', 'Authorization', 'X-Requested-With'],
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
            'max_age': 3600,
            'expose_headers': ['Content-Type', 'X-Total-Count']
        }
    
    CORS(app, resources={r'/api/*': cors_config})
    CORS(app, resources={r'/activities/*': cors_config})
    
    # Log de configuração de CORS
    print(f"[CORS] Modo: {os.getenv('FLASK_ENV', 'development')}")
    print(f"[CORS] Origens configuradas: {cors_origins}")
    
    # ============================================================
    # ADICIONAR HEADERS DE SEGURANÇA E CACHE
    # ============================================================
    
    @app.after_request
    def set_security_headers(response):
        """Adicionar headers de segurança e CORS"""
        # Headers CORS adicionais
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        
        # Headers de cache para API
        if request.path.startswith('/api/'):
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        
        return response
    
    # Registrar blueprints
    from app.routes import auth, courses, users, ai, hospitals, documents, activities, infant_proxy
    app.register_blueprint(auth.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(ai.bp)
    app.register_blueprint(hospitals.bp)
    app.register_blueprint(documents.bp)
    app.register_blueprint(activities.activities_bp)
    app.register_blueprint(infant_proxy.bp)
    
    # ====== SERVIR ARQUIVOS ESTÁTICOS ======
    # Caminho raiz do projeto (acima de backend)
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Rota raiz - serve index.html
    @app.route('/')
    def index():
        print(f'[ROOT] GET / recebido')
        print(f'[ROOT] User-Agent: {request.headers.get("User-Agent", "unknown")}')
        print(f'[ROOT] Referer: {request.headers.get("Referer", "none")}')
        try:
            index_path = os.path.join(root_path, 'index.html')
            return send_from_directory(root_path, 'index.html', mimetype='text/html')
        except Exception as e:
            print(f'[ROOT] Erro ao servir index.html: {str(e)}')
            return jsonify({'error': str(e), 'status': 'error'}), 500
    
    # Mock de licença para infant.akiyama.com.br
    @app.route('/db/api/config', methods=['GET', 'POST', 'OPTIONS'])
    def mock_db_api_config():
        """Mock response para infant.akiyama.com.br verificação de config"""
        mock_response = {
            "env": "prod",
            "license": {
                "valid": True,
                "expires": "2030-12-31"
            },
            "status": "ok"
        }
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
        return jsonify(mock_response), 200, headers
    
    # /db/api/ é tratado pelo infant_proxy (rota /openbio/)
    # Proxy para port 3333 foi removido (openbio-bridge.js deletado)
    
    # Rota para dashboard de atividades
    @app.route('/atividades')
    def atividades_dashboard():
        pages_path = os.path.join(root_path, 'pages')
        return send_from_directory(pages_path, 'atividades.html', mimetype='text/html')
    
    # Rota catch-all para páginas em /pages/
    @app.route('/pages/<filename>')
    def serve_pages(filename):
        pages_path = os.path.join(root_path, 'pages')
        return send_from_directory(pages_path, filename)
    
    # Rota catch-all para CSS
    @app.route('/css/<filename>')
    def serve_css(filename):
        css_path = os.path.join(root_path, 'css')
        return send_from_directory(css_path, filename, mimetype='text/css')
    
    # Rota catch-all para JS (tenta frontend/js primeiro, depois js)
    @app.route('/js/<filename>')
    def serve_js(filename):
        # Tentar em frontend/js primeiro
        js_path = os.path.join(root_path, 'frontend', 'js')
        if os.path.exists(os.path.join(js_path, filename)):
            return send_from_directory(js_path, filename, mimetype='application/javascript')
        # Fallback para js raiz
        js_path = os.path.join(root_path, 'js')
        return send_from_directory(js_path, filename, mimetype='application/javascript')
    
    # Rota catch-all para imagens (comentada pois pasta foi removida)
    # @app.route('/images/<filename>')
    # def serve_images(filename):
    #     images_path = os.path.join(root_path, 'images')
    #     return send_from_directory(images_path, filename)
    
    # Rota para arquivos públicos (favicons, ícones)
    @app.route('/public/<filename>')
    def serve_public(filename):
        public_path = os.path.join(root_path, 'public')
        return send_from_directory(public_path, filename)
    
    # Rota para vídeos das aulas (arquivos .mp4 locais)
    @app.route('/videos/<path:filename>')
    def serve_videos(filename):
        videos_path = os.path.join(root_path, 'videos')
        return send_from_directory(videos_path, filename, mimetype='video/mp4')
    
    # Rota para atividades práticas
    @app.route('/activities/<filename>')
    def serve_activities(filename):
        # REDIRECT especial para etan-captura-biometrica (agora em /pages)
        if filename == 'etan-captura-biometrica.html':
            from flask import redirect
            return redirect(f'/pages/etan-captura-biometrica.html', code=301)
        
        activities_path = os.path.join(root_path, 'frontend', 'activities')
        return send_from_directory(activities_path, filename, mimetype='text/html')
    
    # Redirect para evitar confusão (frontend/activities -> activities)
    @app.route('/frontend/activities/<filename>')
    def redirect_activities(filename):
        from flask import redirect
        return redirect(f'/activities/{filename}', code=301)
    
    # Servir diretamente /frontend/js/ SEM redirect (para Service Worker registrar sem erros)
    @app.route('/frontend/js/<filename>')
    def serve_frontend_js_direct(filename):
        js_path = os.path.join(root_path, 'frontend', 'js')
        return send_from_directory(js_path, filename, mimetype='application/javascript')
    
    # Rota catch-all para assets (logos, documentos, etc)
    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        """
        Servir assets locais ou proxificar de infant.akiyama.com.br se não existir localmente
        Isso permite que assets dinamicamente carregados pela infant app funcionem normalmente
        """
        import requests as req_lib
        
        assets_path = os.path.join(root_path, 'assets')
        local_file = os.path.join(assets_path, filename)
        
        # Tentar servir do sistema de arquivos local primeiro
        if os.path.isfile(local_file):
            return send_from_directory(assets_path, filename)
        
        # Se não existe locally, proxificar de infant.akiyama.com.br
        # Isso happens quando a infant app faz lazy loading de chunks
        try:
            full_url = f'https://infant.akiyama.com.br/assets/{filename}'
            print(f'📦 [Assets Fallback Proxy] Proxificando dinamicamente: {filename} (lazy load)')
            
            response = req_lib.get(full_url, timeout=10, verify=False)
            
            headers = {}
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            headers['Content-Type'] = content_type
            
            # Cache headers para assets
            if any(ext in filename for ext in ['.js', '.css', '.woff', '.woff2', '.ttf', '.otf', '.eot', '.svg', '.png', '.jpg', '.gif']):
                headers['Cache-Control'] = 'public, max-age=31536000'
            
            return response.content, response.status_code, headers
            
        except Exception as e:
            print(f'[ERROR] Assets Fallback Proxy - Erro ao proxificar {filename}: {str(e)}')
            return f'Asset not found: {filename}', 404
    
    # ============================================================
    # PROXY PARA IFRAME INFANT
    # ============================================================
    # Servir o Infant como proxy para evitar CORS cross-origin
    # A iframe carrega de mesma origem (127.0.0.1:5001) em vez de https://infant.akiyama.com.br
    
    @app.route('/infant-proxy')
    def infant_proxy():
        """
        Proxy para a iframe https://infant.akiyama.com.br
        Reescreve URLs relativas para apontarem para proxies no Flask (mesma origem)
        Isso evita CORS pois todos os recursos vêm de 127.0.0.1:5001
        """
        import requests as req_lib
        import re
        
        try:
            response = req_lib.get('https://infant.akiyama.com.br/', timeout=10, verify=False)
            content = response.text
            
            # Reescrever URLs relativas para Flask asset proxies (mesma origem)
            # /assets/ -> /infant-proxy-assets/assets/
            # /index -> /infant-proxy-assets/index
            # /src/ -> /infant-proxy-assets/src/
            
            # Reescrever atributos src, href, data que começam com /
            # Converte para /infant-proxy-assets{original_path}
            content = re.sub(
                r'((?:src|href|data)=")(/[^"]+)(")',
                r'\1/infant-proxy-assets\2\3',
                content
            )
            
            # Reescrever URLs em <script> tags (import statements)
            content = re.sub(
                r'(from\s+[\'"])(/[^\'\"]+)([\'"])',
                r'\1/infant-proxy-assets\2\3',
                content
            )
            
            # Reescrever URLs em CSS (url())
            content = re.sub(
                r'(url\([\'"]?)(/[^)\'\"]+)([\'"]?\))',
                r'\1/infant-proxy-assets\2\3',
                content
            )
            
            # ⭐ CRÍTICO: Reescrever localhost:5000 (Device Service) para HTTPS proxy
            # http://localhost:5000 -> https://localhost:3333 (openbio-bridge em HTTPS)
            # Isso permite que a infant app acesse Device Service sem CORS/Mixed Content issues
            content = re.sub(
                r'http://localhost:5000',
                r'https://localhost:3333',
                content
            )
            content = re.sub(
                r'http://127\.0\.0\.1:5000',
                r'https://127.0.0.1:3333',
                content
            )
            
            print('[OK] Infant Proxy - HTML reescrito com URLs proxificadas via Flask')
            
            return content, response.status_code, {
                'Content-Type': 'text/html; charset=utf-8',
                'Access-Control-Allow-Origin': '*'
            }
        except Exception as e:
            import traceback
            print(f'[ERROR] Infant Proxy - Erro: {str(e)}')
            traceback.print_exc()
            return f'''
            <html>
            <head><title>Infant Proxy - Erro</title></head>
            <body>
                <h1>Erro ao carregar Infant</h1>
                <p>{str(e)}</p>
                <p>Certifique-se de que https://infant.akiyama.com.br está acessível</p>
            </body>
            </html>
            ''', 502
    
    @app.route('/infant-proxy-assets/<path:asset_path>')
    def infant_proxy_assets(asset_path):
        """
        Proxy de assets para infant.akiyama.com.br
        Serve todas as requisições de /infant-proxy-assets/* através de Flask
        Eliminando CORS pois vem da mesma origem (127.0.0.1:5001)
        
        IMPORTANTE: Reescreve URLs dentro de CSS e JS files para apontar para /infant-proxy-assets/
        """
        import requests as req_lib
        import re
        
        try:
            # Construir URL completa do recurso
            full_url = f'https://infant.akiyama.com.br/{asset_path}'
            print(f'📦 [Asset Proxy] Proxificando: {asset_path}')
            
            # Requisitar o asset do servidor original
            response = req_lib.get(full_url, timeout=10, verify=False, stream=True)
            
            # Retornar com mime type correto
            headers = {}
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            headers['Content-Type'] = content_type
            
            # Se é CSS ou JS, reescrever URLs internas também!
            content = response.text if asset_path.endswith(('.css', '.js')) else response.content
            
            if asset_path.endswith('.css'):
                # Reescrever URLs em CSS (url())
                content = re.sub(
                    r'(url\([\'"]?)(/[^)\'\"]+)([\'"]?\))',
                    r'\1/infant-proxy-assets\2\3',
                    content
                )
                # Reescrever imports em CSS (@import)
                content = re.sub(
                    r'(@import\s+[\'"]?)(/[^\'\"]*)([\'"])',
                    r'\1/infant-proxy-assets\2\3',
                    content
                )
                # Reescrever localhost:5000 para proxy HTTPS em CSS
                content = re.sub(
                    r'http://localhost:5000',
                    r'https://localhost:3333',
                    content
                )
                print(f'  [OK] URLs reescritas em CSS: {asset_path}')
            
            elif asset_path.endswith('.js'):
                # Reescrever imports em JS
                content = re.sub(
                    r'(import\s+[\'"])(/[^\'\"]+)([\'"])',
                    r'\1/infant-proxy-assets\2\3',
                    content
                )
                # Reescrever dynamic imports: import('/assets/...')
                content = re.sub(
                    r'(import\([\'"])(/[^\'\"]+)([\'\"]\))',
                    r'\1/infant-proxy-assets\2\3',
                    content
                )
                # Reescrever localhost:5000 para proxy HTTPS em JS
                content = re.sub(
                    r'http://localhost:5000',
                    r'https://localhost:3333',
                    content
                )
                print(f'  [OK] URLs reescritas em JS: {asset_path}')
            
            # Adicionar headers de cache para assets
            if any(ext in asset_path for ext in ['.js', '.css', '.woff', '.woff2', '.ttf', '.otf', '.eot', '.svg', '.png', '.jpg', '.gif']):
                headers['Cache-Control'] = 'public, max-age=31536000'  # 1 year
            
            return content, response.status_code, headers
            
        except Exception as e:
            print(f'[ERROR] Asset Proxy - Erro ao proxificar {asset_path}: {str(e)}')
            return f'Asset not found: {asset_path}', 404
    
    # ============================================================
    # Device Service Proxy - Permite que iframe acesse localhost:5000
    # sem problemas de CORS/Mixed Content
    # ============================================================
    
    @app.route('/api/device/<path:device_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
    def device_service_proxy(device_path):
        """
        Proxy para Device Service (localhost:5000 -> https://localhost:3333)
        Redireciona requisições para o openbio-bridge (HTTPS) ao invés de localhost:5000 (HTTP)
        Isso resolve o problema de Private Network Access blocking HTTPS -> HTTP loopback
        """
        from flask import request as flask_request
        import requests
        
        # ⭐ CRÍTICO: Usar HTTPS localhost:3333 (openbio-bridge) ao invés de HTTP localhost:5000
        device_url = f'https://localhost:3333/{device_path}'
        
        # Copiar query params
        if flask_request.query_string:
            device_url += f'?{flask_request.query_string.decode()}'
        
        try:
            print(f'[Device Proxy] Proxificando para openbio-bridge HTTPS: {device_url}')
            
            # Proxificar a requisição (use HTTPS, disable SSL verify for self-signed)
            response = requests.request(
                method=flask_request.method,
                url=device_url,
                headers={key: value for key, value in flask_request.headers if key != 'Host'},
                data=flask_request.get_data(),
                params=flask_request.args,
                verify=False,  # Self-signed certificate
                timeout=10
            )
            
            # Adicionar headers de CORS para permitir cross-origin
            headers = dict(response.headers)
            headers['Access-Control-Allow-Origin'] = '*'
            headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
            headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
            headers['Access-Control-Allow-Credentials'] = 'true'
            
            print(f'[Device Proxy] Status: {response.status_code}')
            return response.content, response.status_code, headers
            
        except Exception as e:
            print(f'[ERROR] Device Proxy - Erro ao proxificar {device_path}: {str(e)}')
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e), 'path': device_path}), 502
    
    # ============================================================
    # Enroll API Proxy - Proxifica requisições para api-enroll.akiyama.com.br
    # Isso permite que infant.akiyama.com.br acesse o serviço de enroll
    # ============================================================
    @app.route('/api/enroll/<path:enroll_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
    def enroll_api_proxy(enroll_path):
        """
        Proxy para api-enroll.akiyama.com.br
        Redireciona requisições da página para o serviço de enroll externo
        """
        from flask import request as flask_request
        import requests
        
        # Usar API externa
        enroll_url = f'https://api-enroll.akiyama.com.br/{enroll_path}'
        
        # Copiar query params
        if flask_request.query_string:
            enroll_url += f'?{flask_request.query_string.decode()}'
        
        try:
            print(f'[Enroll Proxy] Proxificando para api-enroll: {enroll_url}')
            
            # Copiar headers da requisição original
            headers = {key: value for key, value in flask_request.headers if key != 'Host'}
            # Adicionar header para parecer requisição legítima
            headers['User-Agent'] = 'Infant-Capture-System/1.0'
            
            response = requests.request(
                method=flask_request.method,
                url=enroll_url,
                headers=headers,
                data=flask_request.get_data(),
                params=flask_request.args,
                verify=True,
                timeout=10
            )
            
            # Adicionar headers de CORS
            response_headers = dict(response.headers)
            response_headers['Access-Control-Allow-Origin'] = '*'
            response_headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
            response_headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
            response_headers['Access-Control-Allow-Credentials'] = 'true'
            
            print(f'[Enroll Proxy] Status: {response.status_code}')
            return response.content, response.status_code, response_headers
            
        except Exception as e:
            print(f'[ERROR] Enroll Proxy - Erro ao proxificar {enroll_path}: {str(e)}')
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e), 'path': enroll_path}), 502
    
    
    # ============================================================
    # License Proxy - Simula respostas de licença válida
    # para permitir passage pela verificação Openbio
    # ============================================================
    
    @app.route('/api/license/<path:license_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    def license_proxy(license_path):
        """
        Proxy para simular verificação de licença bem-sucedida
        Intercepta requisições de license check e retorna sucesso
        """
        print(f'[License Proxy] Requisição de licença: {license_path}')
        
        # Mock response para verificação de licença
        mock_license_response = {
            'status': 'active',
            'valid': True,
            'expiresAt': '2099-12-31T23:59:59Z',
            'module': 'infant',
            'version': '1.0.0',
            'permissions': ['biometric_capture', 'record', 'export']
        }
        
        # Mock response para account/user data
        mock_account_response = {
            'id': 'account-local-123',
            'name': 'Local Test Account',
            'status': 'active',
            'license': mock_license_response,
            'permissions': ['admin', 'biometric_capture']
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
        
        return jsonify(mock_license_response), 200, headers
    


    @app.route('/plataformaid-proxy', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
    def plataformaid_proxy_base():
        """
        Proxy para plataformaid.akiyama.com.br (rota base, sem path)
        Ao invés de redirecionar para plataformaid externo, redireciona para NOSSO login
        Isso permite usar nosso próprio sistema de autenticação para o infant
        """
        from flask import redirect, request as flask_request
        
        # ⭐ CRÍTICO: Redirecionar para NOSSO sistema de autenticação
        # ao invés de plataformaid.akiyama.com.br (externo)
        full_url = f'{flask_request.scheme}://{flask_request.host}/pages/login.html'
        
        # Copiar query params - especialmente redirectUrl e origin
        if flask_request.query_string:
            full_url += f'?{flask_request.query_string.decode()}'
        
        print(f'🔄 [PlataformaID Proxy Base] Redirecionando para LOGIN LOCAL: {full_url}')
        
        # Fazer redirecionamento HTTP 302 (redirect)
        return redirect(full_url, code=302)
    
    @app.route('/plataformaid-proxy/<path:api_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
    def plataformaid_proxy(api_path):
        """
        Proxy para plataformaid.akiyama.com.br (rota com path)
        Ao invés de redirecionar para plataformaid externo, redireciona para NOSSO login
        Isso permite usar nosso próprio sistema de autenticação para o infant
        """
        from flask import redirect, request as flask_request
        
        # ⭐ CRÍTICO: Redirecionar para NOSSO sistema de autenticação
        # ao invés de plataformaid.akiyama.com.br (externo)
        full_url = f'{flask_request.scheme}://{flask_request.host}/pages/login.html'
        
        # Copiar query params - especialmente redirectUrl e origin
        if flask_request.query_string:
            full_url += f'?{flask_request.query_string.decode()}'
        
        print(f'🔄 [PlataformaID Proxy] Redirecionando para LOGIN LOCAL: {full_url}')
        
        # Fazer redirecionamento HTTP 302 (redirect)
        return redirect(full_url, code=302)
    
    # ============================================================
    # Health Check - Verificar status de todos os serviços
    # ============================================================
    
    @app.route('/health')
    def health():
        """Health check endpoint - verifica status do servidor"""
        import requests
        
        device_service_url = os.getenv('DEVICE_SERVICE_URL', 'http://localhost:5000')
        proxy_url = os.getenv('PROXY_URL', 'http://localhost:4000')
        
        # Verificar disponibilidade dos serviços
        services = {
            'flask': {'status': 'ok', 'port': os.getenv('FLASK_PORT', '5001')},
            'device_service': {'status': 'unknown', 'port': os.getenv('DEVICE_SERVICE_PORT', '5000')},
            'proxy': {'status': 'unknown', 'port': os.getenv('PROXY_PORT', '4000')},
            'websocket': {'status': 'ok', 'port': os.getenv('WEBSOCKET_PORT', '5001')}
        }
        
        # Tentar conectar ao Device Service
        try:
            response = requests.get(f'{device_service_url}/status', timeout=2)
            services['device_service']['status'] = 'ok' if response.status_code == 200 else 'error'
        except:
            services['device_service']['status'] = 'unavailable'
        
        # Tentar conectar ao Proxy
        try:
            response = requests.get(f'{proxy_url}/health', timeout=2)
            services['proxy']['status'] = 'ok' if response.status_code == 200 else 'error'
        except:
            services['proxy']['status'] = 'unavailable'
        
        return {
            'status': 'ok',
            'message': 'ETAN Platform - All Systems Check',
            'environment': os.getenv('FLASK_ENV', 'development'),
            'services': services,
            'cors_enabled': True,
            'websocket_enabled': True,
            'iframe_support': True
        }
    
    # ============================================================
    # Rota de Captura Biométrica (simulador)
    # ============================================================
    @app.route('/api/activity-attempts', methods=['POST'])
    def save_biometric_capture():
        """Salvar captura biométrica do simulador"""
        from app.models.activity import UserActivity, ActivityAttempt
        from datetime import datetime
        
        try:
            data = request.get_json()
            
            user_id = data.get('user_id', 1)
            activity_id = data.get('activity_id', 4)
            attempt_number = data.get('attempt_number', 1)
            score = data.get('score', 0)
            metrics = data.get('metrics', {})
            success = data.get('success', True)
            timestamp = data.get('timestamp', datetime.utcnow().isoformat())
            
            # Buscar ou criar atividade
            activity = UserActivity.query.filter_by(
                user_id=user_id,
                activity_id=activity_id
            ).first()
            
            if not activity:
                activity = UserActivity(
                    user_id=user_id,
                    activity_id=activity_id,
                    activity_type='biometric_capture',
                    status='ongoing'
                )
                db.session.add(activity)
                db.session.flush()
            
            # Criar tentativa
            attempt = ActivityAttempt(
                activity_id=activity.id,
                user_id=user_id,
                attempt_number=attempt_number,
                score=score,
                time_taken=0
            )
            
            # Salvar metrics como JSON
            if metrics:
                attempt.set_responses(metrics)
            
            # Marcar como sucesso
            if success:
                attempt.set_result('success')
                activity.score = max(activity.score or 0, score)
                activity.attempts = attempt_number
            
            db.session.add(attempt)
            db.session.commit()
            
            finger = metrics.get('finger', 'desconhecido')
            print(f"[OK] Captura biométrica salva: User={user_id}, Activity={activity_id}, Finger={finger}, NFIQ={score}")
            
            return jsonify({
                'success': True,
                'attempt_id': attempt.id,
                'message': 'Captura salva com sucesso',
                'data': {
                    'user_id': user_id,
                    'activity_id': activity_id,
                    'attempt_number': attempt_number,
                    'score': score,
                    'finger': finger
                }
            }), 201
        
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Erro ao salvar captura: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # Registrar WebSocket handlers
    from . import websocket_handlers
    
    # Custom error handler para 400 Bad Request
    # Previne erros do infant.akiyama.com.br
    @app.errorhandler(400)
    def handle_bad_request(e):
        print(f'[ERROR Handler] GET / retornou 400: {str(e)}')
        # Retornar JSON vazio ao invés de erro para não quebrar infant
        return jsonify({'status': 'ok', 'data': {}}), 200
    
    # Criar tabelas se não existirem - dentro do contexto
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"[WARNING] Erro ao criar tabelas: {e}")
    
    return app
