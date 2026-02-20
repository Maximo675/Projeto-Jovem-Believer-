"""
Script para atualizar aulas do Curso 3 com conteudo sobre
Seguranca, Manutencao, Conformidade e Auditoria
"""

import sys
from pathlib import Path
from lessons_course3_content import LESSONS_COURSE3

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app import create_app
from app.models import Lesson
from database.database import db

def update_course3_lessons():
    """Atualiza aulas do Curso 3"""
    
    app = create_app()
    
    with app.app_context():
        print("="*70)
        print("ATUALIZANDO AULAS DO CURSO 3 (GERENCIAMENTO DE USUARIOS)")
        print("="*70)
        
        total_updated = 0
        created = 0
        errors = 0
        
        for lesson_id, lesson_data in LESSONS_COURSE3.items():
            try:
                # Procurar aula pela ID
                lesson = Lesson.query.filter_by(id=lesson_id).first()
                
                if lesson:
                    # Atualizar conteudo existente
                    lesson.titulo = lesson_data['title']
                    lesson.conteudo = lesson_data['content']
                    lesson.duracao = int(lesson_data['duration'].split()[0])
                    
                    db.session.add(lesson)
                    db.session.commit()
                    
                    print(f"\n✓ Atualizado - Aula {lesson_id}: {lesson_data['title']}")
                    total_updated += 1
                    
                else:
                    # Criar nova aula se nao existir
                    new_lesson = Lesson(
                        curso_id=lesson_data['course_id'],
                        titulo=lesson_data['title'],
                        descricao=lesson_data['title'],
                        conteudo=lesson_data['content'],
                        ordem=lesson_id,
                        duracao=int(lesson_data['duration'].split()[0])
                    )
                    
                    db.session.add(new_lesson)
                    db.session.commit()
                    
                    print(f"\n✓ Criada - Aula {lesson_id}: {lesson_data['title']}")
                    created += 1
                    
            except Exception as e:
                print(f"\n✗ Erro ao processar aula {lesson_id}: {e}")
                db.session.rollback()
                errors += 1
        
        print("\n" + "="*70)
        print(f"RESULTADO:")
        print(f"  ✓ Atualizadas: {total_updated}")
        print(f"  ✓ Criadas: {created}")
        if errors > 0:
            print(f"  ✗ Erros: {errors}")
        print("="*70)
        
        if total_updated > 0 or created > 0:
            print("\n✓ Conteudo profissional implementado!")
            print("✓ Conformidade LGPD integrada!")
            print("✓ Seguranca e Manutencao documentadas!")

if __name__ == "__main__":
    try:
        update_course3_lessons()
        print("\nSucesso! Aulas do Curso 3 processadas.")
    except Exception as e:
        print(f"\nErro durante processamento: {e}")
        import traceback
        traceback.print_exc()
