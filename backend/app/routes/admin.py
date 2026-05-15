from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User
from app.models.hospital import Hospital
from app.models.course import Course
from app.models.progress import Progress
from app.models.certificate import Certificate
from app.models.activity import UserActivity
from app.models.admin_note import AdminNote
from app.decorators import requer_funcao, usuario_atual
from datetime import datetime
import json
import os

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
    """Retorna dados completos de um usuário com desempenho, atividades e notas."""
    try:
        eu = usuario_atual()
        usuario = User.query.get_or_404(usuario_id)

        if eu.funcao == 'admin' and usuario.hospital_id != eu.hospital_id:
            return jsonify({'erro': 'Acesso negado'}), 403

        # ── Progresso com nome dos cursos ─────────────────────────────────
        progressos = Progress.query.filter_by(usuario_id=usuario_id).all()
        curso_ids  = [p.curso_id for p in progressos]
        cursos_map = {c.id: c for c in Course.query.filter(Course.id.in_(curso_ids)).all()} if curso_ids else {}

        progresso_enriquecido = []
        for p in progressos:
            curso = cursos_map.get(p.curso_id)
            progresso_enriquecido.append({
                **p.to_dict(),
                'curso_titulo': curso.titulo if curso else f'Curso {p.curso_id}',
                'curso_nivel':  curso.nivel  if curso else None,
            })

        # ── Atividades práticas ───────────────────────────────────────────
        atividades = (UserActivity.query
                      .filter_by(user_id=usuario_id)
                      .order_by(UserActivity.started_at.desc())
                      .all())

        tipos_label = {
            'protocol': 'Protocolo', 'cases': 'Casos Clínicos',
            'troubleshooting': 'Resolução de Problemas', 'live': 'Simulação ao Vivo',
        }
        atividades_dicts = []
        for a in atividades:
            atividades_dicts.append({
                **a.to_dict(),
                'tipo_label': tipos_label.get(a.activity_type, a.activity_type),
                'curso_titulo': cursos_map.get(a.course_id, None) and cursos_map[a.course_id].titulo,
            })

        # ── Score médio e dificuldades ────────────────────────────────────
        scores = [a.score for a in atividades if a.score is not None]
        score_medio = round(sum(scores) / len(scores), 1) if scores else None

        # Dificuldades = atividades com score < 60 ou mais de 2 tentativas
        dificuldades = [
            a for a in atividades
            if (a.score is not None and a.score < 60) or (a.attempts or 0) > 2
        ]

        # ── Aptidão (0-100) ───────────────────────────────────────────────
        progresso_medio = round(
            sum(p.percentual for p in progressos) / len(progressos), 1
        ) if progressos else 0
        cursos_concluidos = sum(1 for p in progressos if p.concluido)
        total_cursos = len(progressos) or 1

        # Fórmula: 40% progresso + 40% score médio + 20% taxa de conclusão
        taxa_conclusao = (cursos_concluidos / total_cursos) * 100
        aptidao = round(
            0.4 * progresso_medio +
            0.4 * (score_medio or 0) +
            0.2 * taxa_conclusao,
            1
        )

        # ── Certificados ──────────────────────────────────────────────────
        certificados = Certificate.query.filter_by(usuario_id=usuario_id).all()

        # ── Notas do admin ────────────────────────────────────────────────
        notas = (AdminNote.query
                 .filter_by(usuario_id=usuario_id)
                 .order_by(AdminNote.data_criacao.desc())
                 .all())

        return jsonify({
            'usuario':      usuario.to_dict(),
            'progresso':    progresso_enriquecido,
            'atividades':   atividades_dicts,
            'certificados': [c.to_dict() for c in certificados],
            'notas':        [n.to_dict() for n in notas],
            'resumo': {
                'progresso_medio':   progresso_medio,
                'score_medio':       score_medio,
                'aptidao':           aptidao,
                'cursos_concluidos': cursos_concluidos,
                'total_atividades':  len(atividades),
                'total_dificuldades': len(dificuldades),
                'tempo_total_min':   round(sum((a.time_spent or 0) for a in atividades) / 60, 1),
            },
        }), 200

    except Exception as e:
        import logging
        logging.getLogger(__name__).exception('Erro em detalhe_usuario')
        return jsonify({'erro': 'Não foi possível carregar os dados.'}), 500


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


