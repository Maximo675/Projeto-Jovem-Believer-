from flask import Blueprint, jsonify, request, redirect, url_for, session
from app import db
from app.models.user import User
from app.models.hospital import Hospital
from app.models.invitation import Invitation
from datetime import datetime, timedelta
import jwt
import os
import msal

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# ─── Configurações Microsoft ──────────────────────────────────────────────────
_MS_CLIENT_ID     = os.getenv('MICROSOFT_CLIENT_ID', '')
_MS_CLIENT_SECRET = os.getenv('MICROSOFT_CLIENT_SECRET', '')
_MS_TENANT_ID     = os.getenv('MICROSOFT_TENANT_ID', 'common')
_MS_AUTHORITY     = f'https://login.microsoftonline.com/{_MS_TENANT_ID}'
_MS_SCOPES        = ['User.Read']

def _ms_app():
    return msal.ConfidentialClientApplication(
        _MS_CLIENT_ID,
        authority=_MS_AUTHORITY,
        client_credential=_MS_CLIENT_SECRET,
    )

def _ms_redirect_uri():
    base = os.getenv('APP_BASE_URL', 'http://localhost:5001')
    return f'{base}/api/auth/microsoft/callback'

# ─── Helper JWT ───────────────────────────────────────────────────────────────
_JWT_SECRET  = os.getenv('JWT_SECRET', 'secret')
_JWT_EXPIRY  = int(os.getenv('JWT_EXPIRY_HOURS', 8))   # padrão: 1 turno

def _gerar_token(usuario):
    payload = {
        'usuario_id': usuario.id,
        'email': usuario.email,
        'funcao': usuario.funcao,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=_JWT_EXPIRY),
    }
    return jwt.encode(payload, _JWT_SECRET, algorithm='HS256')


# ─── Rotas Microsoft OAuth ────────────────────────────────────────────────────

@bp.route('/microsoft/login', methods=['GET'])
def microsoft_login():
    """Inicia o fluxo OAuth com Microsoft. Redireciona para a tela de login MS."""
    if not _MS_CLIENT_ID:
        return jsonify({'erro': 'Login Microsoft não configurado neste ambiente.'}), 503
    app = _ms_app()
    auth_url = app.get_authorization_request_url(
        scopes=_MS_SCOPES,
        redirect_uri=_ms_redirect_uri(),
        prompt='select_account',
    )
    return redirect(auth_url)


@bp.route('/microsoft/callback', methods=['GET'])
def microsoft_callback():
    """Callback OAuth — troca code por token, cria/recupera usuário, emite JWT."""
    code  = request.args.get('code')
    error = request.args.get('error')

    # URL base do frontend (onde redirecionar após autenticação)
    frontend_base = os.getenv('APP_BASE_URL', 'http://localhost:5001')
    login_page    = f'{frontend_base}/pages/login.html'
    dash_page     = f'{frontend_base}/pages/dashboard.html'

    if error or not code:
        desc = request.args.get('error_description', error or 'Acesso negado')
        return redirect(f'{login_page}?ms_error={desc}')

    try:
        app = _ms_app()
        result = app.acquire_token_by_authorization_code(
            code,
            scopes=_MS_SCOPES,
            redirect_uri=_ms_redirect_uri(),
        )
    except Exception as e:
        return redirect(f'{login_page}?ms_error=Falha+na+troca+de+token')

    if 'error' in result:
        return redirect(f'{login_page}?ms_error={result.get("error_description","Erro")}')

    claims = result.get('id_token_claims', {})
    email  = claims.get('preferred_username') or claims.get('email') or claims.get('upn', '')
    nome   = claims.get('name', email.split('@')[0] if email else 'Usuário')

    if not email:
        return redirect(f'{login_page}?ms_error=Email+nao+retornado+pela+Microsoft')

    email = email.strip().lower()

    # ── 1. Usuário já existe → login direto ──────────────────────────────────
    usuario = User.query.filter_by(email=email).first()
    if usuario:
        if not usuario.ativo:
            return redirect(f'{login_page}?ms_error=Conta+desativada')
        token = _gerar_token(usuario)
        return redirect(f'{dash_page}?auth_token={token}')

    # ── 2. Verificar convite pendente para este email ─────────────────────────
    convite = (Invitation.query
               .filter_by(email=email, usado=False)
               .filter(Invitation.expires_at > datetime.utcnow())
               .order_by(Invitation.data_criacao.desc())
               .first())

    hospital_id = None
    funcao      = 'usuario'

    if convite:
        hospital_id = convite.hospital_id
        funcao      = convite.funcao
    else:
        # ── 3. Sem convite — verificar domínio do hospital ───────────────────
        dominio = email.split('@')[-1] if '@' in email else ''
        if dominio:
            hospital = Hospital.query.filter_by(
                dominio_email=dominio, ativo=True
            ).first()
            if hospital:
                hospital_id = hospital.id

    # ── 4. Nenhuma forma de associar hospital → negar acesso ─────────────────
    if not hospital_id:
        return redirect(
            f'{login_page}?ms_error=Sem+convite+valido.+Solicite+ao+administrador+do+seu+hospital.'
        )

    # ── 5. Criar conta ────────────────────────────────────────────────────────
    try:
        usuario = User(
            email=email,
            nome=nome,
            senha='',
            hospital_id=hospital_id,
            funcao=funcao,
            ativo=True,
        )
        if hasattr(usuario, 'set_password'):
            usuario.set_password(os.urandom(32).hex())
        db.session.add(usuario)

        if convite:
            convite.usado = True

        db.session.commit()
    except Exception:
        db.session.rollback()
        return redirect(f'{login_page}?ms_error=Erro+ao+criar+usuario')

    token = _gerar_token(usuario)
    return redirect(f'{dash_page}?auth_token={token}')


# ─── Rotas existentes (adaptadas para usar helper) ────────────────────────────

@bp.route('/register', methods=['POST'])
def register():
    """Registrar novo usuário"""
    try:
        data = request.get_json()

        required_fields = ['email', 'nome', 'senha', 'hospital_id']
        if not all(field in data for field in required_fields):
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'Email já cadastrado'}), 400

        usuario = User(
            email=data['email'],
            nome=data['nome'],
            senha=data['senha'],
            hospital_id=data.get('hospital_id'),
            funcao='usuario',
        )
        usuario.set_password(data['senha'])

        db.session.add(usuario)
        db.session.commit()

        return jsonify({
            'mensagem': 'Usuário registrado com sucesso',
            'usuario': usuario.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """Fazer login com email + senha"""
    try:
        data = request.get_json()
        if not data or not data.get('email') or not data.get('senha'):
            return jsonify({'erro': 'Email e senha são obrigatórios'}), 400

        usuario = User.query.filter_by(email=data.get('email')).first()
        if not usuario or not usuario.check_password(data.get('senha')):
            return jsonify({'erro': 'Email ou senha inválidos'}), 401

        if not usuario.ativo:
            return jsonify({'erro': 'Usuário desativado'}), 403

        token = _gerar_token(usuario)

        return jsonify({
            'mensagem': 'Login realizado com sucesso',
            'token': token,
            'expira_em_horas': _JWT_EXPIRY,
            'usuario': usuario.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/logout', methods=['POST'])
def logout():
    """Logout (client-side, apenas para confirmação)"""
    return jsonify({'mensagem': 'Logout realizado com sucesso'}), 200

