# -*- coding: utf-8 -*-
"""
Corrige o conteúdo das aulas do Curso 1 que estão com encoding corrompido.
Os caracteres acentuados foram armazenados com codificação errada (latin-1/cp1252
lidos como ASCII), resultando em: Û→ê, Ò→ão, þ→ç, Ú→é, ß→á, ·→ú, ¾→ó/ô, etc.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.lesson import Lesson

app = create_app()

# ─────────────────────────────────────────────────────────────────────────────
# CONTEÚDO CORRIGIDO DAS 6 AULAS DO CURSO 1
# ─────────────────────────────────────────────────────────────────────────────

AULA26_CONTEUDO = """
<div class="aula-container">
    <h1>Bem-vindo ao Sistema INFANT.ID</h1>

    <h2>O que você vai aprender neste módulo</h2>
    <p>Bem-vindo ao INFANT.ID! Nesta primeira aula, você conhecerá o sistema de
identificação biométrica infantil mais avançado do Brasil.</p>

    <h3>Objetivos da Plataforma</h3>
    <ul>
        <li><strong>Segurança Máxima:</strong> Coleta biométrica segura e LGPD-compliant</li>
        <li><strong>Eficiência:</strong> Reduz tempo de atendimento em hospitais</li>
        <li><strong>Confiabilidade:</strong> Identificação unívoca de pacientes pediátricos</li>
        <li><strong>Integração:</strong> Funciona com sistemas hospitalares existentes</li>
    </ul>

    <h3>Público-alvo</h3>
    <p>Este treinamento é voltado para:</p>
    <ul>
        <li>Profissionais de saúde (médicos, enfermeiros, técnicos)</li>
        <li>Administradores de sistemas hospitalares</li>
        <li>Pessoal de TI responsável pela integração</li>
        <li>Gestores de qualidade em saúde</li>
    </ul>

    <h3>Duração Total do Módulo</h3>
    <p><strong>2 horas</strong> divididas em 6 aulas práticas</p>

    <div class="destaque">
        <h4>Próximos Passos</h4>
        <p>Prossiga para a próxima aula: "Princípios de Biometria Infantil"</p>
    </div>
</div>
"""

AULA27_CONTEUDO = """
<div class="aula-container">
    <h1>Fundamentos da Biometria Infantil</h1>

    <h2>O que é Biometria?</h2>
    <p>Biometria é a medição e análise estatística dos padrões únicos de
características físicas e de comportamento.
No INFANT.ID, usamos múltiplas modalidades biométricas para identificação
infantil segura.</p>

    <h3>Modalidades Biométricas Suportadas</h3>
    <table class="tabela-conteudo">
        <tr>
            <th>Modalidade</th>
            <th>Características</th>
            <th>Idade Mínima</th>
            <th>Confiabilidade</th>
        </tr>
        <tr>
            <td><strong>Impressão Digital</strong></td>
            <td>Padrões únicos das cristas papilares</td>
            <td>6 meses</td>
            <td>99,9%</td>
        </tr>
        <tr>
            <td><strong>Íris</strong></td>
            <td>Padrão das estruturas da íris</td>
            <td>Nascimento</td>
            <td>99,99%</td>
        </tr>
        <tr>
            <td><strong>Foto Facial</strong></td>
            <td>Geometria e características faciais</td>
            <td>Nascimento</td>
            <td>98%</td>
        </tr>
        <tr>
            <td><strong>Voz</strong></td>
            <td>Padrões acústicos da voz</td>
            <td>3 meses</td>
            <td>97%</td>
        </tr>
    </table>

    <h2>Por que Biometria Infantil?</h2>
    <ul>
        <li><strong>Imutável:</strong> Diferente de documentos, não pode ser falsificada</li>
        <li><strong>Universal:</strong> Todos têm características biométricas</li>
        <li><strong>Permanente:</strong> Não muda ao longo da vida</li>
        <li><strong>Resistente:</strong> Funciona com variações de apresentação</li>
    </ul>

    <h2>Especificidades da Coleta Infantil</h2>
    <p>A coleta em crianças requer protocolos especiais:</p>
    <ul>
        <li>Consentimento informado dos responsáveis</li>
        <li>Equipamento adaptado para pequenas mãos</li>
        <li>Ambiente acolhedor e seguro</li>
        <li>Procedimentos rápidos e indolores</li>
        <li>Cumprimento da LGPD e resoluções éticas</li>
    </ul>

    <div class="dica">
        <strong>Dica Importante:</strong> Sempre priorize o bem-estar da criança
