from flask import Blueprint, jsonify, request, redirect, url_for, session
from app import db
from app.models.user import User
from app.models.hospital import Hospital
from app.models.invitation import Invitation
from datetime import datetime, timedelta
import jwt
import os

try:
    import msal
    _MSAL_AVAILABLE = True
except ImportError:
    _MSAL_AVAILABLE = False

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# ─── Configurações Microsoft ──────────────────────────────────────────────────
_MS_CLIENT_ID     = os.getenv('MICROSOFT_CLIENT_ID', '').strip()
_MS_CLIENT_SECRET = os.getenv('MICROSOFT_CLIENT_SECRET', '').strip()
_MS_TENANT_ID     = os.getenv('MICROSOFT_TENANT_ID', 'common').strip()
_MS_AUTHORITY     = f'https://login.microsoftonline.com/{_MS_TENANT_ID}'
_MS_SCOPES        = ['User.Read']

def _ms_configurado():
    """Retorna True apenas se msal está instalado E as variáveis foram configuradas."""
    return _MSAL_AVAILABLE and bool(_MS_CLIENT_ID) and bool(_MS_CLIENT_SECRET)

def _ms_app():
    return msal.ConfidentialClientApplication(
        _MS_CLIENT_ID,
        authority=_MS_AUTHORITY,
        client_credential=_MS_CLIENT_SECRET,
    )

def _ms_redirect_uri():
    base = os.getenv('APP_BASE_URL', 'http://localhost:5001').strip().rstrip('/')
    return f'{base}/api/auth/microsoft/callback'

# ─── Helper JWT ───────────────────────────────────────────────────────────────
_JWT_SECRET  = os.getenv('JWT_SECRET', 'secret-dev-inseguro-troque-em-producao').strip()
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
    if not _ms_configurado():
        # Diagnóstico claro para facilitar o debug
        problemas = []
        if not _MSAL_AVAILABLE:
            problemas.append('biblioteca msal não instalada (verifique requirements.txt e redeploy)')
        if not _MS_CLIENT_ID:
            problemas.append('variável MICROSOFT_CLIENT_ID não configurada no Render')
        if not _MS_CLIENT_SECRET:
            problemas.append('variável MICROSOFT_CLIENT_SECRET não configurada no Render')
        return jsonify({
            'erro': 'Login Microsoft não configurado neste ambiente.',
            'detalhes': problemas
        }), 503
    try:
        ms = _ms_app()
        auth_url = ms.get_authorization_request_url(
            scopes=_MS_SCOPES,
            redirect_uri=_ms_redirect_uri(),
            prompt='select_account',
        )
    except Exception as exc:
        import traceback
        return jsonify({
            'erro': str(exc),
            'tipo': type(exc).__name__,
            'trace': traceback.format_exc(),
        }), 500
    return redirect(auth_url)


@bp.route('/microsoft/callback', methods=['GET'])
def microsoft_callback():
    """Callback OAuth — troca code por token, cria/recupera usuário, emite JWT."""
    import traceback as _tb

    code  = request.args.get('code')
    error = request.args.get('error')

    # URL base do frontend (onde redirecionar após autenticação)
    frontend_base = os.getenv('APP_BASE_URL', 'http://localhost:5001').strip().rstrip('/')
    login_page    = f'{frontend_base}/pages/login.html'
    dash_page     = f'{frontend_base}/pages/dashboard.html'

    if error or not code:
        desc = request.args.get('error_description', error or 'Acesso negado')
        return redirect(f'{login_page}?ms_error={desc}')

    try:
        ms = _ms_app()
        result = ms.acquire_token_by_authorization_code(
            code,
            scopes=_MS_SCOPES,
            redirect_uri=_ms_redirect_uri(),
        )
    except Exception as e:
        return jsonify({
            'etapa': 'acquire_token',
            'erro': str(e),
            'tipo': type(e).__name__,
            'trace': _tb.format_exc(),
        }), 500

    if 'error' in result:
        return jsonify({
            'etapa': 'msal_result',
            'erro': result.get('error'),
            'descricao': result.get('error_description'),
        }), 500

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


# ─── Reset de senha ───────────────────────────────────────────────────────────

def _expiry_label(minutes):
    """Converte minutos em texto legível: '30 minutos', '1 hora', '2 horas'."""
    if minutes < 60:
        return f'{minutes} minuto{"s" if minutes != 1 else ""}'
    horas = minutes // 60
    return f'{horas} hora{"s" if horas != 1 else ""}'


