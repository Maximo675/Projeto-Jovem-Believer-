# -*- coding: utf-8 -*-
"""
Configuração do Gunicorn — carregada automaticamente quando o CWD é backend/.
O start command do Render executa: cd backend && gunicorn ... então este arquivo
é sempre lido, independentemente do que estiver configurado no dashboard.

Problema resolvido aqui:
  eventlet.monkey_patch() itera todos os objetos em memória via gc.get_objects()
  e chama isinstance() em cada um. Os proxy objects lazy do openai SDK v1.x
  respondem a isinstance() disparando _load_client() → OpenAI() → crash fatal se
  OPENAI_API_KEY não estiver definida. O hook post_fork() define a variável ANTES
  de worker.init_process() chamar monkey_patch(), impedindo o crash.
"""
import os


def post_fork(server, worker):
    """
    Executado no processo worker logo após o fork() e ANTES de init_process()
    chamar eventlet.monkey_patch(). Garante que OPENAI_API_KEY exista para que
    os proxy objects do openai SDK não disparem OpenAIError durante a varredura
    do GC feita por monkey_patch().
    """
    os.environ.setdefault('OPENAI_API_KEY', 'dummy-not-used-mock-mode')
    os.environ.setdefault('USE_MOCK_AI', 'true')
    os.environ.setdefault('USE_OLLAMA', 'false')
