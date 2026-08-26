# -*- coding: utf-8 -*-
"""
Configuração do Gunicorn — carregada automaticamente quando o CWD é backend/.
O start command do Render executa: cd backend && gunicorn ... então este arquivo
é sempre lido, independentemente do que estiver configurado no dashboard.

PROBLEMA RAIZ (relevante só se o worker for "eventlet"):
  O worker "eventlet" do gunicorn chama eventlet.monkey_patch() dentro do
  próprio init_process(), depois que preload_app já carregou a app inteira
  no master (com ela, os proxy objects lazy do SDK da openai). Esse
  monkey_patch tenta "atualizar" esses objetos já existentes e quebra —
  reproduzido isoladamente e confirmado com traceback real.

  O worker configurado hoje em render.yaml é "gthread", não "eventlet" —
  reproduzido também isoladamente com --worker-class gthread + openai
  importada de verdade: zero erros. Esse problema não afeta o Render atual;
  o bloqueio em run.py agora só entra em ação se detectar "eventlet" no
  próprio comando (sys.argv), então esse arquivo continua correto tanto se
  o worker for gthread (IA real liberada) quanto se alguém futuramente
  reconfigurar para eventlet (bloqueio automático, sem crash).

preload_app = True:
  Mantido por ainda ser boa prática (workers sobem mais rápido, e o check de
  sys.argv em run.py roda uma vez só no master antes do fork, exatamente
  como antes) — não é mais o que evita o crash, é o worker class certo.
"""

preload_app = True


def post_fork(server, worker):
    """Segurança extra após fork: garante variáveis de modo mock no worker."""
    import os
    os.environ.setdefault('OPENAI_API_KEY', 'dummy-not-used-mock-mode')
    os.environ.setdefault('USE_MOCK_AI', 'true')
    os.environ.setdefault('USE_OLLAMA', 'false')

