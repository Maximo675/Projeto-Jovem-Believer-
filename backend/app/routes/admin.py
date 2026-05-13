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


# ══════════════════════════════════════════════════════════════════════════════
# ROTAS EXCLUSIVAS SUPER_ADMIN
# ══════════════════════════════════════════════════════════════════════════════

@bp.route('/super/visao-geral', methods=['GET'])
@requer_funcao('super_admin')
def super_visao_geral():
    """Visão consolidada de toda a plataforma por hospital."""
    try:
        hospitais = Hospital.query.order_by(Hospital.nome).all()
        resultado = []

        for h in hospitais:
            ids = [u.id for u in User.query.filter_by(hospital_id=h.id, funcao='usuario').all()]
            total_usuarios = len(ids)
            total_certs = 0
            progresso_soma = 0
            total_concluidos = 0
            total_progressos = 0

            if ids:
                progressos = Progress.query.filter(Progress.usuario_id.in_(ids)).all()
                total_progressos = len(progressos)
                for p in progressos:
                    progresso_soma += p.percentual
                    if p.concluido:
                        total_concluidos += 1
                total_certs = Certificate.query.filter(Certificate.usuario_id.in_(ids)).count()

            resultado.append({
                **h.to_dict(),
                'total_usuarios': total_usuarios,
                'progresso_medio': round(progresso_soma / total_progressos, 1) if total_progressos else 0,
                'cursos_concluidos': total_concluidos,
                'total_certificados': total_certs,
            })

        total_plataforma = {
            'hospitais': len(hospitais),
            'usuarios': sum(r['total_usuarios'] for r in resultado),
            'certificados': sum(r['total_certificados'] for r in resultado),
            'progresso_medio': round(
                sum(r['progresso_medio'] * r['total_usuarios'] for r in resultado if r['total_usuarios'])
                / max(sum(r['total_usuarios'] for r in resultado), 1),
                1
            ),
        }

        return jsonify({'hospitais': resultado, 'totais': total_plataforma}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/super/admins', methods=['GET'])
@requer_funcao('super_admin')
def listar_admins():
    """Lista todos os administradores de hospital."""
    try:
        admins = User.query.filter_by(funcao='admin').order_by(User.nome).all()
        resultado = []
        for a in admins:
            h = Hospital.query.get(a.hospital_id) if a.hospital_id else None
            resultado.append({
                **a.to_dict(),
                'hospital_nome': h.nome if h else None,
            })
        return jsonify({'admins': resultado}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/super/admins/<int:usuario_id>/funcao', methods=['PATCH'])
@requer_funcao('super_admin')
def alterar_funcao(usuario_id):
    """Alterar função de um usuário (promover/rebaixar)."""
    try:
        usuario = User.query.get_or_404(usuario_id)
        dados = request.get_json()
        nova_funcao = dados.get('funcao')
        funcoes_validas = ['usuario', 'instrutor', 'admin']
        if nova_funcao not in funcoes_validas:
            return jsonify({'erro': f'Função inválida. Opções: {funcoes_validas}'}), 400

        usuario.funcao = nova_funcao
        db.session.commit()
        return jsonify({'mensagem': f'Função alterada para {nova_funcao}', 'usuario': usuario.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@bp.route('/super/hospitais', methods=['POST'])
@requer_funcao('super_admin')
def criar_hospital():
    """Criar novo hospital (alias protegido)."""
    from app.routes.hospitals import create_hospital
    return create_hospital()


@bp.route('/super/hospitais/<int:hospital_id>/status', methods=['PATCH'])
@requer_funcao('super_admin')
def alterar_status_hospital(hospital_id):
    """Ativar / desativar hospital."""
    try:
        hospital = Hospital.query.get_or_404(hospital_id)
        dados = request.get_json()
        ativo = dados.get('ativo')
        if ativo is None:
            return jsonify({'erro': 'Campo "ativo" obrigatório'}), 400
        hospital.ativo = bool(ativo)
        db.session.commit()
        return jsonify({'mensagem': f'Hospital {"ativado" if hospital.ativo else "desativado"}'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