durante qualquer coleta biométrica.
    </div>
</div>
"""

AULA28_CONTEUDO = """
<div class="aula-container">
    <h1>Equipamentos e Sensores do INFANT.ID</h1>

    <h2>Scanner de Impressão Digital</h2>
    <p>Captura os padrões únicos das cristas papilares das digitais.</p>
    <ul>
        <li><strong>Tecnologia:</strong> Sensor óptico de alta resolução (1000 DPI)</li>
        <li><strong>Tempo de captura:</strong> 2-3 segundos</li>
        <li><strong>Iluminação:</strong> LED verde para melhor contraste</li>
        <li><strong>Certificação:</strong> ISO/IEC 19794-2</li>
    </ul>

    <h2>Câmera Facial</h2>
    <p>Captura a geometria facial para identificação por reconhecimento facial.</p>
    <ul>
        <li><strong>Resolução:</strong> 8MP, auto-foco</li>
        <li><strong>Distância:</strong> 30-60cm (ideal para crianças)</li>
        <li><strong>Iluminação:</strong> Sistema IR para funcionar em qualquer condição</li>
        <li><strong>Certificação:</strong> ISO/IEC 39794-5</li>
    </ul>

    <h2>Leitor de Íris</h2>
    <p>Tecnologia mais avançada de identificação biométrica.</p>
    <ul>
        <li><strong>Alcance:</strong> 10-35cm (maior liberdade de movimento)</li>
        <li><strong>Análise:</strong> 400+ pontos de características únicas</li>
        <li><strong>Velocidade:</strong> Menos de 1 segundo</li>
        <li><strong>Certificação:</strong> ISO/IEC 19794-6</li>
    </ul>

    <h2>Microfone Biométrico</h2>
    <p>Coleta padrões acústicos para verificação de voz.</p>
    <ul>
        <li><strong>Frequência:</strong> 16-48 kHz</li>
        <li><strong>Ruído Ambiente:</strong> Cancelamento ativo até 65dB</li>
        <li><strong>Frase-senha:</strong> 3-5 palavras para máxima segurança</li>
        <li><strong>Certificação:</strong> ISO/IEC 19794-13</li>
    </ul>

    <h2>Protocolo de Validação</h2>
    <div class="protocolo">
        <ol>
            <li><strong>Captura:</strong> Obter dados biométricos de qualidade</li>
            <li><strong>Pré-processamento:</strong> Normalizar e otimizar imagem</li>
            <li><strong>Extração:</strong> Extrair características únicas</li>
            <li><strong>Comparação:</strong> Comparar com base de dados</li>
            <li><strong>Decisão:</strong> Gerar score de confiança</li>
        </ol>
    </div>
</div>
"""

AULA29_CONTEUDO = """
<div class="aula-container">
    <h1>Procedimento de Coleta Biométrica</h1>

    <h2>Preparação</h2>
    <ul class="checklist">
        <li><input type="checkbox" disabled> Verificar se todos os equipamentos estão calibrados</li>
        <li><input type="checkbox" disabled> Confirmar identidade da criança e responsável</li>
        <li><input type="checkbox" disabled> Obter consentimento informado assinado</li>
        <li><input type="checkbox" disabled> Explicar o procedimento à criança de forma amigável</li>
        <li><input type="checkbox" disabled> Garantir ambiente confortável e bem iluminado</li>
    </ul>

    <h2>Fase 1: Coleta de Impressões Digitais (5 min)</h2>
    <div class="passo">
        <h3>Passo 1: Posicionamento</h3>
        <p>Coloque a mão da criança no scanner com o dedo indicador primeiro.</p>
        <p><strong>Dica:</strong> Se a criança estiver nervosa, deixe-a explorar o equipamento antes.</p>
    </div>

    <div class="passo">
        <h3>Passo 2: Captura</h3>
        <p>Pressione suavemente por 2-3 segundos. O sistema confirma com beep sonoro.</p>
        <p><strong>Alerta:</strong> Não pressione com força excessiva!</p>
    </div>

    <div class="passo">
        <h3>Passo 3: Validação</h3>
        <p>Sistema exibe qualidade da captura (verde = OK, vermelho = repetir).</p>
    </div>

    <h2>Fase 2: Captura de Foto Facial (3 min)</h2>
    <div class="passo">
        <h3>Passo 1: Posicionamento</h3>
        <p>Posicione a criança a 45cm da câmera. Olhos alinhados com a linha central.</p>
    </div>

    <div class="passo">
        <h3>Passo 2: Captura</h3>
        <p>Sistema captura automaticamente quando detecta rosto frontal com boa iluminação.</p>
    </div>

    <div class="passo">
        <h3>Passo 3: Validação</h3>
        <p>Verificar se olhos e boca estão abertos e o rosto está claro.</p>
    </div>

    <h2>Fase 3: Leitura de Íris (2 min)</h2>
    <div class="passo">
        <h3>Passo 1: Orientação</h3>
        <p>"Olhe para o ponto de luz vermelho à sua frente"</p>
    </div>

    <div class="passo">
        <h3>Passo 2: Captura</h3>
        <p>Sistema captura quando detecta a íris com padrões visíveis.</p>
        <p><strong>Importante:</strong> Capturar ambos os olhos (esquerdo + direito)</p>
    </div>

    <h2>Fase 4: Gravação de Voz (1 min)</h2>
    <div class="passo">
        <h3>Instruções</h3>
        <p>Peça à criança que diga a frase fornecida pelo sistema (ex: "Meu nome é...")</p>
    </div>

    <h2>Finalização</h2>
    <ul>
        <li>Sistema processa e gera ID biométrico único</li>
        <li>Imprimir recibo de coleta</li>
        <li>Solicitar assinatura do responsável</li>
        <li>Registrar observações especiais (cicatrizes, etc.)</li>
        <li>Entregar cópia ao responsável</li>
    </ul>

    <div class="aviso">
        <strong>Importante:</strong> Se qualquer coleta falhar mais de 3 vezes,
