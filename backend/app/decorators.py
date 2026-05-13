"""
Decorators de autenticação e autorização por função.
Fachada sobre app.utils.decorators para uso uniforme em toda a aplicação.

Uso:
    from app.decorators import requer_auth, requer_funcao, usuario_atual

    @bp.route('/exemplo')
    @requer_auth
    def rota_protegida():
        u = usuario_atual()   # objeto User completo

    @bp.route('/admin')
    @requer_funcao('admin', 'super_admin')
    def so_admins():
        ...
"""

from app.utils.decorators import token_requerido as requer_auth, requer_papel
from flask import g


def requer_funcao(*funcoes):
    """
    Exige que o usuário autenticado tenha uma das funções listadas.
    super_admin sempre tem acesso implicitamente.
    Combina token_requerido + requer_papel.

    Uso:
        @requer_funcao('admin', 'super_admin')
        def rota(): ...
    """
    # Usa o papel mínimo (mais permissivo da lista) na hierarquia
    from app.utils.decorators import ROLES_ORDER, token_requerido
    from functools import wraps
    from flask import jsonify

    # Menor índice = maior privilégio
    indices = [ROLES_ORDER.index(f) for f in funcoes if f in ROLES_ORDER]
    papel_minimo = ROLES_ORDER[min(indices)] if indices else funcoes[0]

    def decorator(f):
        @token_requerido
        @wraps(f)
        def wrapper(*args, **kwargs):
            funcao = g.usuario.funcao if hasattr(g.usuario, 'funcao') else g.usuario.get('funcao', '')
            if funcao == 'super_admin' or funcao in funcoes:
                return f(*args, **kwargs)
            return jsonify({
                'erro': 'Acesso negado.',
                'detalhe': f'Requer uma das funções: {", ".join(funcoes)}'
            }), 403
        return wrapper
    return decorator


def usuario_atual():
    """Retorna o objeto User do usuário autenticado (após @requer_auth ou @requer_funcao)."""
    return getattr(g, 'usuario', None)


def mesmo_hospital_ou_superior(hospital_id):
    """Retorna True se o usuário pertence ao hospital ou é super_admin."""
    u = usuario_atual()
    if not u:
        return False
    funcao = u.funcao if hasattr(u, 'funcao') else u.get('funcao', '')
    if funcao == 'super_admin':
        return True
    uid = u.hospital_id if hasattr(u, 'hospital_id') else u.get('hospital_id')
    return uid == hospital_id

