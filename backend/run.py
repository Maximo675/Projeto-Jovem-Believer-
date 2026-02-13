# -*- coding: utf-8 -*-
"""
Script principal para executar a aplicação.
"""

import os
from app import create_app, db
from app.models import *

# Criar aplicação
app = create_app()

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
    print("✅ Banco de dados inicializado")

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
    
    print("✅ Banco de dados populado com dados de exemplo")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
