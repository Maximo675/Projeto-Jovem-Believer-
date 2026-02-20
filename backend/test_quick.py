#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste rápido - Verifica se o backend pode iniciar
"""

import sys
import os

# Adicionar diretório do app ao path
sys.path.insert(0, os.path.dirname(__file__))

print("")
print("=" * 60)
print("TESTE RÁPIDO - VERIFICANDO BACKEND")
print("=" * 60)
print("")

# Teste 1: Verificar Python
print("[1/5] Verificando Python...", end=" ")
try:
    print(f"✅ Python {sys.version.split()[0]}")
except:
    print("❌ Erro")
    sys.exit(1)

# Teste 2: Verificar Flask
print("[2/5] Verificando Flask...", end=" ")
try:
    import flask
    print(f"✅ Flask {flask.__version__}")
except ImportError:
    print("❌ Flask não instalado")
    print("     Execute: pip install flask")
    sys.exit(1)

# Teste 3: Verificar SQLAlchemy
print("[3/5] Verificando SQLAlchemy...", end=" ")
try:
    import sqlalchemy
    print(f"✅ SQLAlchemy {sqlalchemy.__version__}")
except ImportError:
    print("❌ SQLAlchemy não instalado")
    print("     Execute: pip install flask-sqlalchemy")
    sys.exit(1)

# Teste 4: Verificar .env
print("[4/5] Verificando arquivo .env...", end=" ")
if os.path.exists(".env"):
    print("✅ Arquivo encontrado")
else:
    print("⚠️  Arquivo .env não encontrado (OK, será criado)")

# Teste 5: Verificar importação do app
print("[5/5] Testando importação da aplicação...", end=" ")
try:
    from app import create_app, db
    print("✅ Aplicação carregada")
except Exception as e:
    print(f"❌ Erro ao carregar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("")
print("=" * 60)
print("✅ TODOS OS TESTES PASSARAM!")
print("=" * 60)
print("")
print("Agora você pode executar:")
print("  python run.py")
print("")