# ── Notas / Feedback do admin sobre uma enfermeira ────────────────────────────

@bp.route('/usuarios/<int:usuario_id>/notas', methods=['GET'])
@requer_funcao('admin', 'super_admin')
def listar_notas(usuario_id):
    try:
        eu = usuario_atual()
        usuario = User.query.get_or_404(usuario_id)
        if eu.funcao == 'admin' and usuario.hospital_id != eu.hospital_id:
            return jsonify({'erro': 'Acesso negado'}), 403

        notas = (AdminNote.query
                 .filter_by(usuario_id=usuario_id)
                 .order_by(AdminNote.data_criacao.desc())
                 .all())
        return jsonify({'notas': [n.to_dict() for n in notas]}), 200
    except Exception:
        return jsonify({'erro': 'Não foi possível carregar as notas.'}), 500


@bp.route('/usuarios/<int:usuario_id>/notas', methods=['POST'])
@requer_funcao('admin', 'super_admin')
def criar_nota(usuario_id):
    try:
        eu = usuario_atual()
        usuario = User.query.get_or_404(usuario_id)
        if eu.funcao == 'admin' and usuario.hospital_id != eu.hospital_id:
            return jsonify({'erro': 'Acesso negado'}), 403

        dados = request.get_json(silent=True) or {}
        conteudo = (dados.get('conteudo') or '').strip()
        tipo     = dados.get('tipo', 'observacao')

        if not conteudo:
            return jsonify({'erro': 'Conteúdo da nota é obrigatório.'}), 400
        if tipo not in ('elogio', 'alerta', 'observacao'):
            tipo = 'observacao'

        nota = AdminNote(
            admin_id=eu.id,
            usuario_id=usuario_id,
            conteudo=conteudo,
            tipo=tipo,
        )
        db.session.add(nota)
        db.session.commit()
        return jsonify({'mensagem': 'Nota adicionada.', 'nota': nota.to_dict()}), 201
    except Exception:
        db.session.rollback()
        import logging; logging.getLogger(__name__).exception('criar_nota')
        return jsonify({'erro': 'Não foi possível salvar a nota.'}), 500


@bp.route('/notas/<int:nota_id>', methods=['DELETE'])
@requer_funcao('admin', 'super_admin')
def deletar_nota(nota_id):
    try:
        eu = usuario_atual()
        nota = AdminNote.query.get_or_404(nota_id)
        usuario = User.query.get(nota.usuario_id)
        if eu.funcao == 'admin' and (not usuario or usuario.hospital_id != eu.hospital_id):
            return jsonify({'erro': 'Acesso negado'}), 403

        db.session.delete(nota)
        db.session.commit()
        return jsonify({'mensagem': 'Nota removida.'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'erro': 'Não foi possível remover a nota.'}), 500


# ── Avaliação IA da enfermeira ────────────────────────────────────────────────