pausar e tentar outro dia.
    </div>
</div>
"""

AULA30_CONTEUDO = """
<div class="aula-container">
    <h1>Segurança e Conformidade LGPD</h1>

    <h2>Criptografia de Dados</h2>
    <p>Todos os dados biométricos são criptografados em múltiplas camadas:</p>
    <ul>
        <li><strong>Em Trânsito:</strong> TLS 1.3 (256-bit)</li>
        <li><strong>Em Repouso:</strong> AES-256 (grau militar)</li>
        <li><strong>Hash Biométrico:</strong> SHA-3 + salting aleatório</li>
        <li><strong>Backup:</strong> Replicado em datacenters SEC-3</li>
    </ul>

    <h2>Conformidade LGPD</h2>
    <p>O INFANT.ID opera em total conformidade com a Lei Geral de Proteção de Dados:</p>
    <table class="tabela-conformidade">
        <tr>
            <th>Artigo LGPD</th>
            <th>Requisito</th>
            <th>Implementação INFANT.ID</th>
        </tr>
        <tr>
            <td>Art. 5</td>
            <td>Consentimento</td>
            <td>Formulário de consentimento digital assinado</td>
        </tr>
        <tr>
            <td>Art. 7</td>
            <td>Base Legal</td>
            <td>Consentimento + exercício de direitos</td>
        </tr>
        <tr>
            <td>Art. 13</td>
            <td>Transparência</td>
            <td>Política clara disponível no sistema</td>
        </tr>
        <tr>
            <td>Art. 30</td>
            <td>Direito de Acesso</td>
            <td>Portal do responsável com dados digitalizados</td>
        </tr>
        <tr>
            <td>Art. 35</td>
            <td>DIA - Direito de Esquecimento</td>
            <td>Exclusão automática ou sob demanda</td>
        </tr>
    </table>

    <h2>Direitos do Titular (Criança)</h2>
    <ul>
        <li><strong>Acesso:</strong> Responsável pode solicitar dados coletados</li>
        <li><strong>Retificação:</strong> Corrigir dados imprecisos</li>
        <li><strong>Exclusão:</strong> Solicitar apagamento permanente</li>
        <li><strong>Portabilidade:</strong> Transferir dados para outro sistema</li>
        <li><strong>Oposição:</strong> Recusar processamento por motivo legítimo</li>
    </ul>

    <h2>Retenção de Dados</h2>
    <p>Política de retenção conforme regulamentações:</p>
    <ul>
        <li><strong>Dados Ativos (0-7 anos):</strong> Mantidos para identificação</li>
        <li><strong>Dados Inativos (7-10 anos):</strong> Arquivados, sem acesso regular</li>
        <li><strong>Dados Arquivados (&gt;10 anos):</strong> Apagamento automático</li>
        <li><strong>Exceção:</strong> Se requerer investigação legal, retém conforme necessário</li>
    </ul>

    <h2>Incidente de Segurança</h2>
    <p>Em caso de violação de dados:</p>
    <ol>
        <li>Notificar responsável em até 48 horas</li>
        <li>Informar autoridade de proteção de dados</li>
        <li>Fornecer medidas de mitigação</li>
        <li>Auditoria completa para identificação da causa raiz</li>
    </ol>
