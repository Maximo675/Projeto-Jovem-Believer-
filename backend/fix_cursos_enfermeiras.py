"""
Corrige os cursos para o público-alvo: enfermeiras de maternidade.
Problemas corrigidos:
  1. Erros de codificação/português em títulos e descrições
  2. Curso 2 totalmente substituído: era sobre integração técnica de TI
     (Node.js, Python, curl, API keys...) e agora aborda o protocolo
     clínico de coleta biométrica, baseado nos materiais oficiais da INFANT.ID.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.course import Course
from app.models.lesson import Lesson

app = create_app()

# ─────────────────────────────────────────────────────────────────────────────
# CONTEÚDO DAS NOVAS AULAS DO CURSO 2
# Baseado nos documentos oficiais:
#   • Procedimento de Coleta.md
#   • Protocolo de Coleta Passo a Passo.md
#   • Informativo Etan.md
#   • Treinamento Replicadores Enfermeiras.md
# ─────────────────────────────────────────────────────────────────────────────

AULA2_1_TITULO = "Seleção do Recém-nascido e da Progenitora"
AULA2_1_DESC   = "Critérios para seleção correta do binômio mãe-bebê antes da coleta"
AULA2_1_CONTEUDO = """
<div class="aula-container">
    <h1>Seleção do Recém-nascido e da Progenitora</h1>

    <h2>Por que a seleção correta é essencial?</h2>
    <p>
        A coleta biométrica só deve ser realizada quando tanto a mãe (progenitora)
        quanto o recém-nascido (RN) estejam <strong>estáveis e fora de risco clínico</strong>.
        Uma seleção adequada garante a segurança do binômio e a qualidade dos dados coletados.
    </p>

    <h2>Critérios de Seleção</h2>
    <ul>
        <li>A seleção é feita pela <strong>equipe médica assistencial</strong> — não pela enfermeira replicadora sozinha.</li>
        <li>Tanto a mãe quanto o RN devem estar clínica e hemodinamicamente estáveis.</li>
        <li>A coleta <strong>não deve interromper</strong> a "Golden Hour" — o contato pele a pele entre mãe e bebê.</li>
        <li>O banho do RN deve ser adiado por pelo menos <strong>24 horas</strong> após o nascimento.</li>
        <li>O <strong>vernix caseoso</strong> (substância branca na pele do bebê) não deve ser removido ao nascer; ele protege a pele e será tratado no momento da coleta com soro de limpeza.</li>
    </ul>

    <h2>Golden Hour — Prioridade Máxima</h2>
    <div class="destaque-info">
        <p>
            A Golden Hour é o período imediatamente após o nascimento, dedicado ao vínculo
            entre mãe e bebê, amamentação e estabilização do RN. A biometria jamais
            deve competir com este momento. Aguarde a autorização da equipe médica.
        </p>
    </div>

    <h2>Checklist de Pré-Seleção</h2>
    <ul class="checklist">
        <li><input type="checkbox" disabled> Equipe médica autorizou a coleta</li>
        <li><input type="checkbox" disabled> RN está estável e fora de risco</li>
        <li><input type="checkbox" disabled> Progenitora está estável e consciente</li>
        <li><input type="checkbox" disabled> Golden Hour foi respeitada</li>
        <li><input type="checkbox" disabled> Banho do RN ainda não foi realizado</li>
    </ul>
