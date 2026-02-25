"""
Script para remover o Rick Roll do banco de dados
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app, db
from app.models.lesson import Lesson

app = create_app()
with app.app_context():
    # Procurar e remover o Rick Roll
    aula = Lesson.query.filter_by(titulo='Bem-vindo ao INFANT.ID').first()
    if aula:
        print(f'Encontrada aula: {aula.titulo}')
        print(f'Video URL atual: {aula.video_url}')
        
        # Limpar o video_url
        aula.video_url = ''
        db.session.commit()
        print(f'✅ Video URL removido com sucesso!')
        print(f'Nova URL: "{aula.video_url}"')
    else:
        print('❌ Aula não encontrada')