</div>
"""

AULA31_CONTEUDO = """
<div class="aula-container">
    <h1>Troubleshooting e Melhores Práticas</h1>

    <h2>Problemas Comuns</h2>

    <h3>Problema: Dígito não reconhecido</h3>
    <p><strong>Causa:</strong> Dedo muito seco, sujo ou com ferimento</p>
    <p><strong>Solução:</strong></p>
    <ul>
        <li>Hidratar a ponta do dedo com loção neutra</li>
        <li>Limpar dedo em pano úmido branco</li>
        <li>Se há ferimento, tentar outro dedo</li>
        <li>Ajustar pressão levemente</li>
    </ul>

    <h3>Problema: Foto facial borrada</h3>
    <p><strong>Causa:</strong> Movimento da cabeça, luz insuficiente ou muito brilho</p>
    <p><strong>Solução:</strong></p>
    <ul>
        <li>Reduzir brilho incidindo luz lateralmente</li>
        <li>Pedir à criança para ficar imóvel</li>
        <li>Aproximar ou afastar adequadamente</li>
        <li>Limpar lente com pano estéril</li>
    </ul>

    <h3>Problema: Íris não detectada</h3>
    <p><strong>Causa:</strong> Criança com olhos muito fechados ou reflexos muito altos</p>
    <p><strong>Solução:</strong></p>
    <ul>
        <li>Ajustar ângulo da câmera</li>
        <li>Aumentar iluminação ambiente</li>
        <li>Deixar criança piscar e tentar novamente</li>
        <li>Se uso de óculos, remover para captura</li>
    </ul>

    <h2>Melhores Práticas</h2>

    <h3>Antes da Coleta</h3>
    <ul class="checkmark">
        <li>Testar todos os equipamentos no início do dia</li>
        <li>Revisar lista de contatos de emergência</li>
        <li>Preparar formulários de consentimento</li>
        <li>Criar ambiente amigável e lúdico</li>
    </ul>

    <h3>Durante a Coleta</h3>
    <ul class="checkmark">
        <li>Ser paciente e calmo com a criança nervosa</li>
        <li>Explicar cada passo em linguagem infantil</li>
        <li>Dar feedback positivo ("Muito bem!")</li>
        <li>Manter temperatura ambiente confortável</li>
        <li>Ter pais/responsáveis próximos para conforto</li>
    </ul>

    <h3>Após a Coleta</h3>
    <ul class="checkmark">
        <li>Revisar qualidade de todos os dados capturados</li>
        <li>Documentar qualquer situação anormal</li>
        <li>Fazer upload seguro ao sistema após revisão</li>
        <li>Arquivar documentação assinada</li>
        <li>Fazer backup de dados críticos</li>
    </ul>

    <h2>Dicas de Ouro</h2>
    <p><strong>🍼 Para crianças muito pequenas (0-3 anos):</strong> Coletar quando dormindo ou imediatamente após alimentação.</p>
    <p><strong>😰 Para crianças nervosas:</strong> Permitir brincar com o equipamento antes para ganhar confiança.</p>
    <p><strong>♿ Para crianças com deficiência:</strong> Adaptar protocolo conforme necessidade individual.</p>
    <p><strong>⭐ Dica Geral:</strong> Qualidade &gt; Velocidade. Uma coleta boa vale mais que 10 ruins.</p>
</div>
"""

# ─────────────────────────────────────────────────────────────────────────────
# APLICAR CORREÇÕES
# ─────────────────────────────────────────────────────────────────────────────

CORRECOES = {
    26: AULA26_CONTEUDO,
    27: AULA27_CONTEUDO,
    28: AULA28_CONTEUDO,
    29: AULA29_CONTEUDO,
    30: AULA30_CONTEUDO,
    31: AULA31_CONTEUDO,
}

with app.app_context():
    print("\n" + "="*60)
    print("CORREÇÃO DE ENCODING — CURSO 1 (IDs 26-31)")
    print("="*60)

    for aid, novo_conteudo in CORRECOES.items():
        aula = db.session.get(Lesson, aid)
        if aula:
            aula.conteudo = novo_conteudo.strip()
            print(f"  ✅ Aula {aid} corrigida: {aula.titulo}")
        else:
            print(f"  ❌ Aula {aid} não encontrada!")

    db.session.commit()
    print("\n✅ TODAS AS CORREÇÕES SALVAS COM SUCESSO!")
    print("="*60)
