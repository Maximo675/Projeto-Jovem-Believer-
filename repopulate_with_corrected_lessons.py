#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para REPOETUALIZAR o banco de dados com aulas corrigidas do lessons_course2_portuguese.py
Use este script para substituir as aulas com as versões corretas de português
"""

import sys
from pathlib import Path

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app import create_app, db
from app.models.course import Course
from app.models.lesson import Lesson

# Importar aulas corrigidas
sys.path.insert(0, str(Path(__file__).parent))
from lessons_course2_portuguese import LESSONS_COURSE2_PORTUGUESE

def update_course_lessons(course_name, lessons_dict):
    """Atualiza aulas de um curso com dados corrigidos"""
    
    app = create_app()
    with app.app_context():
        # Encontrar curso
        curso = Course.query.filter_by(titulo=course_name).first()
        if not curso:
            print(f"❌ Curso '{course_name}' não encontrado")
            return False
        
        print(f"📝 Atualizando curso: {course_name}")
        print(f"   ID do curso: {curso.id}")
        
        # Deletar aulas antigas
        old_count = Lesson.query.filter_by(curso_id=curso.id).count()
        Lesson.query.filter_by(curso_id=curso.id).delete()
        db.session.commit()
        print(f"   🗑️  Deletadas {old_count} aulas antigas")
        
        # Adicionar novas aulas
        added = 0
        for lesson_id, lesson_data in lessons_dict.items():
            if lesson_data.get('course_id') == 2:  # Apenas aulas do curso 2
                aula = Lesson(
                    curso_id=curso.id,
                    titulo=lesson_data.get('title'),
                    descricao='Conteúdo estruturado com textos, exemplos e procedimentos',
                    conteudo=lesson_data.get('content'),
                    ordem=lesson_data.get('id', lesson_id),
                    duracao=lesson_data.get('duration'),
                    video_url=lesson_data.get('video_url'),
                    ativo=True
                )
                db.session.add(aula)
                added += 1
                print(f"   ✅ {lesson_data.get('title')}")
        
        db.session.commit()
        print(f"\n✅ {added} aulas atualizadas com sucesso!")
        return True

if __name__ == "__main__":
    print("=" * 60)
    print("ATUALIZAR AULAS COM PORTUGUÊS CORRETO")
    print("=" * 60)
    
    update_course_lessons("Integração Hospitalar", LESSONS_COURSE2_PORTUGUESE)
    
    print("\n" + "=" * 60)
    print("✅ PROCESSO CONCLUÍDO!")
    print("=" * 60)
