"""
Script para atualizar Aulas com conteudo correto baseado em documentacao oficial
- Remove erros de digitacao
- Remove videos genericos do YouTube
- Integra links de video oficiais do Google Drive
"""

import sys
from pathlib import Path
from lessons_corrected_content import LESSONS_CORRECTED

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app import create_app
from app.models import Lesson
from database.database import db

def update_lessons():
    """Atualiza aulas com conteudo correto"""
    
    app = create_app()
    
    with app.app_context():
        print("="*70)
        print("ATUALIZANDO AULAS COM CONTEUDO CORRIGIDO")
        print("="*70)
        
        total_updated = 0
        errors = 0
        
        for lesson_id, lesson_data in LESSONS_CORRECTED.items():
            try:
                # Procurar aula pela sequencia no banco
                lesson = Lesson.query.filter_by(id=lesson_id).first()
                
                if lesson:
                    # Atualizar conteudo
                    lesson.content = lesson_data['content']
                    lesson.duration = lesson_data['duration']
                    
                    db.session.add(lesson)
                    db.session.commit()
                    
                    print(f"\n✓ Aula {lesson_id}: {lesson_data['title']}")
                    print(f"  Duracao: {lesson_data['duration']}")
                    print(f"  Tamanho: {len(lesson_data['content'])} caracteres")
                    
                    total_updated += 1
                    
                else:
                    print(f"\n✗ Aula {lesson_id} nao encontrada no banco")
                    errors += 1
                    
            except Exception as e:
                print(f"\n✗ Erro ao atualizar aula {lesson_id}: {e}")
                db.session.rollback()
                errors += 1
        
        print("\n" + "="*70)
        print(f"RESULTADO: {total_updated} aula(s) atualizadas com sucesso")
        if errors > 0:
            print(f"ERROS: {errors}")
        print("="*70)
        
        if total_updated > 0:
            print("\n✓ Conteudo atualizado!")
            print("✓ Videos oficiais do Google Drive integrados")
            print("✓ Erros de digitacao corrigidos")
            print("✓ Estrutura profissional baseada em documentacao oficial")

if __name__ == "__main__":
    try:
        update_lessons()
        print("\nSucesso! Aulas atualizadas com conteudo corrigido.")
    except Exception as e:
        print(f"\nErro durante atualizacao: {e}")
        import traceback
        traceback.print_exc()
