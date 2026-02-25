"""
Adiciona vídeo apropriado ao Curso 1 (Bem-vindo ao INFANT.ID)
Escolhe o vídeo mais útil da lista disponível
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app, db
from app.models.lesson import Lesson

# Vídeo mais apropriado para introdução (Seleção do Recém-nascido é o primeiro passo prático)
VIDEO_URL = 'https://drive.google.com/file/d/1uOILNO0clQYeP9PFpuvkaP1h4570kaRA/view?usp=sharing'

app = create_app()
with app.app_context():
    # Encontrar a primeira aula do Curso 1
    aula = Lesson.query.filter_by(titulo='Bem-vindo ao INFANT.ID').first()
    
    if aula:
        print(f'✅ Encontrada aula: {aula.titulo}')
        print(f'   Vídeo anterior: "{aula.video_url}"')
        
        # Adicionar vídeo
        aula.video_url = VIDEO_URL
        db.session.commit()
        
        print(f'   ✅ Vídeo adicionado!')
        print(f'   Link: Google Drive - Seleção do Recém-nascido')
        print(f'   Descrição: Tutorial prático de seleção e preparação do RN')
    else:
        print('❌ Aula não encontrada!')
