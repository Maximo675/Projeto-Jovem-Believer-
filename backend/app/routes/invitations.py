# -*- coding: utf-8 -*-
"""
Rotas de convites — /api/invitations

Permissões:
  POST   /                        → admin ou super_admin (convida enfermeira)
  GET    /                        → admin (lista convites do seu hospital)
                                    super_admin (lista todos)
  DELETE /<id>                    → admin (cancela convite do seu hospital)
  GET    /validate/<token>        → público (frontend exibe dados antes de aceitar)
  POST   /accept/<token>          → público (aceita via email/senha)
"""

from flask import Blueprint, jsonify, request, g
from app import db
from app.models.invitation import Invitation
from app.models.user import User
from app.models.hospital import Hospital
from app.utils.decorators import token_requerido, admin_requerido, requer_papel
from datetime import datetime
import os

bp = Blueprint('invitations', __name__, url_prefix='/api/invitations')


def _enviar_email_convite(email_destino, nome_hospital, funcao, link, criado_por_nome):
    """Envia email de convite via Microsoft Graph ou loga o link."""
    funcao_labels = {
        'usuario': 'Usuário',
        'instrutor': 'Instrutor',
        'admin': 'Administrador',
        'super_admin': 'Super Admin',
    }
    funcao_label = funcao_labels.get(funcao, funcao.title())

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:0 auto;padding:32px 24px">
      <img src="https://projeto-jovem-believer.onrender.com/assets/logo/winged_mind_azul.png"
           style="height:48px;margin-bottom:28px" alt="Winged Mind">
      <h2 style="color:#1a73e8;margin:0 0 16px">Você foi convidado!</h2>
      <p style="color:#444">
        <strong>{criado_por_nome}</strong> convidou você para acessar a plataforma
        <strong>Winged Mind</strong> como <strong>{funcao_label}</strong>
        do <strong>{nome_hospital}</strong>.
      </p>
      <p style="color:#444">Clique no botão abaixo para criar sua conta. O link expira em <strong>7 dias</strong>.</p>
      <a href="{link}"
         style="display:inline-block;margin:24px 0;padding:14px 32px;
                background:#1a73e8;color:#fff;text-decoration:none;
                border-radius:8px;font-weight:600;font-size:1rem">
        Criar minha conta
      </a>
      <p style="color:#888;font-size:.83rem">
        Se você não esperava este convite, ignore este email.
      </p>
      <hr style="border:none;border-top:1px solid #eee;margin:24px 0">
      <p style="color:#bbb;font-size:.75rem">Winged Mind · Plataforma de Treinamento Hospitalar</p>
    </div>
    """

    # Tenta Microsoft Graph API
    try:
        import msal as _msal
        import requests as _req
        client_id     = os.getenv('MICROSOFT_CLIENT_ID', '').strip()
        client_secret = os.getenv('MICROSOFT_CLIENT_SECRET', '').strip()
        tenant_id     = os.getenv('MICROSOFT_TENANT_ID', 'common').strip()
        mail_sender   = os.getenv('MAIL_SENDER', '').strip()

        if client_id and client_secret and mail_sender:
            authority = f'https://login.microsoftonline.com/{tenant_id}'
            ms = _msal.ConfidentialClientApplication(
                client_id, authority=authority, client_credential=client_secret
            )
            result = ms.acquire_token_for_client(
                scopes=['https://graph.microsoft.com/.default']
            )
            if 'access_token' in result:
                payload = {
                    'message': {
                        'subject': f'Convite para a plataforma Winged Mind — {nome_hospital}',
                        'body': {'contentType': 'HTML', 'content': html},
                        'toRecipients': [{'emailAddress': {'address': email_destino}}],
                    },
                    'saveToSentItems': False,
                }
                resp = _req.post(
                    f'https://graph.microsoft.com/v1.0/users/{mail_sender}/sendMail',
                    json=payload,
                    headers={'Authorization': f'Bearer {result["access_token"]}',
                             'Content-Type': 'application/json'},
                    timeout=15,
                )
                if resp.status_code == 202:
                    print(f'[CONVITE] Email enviado via Graph para {email_destino}')
                    return
                print(f'[CONVITE] Graph retornou {resp.status_code}: {resp.text}')
    except Exception as exc:
        print(f'[CONVITE] Erro Graph API: {exc}')

    # Fallback: log do link
    print(f'[CONVITE] Link de convite para {email_destino}: {link}')


# ─── Criar convite ────────────────────────────────────────────────────────────

@bp.route('', methods=['POST'])
@token_requerido
@admin_requerido
def criar_convite():
    """admin convida enfermeira; super_admin pode convidar qualquer papel."""
    data = request.get_json() or {}

    email      = (data.get('email') or '').strip().lower()
    funcao     = data.get('funcao', 'usuario')
    hospital_id = data.get('hospital_id')

    if not email:
        return jsonify({'erro': 'Email é obrigatório'}), 400

    # admin só pode convidar para o próprio hospital e apenas papel 'usuario'
    if g.usuario.funcao == 'admin':
        hospital_id = g.usuario.hospital_id
        if funcao not in ('usuario', 'instrutor'):
            return jsonify({'erro': 'Admin pode convidar apenas usuários e instrutores'}), 403
    else:
        # super_admin deve informar hospital_id
        if not hospital_id:
            return jsonify({'erro': 'hospital_id é obrigatório'}), 400
        if funcao not in ('usuario', 'instrutor', 'admin'):
            return jsonify({'erro': 'Papel inválido'}), 400

    hospital = Hospital.query.get(hospital_id)
    if not hospital or not hospital.ativo:
        return jsonify({'erro': 'Hospital não encontrado ou inativo'}), 404

    # Não convidar quem já tem conta
    if User.query.filter_by(email=email).first():
        return jsonify({'erro': 'Já existe uma conta com este email'}), 409

    # Invalidar convites anteriores não usados para o mesmo email/hospital
    Invitation.query.filter_by(
        email=email, hospital_id=hospital_id, usado=False
    ).update({'usado': True})

    convite = Invitation(
        email=email,
        hospital_id=hospital_id,
        funcao=funcao,
        criado_por_id=g.usuario.id,
    )
    db.session.add(convite)
    db.session.commit()

    base_url = os.getenv('APP_BASE_URL', 'http://localhost:5001').strip().rstrip('/')
    link = f'{base_url}/pages/accept-invite.html?token={convite.token}'

    _enviar_email_convite(
        email_destino=email,
        nome_hospital=hospital.nome,
        funcao=funcao,
        link=link,
        criado_por_nome=g.usuario.nome,
    )

    return jsonify({
        'mensagem': 'Convite criado com sucesso',
        'convite': convite.to_dict(),
        'link': link,
    }), 201


# ─── Listar convites ──────────────────────────────────────────────────────────

@bp.route('', methods=['GET'])
@token_requerido
@admin_requerido
def listar_convites():
    query = Invitation.query
    if g.usuario.funcao == 'admin':
        query = query.filter_by(hospital_id=g.usuario.hospital_id)

    apenas_ativos = request.args.get('apenas_ativos', 'false').lower() == 'true'
    if apenas_ativos:
        query = query.filter_by(usado=False).filter(
            Invitation.expires_at > datetime.utcnow()
        )

    convites = query.order_by(Invitation.data_criacao.desc()).all()
    return jsonify([c.to_dict() for c in convites]), 200


# ─── Cancelar convite ─────────────────────────────────────────────────────────

@bp.route('/<int:convite_id>', methods=['DELETE'])
@token_requerido
@admin_requerido
def cancelar_convite(convite_id):
    convite = Invitation.query.get_or_404(convite_id)

    if g.usuario.funcao == 'admin' and convite.hospital_id != g.usuario.hospital_id:
        return jsonify({'erro': 'Sem permissão para este convite'}), 403

    convite.usado = True
    db.session.commit()
    return jsonify({'mensagem': 'Convite cancelado'}), 200


# ─── Validar token (público — frontend exibe dados antes de aceitar) ──────────

@bp.route('/validate/<token>', methods=['GET'])
def validar_token(token):
    convite = Invitation.query.filter_by(token=token).first()
    if not convite:
        return jsonify({'erro': 'Convite não encontrado'}), 404
    if not convite.valido:
        return jsonify({'erro': 'Convite expirado ou já utilizado'}), 410

    return jsonify({
        'email':    convite.email,
        'hospital': convite.hospital.nome if convite.hospital else None,
        'funcao':   convite.funcao,
    }), 200


# ─── Aceitar convite via email/senha ─────────────────────────────────────────

@bp.route('/accept/<token>', methods=['POST'])
def aceitar_convite(token):
    """Cria a conta da enfermeira via email + senha usando o convite."""
    convite = Invitation.query.filter_by(token=token).first()
    if not convite:
        return jsonify({'erro': 'Convite não encontrado'}), 404
    if not convite.valido:
        return jsonify({'erro': 'Convite expirado ou já utilizado'}), 410

    data  = request.get_json() or {}
    nome  = (data.get('nome') or '').strip()
    senha = data.get('senha', '')

    if not nome:
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    if len(senha) < 8:
        return jsonify({'erro': 'Senha deve ter pelo menos 8 caracteres'}), 400

    if User.query.filter_by(email=convite.email).first():
        return jsonify({'erro': 'Já existe uma conta com este email'}), 409

    try:
        usuario = User(
            email=convite.email,
            nome=nome,
            senha=senha,
            hospital_id=convite.hospital_id,
            funcao=convite.funcao,
            ativo=True,
        )
        db.session.add(usuario)

        convite.usado = True
        db.session.commit()

        from app.routes.auth import _gerar_token
        jwt_token = _gerar_token(usuario)

        return jsonify({
            'mensagem': 'Conta criada com sucesso!',
            'token': jwt_token,
            'usuario': usuario.to_dict(),
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
