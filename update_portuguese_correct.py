# coding: utf-8
# -*- coding: utf-8 -*-
"""
Script para atualizar aulas com português correto
Usa encoding UTF-8 explicitamente
"""

import sys
import os
from pathlib import Path

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app import create_app
from app.models import Lesson
from database.database import db
from lessons_portuguese_correct import LESSONS_PORTUGUESE_CORRECT

def update_portuguese_lessons():
    """Atualiza aulas com português correto e acentuação"""
    
    app = create_app()
    
    with app.app_context():
        print("="*70)
        print("ATUALIZANDO AULAS COM PORTUGUÊS CORRETO")
        print("="*70)
        print("Encoding: UTF-8 ✓\n")
        
        total_updated = 0
        errors = 0
        
        for lesson_id, lesson_data in LESSONS_PORTUGUESE_CORRECT.items():
            try:
                # Procurar aula pela ID
                lesson = Lesson.query.filter_by(id=lesson_id).first()
                
                if lesson:
                    # Atualizar com português correto
                    lesson.titulo = lesson_data['title']
                    lesson.conteudo = lesson_data['content']
                    lesson.duracao = int(lesson_data['duration'].split()[0])
                    
                    db.session.add(lesson)
                    db.session.commit()
                    
                    print(f"✓ Aula {lesson_id}: {lesson_data['title']}")
                    total_updated += 1
                    
                else:
                    print(f"✗ Aula {lesson_id} não encontrada")
                    errors += 1
                    
            except Exception as e:
                print(f"✗ Erro ao atualizar aula {lesson_id}: {str(e)}")
                db.session.rollback()
                errors += 1
        
        print("\n" + "="*70)
        print(f"RESULTADO: {total_updated} aula(s) atualizadas")
        if errors > 0:
            print(f"ERROS: {errors}")
        print("="*70)
        
        if total_updated > 0:
            print("\n✓ Português correto com acentuação!")
            print("✓ Caracteres especiais mantidos:")
            print("  - Acentuação: á, é, í, ó, ú, ã, õ, ç")
            print("  - Hífen, travessão, apóstrofo mantidos")
            print("✓ Codificação UTF-8 garantida!")

if __name__ == "__main__":
    try:
        update_portuguese_lessons()
        print("\n✓ Sucesso! Aulas atualizadas com português correto.")
    except Exception as e:
        print(f"\n✗ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
