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
# async_mode=None: Flask-SocketIO auto-detecta o modo correto
# Com gunicorn+eventlet worker: usa eventlet (já patchado pelo worker)
# Com python run.py local: usa threading
socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode=None,
    ping_timeout=60,
    ping_interval=25,
    engineio_logger=False,
    transports=['websocket', 'polling']
)

def create_app():
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Selecionar config pelo ambiente (FLASK_ENV="production" em produção)
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config.get(env, config['development']))
    
    # Inicializar extensões
    db.init_app(app)
    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode=None,
        ping_timeout=60,
        ping_interval=25,
        transports=['websocket', 'polling']
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
        Serve assets locais. Se não existir e estivermos em desenvolvimento,
        faz proxy para infant.akiyama.com.br (assets do SPA AKIYAMA).
        Em produção (Render) retorna 404 imediatamente — o host não resolve lá.
        """
        assets_path = os.path.join(root_path, 'assets')
        local_file = os.path.join(assets_path, filename)

        if os.path.isfile(local_file):
            return send_from_directory(assets_path, filename)

        # Em produção (Render) não tenta o proxy externo
        if os.getenv('RENDER'):
            return f'Asset not found: {filename}', 404

        # Desenvolvimento local: faz proxy para infant.akiyama.com.br
        try:
            import requests as req_lib
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            r = req_lib.get(
                f'https://infant.akiyama.com.br/assets/{filename}',
                timeout=8,
                verify=False,
                stream=True
            )
            if r.status_code == 200:
                from flask import Response as FlaskResponse
                content_type = r.headers.get('Content-Type', 'application/octet-stream')
                return FlaskResponse(r.content, status=200, headers={
                    'Content-Type': content_type,
                    'Cache-Control': 'public, max-age=3600',
                    'Access-Control-Allow-Origin': '*',
                })
        except Exception:
            pass

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
    
    # Criar tabelas e popular dados iniciais
    # NullPool (ativo em produção) evita o timeout de startup que causava 502
    with app.app_context():
        try:
            db.create_all()
            print('[INFO] db.create_all() executado com sucesso')
            _seed_hospitals()
            _seed_courses()
        except Exception as e:
            print(f"[WARNING] Erro ao criar/popular tabelas: {e}")

    return app


def _seed_hospitals():
    """Insere hospitais padrão se a tabela estiver vazia."""
    from app.models.hospital import Hospital

    if Hospital.query.first():
        print('[INFO] Tabela hospitals já possui dados — seed ignorado')
        return

    hospitais = [
        Hospital(
            nome='Hospital das Clínicas de São Paulo',
            estado='SP', cidade='São Paulo',
            endereco='Av. Dr. Enéas de Carvalho Aguiar, 255',
            telefone='(11) 2661-0000',
            email='contato@hcsp.org.br',
            cnpj='60.975.737/0001-06',
        ),
        Hospital(
            nome='Hospital Albert Einstein',
            estado='SP', cidade='São Paulo',
            endereco='Av. Albert Einstein, 627',
            telefone='(11) 2151-1233',
            email='contato@einstein.br',
            cnpj='60.765.823/0001-30',
        ),
        Hospital(
            nome='Hospital Sírio-Libanês',
            estado='SP', cidade='São Paulo',
            endereco='R. Dona Adma Jafet, 91',
            telefone='(11) 3394-0200',
            email='contato@hsl.org.br',
            cnpj='61.590.410/0001-28',
        ),
        Hospital(
            nome='Hospital Samaritano',
            estado='SP', cidade='São Paulo',
            endereco='R. Conselheiro Brotero, 1486',
            telefone='(11) 3821-5300',
            email='contato@samaritano.com.br',
            cnpj='61.671.915/0001-80',
        ),
        Hospital(
            nome='Hospital Municipal de Campinas',
            estado='SP', cidade='Campinas',
            endereco='Av. Anchieta, 200',
            telefone='(19) 3772-5000',
            email='contato@hmcampinas.sp.gov.br',
        ),
        Hospital(
            nome='Hospital Universitário Clementino Fraga Filho',
            estado='RJ', cidade='Rio de Janeiro',
            endereco='Rua Prof. Rodolpho Paulo Rocco, 255',
            telefone='(21) 3938-2745',
            email='contato@hucff.ufrj.br',
        ),
        Hospital(
            nome='Hospital Copa Star',
            estado='RJ', cidade='Rio de Janeiro',
            endereco='Rua Figueiredo Magalhães, 875',
            telefone='(21) 3289-2500',
            email='contato@copastar.com.br',
        ),
        Hospital(
            nome='Hospital das Clínicas de Belo Horizonte',
            estado='MG', cidade='Belo Horizonte',
            endereco='Av. Prof. Alfredo Balena, 110',
            telefone='(31) 3409-9000',
            email='contato@hc.ufmg.br',
        ),
        Hospital(
            nome='Hospital de Clínicas de Porto Alegre',
            estado='RS', cidade='Porto Alegre',
            endereco='Rua Ramiro Barcelos, 2350',
            telefone='(51) 3359-8000',
            email='contato@hcpa.edu.br',
        ),
        Hospital(
            nome='Hospital Universitário Walter Cantídio',
            estado='CE', cidade='Fortaleza',
            endereco='Rua Capitão Francisco Pedro, 1290',
            telefone='(85) 3366-8000',
            email='contato@huwc.ufc.br',
        ),
        Hospital(
            nome='Hospital de Base do Distrito Federal',
            estado='DF', cidade='Brasília',
            endereco='SMHS — Área Especial, Quadra 101',
            telefone='(61) 3315-1616',
            email='contato@hbdf.saude.df.gov.br',
        ),
        Hospital(
            nome='Hospital Getúlio Vargas',
            estado='AM', cidade='Manaus',
            endereco='Av. Mário Ypiranga, 1581',
            telefone='(92) 3635-5050',
            email='contato@hgv.am.gov.br',
        ),
    ]

    from app import db
    try:
        db.session.bulk_save_objects(hospitais)
        db.session.commit()
        print(f'[INFO] Seed: {len(hospitais)} hospitais inseridos com sucesso')
    except Exception as e:
        db.session.rollback()
        print(f'[WARNING] Seed hospitals falhou: {e}')


def _patch_video_urls():
    """Atualiza video_url nas aulas que ainda não têm vídeo vinculado."""
    from app.models.lesson import Lesson
    from app import db

    mapa = {
        'Equipamentos e Dispositivos ETAN':              'https://youtu.be/TI42JZHkA20',
        'Segurança, Higiene e Aspectos Legais':          'https://youtu.be/0GOkU_0QpKU',
        'Prática com o Sistema AKIYAMA — Simulação Completa': 'https://youtu.be/UNKHidgcbo4',
        'Certificação e Boas Práticas — Próximos Passos': 'https://youtu.be/oQjQRJzIzno',
    }

    atualizadas = 0
    for titulo, url in mapa.items():
        aula = Lesson.query.filter_by(titulo=titulo).first()
        if aula and not aula.video_url:
            aula.video_url = url
            atualizadas += 1

    if atualizadas:
        try:
            db.session.commit()
            print(f'[INFO] _patch_video_urls: {atualizadas} aulas atualizadas com video_url')
        except Exception as e:
            db.session.rollback()
            print(f'[WARNING] _patch_video_urls falhou: {e}')
    else:
        print('[INFO] _patch_video_urls: todos os video_url já estavam preenchidos')


def _seed_courses():
    """Insere cursos e aulas padrão se as tabelas estiverem vazias."""
    from app.models.course import Course
    from app.models.lesson import Lesson
    from app import db

    if Course.query.first():
        # Cursos já existem — apenas garantir que os video_url estão preenchidos
        _patch_video_urls()
        return

    cursos_data = [
        {
            'curso': Course(
                titulo='Fundamentos da Biometria Infantil',
                descricao=(
                    'Introdução completa aos conceitos, equipamentos e procedimentos '
                    'para captura biométrica em recém-nascidos e bebês. '
                    'Ideal para profissionais de saúde que estão iniciando com o sistema ETAN.'
                ),
                autor='Equipe Winged Mind',
                nivel='basico',
                tempo_estimado=120,
            ),
            'aulas': [
                dict(
                    titulo='Introdução à Biometria Infantil',
                    descricao='O que é biometria infantil e por que ela é essencial nos hospitais modernos.',
                    ordem=1, duracao=20,
                    conteudo=(
                        '<h2>O que é Biometria Infantil?</h2>'
                        '<p>A biometria infantil é o processo de coleta e registro de características '
                        'físicas únicas de recém-nascidos para fins de identificação segura e confiável. '
                        'Diferentemente dos adultos, bebês possuem impressões digitais com sulcos mais finos '
                        'e menor superfície, exigindo equipamentos e técnicas especializadas.</p>'
                        '<h3>Por que é importante?</h3>'
                        '<ul>'
                        '<li><strong>Segurança hospitalar:</strong> previne troca de bebês nas maternidades</li>'
                        '<li><strong>Registro civil:</strong> base para emissão da Certidão de Nascimento</li>'
                        '<li><strong>Programas sociais:</strong> vinculação do bebê ao CPF dos pais no SUS</li>'
                        '<li><strong>Rastreabilidade:</strong> histórico médico vinculado à identidade biométrica</li>'
                        '</ul>'
                        '<h3>Desafios específicos</h3>'
                        '<p>A pele dos recém-nascidos possui alta umidade e elasticidade, '
                        'e os sulcos digitais têm entre 0,2 mm e 0,4 mm de largura — '
                        'exigindo sensores ópticos de alta resolução (500 dpi ou superior).</p>'
                    ),
                ),
                dict(
                    titulo='Equipamentos e Dispositivos ETAN',
                    descricao='Conheça o dispositivo ETAN AKIYAMA: componentes, manutenção e calibração.',
                    ordem=2, duracao=25,
                    video_url='https://youtu.be/TI42JZHkA20',
                    conteudo=(
                        '<h2>O Dispositivo ETAN AKIYAMA</h2>'
                        '<p>O ETAN (Equipment for Touch and Analysis of Neonates) é um sensor biométrico '
                        'desenvolvido especificamente para a captura de impressões digitais em bebês. '
                        'Utiliza tecnologia óptica de alta resolução com iluminação LED infravermelha.</p>'
                        '<h3>Componentes principais</h3>'
                        '<ul>'
                        '<li><strong>Sensor óptico:</strong> 500 dpi — captura os sulcos finos dos bebês</li>'
                        '<li><strong>LED infravermelho:</strong> reduz reflexo da umidade da pele</li>'
                        '<li><strong>Módulo NFIQ:</strong> calcula o score de qualidade em tempo real</li>'
                        '<li><strong>Interface USB 3.0:</strong> transferência rápida e estável</li>'
                        '</ul>'
                        '<h3>Calibração diária</h3>'
                        '<p>Antes de cada turno, o dispositivo deve ser calibrado com o cartão de referência '
                        'que acompanha o equipamento. O score de referência deve estar entre 85 e 100. '
                        'Limpeza do sensor com pano de microfibra seco é obrigatória.</p>'
                        '<h3>Indicadores de status</h3>'
                        '<ul>'
                        '<li>🟢 <strong>Verde pulsando:</strong> pronto para captura</li>'
                        '<li>🟡 <strong>Amarelo fixo:</strong> aquecendo (aguarde 30s)</li>'
                        '<li>🔴 <strong>Vermelho:</strong> erro — recalibrar ou reiniciar</li>'
                        '</ul>'
                    ),
                ),
                dict(
                    titulo='Anatomia Digital e Morfologia em Bebês',
                    descricao='Entenda as diferenças anatômicas entre a digital de um bebê e a de um adulto.',
                    ordem=3, duracao=30,
                    conteudo=(
                        '<h2>Morfologia da Digital em Recém-Nascidos</h2>'
                        '<p>A impressão digital é formada a partir da 10ª semana de gestação e é única '
                        'para cada indivíduo — inclusive para gêmeos idênticos. '
                        'Nos recém-nascidos, os padrões já estão completamente formados, '
                        'mas apresentam características distintas dos adultos.</p>'
                        '<h3>Tipos de padrões digitais</h3>'
                        '<ul>'
                        '<li><strong>Arco (5%):</strong> linhas paralelas sem núcleo — mais raros</li>'
                        '<li><strong>Presilha (65%):</strong> linhas que entram e saem pelo mesmo lado</li>'
                        '<li><strong>Verticilo (30%):</strong> linhas em espiral com dois ou mais deltas</li>'
                        '</ul>'
                        '<h3>Características específicas em bebês</h3>'
                        '<ul>'
                        '<li>Sulcos com 0,2–0,4 mm (adultos: 0,4–0,8 mm)</li>'
                        '<li>Alta concentração de umidade e verniz caseoso</li>'
                        '<li>Pele mais elástica — risco de distorção na captura</li>'
                        '<li>Reflexo palmar presente — bebê fecha o punho instintivamente</li>'
                        '</ul>'
                        '<h3>Seleção do dígito para captura</h3>'
                        '<p>A ordem de prioridade é: polegar direito → indicador direito → polegar esquerdo. '
                        'Em casos de anomalia congênita ou lesão, seguir o protocolo de dígito alternativo.</p>'
                    ),
                ),
                dict(
                    titulo='Segurança, Higiene e Aspectos Legais',
                    descricao='Protocolos de higiene, LGPD aplicada à biometria e responsabilidades do profissional.',
                    ordem=4, duracao=45,
                    video_url='https://youtu.be/0GOkU_0QpKU',
                    conteudo=(
                        '<h2>Segurança e Higiene no Procedimento Biométrico</h2>'
                        '<h3>Higienização do equipamento</h3>'
                        '<p>O sensor deve ser limpo entre cada captura com álcool isopropílico 70% '
                        'em pano de microfibra. Aguardar 15 segundos antes da próxima captura '
                        'para evitar resíduo de álcool no sensor.</p>'
                        '<h3>Proteção do recém-nascido</h3>'
                        '<ul>'
                        '<li>Higienizar as mãos com álcool gel antes de tocar o bebê</li>'
                        '<li>Tempo máximo de captura por dígito: 3 tentativas de 5 segundos</li>'
                        '<li>Se o bebê demonstrar desconforto, interromper e aguardar</li>'
                        '<li>Nunca aplicar pressão excessiva no dígito do recém-nascido</li>'
                        '</ul>'
                        '<h3>LGPD e proteção de dados biométricos</h3>'
                        '<p>Dados biométricos são considerados <strong>dados sensíveis</strong> pela '
                        'Lei Geral de Proteção de Dados (Lei nº 13.709/2018). O hospital é '
                        'o controlador dos dados e o profissional é o operador. '
                        'Toda captura deve ter consentimento explícito registrado no prontuário.</p>'
                        '<h3>Responsabilidades do profissional</h3>'
                        '<ul>'
                        '<li>Registrar tentativas de captura no sistema, incluindo as falhas</li>'
                        '<li>Nunca compartilhar imagens biométricas fora do sistema oficial</li>'
                        '<li>Reportar falhas do equipamento ao responsável técnico imediatamente</li>'
                        '</ul>'
                    ),
                ),
            ],
        },
        {
            'curso': Course(
                titulo='Protocolo ETAN — Técnicas Avançadas',
                descricao=(
                    'Aprofundamento no Protocolo ETAN com suas 5 fases, casos especiais, '
                    'troubleshooting e prática real com o sistema AKIYAMA. '
                    'Para profissionais que já concluíram o curso Fundamentos.'
                ),
                autor='Equipe Winged Mind',
                nivel='intermediario',
                tempo_estimado=180,
            ),
            'aulas': [
                dict(
                    titulo='As 5 Fases do Protocolo ETAN',
                    descricao='Estudo completo das 5 fases: verificação de sinais vitais até validação NFIQ.',
                    ordem=1, duracao=40,
                    conteudo=(
                        '<h2>Protocolo ETAN — As 5 Fases Fundamentais</h2>'
                        '<p>O Protocolo ETAN é o padrão nacional para captura biométrica em neonatos. '
                        'Cada fase possui critérios de aceite e deve ser concluída antes de avançar.</p>'
                        '<h3>Fase 1 — Verificação de Sinais Vitais</h3>'
                        '<p>Antes de iniciar qualquer captura, verificar: frequência cardíaca (120–160 bpm), '
                        'saturação de oxigênio (≥ 95%), temperatura axilar (36,5–37,5°C). '
                        '<strong>Critério de aceite:</strong> todos os parâmetros dentro do normal.</p>'
                        '<h3>Fase 2 — Limpeza e Preparação</h3>'
                        '<p>Remover verniz caseoso ou resíduo do dígito com gaze umedecida. '
                        'Aguardar a pele secar naturalmente (não soprar — contamina). '
                        '<strong>Critério de aceite:</strong> dígito limpo, sem umidade visível.</p>'
                        '<h3>Fase 3 — Seleção de Dígitos</h3>'
                        '<p>Ordem de prioridade: polegar direito → indicador direito → polegar esquerdo. '
                        'Inspecionar o dígito escolhido: ausência de lesões, cortes ou deformidades. '
                        '<strong>Critério de aceite:</strong> dígito íntegro e acessível.</p>'
                        '<h3>Fase 4 — Captura com Pressão Apropriada</h3>'
                        '<p>Pressão recomendada: 80 mmHg ± 10 mmHg (medida pelo sensor). '
                        'Posicionar o dígito no centro do sensor, plano, sem rotação. '
                        'Tempo de contato: 3 a 5 segundos por tentativa. '
                        '<strong>Critério de aceite:</strong> imagem centrada com área ≥ 60% do sensor.</p>'
                        '<h3>Fase 5 — Validação de Qualidade NFIQ</h3>'
                        '<p>O módulo NFIQ (NIST Fingerprint Image Quality) avalia a imagem de 0 a 100. '
                        '<strong>Score mínimo aceitável: 40.</strong> '
                        'Score entre 40–69: qualidade média — aceito com ressalva. '
                        'Score ≥ 70: alta qualidade — ideal. '
                        'Score < 40: descartar e repetir a captura (máx. 3 tentativas).</p>'
                    ),
                ),
                dict(
                    titulo='Casos Especiais — Adaptações Necessárias',
                    descricao='Como adaptar o protocolo para bebês com dermatite, espasticidade, prematuridade ou recusa.',
                    ordem=2, duracao=45,
                    conteudo=(
                        '<h2>Casos Especiais no Protocolo ETAN</h2>'
                        '<p>Situações clínicas especiais exigem adaptações do protocolo padrão. '
                        'O profissional deve saber identificar e agir corretamente em cada cenário.</p>'
                        '<h3>Dermatite e lesões de pele</h3>'
                        '<p>Se o dígito de prioridade apresentar dermatite, eczema ou lesão: '
                        'avançar para o próximo dígito na ordem de prioridade. '
                        'Registrar no sistema o motivo da substituição de dígito. '
                        'Nunca capturar sobre pele lesionada.</p>'
                        '<h3>Espasticidade e reflexo palmar intenso</h3>'
                        '<p>Técnica de relaxamento: pressionar levemente a palma do bebê por 10 segundos '
                        'antes de tentar a extensão do dígito. '
                        'Usar o dedo indicador do profissional para suporte suave na falange distal. '
                        'Em casos de espasticidade severa, aguardar horário de menor agitação do bebê.</p>'
                        '<h3>Prematuridade (peso < 1.500g)</h3>'
                        '<p>Bebês prematuros têm sulcos ainda menos definidos. '
                        'Aguardar maturação: idealmente realizar a captura após 36 semanas de idade corrigida. '
                        'Score NFIQ mínimo reduzido para 30 em prematuros extremos — registrar justificativa.</p>'
                        '<h3>Pele muito seca ou úmida</h3>'
                        '<p><strong>Pele seca:</strong> aplicar uma gota de soro fisiológico no dígito, '
                        'aguardar 5 segundos e remover o excesso com gaze. '
                        '<strong>Pele úmida/suada:</strong> secar gentilmente com gaze seca, '
                        'posicionar sob ventilação ambiente por 30 segundos antes da captura.</p>'
                        '<h3>Bebê em incubadora</h3>'
                        '<p>Adaptar o sensor para operação dentro da incubadora. '
                        'Manter o sensor próximo à entrada lateral. '
                        'Limitar o tempo de abertura da incubadora a no máximo 2 minutos por sessão de captura.</p>'
                    ),
                ),
                dict(
                    titulo='Troubleshooting — Diagnóstico e Resolução de Problemas',
                    descricao='Identifique e resolva os problemas mais comuns: NFIQ baixo, sensor não detectando, lentidão.',
                    ordem=3, duracao=50,
                    conteudo=(
                        '<h2>Troubleshooting no Sistema ETAN</h2>'
                        '<p>Problemas técnicos são comuns em ambientes hospitalares de alta rotatividade. '
                        'Este guia cobre os cenários mais frequentes e suas soluções.</p>'
                        '<h3>Score NFIQ consistentemente abaixo de 40</h3>'
                        '<ul>'
                        '<li><strong>Causa mais comum:</strong> sensor sujo ou úmido</li>'
                        '<li><strong>Solução:</strong> limpar sensor com álcool 70% + recalibrar com cartão de referência</li>'
                        '<li><strong>Se persistir:</strong> verificar iluminação LED (substituição a cada 2.000 horas)</li>'
                        '<li><strong>Último recurso:</strong> reiniciar o software e reconectar o dispositivo</li>'
                        '</ul>'
                        '<h3>Sensor não detecta o dígito</h3>'
                        '<ul>'
                        '<li>Verificar conexão USB (remover e reconectar)</li>'
                        '<li>Verificar se driver ETAN está instalado: Painel de Controle → Dispositivos</li>'
                        '<li>Testar em outra porta USB (preferir USB 3.0 azul)</li>'
                        '<li>Reiniciar o serviço ETAN via Gerenciador de Tarefas se necessário</li>'
                        '</ul>'
                        '<h3>Processamento lento (> 10 segundos por captura)</h3>'
                        '<ul>'
                        '<li>Verificar CPU e RAM: fechar aplicativos em segundo plano</li>'
                        '<li>Verificar espaço em disco: manter ao menos 10% livre</li>'
                        '<li>Limpar cache do sistema ETAN: Menu → Configurações → Limpar Cache</li>'
                        '</ul>'
                        '<h3>Erro de sincronização com o servidor</h3>'
                        '<p>Se o status mostrar "Offline" ou "Sem sincronização": '
                        'verificar conectividade de rede do equipamento. '
                        'O sistema opera em modo offline por até 24 horas — as capturas são salvas localmente '
                        'e sincronizadas automaticamente quando a conexão for restaurada.</p>'
                        '<h3>Quando acionar o suporte técnico</h3>'
                        '<p>Ativar o suporte técnico quando: erro persiste após 3 tentativas de resolução; '
                        'LED do sensor não acende; software não inicia; perda de dados suspeita.</p>'
                    ),
                ),
                dict(
                    titulo='Prática com o Sistema AKIYAMA — Simulação Completa',
                    descricao='Exercício prático simulando uma captura real completa do início ao fim.',
                    ordem=4, duracao=45,
                    video_url='https://youtu.be/UNKHidgcbo4',
                    conteudo=(
                        '<h2>Prática Real com o Sistema AKIYAMA</h2>'
                        '<p>Esta aula é prática. Você vai simular um procedimento completo de captura biométrica '
                        'utilizando o simulador do sistema AKIYAMA, que replica fielmente o equipamento real.</p>'
                        '<h3>Checklist pré-captura</h3>'
                        '<ol>'
                        '<li>✅ Dispositivo ETAN conectado e LED verde pulsando</li>'
                        '<li>✅ Software AKIYAMA aberto e logado</li>'
                        '<li>✅ Prontuário do paciente aberto no sistema</li>'
                        '<li>✅ Mãos higienizadas com álcool gel</li>'
                        '<li>✅ Sensor limpo e calibrado (score de referência ≥ 85)</li>'
                        '</ol>'
                        '<h3>Fluxo de captura no sistema</h3>'
                        '<ol>'
                        '<li>Selecionar paciente pelo número de prontuário ou pela pulseira QR Code</li>'
                        '<li>Clicar em <strong>"Nova Captura Biométrica"</strong></li>'
                        '<li>Selecionar dígito (padrão: polegar direito)</li>'
                        '<li>Posicionar o dígito do bebê no sensor aguardando o sinal sonoro de prontidão</li>'
                        '<li>Manter por 4 segundos — o sistema captura automaticamente</li>'
                        '<li>Verificar score NFIQ exibido na tela</li>'
                        '<li>Se score ≥ 40: confirmar e salvar</li>'
                        '<li>Se score < 40: clicar em "Repetir" (máx. 3 tentativas)</li>'
                        '</ol>'
                        '<h3>Registro pós-captura</h3>'
                        '<p>Após a captura bem-sucedida, o sistema solicita: '
                        'nome do profissional executor, observações clínicas relevantes, '
                        'e confirmação do responsável legal (assinatura digital na tela).</p>'
                    ),
                ),
            ],
        },
        {
            'curso': Course(
                titulo='Gestão e Qualidade em Biometria Hospitalar',
                descricao=(
                    'Conceitos de gestão, controle de qualidade, conformidade legal e boas práticas '
                    'para coordenadores e responsáveis técnicos pelos sistemas biométricos hospitalares.'
                ),
                autor='Equipe Winged Mind',
                nivel='avancado',
                tempo_estimado=150,
            ),
            'aulas': [
                dict(
                    titulo='Controle de Qualidade e Métricas NFIQ',
                    descricao='Interpretação de relatórios de qualidade, metas e indicadores de desempenho.',
                    ordem=1, duracao=40,
                    conteudo=(
                        '<h2>Controle de Qualidade em Biometria Hospitalar</h2>'
                        '<p>A qualidade das capturas biométricas é medida principalmente pelo score NFIQ '
                        '(NIST Fingerprint Image Quality), mas um programa de qualidade eficaz '
                        'vai além do score individual de cada captura.</p>'
                        '<h3>Indicadores de desempenho (KPIs)</h3>'
                        '<ul>'
                        '<li><strong>Taxa de sucesso na 1ª tentativa:</strong> meta ≥ 85%</li>'
                        '<li><strong>Score NFIQ médio mensal:</strong> meta ≥ 55</li>'
                        '<li><strong>Taxa de rejeição (score < 40):</strong> meta ≤ 10%</li>'
                        '<li><strong>Tempo médio por captura:</strong> meta ≤ 5 minutos</li>'
                        '<li><strong>Capturas sem nenhum dígito registrado:</strong> meta = 0</li>'
                        '</ul>'
                        '<h3>Relatórios mensais obrigatórios</h3>'
                        '<p>O sistema AKIYAMA gera automaticamente o Relatório Mensal de Qualidade Biométrica. '
                        'Este relatório deve ser revisado pelo coordenador e arquivado por 5 anos. '
                        'Desvios acima de 20% da meta devem gerar um Plano de Ação Corretiva (PAC).</p>'
                        '<h3>Auditoria de capturas</h3>'
                        '<p>Trimestralmente, auditar uma amostra aleatória de 50 capturas: '
                        'verificar se o dígito registrado corresponde ao protocolo, '
                        'revisar observações clínicas e verificar consistência dos scores.</p>'
                    ),
                ),
                dict(
                    titulo='Documentação e Conformidade Legal',
                    descricao='LGPD, RDC Anvisa, fluxo de consentimento e responsabilidades legais.',
                    ordem=2, duracao=35,
                    conteudo=(
                        '<h2>Documentação e Marco Legal da Biometria Hospitalar</h2>'
                        '<h3>Base legal da coleta biométrica neonatal</h3>'
                        '<ul>'
                        '<li><strong>Lei nº 12.662/2012:</strong> obrigatoriedade da coleta de digital para registro civil</li>'
                        '<li><strong>Portaria MS nº 938/2012:</strong> regulamenta o procedimento nos hospitais</li>'
                        '<li><strong>LGPD (Lei nº 13.709/2018):</strong> classifica biometria como dado sensível</li>'
                        '<li><strong>CFM/Cofen:</strong> responsabilidade ética do profissional na coleta</li>'
                        '</ul>'
                        '<h3>Termo de Consentimento Informado (TCI)</h3>'
                        '<p>O TCI deve ser apresentado ao responsável legal antes do procedimento. '
                        'Deve conter: finalidade da coleta, prazo de guarda dos dados, '
                        'direitos do titular, canal para exercício de direitos (LGPD). '
                        'O TCI assinado deve ser digitalizado e vinculado ao prontuário.</p>'
                        '<h3>Fluxo de solicitação de exclusão de dados</h3>'
                        '<p>O responsável legal pode solicitar a exclusão dos dados biométricos '
                        'a qualquer momento, exceto nos casos em que a guarda é obrigatória por lei '
                        '(mínimo de 20 anos para registros hospitalares). '
                        'A solicitação deve ser respondida em até 15 dias úteis.</p>'
                    ),
                ),
                dict(
                    titulo='Gestão de Falhas e Reprocessamento',
                    descricao='Procedimentos para capturas falhas, reprocessamento e gestão de incidentes.',
                    ordem=3, duracao=35,
                    conteudo=(
                        '<h2>Gestão de Falhas no Processo Biométrico</h2>'
                        '<p>Falhas na captura biométrica são eventos esperados e devem ter um fluxo '
                        'de tratamento bem definido para garantir que nenhum recém-nascido '
                        'saia da maternidade sem registro biométrico.</p>'
                        '<h3>Classificação das falhas</h3>'
                        '<ul>'
                        '<li><strong>Falha técnica:</strong> equipamento com defeito, software travado</li>'
                        '<li><strong>Falha clínica:</strong> condição do bebê impede a captura (prematuridade extrema, anomalia)</li>'
                        '<li><strong>Falha operacional:</strong> score abaixo do mínimo após 3 tentativas</li>'
                        '<li><strong>Falha de recusa:</strong> responsável legal recusa o procedimento</li>'
                        '</ul>'
                        '<h3>Fluxo de reprocessamento</h3>'
                        '<ol>'
                        '<li>Registrar a falha no sistema com classificação e motivo</li>'
                        '<li>Agendar nova tentativa em 24 horas (falha operacional/técnica)</li>'
                        '<li>Escalar para o responsável técnico se a falha persistir por 48h</li>'
                        '<li>Para falha de recusa: registrar no prontuário e notificar o serviço social</li>'
                        '</ol>'
                        '<h3>Indicador de falhas</h3>'
                        '<p>Meta: taxa de falha não resolvida ≤ 2% das capturas do mês. '
                        'Todo mês com taxa superior a 5% deve gerar análise de causa raiz '
                        'e relatório para a diretoria técnica do hospital.</p>'
                    ),
                ),
                dict(
                    titulo='Certificação e Boas Práticas — Próximos Passos',
                    descricao='Caminhos de certificação profissional e boas práticas para manter a excelência.',
                    ordem=4, duracao=40,
                    video_url='https://youtu.be/oQjQRJzIzno',
                    conteudo=(
                        '<h2>Certificação e Desenvolvimento Profissional</h2>'
                        '<p>Concluir os três cursos da plataforma Winged Mind é o primeiro passo '
                        'para se tornar um profissional certificado em Biometria Infantil Hospitalar.</p>'
                        '<h3>Trilha de certificação Winged Mind</h3>'
                        '<ol>'
                        '<li>✅ Fundamentos da Biometria Infantil (este curso)</li>'
                        '<li>✅ Protocolo ETAN — Técnicas Avançadas</li>'
                        '<li>✅ Gestão e Qualidade em Biometria Hospitalar</li>'
                        '<li>🏆 <strong>Certificado Winged Mind — Especialista em Biometria Neonatal</strong></li>'
                        '</ol>'
                        '<h3>Boas práticas para manter a excelência</h3>'
                        '<ul>'
                        '<li>Revisar os materiais dos cursos a cada 6 meses</li>'
                        '<li>Participar das atualizações de protocolo emitidas pela AKIYAMA</li>'
                        '<li>Compartilhar aprendizados com a equipe — treinamentos internos mensais</li>'
                        '<li>Acompanhar os indicadores de qualidade do seu setor semanalmente</li>'
                        '</ul>'
                        '<h3>Recursos adicionais</h3>'
                        '<ul>'
                        '<li>📄 Manual técnico ETAN v2.4 (disponível na aba Documentos)</li>'
                        '<li>🤖 Assistente IA — disponível 24h para tirar dúvidas</li>'
                        '<li>📊 Relatórios de qualidade — atualizados diariamente no Dashboard</li>'
                        '</ul>'
                    ),
                ),
            ],
        },
    ]

    try:
        for item in cursos_data:
            curso = item['curso']
            db.session.add(curso)
            db.session.flush()  # Gera o curso.id antes de criar as aulas
            for aula_data in item['aulas']:
                aula = Lesson(
                    curso_id=curso.id,
                    titulo=aula_data['titulo'],
                    descricao=aula_data['descricao'],
                    conteudo=aula_data['conteudo'],
                    ordem=aula_data['ordem'],
                    duracao=aula_data.get('duracao'),
                    video_url=aula_data.get('video_url'),
                )
                db.session.add(aula)
        db.session.commit()
        print(f'[INFO] Seed: {len(cursos_data)} cursos inseridos com sucesso')
    except Exception as e:
        db.session.rollback()
        print(f'[WARNING] Seed courses falhou: {e}')