def _avaliar_com_openai(usuario, prog_medio, score_medio, taxa_conclusao,
                        aptidao, dificuldades, atividades, tempo_min):
    """Chama OpenAI e retorna dict de avaliação estruturada, ou None se falhar."""
    try:
        from openai import OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return None

        client = OpenAI(api_key=api_key)

        dif_texto = '; '.join(
            f"{a.activity_type} (score:{a.score}, tentativas:{a.attempts})"
            for a in dificuldades[:5]
        ) if dificuldades else 'nenhuma'

        prompt = (
            f"Você é um avaliador pedagógico especializado em treinamento de enfermagem hospitalar. "
            f"Analise os dados de desempenho de {usuario.nome} e retorne SOMENTE um JSON válido (sem markdown).\n\n"
            f"Dados:\n"
            f"- Progresso médio nos cursos: {prog_medio}%\n"
            f"- Score médio nas atividades: {score_medio}/100\n"
            f"- Taxa de conclusão de cursos: {taxa_conclusao}%\n"
            f"- Aptidão calculada: {aptidao}/100\n"
            f"- Total de atividades realizadas: {len(atividades)}\n"
            f"- Atividades com dificuldade: {len(dificuldades)}\n"
            f"- Tempo total de estudo: {tempo_min} minutos\n"
            f"- Detalhes das dificuldades: {dif_texto}\n\n"
            f"Retorne exatamente este JSON:\n"
            '{{\n'
            '  "nota_final": <inteiro 0-100>,\n'
            '  "nivel": "<aprovada|em_desenvolvimento|em_recuperacao|critica>",\n'
            '  "recomenda_certificado": <true|false>,\n'
            '  "parecer": "<2-3 frases objetivas>",\n'
            '  "pontos_fortes": ["<1>","<2>"],\n'
            '  "pontos_fracos": ["<1>","<2>"],\n'
            '  "plano_recuperacao": {{\n'
            '    "necessario": <true|false>,\n'
            '    "prazo_dias": <30|60|90>,\n'
            '    "acoes": ["<ação 1>","<ação 2>","<ação 3>"],\n'
            '    "meta_aptidao": <inteiro 0-100>\n'
            '  }}\n'
            '}}'
        )

        resp = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.3,
            max_tokens=700,
        )
        text = resp.choices[0].message.content.strip()
        # Remover cercas de markdown se presentes
        if '```' in text:
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
        avaliacao = json.loads(text.strip())
        avaliacao['fonte'] = 'openai'
        return avaliacao
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning('OpenAI avaliação falhou: %s', e)
        return None


def _avaliar_algoritmico(aptidao, prog_medio, score_medio, taxa_conclusao,
                         n_dific, n_atv):
    """Avaliação determinística como fallback quando OpenAI não está disponível."""
    nota = int(round(aptidao))

    if nota >= 80:
        nivel, recomenda = 'aprovada', True
    elif nota >= 60:
        nivel, recomenda = 'em_desenvolvimento', False
    elif nota >= 40:
        nivel, recomenda = 'em_recuperacao', False
    else:
        nivel, recomenda = 'critica', False

    pareceres = {
        'aprovada': (
            f'Excelente desempenho: {prog_medio}% de progresso médio e score de {score_medio}/100. '
            f'Demonstra domínio consistente do conteúdo e está apta a receber o certificado.'
        ),
        'em_desenvolvimento': (
            f'Progresso de {prog_medio}% com score médio de {score_medio}/100. '
            f'Demonstra compreensão sólida, mas ainda há espaço para melhoria antes da certificação.'
        ),
        'em_recuperacao': (
            f'Progresso de {prog_medio}% abaixo do esperado, score médio {score_medio}/100. '
            f'Indicam dificuldades significativas — recomenda-se plano de recuperação focado nas áreas problemáticas.'
        ),
        'critica': (
            f'Desempenho crítico: {prog_medio}% de progresso e score {score_medio}/100. '
            f'Necessária reavaliação completa e acompanhamento intensivo pelo instrutor responsável.'
        ),
    }

    fortes, fracos = [], []
    if prog_medio >= 70:   fortes.append(f'Alto progresso nos cursos ({prog_medio}%)')
    elif prog_medio < 40:  fracos.append(f'Baixo progresso nos cursos ({prog_medio}%)')
    if score_medio and score_medio >= 70: fortes.append(f'Bom score nas atividades ({score_medio}/100)')
    elif score_medio and score_medio < 50: fracos.append(f'Score abaixo da média nas atividades ({score_medio}/100)')
    if taxa_conclusao >= 80:  fortes.append(f'Alta taxa de conclusão ({taxa_conclusao:.0f}%)')
    elif taxa_conclusao < 30: fracos.append(f'Poucos cursos concluídos ({taxa_conclusao:.0f}%)')
    if n_atv >= 5:   fortes.append(f'Boa participação em atividades práticas ({n_atv} realizadas)')
    if n_dific <= 1: fortes.append('Poucas dificuldades registradas')
    elif n_dific >= 3: fracos.append(f'{n_dific} atividades com score baixo ou múltiplas tentativas')
    if not fortes: fortes = ['Está com cadastro ativo e acessa a plataforma']
    if not fracos: fracos = ['Nenhuma dificuldade crítica identificada']

    if nivel in ('em_recuperacao', 'critica'):
        prazo = 30 if nivel == 'em_recuperacao' else 60
        acoes = [
            'Revisão dos módulos com score abaixo de 60%',
            'Refazer as atividades práticas com dificuldades registradas',
            'Assistir aos vídeos de cada módulo problemático antes de nova tentativa',
        ]
        if nivel == 'critica':
            acoes.append('Agendar orientação presencial com o instrutor responsável')
        meta = 70 if nivel == 'em_recuperacao' else 60
        plano = {'necessario': True, 'prazo_dias': prazo, 'acoes': acoes, 'meta_aptidao': meta}
    else:
        plano = {'necessario': False, 'prazo_dias': 0, 'acoes': [], 'meta_aptidao': 80}

    return {
        'nota_final': nota,
        'nivel': nivel,
        'recomenda_certificado': recomenda,
        'parecer': pareceres[nivel],
        'pontos_fortes': fortes[:3],
        'pontos_fracos': fracos[:3],
        'plano_recuperacao': plano,
        'fonte': 'algoritmo',
    }


