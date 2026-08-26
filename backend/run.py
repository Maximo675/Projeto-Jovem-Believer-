# -*- coding: utf-8 -*-
"""
Script principal para executar a aplicação.
"""

import os
import sys

# ─────────────────────────────────────────────────────────────────────────────
# BLOQUEAR OPENAI SÓ SE O WORKER DO GUNICORN FOR "eventlet"
#
# Problema real (reproduzido isoladamente antes de mexer aqui): o worker
# "eventlet" do gunicorn chama eventlet.monkey_patch() dentro do próprio
# init_process(), DEPOIS que preload_app já importou a app (e com ela os
# proxy objects lazy do SDK da openai). Esse monkey_patch tenta "atualizar"
# esses objetos já existentes e quebra — confirmado com traceback real ao
# reproduzir gunicorn --worker-class eventlet + openai importada.
#
# A versão anterior deste bloqueio desconfiava de QUALQUER execução via
# gunicorn (checando __name__ != '__main__'), o que também bloqueava sem
# necessidade o worker "gthread" — que é o que o render.yaml realmente usa
# em produção. Reproduzi gunicorn --worker-class gthread (com --preload,
# igual ao gunicorn.conf.py) com a openai importada e instanciada de
# verdade: zero erros. O problema é do worker eventlet especificamente, não
# de rodar sob gunicorn em si.
#
# Por isso agora o bloqueio olha o próprio comando com que o processo foi
# iniciado (sys.argv) e só entra em ação se detectar "eventlet" como worker
# class — o que cobre o Render de hoje (gthread, sem bloqueio, IA real
# liberada) e continua protegendo contra alguém reconfigurar para eventlet
# no futuro sem saber do motivo.
_argv_str = ' '.join(sys.argv).lower()
_worker_eventlet = 'gunicorn' in sys.argv[0].lower() and 'eventlet' in _argv_str

if _worker_eventlet and 'openai' not in sys.modules:
    sys.modules['openai'] = None  # type: ignore[assignment]
    print("[BOOT] openai bloqueado — worker eventlet detectado (risco de crash confirmado em teste)")

# Adicionar diretório do app ao path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import create_app, db
    from app.models import *
except ImportError as e:
    print(f"[ERROR] Erro ao importar módulos: {e}")
    print("Certifique-se de que todas as dependências estão instaladas:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

# Criar aplicação
try:
    app = create_app()
except Exception as e:
    print(f"[ERROR] Erro ao criar a aplicação: {e}")
    import traceback; traceback.print_exc()
    # Tentar criar app mínimo para não matar o processo no Render (evita 502)
    try:
        os.environ.setdefault('FLASK_ENV', 'development')
        app = create_app()
    except Exception:
        sys.exit(1)

@app.shell_context_processor
def make_shell_context():
    """Contexto para shell Flask."""
    return {
        'db': db,
        # Importar modelos aqui para usar no shell
    }

@app.cli.command()
def init_db():
    """Inicializa o banco de dados."""
    db.create_all()
    print("[OK] Banco de dados inicializado")

@app.cli.command()
def seed_db():
    """Popula o banco de dados com dados de exemplo."""
    from app.models.hospital import Hospital
    from app.models.course import Course
    from app.models.lesson import Lesson
    
    # Dados de exemplo
    hospitals = [
        Hospital(
            nome="Hospital Central São Paulo",
            estado="SP",
            cidade="São Paulo",
            endereco="Rua Test, 123",
            telefone="(11) 1234-5678",
            email="hospital-sp@infantid.com",
            cnpj="12.345.678/0001-99"
        ),
        Hospital(
            nome="Hospital Rio de Janeiro",
            estado="RJ",
            cidade="Rio de Janeiro",
            endereco="Av. Test, 456",
            telefone="(21) 1234-5678",
            email="hospital-rj@infantid.com",
            cnpj="98.765.432/0001-11"
        )
    ]
    
    for h in hospitals:
        if not Hospital.query.filter_by(email=h.email).first():
            db.session.add(h)
    
    db.session.commit()
    
    # Criar um curso de exemplo
    curso = Course(
        titulo="Onboarding Infantil ID - Módulo 1",
        descricao="Primeiro módulo de treinamento para profissionais de saúde",
        autor="Group Akiyama",
        nivel="basico",
        tempo_estimado=180
    )
    
    if not Course.query.filter_by(titulo=curso.titulo).first():
        db.session.add(curso)
        db.session.commit()
        
        # Adicionar aulas
        aulas = [
            Lesson(
                curso_id=curso.id,
                titulo="Introdução ao Onboarding",
                descricao="Bem-vindo ao programa de onboarding",
                conteudo="<h1>Bem-vindo!</h1><p>Este é o primeiro módulo...</p>",
                ordem=1,
                duracao=30
            ),
            Lesson(
                curso_id=curso.id,
                titulo="Processos e Procedimentos",
                descricao="Conheça os processos principais",
                conteudo="<h1>Processos</h1><p>Os processos são...</p>",
                ordem=2,
                duracao=45
            )
        ]
        
        for aula in aulas:
            db.session.add(aula)
        
        db.session.commit()
    
    print("[OK] Banco de dados populado com dados de exemplo")

if __name__ == '__main__':
    # Configurar porta (padrão 5001)
    port = int(os.getenv('FLASK_PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    
    try:
        print("")
        print("=" * 60)
        print(f"[OK] Iniciando servidor Flask na porta {port}...")
        print("=" * 60)
        print("")
        print(f"WEB Abra no navegador: http://localhost:{port}")
        print(f"API Disponível em: http://localhost:{port}/api")
        print("")
        print("Pressione CTRL+C para parar o servidor")
        print("")
        
        # Iniciar servidor com SocketIO
        from app import socketio
        # Use app.run with socketio as middleware instead of socketio.run
        # This allows Flask to serve normal HTTP requests and SocketIO to handle WebSocket
        socketio.run(app, debug=debug, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
        
    except OSError as e:
        if "Address already in use" in str(e):
            print("")
            print("[ERROR] ERRO: Porta {} já está em uso!".format(port))
            print("")
            print("Solução:")
            print("  1. Feche outras aplicações usando essa porta")
            print("  2. Ou use outra porta: FLASK_PORT=5002 python backend/run.py")
            print("")
            sys.exit(1)
        else:
            print(f"[ERROR] Erro ao iniciar servidor: {e}")
            sys.exit(1)
    except KeyboardInterrupt:
        print("")
        print("[OK] Servidor encerrado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
