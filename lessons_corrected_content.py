"""
Popula aulas com conteudo CORRETO baseado nos documentos oficiais
- Remove erros de digitacao
- Remove videos genericos do YouTube
- Integra links de video oficiais do Google Drive
- Baseado em documentacao profissional
"""

import json
from datetime import datetime
from pathlib import Path

# Ler conteudos dos .md
docs_path = Path("assets/documents")

with open(docs_path / "Informativo Etan.md", 'r', encoding='utf-8') as f:
    informativo_etan = f.read()

with open(docs_path / "Protocolo de Coleta Passo a Passo.md", 'r', encoding='utf-8') as f:
    protocolo_coleta = f.read()

with open(docs_path / "Procedimento de Coleta.md", 'r', encoding='utf-8') as f:
    procedimento_coleta = f.read()

# Estrutura das aulas corrigidas
LESSONS_CORRECTED = {
    1: {  # Onboarding INFANT.ID
        "id": 1,
        "course_id": 1,
        "title": "Bem-vindo ao INFANT.ID",
        "content": """
<h1>Bem-vindo ao INFANT.ID</h1>
<p>Bem-vindo ao programa de treinamento para enfermeiras sobre a plataforma INFANT.ID!</p>

<h2>O que Voce vai aprender?</h2>
<p>Este modulo de onboarding foi desenvolvido para capacitar voce a:</p>
<ul>
    <li>Entender o que eh a plataforma INFANT.ID</li>
    <li>Dominar o uso do equipamento ETAN</li>
    <li>Realizar coletas biometricas corretas</li>
    <li>Resolver problemas comuns</li>
    <li>Seguir protocolos de seguranca e qualidade</li>
</ul>

<h2>Estrutura do Treinamento</h2>
<p>O programa eh dividido em 3 cursos principais:</p>
<table border="1" cellpadding="10">
    <tr>
        <th>Curso</th>
        <th>Objetivo</th>
        <th>Duracao</th>
    </tr>
    <tr>
        <td><strong>Onboarding INFANT.ID</strong></td>
        <td>Conhecer a plataforma e o equipamento</td>
        <td>45 minutos</td>
    </tr>
    <tr>
        <td><strong>Integracao Hospitalar</strong></td>
        <td>Protocolos de coleta e procedimentos clinicos</td>
        <td>60 minutos</td>
    </tr>
    <tr>
        <td><strong>Gerenciamento de Usuarios</strong></td>
        <td>Seguranca, controle de acesso e auditoria</td>
        <td>30 minutos</td>
    </tr>
</table>

<h2>Como usar este treinamento</h2>
<ol>
    <li>Siga as aulas em sequencia</li>
    <li>Assista aos videos de demonstracao quando disponivel</li>
    <li>Pratique os procedimentos com supervisao</li>
    <li>Tire duvidas com seu supervisor</li>
    <li>Complete o treinamento antes de atuar independentemente</li>
</ol>

<h2>Duracao estimada: 10 minutos</h2>
        """,
        "duration": "10 minutos"
    },
    
    2: {  # INFANT.ID - The Solution
        "id": 2,
        "course_id": 1,
        "title": "O que eh INFANT.ID",
        "content": """
<h1>Conhecendo a Plataforma INFANT.ID</h1>

<h2>Historia e Desenvolvimento</h2>
<p>Apos 13 anos de estudo e desenvolvimento, a equipe da INFANT.ID transformou uma visao em realidade. 
Embora recém-chegados ao mercado, trazemos uma experiência robusta e conhecimento profundo que sustentam 
a tecnologia oferecida.</p>

<h2>Diferenciais Estrategicos</h2>
<p>Nosso diferencial reside na capacidade comprovada de:</p>
<ul>
    <li><strong>Capturar digitais de recém-nascidos</strong> - Com precisao desde o primeiro dia de vida</li>
    <li><strong>Realizar o match</strong> - Comparacao de digitais ao longo de toda a vida do individuo</li>
    <li><strong>Garantir autenticidade</strong> - Assegura continuidade da identidade desde o nascimento</li>
</ul>

<h2>O Produto ETAN</h2>
<p>Dispositivo de captura biometrica infantil, especialmente projetado para:</p>
<ul>
    <li>Cadastramento biometrico de recém-nascidos (a partir de 0 dias de vida)</li>
    <li>Autenticacao biometrica inicial</li>
    <li>Solucoes de identidade digital</li>
</ul>

<h2>Características Tecnicas do ETAN</h2>
<table border="1" cellpadding="10">
    <tr>
        <th>Caracteristica</th>
        <th>Beneficio</th>
    </tr>
    <tr>
        <td>Gerenciamento 100% via SDK proprietario</td>
        <td>Integracao perfeita com sistemas hospitalares</td>
    </tr>
    <tr>
        <td>Sem adaptadores ou fontes externas</td>
        <td>Implementacao simples e rapida</td>
    </tr>
    <tr>
        <td>Cabo USB unico para alimentacao e comunicacao</td>
        <td>Menos equipamento, menos cables</td>
    </tr>
    <tr>
        <td>Leve e ergonomico</td>
        <td>Conforto para o operador e seguranca para o bebe</td>
    </tr>
</table>

<h2>Aplicacoes Praticas</h2>
<p>A tecnologia INFANT.ID possibilita:</p>
<ul>
    <li>Identidade civil digital desde o nascimento</li>
    <li>Seguranca na identificacao de bebes em ambiente hospitalar</li>
    <li>Reducao de fraudes de identidade</li>
    <li>Melhor gestao de registros de saude</li>
</ul>

<h2>Duracao estimada: 15 minutos</h2>
        """,
        "duration": "15 minutos"
    },

    3: {  # Equipamento ETAN
        "id": 3,
        "course_id": 1,
        "title": "O Equipamento ETAN",
        "content": """
<h1>Dominio do Equipamento ETAN</h1>

<h2>Componentes principais</h2>
<ul>
    <li><strong>Scanner biometrico</strong> - Area de captura de impressoes digitais</li>
    <li><strong>Cabo USB-C</strong> - Conexao ao computador</li>
    <li><strong>Suporte ergonomico</strong> - Facilita o posicionamento do bebe</li>
</ul>

<h2>Como Conectar o ETAN</h2>
<ol>
    <li>Conecte a ponta USB tipo C do cabo ao dispositivo</li>
    <li>Plugue a outra ponta USB A no computador</li>
    <li>Observe: a led de alimentacao deve acender</li>
    <li>O sistema deve reconhecer automaticamente o dispositivo</li>
</ol>

<h2>Posicionando o Dedo para Coleta</h2>
<p><strong>IMPORTANTE:</strong> Always position the finger in the center of the capture area.</p>
<ul>
    <li>Posicione o dedo <strong>no centro</strong> da area de captura</li>
    <li>Mantenha o dedo <strong>baixo</strong> - nao pressione com forca excessiva</li>
    <li>Certifique-se de que a <strong>falange distal</strong> esta bem colocada</li>
    <li>O nucleo da digital deve ser capturado corretamente</li>
</ul>

<h2>Cuidados Essenciais</h2>
<ul>
    <li><strong>Nunca</strong> coloque a mao molhada no scanner</li>
    <li><strong>Nunca</strong> use as duas maos no scanner ao mesmo tempo</li>
    <li><strong>Nunca</strong> derrubar o leitor</li>
    <li><strong>Nunca</strong> riscara area de captura</li>
    <li>Evite qualquer acao que possa danificar o equipamento</li>
</ul>

<h2>Limpeza da Area de Captura</h2>
<p>Sempre limpe a area de captura apos usar, seguindo estes passos:</p>
<ol>
    <li>Use uma flanela de material nao-abrasivo</li>
    <li>Limpe com movimentos suaves</li>
    <li>Seque completamente antes da proxima coleta</li>
    <li>Limpe novamente a cada dedo capturado para evitar interferencias</li>
</ol>

<h2>Guarda e Armazenamento</h2>
<p>Ao terminar a coleta:</p>
<ul>
    <li>Posicione o leitor de maneira segura</li>
    <li>Nao deixe objetos sobre o equipamento</li>
    <li>Mantenha em local livro de umidade excessiva</li>
    <li>Armazene em ambiente controlado</li>
</ul>

<h2>Duracao estimada: 12 minutos</h2>
        """,
        "duration": "12 minutos"
    },

    4: {  # Biometria
        "id": 4,
        "course_id": 1,
        "title": "Fundamentos de Biometria Infantil",
        "content": """
<h1>Entendendo a Biometria Infantil</h1>

<h2>O que eh Biometria?</h2>
<p>Biometria eh a medicao de caracteristicas fisicas unicas. A INFANT.ID utiliza impressoes digitais 
(datilogarfia) como base para identificacao e autenticacao.</p>

<h2>Modalidades Biometricas Suportadas</h2>
<ul>
    <li><strong>Impressao Digital</strong> - Padrao de linhas na falange distal</li>
    <li><strong>Facial Recognition</strong> - Mapeamento de caracteristicas faciais</li>
    <li><strong>Iris Recognition</strong> - Padrao da iris disponivel</li>
    <li><strong>Voz</strong> - Padrao de voz e fala</li>
</ul>

<h2>Por que Biometria em Recém-nascidos?</h2>
<p>A tecnologia permite:</p>
<ul>
    <li>Identificacao precisa desde o nascimento</li>
    <li>Prevencao de fraudes de substituicao de bebes</li>
    <li>Rastreamento de identidade ao longo da vida</li>
    <li>Seguranca e confiabilidade aprimorada</li>
</ul>

<h2>Impressoes Digitais em Recém-nascidos</h2>
<p>As impressoes digitais de um recém-nascido apresentam caracteristicas unicas:</p>
<ul>
    <li>Já totalmente formadas ao nascer</li>
    <li>Permanecem estáveis ao longo da vida</li>
    <li>Tamanho pequeno, requer equipamento especializado</li>
    <li>Sensibilidade especial - requer cuidado extra</li>
</ul>

<h2>Qualidade da Captura Biometrica</h2>
<p>Para garantir qualidade e precisao:</p>
<ol>
    <li>Limpe sempre os dedos antes da captura</li>
    <li>Posicione o dedo no centro da area de captura</li>
    <li>Evite pressao excessiva</li>
    <li>Certifique-se de que o nucleo da digital foi capturado</li>
    <li>Se ilegivel, realize uma nova captura</li>
</ol>

<h2>Duracao estimada: 10 minutos</h2>
        """,
        "duration": "10 minutos"
    },

    5: {  # Preparacao e Higiene
        "id": 5,
        "course_id": 1,
        "title": "Preparacao e Higiene para Coleta",
        "content": """
<h1>Preparacao para Coleta de Impressoes Digitais</h1>

<h2>Informacoes Pre-coleta</h2>
<p>Antes de iniciar o procedimento de coleta, certifique-se de:</p>
<ul>
    <li>Ter os dados biograficos do recem-nascido e da mae prontos</li>
    <li>O sistema estar conectado e pronto para iniciar A atividade</li>
    <li>Ter todos os materiais de limpeza disponiveis</li>
    <li>O equipamento estar funcionando corretamente</li>
</ul>

<h2>Conforto da Mae e do Recem-nascido</h2>
<p>Posicione com cuidado:</p>
<ul>
    <li>Garantir que a mae esteja confortável</li>
    <li>Garantir que o recem-nascido esteja estavel</li>
    <li>Providenciar ambiente calmo e sem distrações</li>
    <li>Considerar o horario ideal (apos alimentacao, de preferencia)</li>
</ul>

<h2>Solucao de Limpeza Recomendada</h2>
<p><strong>Formula: Soro de Limpeza Infantil</strong></p>
<table border="1" cellpadding="10">
    <tr>
        <th>Componente</th>
        <th>Quantidade</th>
        <th>Proposito</th>
    </tr>
    <tr>
        <td>Soro Fisiologico</td>
        <td>Base</td>
        <td>Limpeza suave</td>
    </tr>
    <tr>
        <td>Shampoo Neutro Infantil</td>
        <td>Pequena quantidade</td>
        <td>Remover residuos e oleosidade</td>
    </tr>
    <tr>
        <td>Clorexidina Liquida</td>
        <td>Pequena quantidade</td>
        <td>Desinfeccao segura</td>
    </tr>
</table>

<h2>Tecnica de Limpeza dos Dedos</h2>
<p>Para higienizar os dedos indicadores e polegares da mae:</p>
<ol>
    <li>Umedeça uma gaze com a solucao de limpeza</li>
    <li>De maneira <strong>circular</strong>, limpe a primeira falange (ponta) dos dedos</li>
    <li>Certifique-se de controlar a umidade</li>
    <li>Evite que os dedos fiquem excessivamente molhados</li>
    <li>Seque bem antes da coleta</li>
</ol>

<p>Para higienizar os 10 dedos do recem-nascido:</p>
<ol>
    <li>Use a mesma solucao de limpeza</li>
    <li>Limpe suavemente todos os 10 dedos</li>
    <li>Remova o Vernix Caseoso com cuidado</li>
    <li>Controle a umidade (muito seco ou muito molhado prejudica a coleta)</li>
    <li>Se necessario, hidrate com a solucao</li>
</ol>

<h2>Hidratacao dos Dedos</h2>
<p>Se os dedos estiverem secos:</p>
<ul>
    <li>Utilize a solucao de limpeza para hidratar as papilas</li>
    <li>Nao force umidade excessiva</li>
    <li>Um dedo levemente umido eh mais facil de capturar</li>
</ul>

<h2>Contraindicacoes para Coleta</h2>
<p>Adie a coleta se:</p>
<ul>
    <li>O recem-nascido nao estiver estavel</li>
    <li>Houver traumatismo nos dedos</li>
    <li>Houver infeccao ou lesao visivel</li>
    <li>A mae nao estiver em condicoes seguras</li>
</ul>

<h2>Duracao estimada: 15 minutos</h2>
        """,
        "duration": "15 minutos"
    },

    6: {  # Troubleshooting
        "id": 6,
        "course_id": 1,
        "title": "Troubleshooting e Manutencao",
        "content": """
<h1>Resolvendo Problemas Comuns</h1>

<h2>Equipamento Nao Reconhecido</h2>
<p><strong>Sintoma:</strong> O sistema nao detecta o ETAN quando conectado.</p>
<p><strong>Solucao:</strong></p>
<ol>
    <li>Verificar se o equipamento esta conectado corretamente</li>
    <li>Tentar outra porta USB no computador</li>
    <li>Se continuar sem funcionar, verificar antivírus com area de TI</li>
    <li>Entrar em contato com provedor de antivírus se necessario</li>
</ol>

<h2>Equipamento Desconectado Constantemente</h2>
<p><strong>Sintoma:</strong> O equipamento se desconecta durante o uso.</p>
<p><strong>Solucao passo a passo:</strong></p>
<ol>
    <li>Trocar a porta USB em que o scanner esta conectado</li>
    <li>Se ainda nao funcionar, desconectar o USB-C e reconectar</li>
    <li>Se problema persistir, reiniciar o computador</li>
    <li>Caso continue, contactar suporte via FreshService</li>
</ol>

<h2>Desconexao Acidental</h2>
<p><strong>Sintoma:</strong> O cabo se soltou acidentalmente durante a coleta.</p>
<p><strong>O que acontece:</strong> A aplicação OpenBio Enroll fecha automaticamente.</p>
<p><strong>Solucao:</strong> Simplesmente reiniciar a aplicação - estará pronta para nova coleta.</p>

<h2>Qualidade Baixa de Captura</h2>
<p><strong>Sintoma:</strong> Mensagem de erro "Qualidade insuficiente" ou "Dedo ilegivel".</p>
<p><strong>Causas possiveis:</strong></p>
<ul>
    <li>Dedos muito secos</li>
    <li>Dedos muito molhados</li>
    <li>Dedo nao alinhado no centro da area</li>
    <li>Pressao insuficiente ou excessiva</li>
    <li>Visor do scanner sujo</li>
</ul>
<p><strong>Solucao:</strong></p>
<ol>
    <li>Limpar o visor do scanner com gaze macia</li>
    <li>Limpar e secar bem os dedos</li>
    <li>Tentar novamente com melhor posicionamento</li>
    <li>Se problema persistir, hidratara solucao e tentar outra vez</li>
</ol>

<h2>Equipamento Descalibrado</h2>
<p><strong>Sintoma:</strong> Margens visíveis na area de captura ou imagem distorcida.</p>
<p><strong>Solucao:</strong> Abrir um ticket via sistema de suporte e entrar em contato com o time de CS.</p>

<h2>Problemas na Instalacao do Software</h2>
<p>Se encontrar problema durante a instalacao:</p>
<ol>
    <li>Verificar se o sistema atende aos requisitos do software</li>
    <li>Executar o arquivo de instalacao como administrador</li>
    <li>Reiniciar o computador e tentar novamente</li>
    <li>Se problema persistir, contactar suporte tecnico</li>
</ol>

<h2>Falha Apos Queda de Energia</h2>
<p><strong>Problema:</strong> Apos queda de energia ou desligamento nao convencional, a aplicacao nao inicia.</p>
<p><strong>Solucao:</strong> Excluir o arquivo Session.json localizado em: C:\\Users\\User\\AppData\\Roaming\\OpenbioServices</p>

<h2>Como Abrir um Chamado Tecnico</h2>
<ol>
    <li>Acessar o link: akiyama.com.br/suporte</li>
    <li>Realizar login com usuario e senha criados</li>
    <li>Clicar na opcao "Enviar um ticket"</li>
    <li>Preencher todos os campos com detalhes do problema</li>
    <li>Clicar em "Enviar" para abrir o chamado</li>
</ol>

<h2>Encaminhar para Suporte Avancado</h2>
<p>Se nenhuma solucao funcionar, entre em contato via <strong>FreshService</strong> informando:</p>
<ul>
    <li>Descricao detalhada do problema</li>
    <li>Passos ja realizados para resolver</li>
    <li>Modelo e serie do equipamento</li>
    <li>Versao do software</li>
</ul>

<h2>Duracao estimada: 18 minutos</h2>
        """,
        "duration": "18 minutos"
    },

    # CURSO 2: INTEGRACAO HOSPITALAR
    7: {
        "id": 7,
        "course_id": 2,
        "title": "Protocolo de Coleta - Visao Geral",
        "content": """
<h1>Protocolo Oficial de Coleta de Impressoes Digitais</h1>

<h2>Introducao</h2>
<p>Este protocolo eh baseado em praticas clinicas comprovadas e foi desenvolvido para garantir:</p>
<ul>
    <li>Seguranca da mae e do recem-nascido</li>
    <li>Qualidade da coleta biometrica</li>
    <li>Conformidade com normas hospitalares</li>
    <li>Melhor experiencia para todos envolvidos</li>
</ul>

<h2>Etapas do Protocolo</h2>
<table border="1" cellpadding="10">
    <tr>
        <th>Etapa</th>
        <th>Objetivo</th>
        <th>Tempo estimado</th>
    </tr>
    <tr>
        <td><strong>1. Selecao</strong></td>
        <td>Escolher mae e RN adequados para coleta</td>
        <td>5 min</td>
    </tr>
    <tr>
        <td><strong>2. Preparacao</strong></td>
        <td>Preparar ambiente, mae, RN e materiais</td>
        <td>10 min</td>
    </tr>
    <tr>
        <td><strong>3. Captura Progenitora</strong></td>
        <td>Coletar digitais da mae (4 dedos)</td>
        <td>5 min</td>
    </tr>
    <tr>
        <td><strong>4. Captura RN</strong></td>
        <td>Coletar digitais do bebe (10 dedos)</td>
        <td>10 min</td>
    </tr>
    <tr>
        <td><strong>5. Verificacao</strong></td>
        <td>Confirmar qualidade da captura</td>
        <td>3 min</td>
    </tr>
</table>

<p><strong>Tempo total estimado:</strong> 33 minutos (pode variar conforme estabilidade do RN)</p>

<h2>Pessoas Envolvidas</h2>
<ul>
    <li><strong>Equipe Medica/Clinica:</strong> Seleciona mae e RN</li>
    <li><strong>Enfermeira Treinada:</strong> Realiza coleta</li>
    <li><strong>Supervisor:</strong> Monitora qualidade do processo</li>
</ul>

<h2>Criterios de Selecao</h2>
<p>Selecione mae e RN quando:</p>
<ul>
    <li>Ambos estejam estáveis</li>
    <li>Ambos estejam fora de risco clinico</li>
    <li>RN atenda protocolos de seguranca hospitalar</li>
    <li>Na etapa adequada do "Golden Hour" se possível</li>
</ul>

<h2>Seguranca no Protocolo</h2>
<p>Este protocolo foi desenvolvido considerando:</p>
<ul>
    <li>Seguranca maxima do recem-nascido</li>
    <li>Conforto da mae em pos-parto</li>
    <li>Nao-invasividade (apenas toque dos dedos)</li>
    <li>Conformidade com normas de higiene hospitalar</li>
</ul>

<h2>Duracao estimada: 12 minutos</h2>
""",
        "duration": "12 minutos"
    },

    8: {
        "id": 8,
        "course_id": 2,
        "title": "Etapa 1: Selecao - Escolha da Mae e RN",
        "content": """
<h1>Etapa 1: Selecao do Recem-nascido e Progenitora</h1>

<h2>Responsabilidade da Equipe Medica</h2>
<p>A seleção é realizada pela equipe medica assistencial, com base em critérios clinicos.</p>

<p><strong>Importante:</strong> A equipe clinica determina quais bebes estao prontos para a coleta biometrica.</p>

<h2>Criterios de Selecao</h2>
<p>O recem-nascido deve estar:</p>
<ul>
    <li>Estavel clinicamente</li>
    <li>Fora de risco (avaliacao medica positiva)</li>
    <li>Com dedos livres de traumatismo</li>
    <li>Com possibilidade de manuseio seguro</li>
</ul>

<p>A progenitora deve estar:</p>
<ul>
    <li>Estavel pos-parto</li>
    <li>Com disponibilidade para o procedimento</li>
    <li>Disposta e consentida para participar</li>
    <li>Em condicoes de higiene adequadas (higiene basica)</li>
</ul>

<h2>Momento Ideal - Golden Hour</h2>
<p>Se possivel, realize a coleta durante o "Golden Hour":</p>
<p>A primeira hora apos o parto eh ideal para:</p>
<ul>
    <li>Contato pele a pele entre mae e bebe</li>
    <li>Promover amamentacao</li>
    <li>Reducao da mortalidade neonatal</li>
    <li>Vínculo entre mae e filho</li>
</ul>

<p><strong>Nota:</strong> A coleta biometrica nao interfere neste vínculo - eh um procedimento nao-invasivo.</p>

<h2>Consentimento Informado</h2>
<ul>
    <li>Explicar o procedimento a mae</li>
    <li>Informar sobre seguranca (nao-invasivo)</li>
    <li>Garantir consentimento informado</li>
    <li>Registrar consentimento no sistema</li>
</ul>

<h2>O que NÃO fazer nesta etapa</h2>
<ul>
    <li>Forcas a coleta se RN nao estiver estavel</li>
    <li>Forcar participacao se mae nao consentir</li>
    <li>Ignorar recomendacoes medicas</li>
    <li>Realizar coleta fora do protocolo clinico</li>
</ul>

<h2>Duracao estimada: 8 minutos</h2>

<div style="color: #c41e3a; border: 2px solid #c41e3a; padding: 10px; margin-top: 20px;">
    <strong>Para mais detalhes, assista o video oficial:</strong><br>
    <a href="https://drive.google.com/file/d/1uOILNO0clQYeP9PFpuvkaP1h4570kaRA/view?usp=sharing" target="_blank">
    Tutorial de Selecao - Google Drive</a>
</div>
""",
        "duration": "8 minutos"
    },

    9: {
        "id": 9,
        "course_id": 2,
        "title": "Etapa 2: Preparacao - Estruturando para Sucesso",
        "content": """
<h1>Etapa 2: Preparacao para Coleta</h1>

<h2>Posicionamento Confortavel</h2>
<p>Primeira atividade da preparacao:</p>
<ol>
    <li>Posicione a mae de forma confortavel</li>
    <li>Posicione o recem-nascido de forma estavel</li>
    <li>Use almofadas ou suporte se necessario</li>
    <li>Certifique-se de que ambos estao descontraidos</li>
</ol>

<h2>Dados Biograficos</h2>
<p>Verifique que todos os dados estao acessiveis:</p>
<ul>
    <li><strong>RN:</strong> Nome completo, data de nascimento, hora de nascimento, peso</li>
    <li><strong>Mae:</strong> Nome completo, documento de identidade</li>
    <li><strong>Hospital/Unidade:</strong> Informacoes de localizacao</li>
</ul>

<p><strong>Importante:</strong> Certifique-se que toda informacao esta acessivel ANTES de iniciar.</p>

<h2>Insercao de Dados no Sistema</h2>
<p>O processo deve ser feito nesta ordem:</p>
<ol>
    <li>Primeiro: Inserir dados do RN</li>
    <li>Depois: Inserir dados da progenitora</li>
    <li>O vínculo entre mae e bebe eh criado neste cadastro</li>
</ol>

<h2>Limpeza e Higiene - Solucao Recomendada</h2>
<p>Use a <strong>Solucao ETAN para Limpeza Infantil:</strong></p>
<ul>
    <li>Soro Fisiologico (base)</li>
    <li>Shampoo Neutro Infantil (pequena quantidade)</li>
    <li>Clorexidina Liquida (pequena quantidade)</li>
</ul>

<h2>Tecnica de Limpeza - Progenitora</h2>
<ol>
    <li>Com "soro de limpeza", higienize os <strong>dedos indicadores e polegares</strong> da mae</li>
    <li>Use uma gaze umedecida</li>
    <li>Limpe de forma circular</li>
    <li>Foco na <strong>primeira falange (ponta dos dedos)</strong></li>
    <li>Controle a umidade - evite que fiquem excessivamente molhados</li>
</ol>

<h2>Tecnica de Limpeza - Recem-nascido</h2>
<ol>
    <li>Com "soro de limpeza", higienize os <strong>10 dedos do RN</strong></li>
    <li>Remova o Vernix Caseoso com cuidado</li>
    <li>Use movimentos suaves</li>
    <li>Controle a umidade (ideal: levemente umido, nao encharcado)</li>
    <li>Se dedos ficarem muito secos, hidrate com a solucao</li>
</ol>

<h2>Verificacao Tecnica Final</h2>
<p>Antes de iniciar a captura:</p>
<ul>
    <li>Certifique-se de que o <strong>sistema esta conectado</strong></li>
    <li>Verifique que o <strong>equipamento ETAN esta pronto</strong></li>
    <li>Teste uma captura de teste se possivel</li>
    <li>Tenha à mao os materiais de limpeza (gaze, solucao)</li>
</ul>

<h2>Explicacao à Progenitora</h2>
<ol>
    <li>Explicar o processo de coleta</li>
    <li>Informar sobre a importancia da biometria</li>
    <li>Garantir que mae entenda o procedimento</li>
    <li>Responder quaisquer duvidas</li>
</ol>

<h2>Duracao estimada: 15 minutos</h2>

<div style="color: #c41e3a; border: 2px solid #c41e3a; padding: 10px; margin-top: 20px;">
    <strong>Para mais detalhes, assista o video oficial:</strong><br>
    <a href="https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link" target="_blank">
    Tutorial de Preparacao - Google Drive</a>
</div>
""",
        "duration": "15 minutos"
    },

    10: {
        "id": 10,
        "course_id": 2,
        "title": "Etapa 3: Captura Biometrica da Progenitora",
        "content": """
<h1>Etapa 3: Capturando as Digitais da Mae</h1>

<h2>Sequencia Correta de Captura</h2>
<p>Apos inserir os dados da progenitora no sistema, inicie a captura biometrica:</p>

<p><strong>Ordem de Captura (IMPORTANTE):</strong></p>
<ol>
    <li><strong>Polegar Direito</strong></li>
    <li><strong>Indicador Direito</strong></li>
    <li><strong>Polegar Esquerdo</strong></li>
    <li><strong>Indicador Esquerdo</strong></li>
</ol>

<p>Total: 4 dedos (dedos "pinça" - polegar e indicador)</p>

<h2>Posicionamento de Cada Dedo</h2>
<p>Para cada dedo:</p>
<ol>
    <li>Posicione no <strong>centro</strong> da area de captura</li>
    <li>Mantenha <strong>baixa pressao</strong> - nao force</li>
    <li>Certifique-se de que a falange distal esta bem posicionada</li>
    <li>Aguarde o sinal do sistema (som ou mensagem)</li>
    <li>Remova o dedo se captura foi bem-sucedida</li>
</ol>

<h2>Qualidade da Captura</h2>
<p>Apos cada captura, o sistema mostrara:</p>
<ul>
    <li><strong>Sucesso:</strong> Mensagem positiva, pode prosseguir</li>
    <li><strong>Qualidade Baixa:</strong> Sistema pede nova captura do mesmo dedo</li>
    <li><strong>Nao Reconhecido:</strong> Dedo nao foi posicionado. Tente novamente</li>
</ul>

<h2>Se Necessaria Nova Captura</h2>
<p>Caso alguma captura nao seja bem-sucedida:</p>
<ol>
    <li>Limite a 2-3 tentativas por dedo</li>
    <li>Se continuar falhando, limpe o visor do scanner</li>
    <li>Limpe e seque bem o dedo da mae</li>
    <li>Tente novamente com melhor posicionamento</li>
</ol>

<h2>Conforto da Progenitora</h2>
<p>Durante todo o processo:</p>
<ul>
    <li>Monitorar conforto da mae</li>
    <li>Dar pausas se necessario</li>
    <li>Tranquilizar se estiver ansiosa</li>
    <li>Explicar cada etapa conforme avanca</li>
</ul>

<h2>Duracao estimada: 10 minutos</h2>

<div style="color: #c41e3a; border: 2px solid #c41e3a; padding: 10px; margin-top: 20px;">
    <strong>Para mais detalhes, assista o video oficial:</strong><br>
    <a href="https://drive.google.com/file/d/1g55icK4TUhLpQxwsTgPbV0e09td8K8ln/view?usp=drive_link" target="_blank">
    Tutorial de Captura da Progenitora - Google Drive</a>
</div>
""",
        "duration": "10 minutos"
    },

    11: {
        "id": 11,
        "course_id": 2,
        "title": "Etapa 4: Captura Biometrica do Recem-nascido",
        "content": """
<h1>Etapa 4: Captura Decadactilar do Bebe</h1>

<h2>O que eh Captura Decadactilar?</h2>
<p>Decadactilar = 10 dedos. Voce coletara as digitais de todos os 10 dedos do recem-nascido.</p>

<h2>Sequencia de Captura (IMPORTANTE)</h2>
<p><strong>Mao Direita - em ordem:</strong></p>
<ol>
    <li>Polegar Direito</li>
    <li>Indicador Direito</li>
    <li>Dedo Medio Direito</li>
    <li>Dedo Anular Direito</li>
    <li>Dedo Minimo Direito</li>
</ol>

<p><strong>Mao Esquerda - em ordem:</strong></p>
<ol>
    <li>Polegar Esquerdo</li>
    <li>Indicador Esquerdo</li>
    <li>Dedo Medio Esquerdo</li>
    <li>Dedo Anular Esquerdo</li>
    <li>Dedo Minimo Esquerdo</li>
</ol>

<p>Total: 10 capturadas, uma por dedo</p>

<h2>Desafios Unicos com Recem-nascido</h2>
<p>Bebes recem-nascidos apresentam:</p>
<ul>
    <li>Maos naturalmente fechadas (reflexo de preensao)</li>
    <li>Movimentos involuntarios (agitacao)</li>
    <li>Dedos pequenos e delicados</li>
    <li>Sensibilidade a manipulacao</li>
</ul>

<h2>Tecnica - Mao Fechada</h2>
<p>Para abrir levemente a mao do bebe:</p>
<ol>
    <li>Segure os quatro dedos com uma mao</li>
    <li>Isso permite acessar o polegar</li>
    <li>Use a outra mao para posicionar no scanner</li>
    <li>Nao force - apenas posicione com suavidade</li>
</ol>

<h2>Tecnica - Reflexo de Grasping</h2>
<p>Use este reflexo natural a seu favor:</p>
<ol>
    <li>Acaricie o dorso ou lateral da mao do bebe</li>
    <li>O bebe naturalmente abre a mao como resposta</li>
    <li>Neste momento, posicione o dedo no scanner</li>
    <li>Muito mais confortavel para o bebe</li>
</ol>

<h2>Posicionamento de Cada Dedo</h2>
<p>Para cada dedo do RN:</p>
<ol>
    <li>Posicione no <strong>centro</strong> da area de captura</li>
    <li>Foque na <strong>falange distal</strong> (ponta do dedo)</li>
    <li>Mantenha <strong>pressao leve</strong> - nao espremam</li>
    <li>Evite excessiva pressao no scanner</li>
    <li>Aguarde o sinal de sucesso</li>
</ol>

<h2>Qualidade da Captura - RN</h2>
<p>Para garantir qualidade:</p>
<ul>
    <li>Certifique-se de que o <strong>nucleo da digital</strong> foi capturado</li>
    <li>O dedo deve estar bem-posicionado no visor</li>
    <li>A imagem deve estar clara e legivel</li>
    <li>Se ilegivel, realizar nova captura</li>
</ul>

<h2>Limpeza do Scanner - Critico!</h2>
<p><strong>IMPORTANTE: Limpe o visor ANTES DE CADA DEDO!</strong></p>
<ol>
    <li>Use uma gaze macia</li>
    <li>Limpe com a solucao recomendada (sem excesso de umidade)</li>
    <li>Seque bem</li>
    <li>Apos cada coleta, limpe novamente para proxima</li>
</ol>

<h2>Se Necessaria Nova Captura</h2>
<p>Caso a qualidade esteja baixa:</p>
<ol>
    <li>Limpar bem dedo do bebe e visor do scanner</li>
    <li>Hidratar dedo se estiver muito seco</li>
    <li>Secar se estiver molhado demais</li>
    <li>Tentar novamente (limite: 2-3 tentativas por dedo)</li>
</ol>

<h2>Estabilidade do Bebe</h2>
<p>Monitore continuamente:</p>
<ul>
    <li>Se bebe ficar agitado, pause o procedimento</li>
    <li>Deixe mae confortar o bebe</li>
    <li>Retome quando bebe estiver calmo</li>
    <li>Nao force se bebe nao estiver colaborativo</li>
</ul>

<h2>Duracao estimada: 20 minutos</h2>

<div style="color: #c41e3a; border: 2px solid #c41e3a; padding: 10px; margin-top: 20px;">
    <strong>Para mais detalhes, assista o video oficial:</strong><br>
    <a href="https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link" target="_blank">
    Tutorial de Captura do Recem-nascido - Google Drive</a>
</div>
""",
        "duration": "20 minutos"
    },

    12: {
        "id": 12,
        "course_id": 2,
        "title": "Etapa 5: Verificacao e Qualidade Final",
        "content": """
<h1>Etapa 5: Verificacao da Qualidade de Captura</h1>

<h2>Importancia da Verificacao</h2>
<p>A verificacao final garante:</p>
<ul>
    <li>Todas as digitais foram capturadas corretamente</li>
    <li>Qualidade suficiente para autenticacao futura</li>
    <li>Nenhuma coleta precisa ser refeita depois</li>
    <li>Record completo no sistema</li>
</ul>

<h2>Processo de Verificacao</h2>
<p><strong>Apos a captura, no sistema:</strong></p>
<ol>
    <li>Verifique se <strong>todas as 14 capturas</strong> sao mostradas:
        <ul>
            <li>4 da progenitora (polegares + indicadores)</li>
            <li>10 do recem-nascido (todos os dedos)</li>
        </ul>
    </li>
    <li>Confirme se cada uma mostra a imagem da digital</li>
    <li>Procure por avisos ou sinais de qualidade baixa</li>
</ol>

<h2>Checklist de Qualidade</h2>
<table border="1" cellpadding="10">
    <tr>
        <th>Item</th>
        <th>Verificar</th>
    </tr>
    <tr>
        <td>Imagem Clara</td>
        <td>Nao há desfoque ou distorcao</td>
    </tr>
    <tr>
        <td>Nucleo Visivel</td>
        <td>Padrao de linhas eh claramente visivel</td>
    </tr>
    <tr>
        <td>Posicionamento</td>
        <td>Dedo estava centrado na area de captura</td>
    </tr>
    <tr>
        <td>Completude</td>
        <td>Toda falange distal foi capturada</td>
    </tr>
    <tr>
        <td>Sem Artefatos</td>
        <td>Sem sujeira ou interferencias visíveis</td>
    </tr>
</table>

<h2>Caso Alguma Captura Esteja Ilegivel</h2>
<p><strong>Procure:</strong> Mensagens do sistema indicando "Qualidade Baixa"</p>

<p><strong>O que fazer:</strong></p>
<ol>
    <li>Identificar qual dedo tem problema</li>
    <li>Refazer apenas aquele dedo (nao o procedimento inteiro)</li>
    <li>Seguir mesma tecnica anterior</li>
    <li>Verificar novamente apos nova coleta</li>
</ol>

<h2>Limpeza Final do Scanner</h2>
<p>Apos todas as coletas:</p>
<ol>
    <li>Limpar completamente o visor do scanner</li>
    <li>Usar gaze macia e material nao-abrasivo</li>
    <li>Secar bem para evitar umidade residual</li>
    <li>Deixar equipamento pronto para proximo uso</li>
</ol>

<h2>Registro do Sucesso</h2>
<p>Quando tudo estiver OK:</p>
<ul>
    <li>Sistema deve mostrar confirmacao de "Coleta Completa"</li>
    <li>Dados estao salvos e sincronizados</li>
    <li>Processo foi bem-sucedido</li>
    <li>Mae e bebe podem ser liberados</li>
</ul>

<h2>Apos a Coleta - Cuidados Finais</h2>
<ul>
    <li>Tranquilizar a mae sobre o resultado</li>
    <li>Permitir que mae e bebe fiquem juntos</li>
    <li>Documentar no prontuario hospitalar se necessario</li>
    <li>Inform a mae sobre proximos passos (se houver)</li>
</ul>

<h2>Troubleshooting de Ultima Hora</h2>
<p>Se ainda houver bloqueios:</p>
<ol>
    <li>Contactar supervisor de treinamento</li>
    <li>Revisar cada dedo em detalhe</li>
    <li>Se problema persistir, refazer coleta inteira se instruido</li>
    <li>Documentar problema para melhoria futura</li>
</ol>

<h2>Duracao estimada: 12 minutos</h2>

<div style="color: #c41e3a; border: 2px solid #c41e3a; padding: 10px; margin-top: 20px;">
    <strong>Para mais detalhes, assista o video oficial:</strong><br>
    <a href="https://drive.google.com/file/d/1vKSLvP5WolPnjJa4y6ylrP9-rkvPwUqs/view?usp=drive_link" target="_blank">
    Tutorial de Verificacao - Google Drive</a>
</div>
""",
        "duration": "12 minutos"
    },
}

print("="*60)
print("Aulas Corrigidas Baseadas em Documentacao Oficial")
print("="*60)

for lesson_id, lesson in LESSONS_CORRECTED.items():
    print(f"\nAula {lesson_id}: {lesson['title']}")
    print(f"  Curso: {lesson['course_id']}")
    print(f"  Duracao: {lesson['duration']}")
    print(f"  Caracteres: {len(lesson['content'])}")

print("\n" + "="*60)
print(f"Total de {len(LESSONS_CORRECTED)} aulas corrigidas criadas")
print("="*60)
print("\nProxima etapa: Executar script para popular banco de dados")
print("Comando: python populate_lessons_with_corrected_content.py")