@bp.route('/usuarios/<int:usuario_id>/avaliar', methods=['POST'])
@requer_funcao('admin', 'super_admin')
def avaliar_enfermeira(usuario_id):
    """Avalia uma enfermeira com IA (OpenAI) ou algoritmo, gera nota + plano de recuperação."""
    try:
        eu      = usuario_atual()
        usuario = User.query.get_or_404(usuario_id)

        if eu.funcao == 'admin' and usuario.hospital_id != eu.hospital_id:
            return jsonify({'erro': 'Acesso negado'}), 403

        progressos  = Progress.query.filter_by(usuario_id=usuario_id).all()
        atividades  = UserActivity.query.filter_by(user_id=usuario_id).all()

        prog_medio     = round(sum(p.percentual for p in progressos) / len(progressos), 1) if progressos else 0
        cursos_conc    = sum(1 for p in progressos if p.concluido)
        total_cursos   = len(progressos) or 1
        taxa_conclusao = round((cursos_conc / total_cursos) * 100, 1)
        scores         = [a.score for a in atividades if a.score is not None]
        score_medio    = round(sum(scores) / len(scores), 1) if scores else 0
        dificuldades   = [a for a in atividades if (a.score is not None and a.score < 60) or (a.attempts or 0) > 2]
        aptidao        = round(0.4 * prog_medio + 0.4 * score_medio + 0.2 * taxa_conclusao, 1)
        tempo_min      = round(sum((a.time_spent or 0) for a in atividades) / 60, 1)

        avaliacao = _avaliar_com_openai(
            usuario, prog_medio, score_medio, taxa_conclusao,
            aptidao, dificuldades, atividades, tempo_min
        ) or _avaliar_algoritmico(
            aptidao, prog_medio, score_medio, taxa_conclusao,
            len(dificuldades), len(atividades)
        )

        # Substituir avaliação IA anterior (se existir)
        AdminNote.query.filter_by(usuario_id=usuario_id, tipo='avaliacao_ia').delete()
        nota_ia = AdminNote(
            admin_id=eu.id,
            usuario_id=usuario_id,
            conteudo=json.dumps(avaliacao, ensure_ascii=False),
            tipo='avaliacao_ia',
        )
        db.session.add(nota_ia)
        db.session.commit()

        return jsonify({'avaliacao': avaliacao}), 200

    except Exception:
        db.session.rollback()
        import logging
        logging.getLogger(__name__).exception('avaliar_enfermeira')
        return jsonify({'erro': 'Não foi possível realizar a avaliação.'}), 500


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

