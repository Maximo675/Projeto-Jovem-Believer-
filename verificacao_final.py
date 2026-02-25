"""
Verificação Final do Sistema
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app, db
from app.models.course import Course
from app.models.lesson import Lesson

app = create_app()
with app.app_context():
    # Statísticas gerais
    cursos = Course.query.all()
    aulas = Lesson.query.all()
    
    print('=' * 70)
    print('📊 VERIFICAÇÃO FINAL DO BANCO DE DADOS')
    print('=' * 70)
    print(f'\n📚 Cursos: {len(cursos)}')
    print(f'📖 Aulas totais: {len(aulas)}')
    
    print(f'\n📝 Detalhes dos Cursos:')
    for curso in cursos:
        aulas_curso = [a for a in aulas if a.curso_id == curso.id]
        print(f'  • {curso.titulo} ({len(aulas_curso)} aulas)')
        for aula in aulas_curso:
            video_status = '📹' if aula.video_url else '⊘'
            print(f'    {video_status} {aula.titulo}')
    
    print(f'\n✅ Verificação de Rick Roll:')
    rick_found = False
    for aula in aulas:
        if aula.video_url and 'dQw4w9WgXcQ' in aula.video_url:
            print(f'  ❌ ENCONTRADO em: {aula.titulo}')
            rick_found = True
    if not rick_found:
        print(f'  ✅ Nenhum Rick Roll encontrado!')
    
    print(f'\n' + '=' * 70)
    print('✨ SISTEMA PRONTO PARA USO ✨')
    print('=' * 70)
