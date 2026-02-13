"""
Script para criar e gerenciar o banco de dados.
"""

import os
import sys
from pathlib import Path

# Adicionar diretório backend ao path
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app, db
from app.models import *

def criar_tabelas():
    """Cria todas as tabelas no banco de dados."""
    app = create_app()
    
    with app.app_context():
        print("Criando tabelas...")
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")

def limpar_banco():
    """Limpa todas as tabelas do banco de dados."""
    app = create_app()
    
    with app.app_context():
        print("⚠️ Confirmação: Tem certeza que deseja LIMPAR o banco de dados? (sim/não)")
        confirmar = input().lower()
        
        if confirmar == 'sim':
            db.drop_all()
            print("✅ Banco de dados limpo!")
        else:
            print("Operação cancelada.")

def resetar_banco():
    """Limpa e recria o banco de dados."""
    app = create_app()
    
    with app.app_context():
        print("Resetando banco de dados...")
        db.drop_all()
        db.create_all()
        print("✅ Banco de dados resetado!")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        comando = sys.argv[1]
        
        if comando == 'criar':
            criar_tabelas()
        elif comando == 'limpar':
            limpar_banco()
        elif comando == 'resetar':
            resetar_banco()
        else:
            print(f"Comando desconhecido: {comando}")
            print("Comandos disponíveis: criar, limpar, resetar")
    else:
        print("Uso: python database.py <comando>")
        print("Comandos: criar, limpar, resetar")
