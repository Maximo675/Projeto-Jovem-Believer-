"""
Script para CORRIGIR TODOS OS ERROS DE PORTUGUÊS no site
Aplica todas as correções de acentuação e ortografia
"""

import os
import re

# Mapa de correções de português
PORTUGUESE_FIXES = {
    # Acentuação e caracteres especiais
    'Segurana': 'Segurança',
    'Mxima': 'Máxima',
    'biomtrica': 'biométrica',
    'biomtricas': 'biométricas',
    'biomtrico': 'biométrico',
    'Integrao': 'Integração',
    'Confiabilidade:': 'Confiabilidade:',  # Já ok
    'Identificao': 'Identificação',
    'unvocêa': 'unívoca',
    'peditricos': 'pediátricos',
    'Pblico': 'Público',
    'alvo': 'alvo',  # Já ok
    'sade': 'saúde',
    'mdicos': 'médicos',
    'enfermeiros,': 'enfermeiros,',  # Já ok
    'tcúnicos': 'técnicos',
    'responsvel': 'responsável',
    'Durao': 'Duração',
    'prticas': 'práticas',
    'Prximos': 'Próximos',
    'Princpios': 'Princípios',
    'Caractersticas': 'Características',
    'Mnima': 'Mínima',
    'cÍristas': 'cristas',
    'Imutvel': 'Imutável',
    'falificada': 'falsificada',
    'tm': 'têm',
    'No': 'Não',
    'muda': 'muda',  # Já ok
    'variaes': 'variações',
    'apresentao': 'apresentação',
    'rpidos': 'rápidos',
    'indolores': 'indolores',  # Já ok
    'resolues': 'resoluções',
    'ticas': 'éticas',
    'criana': 'criança',
    'crianas': 'crianças',
    'responsveis': 'responsáveis',
    'mos': 'mãos',
    'acolhedor': 'acolhedor',  # Já ok
    'bem-estar': 'bem-estar',  # Já ok
    'cmera': 'câmera',
    'iluminao': 'iluminação',
    'ptico': 'óptico',
    'dilogos': 'diálogos',
    'estruturas': 'estruturas',  # Já ok
    'caractersticas': 'características',
    'Padres': 'Padrões',
    'Universal:': 'Universal:',  # Já ok
    'Permanente:': 'Permanente:',  # Já ok
    'Resistente:': 'Resistente:',  # Já ok
    'resoluo': 'resolução',
    'verificao': 'verificação',
    'Anlise': 'Análise',
    'nicas': 'únicas',
    'Velocidade:': 'Velocidade:',  # Já ok
    'Microfone': 'Microfone',  # Já ok
    'Freqência': 'Frequência',
    'Rudo': 'Ruído',
    'at': 'até',
    'mxima': 'máxima',
    'Protocolo': 'Protocolo',  # Já ok
    'Validao': 'Validação',
    'Pr-processamento': 'Pré-processamento',
    'Extrao': 'Extração',
    'Comparao': 'Comparação',
    'confiana': 'confiança',
    'Preparao': 'Preparação',
    'esto': 'estão',
    'procedure': 'procedimento',
    'confortvel': 'confortável',
    'bem': 'bem',  # Já ok
    'Impresses': 'Impressões',
    'Posicionamento': 'Posicionamento',  # Já ok
    'dedo': 'dedo',  # Já ok
    'Dica:': 'Dica:',  # Já ok
    'explorar': 'explorar',  # Já ok
    'equipamento': 'equipamento',  # Já ok
    'Captura': 'Captura',  # Já ok
    'Pressione': 'Pressione',  # Já ok
    'suavemente': 'suavemente',  # Já ok
    'beep': 'beep',  # Já ok
    'No': 'Não',
    'Alerta:': 'Alerta:',  # Já ok
    'Validao': 'Validação',
    'claro': 'claro',  # Já ok
    'Orientao': 'Orientação',
    'ponto': 'ponto',  # Já ok
    'visveis': 'visíveis',
    'Importante:': 'Importante:',  # Já ok
    'Instrues': 'Instruções',
    'Pea': 'Peça',
    'frase': 'frase',  # Já ok
    'Finalizao': 'Finalização',
    'gera': 'gera',  # Já ok
    'ID': 'ID',  # Já ok
    'nico': 'único',
    'recibo': 'recibo',  # Já ok
    'assinatura': 'assinatura',  # Já ok
    'observaes': 'observações',
    'especiais': 'especiais',  # Já ok
    'cicatrizes': 'cicatrizes',  # Já ok
    'copia': 'cópia',
    'pausar': 'pausar',  # Já ok
    'tentar': 'tentar',  # Já ok
    'outro': 'outro',  # Já ok
    'Segurana': 'Segurança',
    'Conformidade': 'Conformidade',  # Já ok
    'Criptografia': 'Criptografia',  # Já ok
    'Trnsito': 'Trânsito',
    'Repouso:': 'Repouso:',  # Já ok
    # Adicionar mais conforme necessário
}

def fix_portuguese_in_file(filepath):
    """Corrige todos os erros de português em um arquivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Aplicar todas as correções
        for wrong, correct in PORTUGUESE_FIXES.items():
            # Case-insensitive replacement mantendo case
            def replace_func(match):
                text = match.group(0)
                if text.isupper():
                    return correct.upper()
                elif text[0].isupper():
                    return correct[0].upper() + correct[1:]
                else:
                    return correct.lower()
            
            # Usar regex com word boundaries quando possível
            pattern = r'\b' + re.escape(wrong) + r'\b'
            content = re.sub(pattern, replace_func, content, flags=re.IGNORECASE)
        
        # Se houve mudanças, salvar arquivo
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"❌ Erro ao processar {filepath}: {e}")
        return False

def main():
    """Processa todos os arquivos necessários"""
    print("\n" + "="*70)
    print("CORRIGINDO PORTUGUÊS EM TODO O SITE")
    print("="*70 + "\n")
    
    files_to_fix = [
        r'c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\backend\populate_lessons_content.py',
        r'c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\pages\dashboard.html',
        r'c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\pages\course.html',
        r'c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\pages\login.html',
        r'c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\pages\register.html',
        r'c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\pages\ia-chat.html',
    ]
    
    fixed_count = 0
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            if fix_portuguese_in_file(filepath):
                print(f"✅ Corrigido: {os.path.basename(filepath)}")
                fixed_count += 1
            else:
                print(f"⊘ Nenhuma alteração: {os.path.basename(filepath)}")
        else:
            print(f"❓ Arquivo não encontrado: {filepath}")
    
    print(f"\n{'='*70}")
    print(f"Total de arquivos corrigidos: {fixed_count}")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    main()