def _enviar_email_reset(email_destino, nome, link, expiry_minutes=60):
    """
    Envia e-mail de reset.
    Prioridade: 1) Microsoft Graph API (usa o app Azure já configurado)
                2) SMTP clássico (MAIL_SERVER + MAIL_USERNAME)
                3) Log no console (sem configuração de e-mail)
    """
    expiry_str = _expiry_label(expiry_minutes)
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:0 auto;padding:32px 24px">
      <img src="https://projeto-jovem-believer.onrender.com/assets/logo/winged_mind_azul.png"
           style="height:48px;margin-bottom:28px" alt="Winged Mind">
      <h2 style="color:#1a73e8;margin:0 0 16px">Redefinição de senha</h2>
      <p style="color:#444">Olá, <strong>{nome}</strong>.</p>
      <p style="color:#444">Recebemos uma solicitação para redefinir a senha da sua conta.<br>
         Clique no botão abaixo — o link expira em <strong>{expiry_str}</strong>.</p>
      <a href="{link}"
         style="display:inline-block;margin:24px 0;padding:14px 32px;
                background:#1a73e8;color:#fff;text-decoration:none;
                border-radius:8px;font-weight:600;font-size:1rem">
        Redefinir minha senha
      </a>
      <p style="color:#888;font-size:.83rem">
        Se você não fez essa solicitação, ignore este email. Sua senha permanece a mesma.
      </p>
      <hr style="border:none;border-top:1px solid #eee;margin:24px 0">
      <p style="color:#bbb;font-size:.75rem">Winged Mind · Plataforma de Treinamento Hospitalar</p>
    </div>
    """

    # ── 1. Microsoft Graph API ────────────────────────────────────────────────
    mail_sender = os.getenv('MAIL_SENDER', '').strip()
    if _MSAL_AVAILABLE and _MS_CLIENT_ID and _MS_CLIENT_SECRET and mail_sender:
        try:
            import requests as _req
            ms = msal.ConfidentialClientApplication(
                _MS_CLIENT_ID,
                authority=_MS_AUTHORITY,
                client_credential=_MS_CLIENT_SECRET,
            )
            result = ms.acquire_token_for_client(
                scopes=['https://graph.microsoft.com/.default']
            )
            if 'access_token' not in result:
                raise RuntimeError(result.get('error_description', 'Falha ao obter token Graph'))

            payload = {
                'message': {
                    'subject': 'Redefinição de senha — Winged Mind',
                    'body': {'contentType': 'HTML', 'content': html},
                    'toRecipients': [{'emailAddress': {'address': email_destino}}],
                },
                'saveToSentItems': False,
            }
            resp = _req.post(
                f'https://graph.microsoft.com/v1.0/users/{mail_sender}/sendMail',
                json=payload,
                headers={
                    'Authorization': f'Bearer {result["access_token"]}',
                    'Content-Type': 'application/json',
                },
                timeout=15,
            )
            if resp.status_code == 202:
                print(f'[RESET] Email enviado via Microsoft Graph para {email_destino}')
                return True
            print(f'[RESET] Graph API retornou {resp.status_code}: {resp.text}')
        except Exception as exc:
            print(f'[RESET] Erro no Graph API: {exc}')
        # Se chegou aqui, Graph falhou — tenta SMTP como fallback

    # ── 2. SMTP clássico ──────────────────────────────────────────────────────
    mail_user   = os.getenv('MAIL_USERNAME', '').strip()
    mail_pass   = os.getenv('MAIL_PASSWORD', '').strip()
    mail_server = os.getenv('MAIL_SERVER', 'smtp.office365.com').strip()
    mail_port   = int(os.getenv('MAIL_PORT', 587))
    mail_from   = os.getenv('MAIL_DEFAULT_SENDER', mail_sender or mail_user).strip()

    if mail_user and mail_pass:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Redefinição de senha — Winged Mind'
        msg['From']    = mail_from
        msg['To']      = email_destino
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        try:
            with smtplib.SMTP(mail_server, mail_port, timeout=10) as smtp:
                smtp.ehlo(); smtp.starttls(); smtp.login(mail_user, mail_pass)
                smtp.sendmail(mail_from, [email_destino], msg.as_string())
            print(f'[RESET] Email enviado via SMTP para {email_destino}')
            return True
        except Exception as exc:
            print(f'[RESET] Falha no SMTP: {exc}')

    # ── 3. Sem configuração: apenas loga o link ───────────────────────────────
    print(f'[RESET] Nenhum provedor de e-mail configurado.')
    print(f'[RESET] Link de reset para {email_destino}: {link}')
    return True


@bp.route('/esqueci-senha', methods=['POST'])
def esqueci_senha():
    from app.models.password_reset import PasswordReset
    dados = request.get_json(silent=True) or {}
    email = (dados.get('email') or '').strip().lower()

    if not email:
        return jsonify({'erro': 'Email obrigatório.'}), 400

    usuario = User.query.filter_by(email=email, ativo=True).first()

    # Sempre responder 200 — evita enumeração de emails cadastrados
    if not usuario:
        return jsonify({'mensagem': 'Se o email estiver cadastrado, você receberá o link em breve.'}), 200

    # Invalidar tokens anteriores ainda não usados
    PasswordReset.query.filter_by(user_id=usuario.id, usado=False).update({'usado': True})
    db.session.flush()

    expiry_minutes = int(os.getenv('RESET_TOKEN_EXPIRY_MINUTES', 60))
    reset = PasswordReset(user_id=usuario.id, expiry_minutes=expiry_minutes)
    db.session.add(reset)
    db.session.commit()

    base = os.getenv('APP_BASE_URL', 'http://localhost:5001').strip().rstrip('/')
    link = f'{base}/pages/redefinir-senha.html?token={reset.token}'
    _enviar_email_reset(usuario.email, usuario.nome, link, expiry_minutes=expiry_minutes)

    return jsonify({'mensagem': 'Se o email estiver cadastrado, você receberá o link em breve.'}), 200


@bp.route('/redefinir-senha', methods=['POST'])
def redefinir_senha():
    from app.models.password_reset import PasswordReset
    dados      = request.get_json(silent=True) or {}
    token      = (dados.get('token') or '').strip()
    nova_senha = dados.get('nova_senha', '')

    if not token or not nova_senha:
        return jsonify({'erro': 'Token e nova senha são obrigatórios.'}), 400

    if len(nova_senha) < 8:
        return jsonify({'erro': 'A senha deve ter pelo menos 8 caracteres.'}), 400

    reset = PasswordReset.query.filter_by(token=token, usado=False).first()
    if not reset or not reset.valido:
        return jsonify({'erro': 'Link inválido ou expirado. Solicite um novo.'}), 410

    reset.usuario.set_password(nova_senha)
    reset.usado = True
    db.session.commit()

    return jsonify({'mensagem': 'Senha redefinida com sucesso!'}), 200

