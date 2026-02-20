# coding: utf-8
"""
Atualizar Curso 2 com português correto
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app import create_app
from app.models import Lesson
from database.database import db
from lessons_course2_portuguese import LESSONS_COURSE2_PORTUGUESE

def update_course2():
    app = create_app()
    
    with app.app_context():
        print("="*70)
        print("ATUALIZANDO CURSO 2 COM PORTUGUÊS CORRETO")
        print("="*70 + "\n")
        
        updated = 0
        errors = 0
        
        for lesson_id, lesson_data in LESSONS_COURSE2_PORTUGUESE.items():
            try:
                lesson = Lesson.query.filter_by(id=lesson_id).first()
                
                if lesson:
                    lesson.titulo = lesson_data['title']
                    lesson.conteudo = lesson_data['content']
                    lesson.duracao = int(lesson_data['duration'].split()[0])
                    
                    db.session.add(lesson)
                    db.session.commit()
                    
                    print(f"✓ Aula {lesson_id}: {lesson_data['title']}")
                    updated += 1
                    
            except Exception as e:
                print(f"✗ Erro aula {lesson_id}: {str(e)}")
                db.session.rollback()
                errors += 1
        
        print("\n" + "="*70)
        print(f"Resultado: {updated} aula(s) | Erros: {errors}")
        print("="*70)

if __name__ == "__main__":
    try:
        update_course2()
        print("\n✓ Curso 2 atualizado com português correto!")
    except Exception as e:
        print(f"\n✗ Erro: {e}")
