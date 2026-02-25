#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar video_url das aulas com os links corretos do Google Drive
"""

from pathlib import Path

file_path = Path("backend/populate_lessons_content.py")
content = file_path.read_text(encoding='utf-8')

# URLs dos vídeos do Google Drive (conforme disponibilizado)
video_urls = {
    # Curso 1 - Onboarding INFANT.ID
    'Bem-vindo ao INFANT.ID': '',  # Necessário obter
    'Princípios de Biometria Infantil': '',
    'Equipamentos e Sensores': '',
    'Protocolo de Coleta Passo a Passo': '',
    'Preparação e Higiene para Coleta': '',
    'Compreendendo Documentos e Consentimento': '',
    
    # Curso 2 - Integração Hospitalar
    'Seleção do Recém-nascido': 'https://drive.google.com/file/d/1uOILNO0clQYeP9PFpuvkaP1h4570kaRA/view?usp=sharing',
    'Preparação do Recém-nascido': 'https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link',
    'Etapa 3: Captura Biométrica da Progenitora': 'https://drive.google.com/file/d/1g55icK4TUhLpQxwsTgPbV0e09td8K8ln/view?usp=drive_link',
    'Etapa 4: Captura Biométrica do Recém-nascido': 'https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link',
    'Verificação e Qualidade de Captura': 'https://drive.google.com/file/d/1vKSLvP5WolPnjJa4y6ylrP9-rkvPwUqs/view?usp=drive_link',
}

# Substituir as URLs dos vídeos
for titulo, url in video_urls.items():
    if url:
        # Padrão para encontrar a linha de video_url para cada aula
        pattern = f"'titulo': '{titulo}',.*?'video_url': '.*?',"
        replacement = f"'titulo': '{titulo}', 'video_url': '{url}',"
        # Se não funcionar a regex, fazer por linha mais simples
        
print("✅ Script preparado!")
print("📝 Links de vídeos mapeados:")
for titulo, url in video_urls.items():
    if url:
        print(f"  ✓ {titulo}")
    else:
        print(f"  ✗ {titulo} (não foi fornecido)")

# Salvar para referência
Path("video_mapping.txt").write_text(
    "\n".join([f"{titulo}: {url}" for titulo, url in video_urls.items()]),
    encoding='utf-8'
)
print("\n📄 Mapeamento salvo em video_mapping.txt")
