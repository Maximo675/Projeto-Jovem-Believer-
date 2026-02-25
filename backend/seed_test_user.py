#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para criar usuário de teste no banco
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.user import User
from app.models.hospital import Hospital

app = create_app()

with app.app_context():
    try:
        # Criar hospital de teste
        hospital = Hospital.query.filter_by(nome='Hospital Teste').first()
        if not hospital:
            hospital = Hospital(
                nome='Hospital Teste',
                endereco='Rua Teste, 123',
                cidade='São Paulo',
                estado='SP',
                telefone='11999999999',
                email='hospital@teste.com'
            )
            db.session.add(hospital)
            db.session.commit()
            print("✅ Hospital criado")
        else:
            print("✅ Hospital já existe")
        
        # Criar usuário de teste
        usuario = User.query.filter_by(email='maximo.teste@gmail.com').first()
        if not usuario:
            usuario = User(
                email='maximo.teste@gmail.com',
                nome='Usuário Teste',
                hospital_id=hospital.id,
                funcao='usuario',
                ativo=True
            )
            usuario.set_password('Teste124*')
            db.session.add(usuario)
            db.session.commit()
            print("✅ Usuário criado com sucesso!")
            print(f"   Email: maximo.teste@gmail.com")
            print(f"   Senha: Teste124*")
        else:
            print("✅ Usuário já existe")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

print("\n✅ Dados de teste prontos!")
