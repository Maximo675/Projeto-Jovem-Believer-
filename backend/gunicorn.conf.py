# -*- coding: utf-8 -*-
"""
Configuração do Gunicorn — carregada automaticamente quando o CWD é backend/.
O start command do Render executa: cd backend && gunicorn ... então este arquivo
é sempre lido, independentemente do que estiver configurado no dashboard.

PROBLEMA RAIZ:
  Sem --preload, cada worker gunicorn reimporta a app de forma independente.
  A ordem de execução no worker é:
    1. init_process() → patch() → eventlet.monkey_patch()  ← crash aqui
    2. load_wsgi() → importa run.py                        ← nosso bloqueio chegaria tarde demais

  O monkey_patch() itera gc.get_objects() e chama isinstance() em cada objeto.
  Os proxy objects lazy do openai SDK v1.x respondem a isinstance() disparando
  _load_client() → TypeError: proxies / OpenAIError (fora de qualquer try/except).

SOLUÇÃO — preload_app = True:
  Com preload, o MASTER carrega a app ANTES de fazer fork dos workers:
    Master: importa run.py → sys.modules['openai'] = None → app carrega em modo mock
    Fork → workers herdam sys.modules limpo (sem proxy objects do openai)
    Worker: monkey_patch() → gc.get_objects() → zero proxy objects → SEM CRASH
"""

# Carrega a app no processo master antes de fazer fork dos workers.
# Garante que sys.modules['openai'] = None (definido em run.py) esteja ativo
# antes de qualquer worker chamar eventlet.monkey_patch().
preload_app = True


def post_fork(server, worker):
    """Segurança extra após fork: garante variáveis de modo mock no worker."""
    import os
    os.environ.setdefault('OPENAI_API_KEY', 'dummy-not-used-mock-mode')
    os.environ.setdefault('USE_MOCK_AI', 'true')
    os.environ.setdefault('USE_OLLAMA', 'false')