</div>
"""

AULA2_2_TITULO = "Preparação para a Coleta Biométrica"
AULA2_2_DESC   = "Como posicionar mãe e RN, verificar dados biográficos e preparar os dedos para coleta"
AULA2_2_CONTEUDO = """
<div class="aula-container">
    <h1>Preparação para a Coleta Biométrica</h1>

    <h2>Posicionamento do Binômio</h2>
    <p>
        Antes de iniciar qualquer coleta, garanta que a mãe e o recém-nascido
        estejam <strong>confortáveis e tranquilos</strong>.
        Um ambiente calmo favorece a abertura das mãos do bebê e a cooperação da progenitora.
    </p>

    <h2>Verificação dos Dados Biográficos</h2>
    <ul>
        <li>Confirme o nome completo da progenitora e do RN no sistema.</li>
        <li>Verifique data e hora do nascimento do RN.</li>
        <li>O cadastro deve ser iniciado pelo RN — o vínculo entre mãe e bebê começa neste registro.</li>
    </ul>

    <h2>Soro de Limpeza (Solução Nato Soro)</h2>
    <p>O soro de limpeza é composto por:</p>
    <ul>
        <li>Soro fisiológico</li>
        <li>Shampoo neutro infantil</li>
        <li>Clorexidina líquida</li>
    </ul>
    <p>
        Umedeça uma gaze com o soro e, de maneira circular, limpe a <strong>primeira falange</strong>
        da ponta dos dedos. Controle a umidade: os dedos <strong>não devem ficar excessivamente molhados</strong>.
    </p>

    <h2>Higienização dos Dedos</h2>

    <h3>Progenitora</h3>
    <p>Higienize os <strong>polegares e indicadores</strong> de ambas as mãos (4 dedos no total).</p>

    <h3>Recém-nascido</h3>
    <p>Higienize os <strong>10 dedos</strong> do RN com o soro de limpeza para remover o vernix caseoso.</p>

    <h3>Situações Especiais</h3>
    <ul>
        <li><strong>Dedos secos:</strong> Hidrate com o soro de limpeza antes da coleta.</li>
        <li><strong>Dedos úmidos:</strong> Utilize swab de álcool com cautela para evitar ressecamento excessivo.</li>
        <li><strong>Descamação:</strong> Não remova — é processo natural do recém-nascido.</li>
    </ul>

    <h2>Equipamento Pronto</h2>
    <ul class="checklist">
        <li><input type="checkbox" disabled> Scanner ETAN conectado via USB e reconhecido pelo sistema</li>
        <li><input type="checkbox" disabled> Visor do scanner limpo com gaze e soro de limpeza</li>
        <li><input type="checkbox" disabled> Software aberto e pronto para iniciar cadastro</li>
        <li><input type="checkbox" disabled> Dados biográficos inseridos no sistema</li>
    </ul>
</div>
"""

AULA2_3_TITULO = "Coleta Biométrica Passo a Passo"
AULA2_3_DESC   = "Protocolo completo de captura das digitais da progenitora e do recém-nascido"
AULA2_3_CONTEUDO = """
<div class="aula-container">
    <h1>Coleta Biométrica Passo a Passo</h1>

    <h2>Parte 1 — Captura das Impressões Digitais da Progenitora</h2>
    <p>
        Após inserir os dados biográficos da mãe e do RN no sistema, inicie a captura
        das impressões digitais das <strong>pinças das mãos direita e esquerda</strong> da progenitora.
    </p>
    <p><strong>Ordem obrigatória:</strong></p>
    <ol>
        <li>Polegar <strong>direito</strong></li>
        <li>Indicador <strong>direito</strong></li>
        <li>Polegar <strong>esquerdo</strong></li>
        <li>Indicador <strong>esquerdo</strong></li>
    </ol>
    <div class="destaque-info">
        <p>
            Se os dedos estiverem secos, utilize o soro de limpeza para hidratar
            as papilas antes de cada captura.
        </p>
    </div>

    <h2>Parte 2 — Captura Decadactilar do RN (10 dedos)</h2>
    <p>
        A captura decadactilar significa coletar as digitais de <strong>todos os 10 dedos</strong>
        do recém-nascido. Siga a ordem rigorosamente:
    </p>

    <h3>Mão Direita — em ordem:</h3>
    <ol>
        <li>Polegar direito</li>
        <li>Indicador direito</li>
        <li>Dedo médio direito</li>
        <li>Anelar direito</li>
        <li>Mínimo direito</li>
    </ol>

    <h3>Mão Esquerda — em ordem:</h3>
    <ol>
        <li>Polegar esquerdo</li>
        <li>Indicador esquerdo</li>
        <li>Dedo médio esquerdo</li>
        <li>Anelar esquerdo</li>
        <li>Mínimo esquerdo</li>
    </ol>

    <h2>Posicionamento Correto do Dedo no Scanner</h2>
    <ul>
        <li>Posicione o dedo no <strong>centro</strong> da área de captura.</li>
        <li>Foque na <strong>falange distal</strong> (ponta do dedo) — é onde está o núcleo da digital.</li>
        <li>Evite pressão excessiva no scanner; apoie suavemente.</li>
        <li>Use o design ergonômico do ETAN a seu favor para facilitar o encaixe.</li>
    </ul>

    <h2>Técnicas para Mãos Fechadas (RN)</h2>
    <ul>
        <li><strong>Reflexo de Grasping:</strong> Acaricie o dorso ou a lateral da mão do bebê para estimular a abertura dos dedos.</li>
        <li>Segure os quatro dedos da mão para liberar e coletar o polegar primeiro.</li>
        <li>Aguarde o bebê relaxar entre cada captura.</li>
    </ul>

    <h2>Limpeza do Scanner a Cada Dedo</h2>
    <p>
        Limpe o visor do scanner com gaze levemente umedecida com o soro de limpeza
        <strong>a cada dedo coletado</strong>. Isto evita interferência de resíduos
        de vernix ou umidade na próxima captura.
    </p>
