"""
Aulas para: Biometria Infantil - Protocolo ETAN Avançado (Curso 4)
Baseado no documento: Treinamento Replicadores e Enfermeiras + INFANT.ID oficial

Este curso aprofunda o protocolo ETAN com casos especiais e troubleshooting.
Público-alvo: Enfermeiras que completaram o onboarding básico.
"""

def get_curso_4_aulas():
    """Aulas para: Biometria Infantil - Protocolo ETAN Avançado"""
    return [
        {
            'titulo': 'Introdução à Biometria Infantil',
            'descricao': 'Conceitos fundamentais sobre biometria em recém-nascidos',
            'ordem': 1,
            'duracao': 20,
            'video_url': '',
            'conteudo': '''
<div class="aula-container">
    <h1>Biometria Infantil - Conceitos Fundamentais</h1>
    
    <h2>O que é Biometria?</h2>
    <p>Biometria é o registro de características físicas únicas que tornam você, exclusivamente você! Para INFANT.ID, o foco principal é a <strong>impressão digital</strong>, que oferece:</p>
    
    <h3>4 Propriedades da Impressão Digital</h3>
    <ul>
        <li><strong>Unicidade:</strong> 99.9% acurácia - cada pessoa tem padrão único no mundo</li>
        <li><strong>Perenidade:</strong> Duram a vida toda (formam-se na 13ª semana de gestação)</li>
        <li><strong>Imutabilidade:</strong> Não mudam ao longo da vida</li>
        <li><strong>Classificabilidade:</strong> Podem ser categorizadas em padrões (Verticilo, Presilha, Arco)</li>
    </ul>
    
    <h2>Especificidades da Biometria Infantil</h2>
    <p>Bebês recém-nascidos têm características biométricas MUITO diferentes de adultos:</p>
    
    <h3>Desafios da Coleta em RN</h3>
    <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color: #f0f0f0;">
            <th style="padding: 10px; border: 1px solid #ddd;">Característica</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Desafio</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Solução</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Tamanho do dedo</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">3-4x menor que adulto</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Scanner infantil específico (ETAN)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Espessura da pele</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Pele muito delicada</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Pressão LEVE - deixe scanner trabalhar</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Vernix (substância branca)</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Cobre os dedos ao nascer</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Limpeza com solução ETAN antes</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Umidade natural</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Pele muito úmida ou seca</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Ajuste de umidade (seque ou hidrate)</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Comportamento</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Choro, reflexos (grasping)</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Paciência e espera de acalmia</td>
        </tr>
    </table>
    
    <h2>Tipos de Padrões de Digitais</h2>
    <p>Todos os recém-nascidos possuem um dos 4 padrões principais:</p>
    <ul>
        <li><strong>Verticilo:</strong> Padrão em espiral (mais comum)</li>
        <li><strong>Presilha Externa:</strong> Padrão em arco aberto</li>
        <li><strong>Presilha Interna:</strong> Padrão em arco fechado</li>
        <li><strong>Arco:</strong> Padrão em linhas horizontais (mais raro)</li>
    </ul>
    
    <h2>Por que isso importa?</h2>
    <p>A biometria infantil é a base para:</p>
    <ul>
        <li>Identificação civil segura desde o nascimento</li>
        <li>Prevenção de tráfico infantil (problema sério na região)</li>
        <li>Vínculo seguro entre criança e documentação</li>
        <li>Futuro digital seguro da criança</li>
    </ul>
    
    <h2>Próximas Etapas</h2>
    <p>Nas aulas seguintes você aprenderá:</p>
    <ul>
        <li>Protocolo ETAN passo a passo (5 fases)</li>
        <li>Casos especiais (prematuro, vernix, grasping, etc)</li>
        <li>Troubleshooting prático</li>
        <li>Qualidade de captura vs velocidade</li>
    </ul>
</div>
''',
        },
        
        {
            'titulo': 'Protocolo ETAN - As 5 Fases Completas',
            'descricao': 'Entenda cada fase do protocolo de coleta biométrica',
            'ordem': 2,
            'duracao': 25,
            'video_url': '',
            'conteudo': '''
<div class="aula-container">
    <h1>Protocolo ETAN - 5 Fases de Coleta</h1>
    
    <h2>Visão Geral</h2>
    <p>O protocolo ETAN é dividido em 5 fases bem definidas. Cada fase é crucial para o sucesso da coleta.</p>
    
    <h3>Duração Total Estimada: ~12 minutos</h3>
    
    <h2>FASE 1: PREPARAÇÃO (5 minutos)</h2>
    <p><strong>Objetivo:</strong> Verificar estabilidade e preparar ambiente</p>
    
    <h4>Passos:</h4>
    <ol>
        <li><strong>Verificar Sinais Vitais do Bebê</strong>
            <ul>
                <li>Respiração: Normal? (30-60 respirações/min)</li>
                <li>Frequência Cardíaca: Estável? (120-160 bpm)</li>
                <li>Oxigenação: OK? (>95% SpO2)</li>
                <li>Temperatura: Adequada? (36.5-37.5°C)</li>
            </ul>
        </li>
        <li><strong>Se qualquer vital estiver anormal:</strong> AGUARDE estabilização ou chame médico</li>
        <li><strong>Preparar Ambiente</strong>
            <ul>
                <li>Local calmo (reduz stimulus)</li>
                <li>Temperatura adequada</li>
                <li>Luz suficiente para visualizar dedos</li>
            </ul>
        </li>
        <li><strong>Preparar Material</strong>
            <ul>
                <li>Solução ETAN (soro fisiológico + shampoo neutro infantil)</li>
                <li>Gaze estéril (múltiplas unidades)</li>
                <li>Toalha macia e limpa</li>
                <li>Scanner ETAN (conectado e funcionando)</li>
            </ul>
        </li>
        <li><strong>Informar Progenitora</strong>
            <ul>
                <li>Explicar o procedimento</li>
                <li>Informar que é não-invasivo</li>
                <li>Obter consentimento informado</li>
                <li>Deixar progenitora próxima (conforta o bebê)</li>
            </ul>
        </li>
    </ol>
    
    <h2>FASE 2: LIMPEZA (5 minutos)</h2>
    <p><strong>Objetivo:</strong> Remover vernix, umidade e sujidade</p>
    
    <h4>Procedimento:</h4>
    <ol>
        <li><strong>Limpe as mãos com Solução ETAN</strong>
            <ul>
                <li>Passe suavemente em cada dedo</li>
                <li>Limpe entre os dedos</li>
                <li>Use movimento suave (não esfregue)</li>
            </ul>
        </li>
        <li><strong>Enxugue com Gaze Estéril</strong>
            <ul>
                <li>Gaze SECA (não úmida)</li>
                <li>Seque completamente cada dedo</li>
                <li>Importante: remover TODA umidade</li>
            </ul>
        </li>
        <li><strong>Verifique Limpeza</strong>
            <ul>
                <li>Dedos devem estar COMPLETAMENTE limpos</li>
                <li>Sem restos de vernix (substância esbranquiçada)</li>
                <li>Sem sujeira visível</li>
            </ul>
        </li>
        <li><strong>Se Vernix Persiste</strong>
            <ul>
                <li>Repita limpeza com solução ETAN</li>
                <li>Seque bem novamente</li>
                <li>Pode precisar de 2-3 tentativas (normal!)</li>
            </ul>
        </li>
    </ol>
    
    <h2>FASE 3: CAPTURA DA PROGENITORA (3 minutos)</h2>
    <p><strong>Objetivo:</strong> Coletar impressão digital da mãe/responsável</p>
    
    <h4>Procedimento:</h4>
    <ol>
        <li><strong>Explicar à Mãe</strong>
            <ul>
                <li>Sua impressão vincula você ao bebê</li>
                <li>Será rápido (30-60 segundos)</li>
            </ul>
        </li>
        <li><strong>Coletar Dedos da Progenitora</strong>
            <ul>
                <li>Mesma ordem: mão direita, depois esquerda</li>
                <li>10 dedos no total</li>
                <li>Sistema vai guiar a progenitora</li>
            </ul>
        </li>
        <li><strong>Verificar Qualidade</strong>
            <ul>
                <li>Sistema deve confirmar aceitação de cada dedo</li>
                <li>Se rejeitado: tentar novamente</li>
            </ul>
        </li>
    </ol>
    
    <h2>FASE 4: CAPTURA DO RECÉM-NASCIDO (10 dedos = ~3-4 minutos)</h2>
    <p><strong>Objetivo:</strong> Coletar 10 dedos do bebê em qualidade alta</p>
    
    <h4>Procedimento Exato:</h4>
    <ol>
        <li><strong>ORDEM CORRETA (NUNCA MUDE):</strong>
            <ul>
                <li>👆 Polegar Direito</li>
                <li>👆 Dedo Indicador Direito</li>
                <li>👆 Dedo Médio Direito</li>
                <li>👆 Dedo Anelar Direito</li>
                <li>👆 Dedo Mínimo Direito</li>
                <li>✋ (Troque de mão)</li>
                <li>👆 Polegar Esquerdo</li>
                <li>👆 Dedo Indicador Esquerdo</li>
                <li>👆 Dedo Médio Esquerdo</li>
                <li>👆 Dedo Anelar Esquerdo</li>
                <li>👆 Dedo Mínimo Esquerdo</li>
            </ul>
        </li>
        <li><strong>Posicionamento Correto</strong>
            <ul>
                <li>Dedo RETO (não inclinado)</li>
                <li>No MEIO da área de captura</li>
                <li>Sistema indicará com mensagem visual</li>
            </ul>
        </li>
        <li><strong>Pressão Adequada</strong>
            <ul>
                <li>LEVE - é só um carinho no dedo</li>
                <li>Nunca force ou aperte</li>
                <li>Deixe o scanner fazer o trabalho</li>
                <li>Dedinhos são frágeis!</li>
            </ul>
        </li>
        <li><strong>Limpeza Entre Dedos</strong>
            <ul>
                <li>ANTES de cada novo dedo: limpe o scanner</li>
                <li>Gaze SECA (não molhe)</li>
                <li>Remova restos de pele, umidade, sujeira</li>
                <li>Isso é CRÍTICO para qualidade!</li>
            </ul>
        </li>
        <li><strong>Controle de Umidade</strong>
            <ul>
                <li>Se dedo muito seco: imagen fica clara demais</li>
                <li>Se dedo muito úmido: imagem fica escura demais</li>
                <li>Ponto de ouro = umidade natural (nem seco, nem molhado)</li>
            </ul>
        </li>
        <li><strong>Se Bebê Chorar</strong>
            <ul>
                <li>PAUSE IMEDIATAMENTE</li>
                <li>Deixe progenitora confortar (30-60 segundos)</li>
                <li>Retome quando bebê acalmar</li>
                <li>Máximo 2 pausas - depois avaliar com médico</li>
            </ul>
        </li>
        <li><strong>Confirmação de Cada Dedo</strong>
            <ul>
                <li>Sistema confirmará quando dedo aceitável</li>
                <li>Se rejeitado: tente novamente neste dedo</li>
                <li>Qualidade > Velocidade (importante!)</li>
            </ul>
        </li>
    </ol>
    
    <h2>FASE 5: VERIFICAÇÃO E FINALIZAÇÃO (2 minutos)</h2>
    <p><strong>Objetivo:</strong> Validar qualidade e registrar</p>
    
    <h4>Procedimento:</h4>
    <ol>
        <li><strong>Verificar Qualidade de Todas as Digitais</strong>
            <ul>
                <li>Sistema mostrará score de qualidade (NFIQ)</li>
                <li>Score >70: Excelente</li>
                <li>Score 50-70: Aceitável (considere repetir se puder)</li>
                <li>Score <50: Rejeitado - refaça deste dedo</li>
            </ul>
        </li>
        <li><strong>Se Alguma Falhou</strong>
            <ul>
                <li>Limpe o scanner bem</li>
                <li>Reptente APENAS aquele dedo</li>
                <li>Não precisa refazer tudo!</li>
            </ul>
        </li>
        <li><strong>Registrar Dados</strong>
            <ul>
                <li>Sistema salva automaticamente</li>
                <li>Confirme que todos os dados foram registrados</li>
                <li>Documento será gerado com dados de ambos</li>
            </ul>
        </li>
        <li><strong>Desconectar Scanner</strong>
            <ul>
                <li>Desconecte o USB corretamente</li>
                <li>Previne danos (não puxe bruscamente)</li>
            </ul>
        </li>
        <li><strong>Higienizar Mãos</strong>
            <ul>
                <li>Limpe as mãos e dedos do bebê novamente</li>
                <li>Pode usar a solução ETAN</li>
                <li>Remova qualquer resíduo</li>
            </ul>
        </li>
        <li><strong>Imprimir Recibo</strong>
            <ul>
                <li>Imprima comprovante de coleta</li>
                <li>Entregue cópia à progenitora</li>
            </ul>
        </li>
    </ol>
    
    <h2>Resumo da Duração</h2>
    <ul>
        <li>Fase 1 (Prep): 5 minutos</li>
        <li>Fase 2 (Limpeza): 5 minutos</li>
        <li>Fase 3 (Progenitora): 3 minutos</li>
        <li>Fase 4 (RN): 3-4 minutos</li>
        <li>Fase 5 (Verificação): 2 minutos</li>
        <li><strong>TOTAL: ~12-18 minutos (depende do RN)</strong></li>
    </ul>
    
    <h2>Dica de Ouro 💡</h2>
    <p><strong>Qualidade em Primeiro Lugar:</strong> Nunca se apresse. Se estiver demorando é porque está fazendo certo! Uma coleta de qualidade vale mais que 5 tentativas fracassadas.</p>
</div>
''',
        },
        
        {
            'titulo': 'Casos Especiais: Bebês Desafiadores',
            'descricao': 'Como lidar com situações específicas de difícil coleta',
            'ordem': 3,
            'duracao': 30,
            'video_url': '',
            'conteudo': '''
<div class="aula-container">
    <h1>Casos Especiais - Protocolos para Situações Difíceis</h1>
    
    <h2>Introdução</h2>
    <p>Nem todo recém-nascido é igual. Esta aula ensina como lidar com casos mais desafiadores mantendo a segurança e qualidade.</p>
    
    <h2>CASO 1: RECÉM-NASCIDO PREMATURO</h2>
    <p><strong>Definição:</strong> Nascimento antes de 37 semanas de gestação</p>
    
    <h3>Características Biométricas:</h3>
    <ul>
        <li>Peso menor (1-2.5 kg)</li>
        <li>Dedos ainda mais delicados</li>
        <li>Vernix mais espessa</li>
        <li>Pele mais fragilizada</li>
        <li>Sem gordura subcutânea</li>
    </ul>
    
    <h3>Protocolo Modificado:</h3>
    <ol>
        <li><strong>Verificação Clínica EXTRA:</strong>
            <ul>
                <li>Prematuros são instáveis clinicamente</li>
                <li>Confirme com médico/enfermeiro antes de coletar</li>
                <li>Verificar suporte respiratório (está em O2? Em ventilador?)</li>
                <li>Se em UTI neonatal: coordenar com equipe</li>
            </ul>
        </li>
        <li><strong>Limpeza com Cuidado Extra:</strong>
            <ul>
                <li>Movimentos AINDA mais suaves</li>
                <li>Vernix pode ser muito espessa - paciência!</li>
                <li>Pode precisar de 3-4 limpezas</li>
            </ul>
        </li>
        <li><strong>Dedos são EXTREMAMENTE Frágeis:</strong>
            <ul>
                <li>Pressão deve ser mínima (praticamente nenhuma)</li>
                <li>Deixe scanner fazer 100% do trabalho</li>
            </ul>
        </li>
        <li><strong>Umidade Especial Atenção:</strong>
            <ul>
                <li>Pele muito seca naturalmente</li>
                <li>Pode precisar hidratar (água filtrada)</li>
                <li>Secar BEM após</li>
            </ul>
        </li>
        <li><strong>Timing:</strong>
            <ul>
                <li>Evite logo após procedimentos (mais instáveis)</li>
                <li>Melhor durante fases calmas do RN</li>
                <li>Pode levar 15-20 minutos (mais longo = normal!)</li>
            </ul>
        </li>
    </ol>
    
    <h2>CASO 2: BEBÊ COM VERNIX ESPESSO</h2>
    <p><strong>O que é:</strong> Substância branca que cobre RN ao nascer (proteção uterina)</p>
    
    <h3>Desafio:</h3>
    <p>Vernix bloqueia a coleta de impressão digital da qualidade.</p>
    
    <h3>Solução:</h3>
    <ol>
        <li><strong>Primeira Limpeza:</strong>
            <ul>
                <li>Use solução ETAN (soro + shampoo)</li>
                <li>Passe suavemente, não esfregue</li>
                <li>Pode levar 2-3 minutos por mão</li>
            </ul>
        </li>
        <li><strong>Secar Completamente:</strong>
            <ul>
                <li>Gaze SECA deve remover toda umidade</li>
                <li>Verifique entre os dedos</li>
            </ul>
        </li>
        <li><strong>Aguardar 2-3 Minutos:</strong>
            <ul>
                <li>Deixe a pele "respirar"</li>
                <li>Umidade natural normalizará</li>
            </ul>
        </li>
        <li><strong>Tentar Coleta:</strong>
            <ul>
                <li>Se qualidade baixa: refaça limpeza</li>
                <li>Persistência é chave</li>
            </ul>
        </li>
        <li><strong>Não Desista:</strong>
            <ul>
                <li>99% dos casos se resolvem com paciência</li>
                <li>Vernix sai da pele dentro de 24 horas</li>
                <li>Se muito difícil agora: coleta depois (permissível)</li>
            </ul>
        </li>
    </ol>
    
    <h2>CASO 3: BEBÊ CHORANDO/AGITADO</h2>
    <p><strong>Realidade:</strong> Bebês choram! Isso é normal.</p>
    
    <h3>Protocolo:</h3>
    <ol>
        <li><strong>NUNCA Force a Coleta</strong>
            <ul>
                <li>RN chorando = mais agitação = qualidade ruim</li>
                <li>Você machuca sem perceber (ainda que levemente)</li>
            </ul>
        </li>
        <li><strong>Pausa Imediata:</strong>
            <ul>
                <li>Quando começar choro PARE</li>
                <li>Tire o dedo do scanner</li>
                <li>Relaxe e reassegure o bebê</li>
            </ul>
        </li>
        <li><strong>Deixar Progenitora Confortar:</strong>
            <ul>
                <li>Pele a pele é o melhor</li>
                <li>Deixe progenitora falar suavemente</li>
                <li>Escureça um pouco o ambiente</li>
            </ul>
        </li>
        <li><strong>Aguardar Acalmia (30-60 segundos):</strong>
            <ul>
                <li>Espere respiração normalizar</li>
                <li>Observe se acalmou</li>
            </ul>
        </li>
        <li><strong>Retomar Com Cuidado:</strong>
            <ul>
                <li>Comece pelo mesmo dedo (não pule)</li>
                <li>Ou comece por novo dedo se mais confortável</li>
            </ul>
        </li>
        <li><strong>Se Choro Persistir:</strong>
            <ul>
                <li>Máximo 2 pausas por dedo</li>
                <li>Se choro continua após 2 pausas:</li>
                <li>PARA e repita o dedo depois</li>
                <li>After 2-3 dedos repetidos: para sessão</li>
                <li>Voltam em 1-2 horas para tentar novamente</li>
            </ul>
        </li>
    </ol>
    
    <h2>CASO 4: REFLEXO DE GRASPING FORTE</h2>
    <p><strong>O que é:</strong> Reflexo de bebê agarrar (coisa de RN normal)</p>
    
    <h3>Desafio:</h3>
    <p>RN agarra seu dedo com força, dificultando posicionamento no scanner.</p>
    
    <h3>Solução:</h3>
    <ol>
        <li><strong>Entenda que é Normal:</strong>
            <ul>
                <li>Todos os RNs têm este reflexo</li>
                <li>Não significa que há problema</li>
                <li>Não machuca o bebê</li>
            </ul>
        </li>
        <li><strong>Use a Favor:</strong>
            <ul>
                <li>Coloque seu dedo suavemente próximo à palma</li>
                <li>Deixe o RN agarrar</li>
                <li>Isso acalma o bebê</li>
            </ul>
        </li>
        <li><strong>Posicione Com Suavidade:</strong>
            <ul>
                <li>COM O GRASPING ATIVO, leve o dedo do bebê ao scanner</li>
                <li>Coloque de forma suave no meio da área</li>
                <li>Mantenha seu dedo PERTO para conforto</li>
            </ul>
        </li>
        <li><strong>Cuando Capturar:</strong>
            <ul>
                <li>Assim que dedo estiver bem posicionado</li>
                <li>Pressione levemente para captura</li>
                <li>Recolha quando sistema confirme</li>
            </ul>
        </li>
        <li><strong>Paciência:</strong>
            <ul>
                <li>Pode levar 2-3 tentativas por dedo</li>
                <li>Isso é normal e aceitável</li>
                <li>Qualidade importa mais que velocidade</li>
            </ul>
        </li>
    </ol>
    
    <h2>CASO 5: DEDOS MUITO SECOS (Imagem Clara Demais)</h2>
    <p><strong>Sintoma:</strong> Scanner mostra imagem muito clara, sem contraste</p>
    
    <h3>Causa:</h3>
    <ul>
        <li>Ambiente muito seco (inverno, ar condicionado)</li>
        <li>RN com dermatite ou pele ressequida</li>
        <li>Tempo entre secagem e captura muito longo</li>
    </ul>
    
    <h3>Solução:</h3>
    <ol>
        <li><strong>Hidratar Levemente:</strong>
            <ul>
                <li>Mergulhe as PONTAS dos dedos em água filtrada/destilada</li>
                <li>1-2 segundos apenas (não de banho!)</li>
                <li>Remova secado que ocorra pele absor</li>
            </ul>
        </li>
        <li><strong>Secar Meticulosamente:</strong>
            <ul>
                <li>Gaze seca (NÃO esfregue)</li>
                <li>Deixe umidade mínima (brilho suave)</li>
            </ul>
        </li>
        <li><strong>Tentar Captura:</strong>
            <ul>
                <li>Ponto de ouro = dedos com brilho úmido natural</li>
                <li>Imagem capturada deve ter bom contraste</li>
            </ul>
        </li>
        <li><strong>Se Persistir:</strong>
            <ul>
                <li>Aguarde 1-2 minutos para pele estabilizar</li>
                <li>Répetir hidrataçãoleve</li>
            </ul>
        </li>
    </ol>
    
    <h2>CASO 6: DEDOS MUITO ÚMIDOS (Imagem Escura Demais)</h2>
    <p><strong>Sintoma:</strong> Scanner mostra imagem muito escura, sem detalhe</p>
    
    <h3>Causa:</h3>
    <ul>
        <li>Suor natural do RN (comum em ambiente quente)</li>
        <li>Secagem incompleta antes</li>
        <li>RN transpirando de ansiedade</li>
    </ul>
    
    <h3>Solução:</h3>
    <ol>
        <li><strong>Secar Muito Bem:</strong>
            <ul>
                <li>Use gaze SECA múltiplas vezes</li>
                <li>Entre os dedos também</li>
                <li>Não tenha pressa nesta etapa</li>
            </ul>
        </li>
        <li><strong>Aguardar Areação:</strong>
            <ul>
                <li>Deixe dedos "respirarem" 1-2 minutos</li>
                <li>Umidade se estabilizará</li>
            </ul>
        </li>
        <li><strong>Tentar Novamente:</strong>
            <ul>
                <li>Qualidade deve estar melhor</li>
                <li>Se melhorou: continuar</li>
            </ul>
        </li>
        <li><strong>ambiente:</strong>
            <ul>
                <li>Se ambiente muito quente: busque local mais fresco</li>
                <li>Ou espere temperatura estabilizar</li>
            </ul>
        </li>
    </ol>
    
    <h2>Checklist para Casos Especiais</h2>
    <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color: #f0f0f0;">
            <th style="padding: 10px; border: 1px solid #ddd;">Caso</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Chave</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Não Esqueça</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Prematuro</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Verificar estabilidade</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Pressão MÍNIMA</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Vernix</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Limpeza + Paciência</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Pode precisar 3-4x</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Choro</td>
            <td style="padding: 10px; border: 1px solid #ddd;">PARAR imediatamente</td>
            <td style="padding: 1px; border: 1px solid #ddd;">Conforto primeiro</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Grasping</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Usar a favor</td>
            <td style="padding: 10px; border: 1px solid #ddd;">RN fica calmo</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Pele Seca</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Hidratar + Secar</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Umidade é ouro</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Úmido</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Secar MUITO bem</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Qualidade essencial</td>
        </tr>
    </table>
</div>
''',
        },
        
        {
            'titulo': 'Troubleshooting: Resolvendo Problemas',
            'descricao': 'Como diagnosticar e resolver problemas comuns',
            'ordem': 4,
            'duracao': 20,
            'video_url': '',
            'conteudo': '''
<div class="aula-container">
    <h1>Troubleshooting - Resolvendo Problemas na Prática</h1>
    
    <h2>Introdução</h2>
    <p>Às vezes as coisas não correm como o planejado. Esta aula ensina como diagnosticar problemas rapidamente.</p>
    
    <h2>PROBLEMA 1: Impression Sempre Borrada</h2>
    
    <h3>Diagnóstico:</h3>
    <ul>
        <li>Imagem visualizada no scanner é pouco clara</li>
        <li>Sistema rejeita com mensagem de qualidade baixa</li>
        <li>Padrão das cristas digitais não visível</li>
    </ul>
    
    <h3>Causas (em ordem de probabilidade):</h3>
    <ol>
        <li><strong>MAIS COMUM (99%):</strong> Scanner não está limpo!
            <ul>
                <li>Restos de pele anterior acumulado</li>
                <li>Suor/umidade residual</li>
            </ul>
        </li>
        <li><strong>Dedos do bebê sujos:</strong>
            <ul>
                <li>Vernix não foi removido completamente</li>
                <li>Limpeza incompleta</li>
            </ul>
        </li>
        <li><strong>Umidade inadequada:</strong>
            <ul>
                <li>Dedos muito molhados (escurecimento)</li>
                <li>Dedos muito secos (clareza excessiva)</li>
            </ul>
        </li>
    </ol>
    
    <h3>Solução Passo a Passo:</h3>
    <ol>
        <li><strong>Primeiro:</strong> LIMPE O SCANNER!
            <ul>
                <li>Pegue gaze SECA</li>
                <li>Limpe a área de captura gentle mas FIRME</li>
                <li>Mude para nova gaze, faça novamente</li>
                <li>Terceira gaze: deveria sair limpa</li>
            </ul>
        </li>
        <li><strong>Depois:</strong> Repita captura do mesmo dedo
            <ul>
                <li>Se melhorou: ótimo! Continue</li>
                <li>Se continuou borrrado: próximo passo</li>
            </ul>
        </li>
        <li><strong>Terceiro:</strong> Verifique dedos do bebê
            <ul>
                <li>Ainda tem vernix? Relimpe com solução ETAN</li>
                <li>Estão sujos? Relimpe e seque BEM</li>
            </ul>
        </li>
        <li><strong>Quarto:</strong> Ajuste umidade
            <ul>
                <li>Se muito seco: hidrate levemente</li>
                <li>Se muito úmido: seque melhor</li>
            </ul>
        </li>
        <li><strong>Quinto:</strong> Tente novamente
            <ul>
                <li>Dessa vez deve estar melhor</li>
                <li>Se ainda borrrado: considere próxima etapa</li>
            </ul>
        </li>
    </ol>
    
    <h3>Quando Chamar Suporte:</h3>
    <p>Se após todos estes passos a imagem CONTINUA borrada:</p>
    <ul>
        <li>Pode haver problema no scanner (raro)</li>
        <li>Abra chamado: akiyama.com.br/suporte</li>
        <li>Descreva: "Todas as imagens borrradas após limpeza"</li>
    </ul>
    
    <h2>PROBLEMA 2: Sistema Diz "Impressão Rejeitada"</h2>
    
    <h3>Significado:</h3>
    <p>Sistema analisou imagem e determinou que não atende qualidade mínima (NFIQ < 50)</p>
    
    <h3>Causas Possíveis:</h3>
    <ol>
        <li>Scanner sujo (causa #1)</li>
        <li>Dedo não está bem posicionado</li>
        <li>Pressão insuficiente ou excessiva</li>
        <li>Umidade inadequada</li>
        <li>Dedos mal limpos</li>
    </ol>
    
    <h3>O Que Fazer:</h3>
    <ol>
        <li><strong>Não Desista!</strong> Rejeição é normal às vezes
            <ul>
                <li>Alguns dedos precisam de 2-3 tentativas</li>
                <li>Especial em RN pequenos</li>
            </ul>
        </li>
        <li><strong>Siga Checklist:</strong>
            <ul>
                <li>Scanner limpo? ✓</li>
                <li>Dedo bem posicionado? ✓</li>
                <li>Pressão adequada? ✓</li>
                <li>Umidade OK? ✓</li>
            </ul>
        </li>
        <li><strong>Tente Novamente</strong>
            <ul>
                <li>Com todos estes ajustes, deve aceitar</li>
            </ul>
        </li>
        <li><strong>Se Ainda Rejeitar (3+ rejeições no mesmo dedo):</strong>
            <ul>
                <li>Dedo pode ter características especiais</li>
                <li>Pule para próximo dedo</li>
                <li>Retorne depois ou em sessão futura</li>
            </ul>
        </li>
    </ol>
    
    <h2>PROBLEMA 3: Scanner Não Conecta</h2>
    
    <h3>Sintoma:</h3>
    <p>Plugou USB mas sistema não reconhece scanner</p>
    
    <h3>Solução Rápida:</h3>
    <ol>
        <li><strong>Desconectar e Reconectar:</strong>
            <ul>
                <li>Retire o cabo USB completamente</li>
                <li>Aguarde 5 segundos</li>
                <li>Reconecte lentamente</li>
                <li>Aguarde sistema reconhecer (10-15 segundos)</li>
            </ul>
        </li>
        <li><strong>Se Ainda Não Funcione:</strong>
            <ul>
                <li>Tente outro porto USB (se houver)</li>
            </ul>
        </li>
        <li><strong>Se Nunca Funcionar:</strong>
            <ul>
                <li>Scanner pode ter problema</li>
                <li>Abra chamado de suporte imediatamente</li>
                <li>Forneça número do kit/scanner</li>
            </ul>
        </li>
    </ol>
    
    <h2>PROBLEMA 4: Dedo Falha em Todos os Dedos (Não é o Scanner)</h2>
    
    <h3>Quando Acontece:</h3>
    <p>Vários dedos falham sequencialmente, não é problema técnico</p>
    
    <h3>Causa Provável:</h3>
    <ul>
        <li>RN tem alguma característica biométrica especial</li>
        <li>Pele muito seca naturalmente</li>
        <li>Padrão de crista muito fino</li>
        <li>Plasticidade de pele alta (comum em RN)</li>
    </ul>
    
    <h3>O que Fazer:</h3>
    <ol>
        <li><strong>Persistir Com Técnicas:</strong>
            <ul>
                <li>Hidratar dedos</li>
                <li>Tentar posições ligeiramente diferentes</li>
                <li>Múltiplas forças de pressão</li>
            </ul>
        </li>
        <li><strong>Se Eventualmente Funcionar:</strong>
            <ul>
                <li>Ótimo! Alguns RN precisam desta persistência</li>
                <li>Todas as pessoas têm digitais colectáveis eventually</li>
            </ul>
        </li>
        <li><strong>Se Realmente Não Funcionar Após Muitas Tentativas:</strong>
            <ul>
                <li>Raro, mas pode acontecer</li>
                <li>Fazer anotação: "RN com dificuldade de captura biométrica"</li>
                <li>Tentar novamente em 1-2 dias (pele pode estabilizar)</li>
                <li>Contactar supervisor e suporte</li>
            </ul>
        </li>
    </ol>
    
    <h2>Quadro Rápido de Diagnóstico</h2>
    
    <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color: #f0f0f0;">
            <th style="padding: 10px; border: 1px solid #ddd;">Problema</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Causa #1</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Solução Rápida</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Imagem Borrada</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Scanner sujo!</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Limpe com gaze seca</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Rejeitado</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Qualidade baixa</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Limpe + tente novamente</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Sem Conexão</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Cabo solto</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Desconecte/reconecte</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Falhas Múltiplas</td>
            <td style="padding: 10px; border: 1px solid #ddd;">RN especial</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Persistir + retry depois</td>
        </tr>
    </table>
    
    <h2>Contatos Importantes</h2>
    <ul>
        <li><strong>Suporte Técnico:</strong> akiyama.com.br/suporte</li>
        <li><strong>Dúvida Médica:</strong> Médico de plantão</li>
        <li><strong>Insegurança:</strong> Supervisor/Treinador</li>
    </ul>
</div>
''',
        },
        
        {
            'titulo': 'Qualidade vs Velocidade - A Importância de Fazer Certo',
            'descricao': 'Por que qualidade é SEMPRE mais importante que rapidez',
            'ordem': 5,
            'duracao': 15,
            'video_url': '',
            'conteudo': '''
<div class="aula-container">
    <h1>Qualidade vs Velocidade: A Filosofia Correta</h1>
    
    <h2>A Tentação da Pressa</h2>
    <p>É fácil pensar: "Preciso ser rápido! O bebê está chorando, a mãe está ansiosa, tenho outros pacientes..."</p>
    
    <p><strong>Mas PARE e pense:</strong> Uma coleta de má qualidade gera problemas futuros MUITO maiores.</p>
    
    <h2>Impacto de Qualidade Ruim</h2>
    
    <h3>Em Curto Prazo (Hoje):</h3>
    <ul>
        <li>❌ Sistema não reconhece impressão</li>
        <li>❌ Documento não pode ser emitido</li>
        <li>❌ Progenitora precisa voltar (mais incômodo!)</li>
        <li>❌ Bebê coleta NOVAMENTE (trauma desnecessário)</li>
    </ul>
    
    <h3>Em Longo Prazo (Futuro):</h3>
    <ul>
        <li>❌ ID biométrico fraco = problemas de verificação depois</li>
        <li>❌ Segurança comprometida</li>
        <li>❌ Possível confusão de identidade (risco serio!)</li>
        <li>❌ Criança prejudicada documentalmente</li>
    </ul>
    
    <h2>Benefício de Fazer Certo</h2>
    
    <h3>Fazer coleta de QUALIDADE significa:</h3>
    <ul>
        <li>✅ Criança tem identidade civil segura PARA A VIDA</li>
        <li>✅ Documento emitido na primeira vez</li>
        <li>✅ Segurança contra tráfico infantil</li>
        <li>✅ Progenitora confia no seu trabalho</li>
        <li>✅ Você ganha reputação de profissional competente</li>
    </ul>
    
    <h2>Estatísticas de Campo</h2>
    <table style="width:100%; border-collapse: collapse;">
        <tr style="background-color: #f0f0f0;">
            <th style="padding: 10px; border: 1px solid #ddd;">Abordagem</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Tempo Total</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Recoletas</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Taxa Sucesso</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Corrida (qualidade baixa)</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">8 min</td>
            <td style="padding: 10px; border: 1px solid #ddd;">3-4 recoletas</td>
            <td style="padding: 10px; border: 1px solid #ddd;">50%</td>
        </tr>
        <tr style="background-color: #d4edda;">
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Meticuloso (qualidade alta)</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">15 min</td>
            <td style="padding: 10px; border: 1px solid #ddd;">0-1 recoleta</td>
            <td style="padding: 10px; border: 1px solid #ddd;">95%</td>
        </tr>
    </table>
    
    <p><strong>Resultado:</strong> Fazer certo a primeira vez economiza TEMPO total! (porque evita recoletas)</p>
    
    <h2>Mindset Correto</h2>
    
    <h3>❌ Pensamento ERRADO:</h3>
    <p><em>"Tenho que ser rápido. O bebê está chorando. Deixa eu terminar logo."</em></p>
    
    <h3>✅ Pensamento CORRETO:</h3>
    <p><em>"Fazer com qualidade é mais rápido no fim. Vou fazer certo, mesmo que demore 15-20 minutos agora."</em></p>
    
    <h2>Golden Rules</h2>
    <ol>
        <li><strong>Uma coleta perfeita > 10 coletas ruins</strong></li>
        <li><strong>Qualidade no scanner > Velocidade</strong></li>
        <li><strong>Limpeza bem feita = 80% do sucesso</strong></li>
        <li><strong>RN calmo = coleta melhor</strong></li>
        <li><strong>Melhor esperar 30 seg do que refazer tudo</strong></li>
    </ol>
    
    <h2>Quando "Rápido" Não Funciona</h2>
    
    <h3>Cenários onde pressa causa problemas:</h3>
    <ul>
        <li>Scanner não limpo "porque tenho pressa" → Imagem borrada</li>
        <li>Limpeza incompleta "porque est rápido" → Vernix atrapalha</li>
        <li>Não aguardar acalmia "porque estou atrasado" → RN agitado = qualidade ruim</li>
        <li>Presão excessiva "para capturar rápido" → RN chora mais + qualidade ruim</li>
    </ul>
    
    <h2>Seu Poder Como Profissional</h2>
    
    <p>Você tem o PODER de:</p>
    <ul>
        <li>✅ Dar à criança uma identidade civil segura</li>
        <li>✅ Protegê-la contra tráfico infantil</li>
        <li>✅ Criar um documento que a acompanhará POR TODA  a vida</li>
        <li>✅ Fazer diferença REAL no mundo</li>
    </ul>
    
    <p><strong>Isso é muito maior que uma coleta biométrica rápida!</strong></p>
    
    <h2>Resumo</h2>
    <ul>
        <li>🎯 Prioridade #1: QUALIDADE</li>
        <li>⏱️ Prioridade #2: Velocidade (consequência da qualidade)</li>
        <li>👶 Criança merece o melhor</li>
        <li>📝 Documento vale para a vida toda</li>
        <li>💪 Você consegue fazer certo!</li>
    </ul>
</div>
''',
        },
    ]

if __name__ == "__main__":
    print("Aulas do Curso 4 definidas com sucesso!")
    aulas = get_curso_4_aulas()
    print(f"Total de aulas: {len(aulas)}")
    for aula in aulas:
        print(f"  - {aula['titulo']} ({aula['duracao']} min)")
