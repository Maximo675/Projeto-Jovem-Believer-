#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Converter PDF para Markdown
Extrai conteúdo de PDF e converte para markdown estruturado
"""

import pdfplumber
import re
import os

def convert_pdf_to_markdown(pdf_path, output_path):
    """
    Converte PDF em Markdown com estrutura preservada
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            markdown_content = []
            markdown_content.append("# 📚 TREINAMENTO PARA REPLICADORES E ENFERMEIRAS\n")
            markdown_content.append("_Documento convertido de PDF_\n")
            markdown_content.append("---\n\n")
            
            current_section = ""
            
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                
                if not text:
                    continue
                
                # Limpar e processar linhas
                lines = text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    # Detectar títulos (linhas em CAPS)
                    if line.isupper() and len(line) > 5:
                        markdown_content.append(f"\n## {line}\n")
                        current_section = line
                    
                    # Detectar subtítulos
                    elif line.startswith(('1.', '2.', '3.', '4.', '5.', '•', '-')):
                        # Se for lista numerada
                        if re.match(r'^\d+\.', line):
                            markdown_content.append(f"- {line[2:].strip()}\n")
                        else:
                            markdown_content.append(f"  - {line[1:].strip()}\n")
                    
                    # Parágrafos normais
                    else:
                        if line and not line.startswith(('Página', 'INFANTID')):
                            # Evitar linhas de página
                            if len(line) > 3:
                                markdown_content.append(f"{line}\n\n")
            
            # Escrever arquivo
            full_markdown = "".join(markdown_content)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_markdown)
            
            print(f"✅ PDF convertido com sucesso!")
            print(f"📁 Arquivo salvo em: {output_path}")
            print(f"📄 Tamanho: {len(full_markdown)} caracteres")
            
            return full_markdown
            
    except Exception as e:
        print(f"❌ Erro ao converter PDF: {e}")
        return None

if __name__ == "__main__":
    pdf_file = r"C:\Users\maximo.silva\Downloads\[CS] TREINAMENTO REPLICADORES E ENFERMEIRAS.pdf"
    output_file = r"c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\notes\TREINAMENTO_REPLICADORES_ENFERMEIRAS.md"
    
    print("🔄 Convertendo PDF para Markdown...")
    print(f"📖 Origem: {pdf_file}")
    print(f"💾 Destino: {output_file}\n")
    
    convert_pdf_to_markdown(pdf_file, output_file)