</div>
"""

AULA2_4_TITULO = "Verificação, Boas Práticas e Cuidados com o Equipamento"
AULA2_4_DESC   = "Como verificar a qualidade das capturas e manter o equipamento ETAN em boas condições"
AULA2_4_CONTEUDO = """
<div class="aula-container">
    <h1>Verificação, Boas Práticas e Cuidados com o ETAN</h1>

    <h2>Verificação da Qualidade da Captura</h2>
    <p>
        Após concluir a coleta de progenitora e RN, verifique no sistema se
        <strong>todos os registros foram bem-sucedidos</strong>.
    </p>
    <ul>
        <li>Caso alguma digital esteja <strong>ilegível</strong>, realize uma nova captura imediatamente.</li>
        <li>Confirme que o núcleo da digital foi capturado corretamente em cada dedo.</li>
        <li>Limpe o visor do scanner antes de repetir qualquer captura.</li>
    </ul>

    <h2>Checklist Final de Verificação</h2>
    <ul class="checklist">
        <li><input type="checkbox" disabled> 4 digitais da progenitora capturadas (2 polegares + 2 indicadores)</li>
        <li><input type="checkbox" disabled> 10 digitais do RN capturadas (decadactilar completo)</li>
        <li><input type="checkbox" disabled> Qualidade aprovada pelo sistema em todos os dedos</li>
        <li><input type="checkbox" disabled> Nenhuma amostra marcada como ilegível</li>
    </ul>

    <h2>Melhores Práticas — Resumo Oficial INFANT.ID</h2>
    <ul>
        <li><strong>Nunca</strong> coloque a mão molhada no scanner.</li>
        <li><strong>Nunca</strong> use as duas mãos no scanner ao mesmo tempo.</li>
        <li>Sempre posicione o dedo <strong>no centro</strong> da área de captura.</li>
        <li>Limpe a área de captura com flanela de material <strong>não abrasivo</strong> após cada uso.</li>
        <li>Evite derrubar o leitor ou riscar a área de captura.</li>
        <li>Ao guardar, posicione o equipamento de modo que o cabo não force o conector.</li>
    </ul>

    <h2>Cuidados com o Equipamento ETAN</h2>

    <h3>Conexão e Uso</h3>
    <ul>
        <li>Conecte a ponta USB-C no dispositivo ETAN e a ponta USB-A no computador.</li>
        <li>Caso o equipamento esteja conectado mas não seja reconhecido:</li>
        <ol>
            <li>Troque a porta USB do computador.</li>
            <li>Desconecte e reconecte o cabo USB-C no dispositivo.</li>
            <li>Reinicie o computador se os passos anteriores não resolverem.</li>
        </ol>
    </ul>

    <h3>Desconexão Acidental</h3>
    <p>
        Se o cabo for desconectado durante a coleta, o software fecha automaticamente.
        Basta reconectar e reabrir a aplicação — não há perda de dados já salvos.
    </p>

    <h3>Limpeza e Manutenção</h3>
    <ul>
        <li>Utilize gaze umedecida com o soro de limpeza recomendado — sem excesso de umidade.</li>
        <li>Siga as recomendações de limpeza exibidas na tela do software quando solicitado.</li>
        <li>Higienize o visor antes de <strong>cada coleta</strong> e a cada dedo coletado.</li>
    </ul>

    <h2>Como Abrir um Chamado de Suporte</h2>
    <p>Se o equipamento apresentar problemas que não se resolvam com os passos acima:</p>
    <ol>
        <li>Acesse <strong>akiyama.com.br/suporte</strong></li>
        <li>Faça login com seu usuário e senha cadastrados.</li>
        <li>Clique em <strong>"Enviar um ticket"</strong>.</li>
        <li>Preencha todos os campos descrevendo o problema e clique em <strong>"Enviar"</strong>.</li>
    </ol>
