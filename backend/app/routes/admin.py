from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User
from app.models.hospital import Hospital
from app.models.progress import Progress
from app.models.certificate import Certificate
from app.decorators import requer_funcao, usuario_atual
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/api/admin')


# ── Visão geral do hospital do admin ──────────────────────────────────────────

@bp.route('/dashboard', methods=['GET'])
@requer_funcao('admin', 'super_admin')
def admin_dashboard():
    """Resumo: total de usuários, progresso médio e certificados do hospital."""
    try:
        eu = usuario_atual()
        hospital_id = eu.hospital_id if eu.funcao == 'admin' else request.args.get('hospital_id', type=int)

        query = User.query.filter_by(funcao='usuario')
        if hospital_id:
            query = query.filter_by(hospital_id=hospital_id)

        usuarios = query.all()
        ids = [u.id for u in usuarios]

        total_usuarios = len(ids)
        total_concluidos = 0
        total_certificados = 0
        progresso_soma = 0

        if ids:
            progressos = Progress.query.filter(Progress.usuario_id.in_(ids)).all()
            for p in progressos:
                progresso_soma += p.percentual
                if p.concluido:
                    total_concluidos += 1

            total_certificados = Certificate.query.filter(Certificate.usuario_id.in_(ids)).count()

        progresso_medio = round(progresso_soma / len(progressos), 1) if progressos else 0

        hospital = Hospital.query.get(hospital_id) if hospital_id else None

        return jsonify({
            'hospital': hospital.to_dict() if hospital else None,
            'total_usuarios': total_usuarios,
            'total_cursos_concluidos': total_concluidos,
            'total_certificados': total_certificados,
            'progresso_medio': progresso_medio,
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ── Lista de usuários do hospital com progresso embutido ─────────────────────

@bp.route('/usuarios', methods=['GET'])
@requer_funcao('admin', 'super_admin')
def listar_usuarios_hospital():
    """Lista enfermeiras/usuários do hospital com progresso e certificados."""
    try:
        eu = usuario_atual()
        hospital_id = eu.hospital_id if eu.funcao == 'admin' else request.args.get('hospital_id', type=int)

        query = User.query.filter_by(funcao='usuario')
        if hospital_id:
            query = query.filter_by(hospital_id=hospital_id)

        usuarios = query.order_by(User.nome).all()
        ids = [u.id for u in usuarios]

        progressos_map: dict[int, list] = {uid: [] for uid in ids}
        for p in Progress.query.filter(Progress.usuario_id.in_(ids)).all():
            progressos_map[p.usuario_id].append(p)

        certs_map: dict[int, int] = {uid: 0 for uid in ids}
        for c in Certificate.query.filter(Certificate.usuario_id.in_(ids)).all():
            certs_map[c.usuario_id] += 1

        resultado = []
        for u in usuarios:
            ps = progressos_map.get(u.id, [])
            media = round(sum(p.percentual for p in ps) / len(ps), 1) if ps else 0
            concluidos = sum(1 for p in ps if p.concluido)
            resultado.append({
                **u.to_dict(),
                'progresso_medio': media,
                'cursos_concluidos': concluidos,
                'total_certificados': certs_map.get(u.id, 0),
            })

        return jsonify({'usuarios': resultado, 'total': len(resultado)}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ── Detalhe de um usuário ─────────────────────────────────────────────────────

@bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
@requer_funcao('admin', 'super_admin')
def detalhe_usuario(usuario_id):
    """Retorna dados completos de um usuário com todo o progresso e certificados."""
    try:
        eu = usuario_atual()
        usuario = User.query.get_or_404(usuario_id)

        if eu.funcao == 'admin' and usuario.hospital_id != eu.hospital_id:
            return jsonify({'erro': 'Acesso negado'}), 403

        progressos = Progress.query.filter_by(usuario_id=usuario_id).all()
        certificados = Certificate.query.filter_by(usuario_id=usuario_id).all()

        return jsonify({
            'usuario': usuario.to_dict(),
            'progresso': [p.to_dict() for p in progressos],
            'certificados': [c.to_dict() for c in certificados],
        }), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ── Ativar / desativar usuário ────────────────────────────────────────────────

@bp.route('/usuarios/<int:usuario_id>/status', methods=['PATCH'])
@requer_funcao('admin', 'super_admin')
def alterar_status_usuario(usuario_id):
    """Ativar ou desativar um usuário do hospital."""
    try:
        eu = usuario_atual()
        usuario = User.query.get_or_404(usuario_id)

        if eu.funcao == 'admin' and usuario.hospital_id != eu.hospital_id:
            return jsonify({'erro': 'Acesso negado'}), 403

        dados = request.get_json()
        ativo = dados.get('ativo')
        if ativo is None:
            return jsonify({'erro': 'Campo "ativo" obrigatório'}), 400

        usuario.ativo = bool(ativo)
        db.session.commit()

        return jsonify({'mensagem': f'Usuário {"ativado" if usuario.ativo else "desativado"} com sucesso'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


# ── Emitir certificado manualmente ───────────────────────────────────────────

@bp.route('/usuarios/<int:usuario_id>/certificados', methods=['POST'])
@requer_funcao('admin', 'super_admin')
def emitir_certificado(usuario_id):
    """Emitir certificado manualmente para um usuário."""
    try:
        eu = usuario_atual()
        usuario = User.query.get_or_404(usuario_id)

        if eu.funcao == 'admin' and usuario.hospital_id != eu.hospital_id:
            return jsonify({'erro': 'Acesso negado'}), 403

        dados = request.get_json()
        curso_id = dados.get('curso_id')
        if not curso_id:
            return jsonify({'erro': 'curso_id obrigatório'}), 400

        existente = Certificate.query.filter_by(usuario_id=usuario_id, curso_id=curso_id).first()
        if existente:
            return jsonify({'erro': 'Certificado já emitido para este curso'}), 409

        cert = Certificate(usuario_id=usuario_id, curso_id=curso_id)
        db.session.add(cert)
        db.session.commit()

        return jsonify({'mensagem': 'Certificado emitido', 'certificado': cert.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


# ── Revogar certificado ───────────────────────────────────────────────────────

@bp.route('/certificados/<int:cert_id>', methods=['DELETE'])
@requer_funcao('admin', 'super_admin')
def revogar_certificado(cert_id):
    """Revogar (deletar) um certificado."""
    try:
        eu = usuario_atual()
        cert = Certificate.query.get_or_404(cert_id)
        usuario = User.query.get(cert.usuario_id)

        if eu.funcao == 'admin' and usuario.hospital_id != eu.hospital_id:
            return jsonify({'erro': 'Acesso negado'}), 403

        db.session.delete(cert)
        db.session.commit()

        return jsonify({'mensagem': 'Certificado revogado'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
