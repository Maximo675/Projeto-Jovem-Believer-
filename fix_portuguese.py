#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir erros de português no populate_lessons_content.py
"""

import re
from pathlib import Path

file_path = Path("backend/populate_lessons_content.py")
content = file_path.read_text(encoding='utf-8')

# Mapeamento de erros para correções
corrections = {
    # Acentuação em palavras
    'Mdulo': 'Módulo',
    'Apresentao': 'Apresentação',
    'voc': 'você',
    'Princpios': 'Princípios',
    'biomtricos': 'biométricos',
    'crianas': 'crianças',
    'Biometria': 'Biometria',
    'medio': 'medição',
    'anlise': 'análise',
    'estatstica': 'estatística',
    'padres': 'padrões',
    'nicos': 'únicos',
    'caractersticas': 'características',
    'fsicas': 'físicas',
    'mltiplas': 'múltiplas',
    'biomtricas': 'biométricas',
    'identificao': 'identificação',
    'Impresso': 'Impressão',
    'Equipamentos': 'Equipamentos',
    'Conhea': 'Conheça',
    'nicos': 'únicos',
    'ptico': 'óptico',
    'resoluo': 'resolução',
    'Iluminao': 'Iluminação',
    'Certificao': 'Certificação',
    'Cmera': 'Câmera',
    'Distncia': 'Distância',
    'Iluminao': 'Iluminação',
    'condio': 'condição',
    'ris': 'Íris',
    'Padro': 'Padrão',
    'Padres': 'Padrões',
    'acsticos': 'acústicos',
    'Protocolo': 'Protocolo',
}

# Aplicar correções
for old, new in corrections.items():
    content = content.replace(old, new)

# Salvar arquivo corrigido
file_path.write_text(content, encoding='utf-8')

print("✅ Arquivo corrigido com sucesso!")
print("📝 Erros de português foram corrigidos em populate_lessons_content.py")