</div>
"""

# ─────────────────────────────────────────────────────────────────────────────
# EXECUÇÃO DAS CORREÇÕES
# ─────────────────────────────────────────────────────────────────────────────

with app.app_context():

    print("\n" + "="*60)
    print("CORREÇÃO DOS CURSOS — INFANT.ID")
    print("="*60)

    # ── 1. CORRIGIR TÍTULOS E DESCRIÇÕES DOS CURSOS ──────────────────────────
    print("\n[1] Corrigindo títulos e descrições dos cursos...")

    c1 = Course.query.get(1)
    if c1:
        c1.titulo    = "Bem-vindo ao INFANT.ID — Módulo 1"
        c1.descricao = "Introdução ao sistema INFANT.ID para profissionais de saúde"
        print(f"   ✅ Curso 1 corrigido: {c1.titulo}")

    c2 = Course.query.get(2)
    if c2:
        c2.titulo    = "Protocolo de Coleta Biométrica"
        c2.descricao = (
            "Aprenda o passo a passo para realizar coletas biométricas de qualidade "
            "em recém-nascidos e suas progenitoras, desde a seleção até a verificação final"
        )
        c2.nivel     = "intermediario"
        print(f"   ✅ Curso 2 renomeado: {c2.titulo}")

    c3 = Course.query.get(3)
    if c3:
        c3.titulo    = "Uso do Equipamento e Operação Segura"
        c3.descricao = (
            "Boas práticas de operação do ETAN, controle de acesso, "
            "manutenção preventiva e conformidade com normas hospitalares"
        )
        print(f"   ✅ Curso 3 corrigido: {c3.titulo}")

    c4 = Course.query.get(4)
    if c4:
        c4.descricao = (
            "Aprofunde seus conhecimentos em biometria infantil com foco no protocolo ETAN, "
            "casos especiais, resolução de problemas e boas práticas para coleta de alta "
            "qualidade em recém-nascidos"
        )
        print(f"   ✅ Curso 4 descrição atualizada")

    db.session.flush()

    # ── 2. SUBSTITUIR AULAS DO CURSO 2 ────────────────────────────────────────
    print("\n[2] Substituindo aulas do Curso 2 (conteúdo técnico de TI → clínico)...")

    aulas_curso2 = Lesson.query.filter_by(curso_id=2).all()
    aulas_ids = [a.id for a in aulas_curso2]
    removidas = len(aulas_ids)
    for aula in aulas_curso2:
        db.session.delete(aula)
    db.session.flush()
    print(f"   🗑️  {removidas} aulas antigas removidas (Node.js, Python, curl...)")

    novas_aulas = [
        Lesson(
            curso_id=2,
            titulo=AULA2_1_TITULO,
            descricao=AULA2_1_DESC,
            conteudo=AULA2_1_CONTEUDO,
            ordem=1,
            duracao=20,
            ativo=True
        ),
        Lesson(
            curso_id=2,
            titulo=AULA2_2_TITULO,
            descricao=AULA2_2_DESC,
            conteudo=AULA2_2_CONTEUDO,
            ordem=2,
            duracao=25,
            ativo=True
        ),
        Lesson(
            curso_id=2,
            titulo=AULA2_3_TITULO,
            descricao=AULA2_3_DESC,
            conteudo=AULA2_3_CONTEUDO,
            ordem=3,
            duracao=30,
            ativo=True
        ),
        Lesson(
            curso_id=2,
            titulo=AULA2_4_TITULO,
            descricao=AULA2_4_DESC,
            conteudo=AULA2_4_CONTEUDO,
            ordem=4,
            duracao=20,
            ativo=True
        ),
    ]

    for aula in novas_aulas:
        db.session.add(aula)
        print(f"   ✅ Nova aula adicionada: {aula.titulo}")

    # ── 3. CORRIGIR ERROS DE PORTUGUÊS EM OUTRAS AULAS ───────────────────────
    print("\n[3] Corrigindo erros de português em aulas existentes...")

    correcoes_titulos = {
        "Architectura de Integração": "Arquitetura de Integração",
        "Implementao Tcnica":         "Implementação Técnica",
        "Workflow Clnico com INFANT.ID": "Fluxo Clínico com INFANT.ID",
        "Troubleshooting de Integração": "Resolução de Problemas de Integração",
    }
    correcoes_desc = {
        "Entenda a arquitetura tcnica da integração com sistemas hospitalares":
            "Entenda a arquitetura técnica da integração com sistemas hospitalares",
        "Como implementar a integração não seu HIS":
            "Como implementar a integração no seu HIS",
        "Entenda o fluxo clnico com integração biométrica":
            "Entenda o fluxo clínico com integração biométrica",
        "Resolva problemas mais comuns de integração":
            "Resolva os problemas mais comuns de integração",
        "Como gerenciar usurios e suas permisses":
            "Como operar o equipamento ETAN e seus acessos",
        "Configure mltiplos hospitais e lojistas":
            "Configure múltiplos perfis e acessos hospitalares",
        "Rastreie aes e cumpra com regulamentaes":
            "Rastreie ações e cumpra as regulamentações vigentes",
        "Entenda as garantias de segurança e cumprimento regulatrio":
            "Entenda as garantias de segurança e conformidade regulatória",
    }

    todas_aulas = Lesson.query.all()
    corrigidas = 0
    for aula in todas_aulas:
        if aula.titulo in correcoes_titulos:
            aula.titulo = correcoes_titulos[aula.titulo]
            corrigidas += 1
        if aula.descricao in correcoes_desc:
            aula.descricao = correcoes_desc[aula.descricao]
            corrigidas += 1

    print(f"   ✅ {corrigidas} campos de aulas corrigidos")

    # ── 4. COMMIT FINAL ────────────────────────────────────────────────────────
    db.session.commit()
    print("\n" + "="*60)
    print("✅ TODAS AS CORREÇÕES APLICADAS COM SUCESSO!")
    print("="*60)

    # Relatório final
    print("\n📋 Estado final dos cursos:")
    for c in Course.query.filter_by(ativo=True).order_by(Course.id).all():
        aulas = Lesson.query.filter_by(curso_id=c.id, ativo=True).count()
        print(f"   Curso {c.id}: {c.titulo} ({aulas} aulas) [{c.nivel}]")
