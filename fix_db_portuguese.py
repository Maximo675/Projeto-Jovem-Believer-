"""
Corrige os erros de português no banco de dados directamente
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app, db
from app.models.course import Course

# Mapa de correções
CORRECOES = {
    'Mdulo': 'Módulo',
    'Integrao': 'Integração',
    'Usurios': 'Usuários',
    'Operaes': 'Operações',
    'Implementao': 'Implementação',
    'Lei Geral de Proteo': 'Lei Geral de Proteção',
}

app = create_app()
with app.app_context():
    cursos = Course.query.all()
    
    print('🔧 Corrigindo português no banco de dados...\n')
    
    for curso in cursos:
        original_titulo = curso.titulo
        novo_titulo = curso.titulo
        
        for wrong, correct in CORRECOES.items():
            novo_titulo = novo_titulo.replace(wrong, correct)
        
        if original_titulo != novo_titulo:
            print(f'  "{original_titulo}" → "{novo_titulo}"')
            curso.titulo = novo_titulo
            db.session.commit()
    
    print(f'\n✅ Correções aplicadas com sucesso!')
