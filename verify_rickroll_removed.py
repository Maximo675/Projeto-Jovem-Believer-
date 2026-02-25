"""
Verifica se o Rick Roll foi removido
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app, db
from app.models.lesson import Lesson

app = create_app()
with app.app_context():
    aula = Lesson.query.filter_by(titulo='Bem-vindo ao INFANT.ID').first()
    print(f'Aula: {aula.titulo}')
    print(f'Video URL agora: "{aula.video_url}"')
    if aula.video_url == '':
        print('✅ Rick Roll removido com sucesso!')
    else:
        print(f'❓ Ainda há URL: {aula.video_url}')
