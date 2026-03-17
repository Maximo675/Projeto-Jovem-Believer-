"""
Servico de IA para consultar e gerar respostas.
Suporta: Mock (demo com respostas humanizadas).
"""

import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from openai import OpenAI
from flask import current_app

# Importar knowledge base
try:
    from .knowledge_base import buscar_resposta, KNOWLEDGE_BASE
    KB_DISPONIVEL = True
except ImportError:
    KB_DISPONIVEL = False
    KNOWLEDGE_BASE = {}

class AiService:
    """Servico para interacoes com IA."""
    
    def __init__(self):
        """Inicializa o servico com IA disponível."""
        self.use_ollama = os.getenv('USE_OLLAMA', 'true').lower() == 'true'
        self.use_mock = os.getenv('USE_MOCK_AI', 'false').lower() == 'true'
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if self.use_mock:
            # Modo mock para demos
            print("[MOCK] AiService: Usando MOCK (demo mode)")
            self.mode = 'mock'
        elif self.use_ollama:
            # Tenta usar Ollama local
            try:
                self.client = OpenAI(
                    base_url="http://localhost:11434/v1",
                    api_key="not-needed"  # Ollama nao requer API key
                )
                print("[OLLAMA] AiService: Usando OLLAMA local")
                self.mode = 'ollama'
            except Exception as e:
                print(f"[FALLBACK] Ollama nao disponivel. Usando mock...")
                self.mode = 'mock'
        else:
            # OpenAI remoto
            if self.api_key:
                self.client = OpenAI(api_key=self.api_key)
                print("[OPENAI] AiService: Usando OpenAI remoto")
                self.mode = 'openai'
            else:
                print("[FALLBACK] Sem configuracao de IA. Usando mock.")
                self.mode = 'mock'
        
        self.model = os.getenv('OPENAI_MODEL', 'llama2')
    
    def responder_pergunta(self, pergunta, contexto_curso=None):
        """
        Responde uma pergunta usando Knowledge Base primeiro, depois IA.
        
        Args:
            pergunta (str): Pergunta do usuario
            contexto_curso (int): ID do curso (opcional, para contexto)
        
        Returns:
            tuple: (resposta, tokens_usados)
        """
        # CAMADA 1: Tentar buscar na Knowledge Base primeiro
        if KB_DISPONIVEL:
            resultado_kb = buscar_resposta(pergunta, contexto_curso)
            if resultado_kb['sucesso'] and resultado_kb['confianca'] > 0.8:
                return resultado_kb['resposta'], 0
        
        # CAMADA 2: Modo MOCK para fins de demonstracao (sempre funciona)
        if self.mode == 'mock':
            return self._responder_mock(pergunta, contexto_curso), 0
        
        # CAMADA 3: Modo Ollama ou OpenAI (mesma interface)
        
        try:
            system_prompt = self._construir_system_prompt(contexto_curso)
            
            # Llama2 ignora idioma no system prompt — forçar PT-BR na mensagem do usuário
            pergunta_pt = f"[RESPONDA APENAS EM PORTUGUÊS BRASILEIRO]\n{pergunta}"
            
            def _chamar_ollama():
                return self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": pergunta_pt}
                    ],
                    temperature=0.7,
                    max_tokens=800
                )
            
            # Timeout real via thread — OpenAI socket não respeita timeout interno
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_chamar_ollama)
                try:
                    response = future.result(timeout=30)
                except FuturesTimeout:
                    future.cancel()
                    raise Exception("Ollama timeout após 30s")
            
            resposta = response.choices[0].message.content
            tokens_usados = response.usage.total_tokens if response.usage else 0
            
            return resposta, tokens_usados
            
        except Exception as e:
            if self.mode == 'ollama':
                print(f"[FALLBACK] Ollama indisponivel. Usando mock...")
                self.mode = 'mock'
                return self._responder_mock(pergunta, contexto_curso), 0
            raise Exception(f"Erro ao consultar IA: {str(e)}")
    
    def _responder_mock(self, pergunta, contexto_curso=None):
        """
        Resposta simulada para fins de demonstração.
        Cobre os principais temas com respostas específicas e inclui links de vídeo.
        """
        pergunta_lower = pergunta.lower()

        # ── EMERGÊNCIA — verificação prioritária ──────────────────────────────
        emergencia_kw = ['urgente', 'instável', 'instavel', 'risco', 'emergência',
                         'emergencia', 'crítico', 'critico', 'cianose', 'roxo',
                         'dificuldade respiratória', 'dificuldade respiratoria',
                         'parou de respirar', 'inconsciente']
        if any(k in pergunta_lower for k in emergencia_kw):
            return """⚠️ **ATENÇÃO — PRIORIDADE CLÍNICA**

A segurança do RN ou da progenitora vem SEMPRE em primeiro lugar.

**Ações imediatas:**
1. **INTERROMPA** a coleta biométrica agora
2. **ACIONE a equipe médica** assistencial imediatamente
3. A coleta biométrica pode ser realizada **posteriormente**, quando mãe e bebê estiverem estáveis e fora de risco

O protocolo INFANT.ID determina que a seleção para coleta só ocorre quando ambos estão em **condições seguras**.

Quando a situação estiver estabilizada, pode voltar aqui e retomar a orientação. Há mais alguma coisa que possa ajudar agora?"""

        # ── TREINAMENTO / PRIMEIRA VEZ ────────────────────────────────────────
        treinamento_kw = ['primeira vez', 'como funciona', 'nunca fiz', 'novo',
                          'nova', 'aprender', 'treinar', 'visão geral', 'visao geral',
                          'me explica tudo', 'por onde começo', 'por onde começo',
                          'onboarding', 'introdução', 'introducao']
        if any(k in pergunta_lower for k in treinamento_kw):
            return """Bem-vinda ao sistema INFANT.ID! Vou te dar uma visão completa do processo.

**🎯 O processo tem 5 etapas:**

**1. Seleção** — Verificar se mãe e RN estão estáveis e liberar para coleta
📹 [Ver vídeo](https://drive.google.com/file/d/1uOILNO0clQYeP9PFpuvkaP1h4570kaRA/view?usp=sharing)

**2. Preparação** — Conforto, dados biográficos e higienização dos dedos
📹 [Ver vídeo](https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link)

**3. Captura Progenitora** — Digitais de 4 dedos (polegares + indicadores)
📹 [Ver vídeo](https://drive.google.com/file/d/1g55icK4TUhLpQxwsTgPbV0e09td8K8ln/view?usp=drive_link)

**4. Captura RN** — Digitais dos 10 dedos (decadactilar)
📹 [Ver vídeo](https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link)

**5. Verificação** — Checar qualidade das imagens no sistema
📹 [Ver vídeo](https://drive.google.com/file/d/1vKSLvP5WolPnjJa4y6ylrP9-rkvPwUqs/view?usp=drive_link)

**🔑 4 pontos para gravar:**
✅ Limpe o scanner com gaze seca **antes de cada dedo**
✅ Controle a umidade — nem encharcado, nem ressecado
✅ Pressão **leve** — o scanner faz o trabalho
✅ Verifique a qualidade após cada captura

Sobre qual etapa quer saber mais detalhes?"""

        # ── ABERTURA DE CHAMADO ───────────────────────────────────────────────
        chamado_kw = ['chamado', 'suporte', 'ticket', 'akiyama', 'abrir chamado',
                      'acionar suporte', 'contato técnico', 'contato tecnico']
        if any(k in pergunta_lower for k in chamado_kw):
            return """Vou te orientar para abrir um chamado técnico:

**📋 Passo a passo:**

1. Acesse: **akiyama.com.br/suporte**
2. Faça login com suas credenciais
3. Clique em **"Enviar um ticket"**
4. Preencha todos os campos:
   - Descreva o problema detalhadamente
   - Informe o que já foi tentado
   - Inclua o número de série do kit (se aplicável)
5. Clique em **"Enviar"**

**⏱️ Tempo de resposta:** conforme o SLA estabelecido com seu hospital.

**💡 Dica:** enquanto aguarda, use outro equipamento disponível ou anote os dados para coleta posterior.

Conseguiu abrir o chamado ou tem alguma dúvida sobre o processo?"""

        # ── PROBLEMA TÉCNICO — EQUIPAMENTO ───────────────────────────────────
        tecnico_kw = ['não funciona', 'nao funciona', 'erro', 'não reconhece',
                      'nao reconhece', 'desconectou', 'desconectado', 'descalibrado',
                      'problema', 'não liga', 'nao liga', 'usb', 'cabo',
                      'equipamento', 'scanner não', 'scanner nao', 'driver',
                      'antivírus', 'antivirus', 'porta usb', 'instalação', 'instalacao']
        if any(k in pergunta_lower for k in tecnico_kw):
            # Sub-caso: não reconhecido / desconectado
            if any(k in pergunta_lower for k in ['não reconhece', 'nao reconhece',
                                                  'desconectado', 'não reconhecido',
                                                  'nao reconhecido']):
                return """Entendo — o scanner aparece como **"Não Reconhecido"** ou **"Desconectado"**. Vamos resolver:

**Soluções em ordem:**

1️⃣ Troque a **porta USB** onde o scanner está conectado
   → Funcionou?

2️⃣ Desconecte o **USB-C do dispositivo** e reconecte firmemente
   → Funcionou?

3️⃣ Verifique se o **antivírus** não está bloqueando o dispositivo
   → Se sim, acione o TI para liberar o ETAN no antivírus

4️⃣ Reinicie o computador
   → Funcionou?

Se após esses passos o problema persistir:
→ Acesse **akiyama.com.br/suporte** → faça login → clique em **"Enviar um ticket"**
   Informe: porta USB testada, sistema operacional, número de série do kit

O problema foi resolvido?"""
            return """Vamos diagnosticar o problema juntas.

**Qual sintoma você está vendo?**
- 🔴 "Equipamento desconectado"
- 🔴 "Não reconhecido"
- 🔴 Imagem não aparece
- 🔴 Outro erro (me descreva)

Enquanto me responde, tente esses primeiros passos:
1️⃣ Verifique se o cabo USB-C está **firmemente conectado** nos dois lados
2️⃣ Troque para outra **porta USB** do computador
3️⃣ Desconecte e reconecte o dispositivo

Se nada funcionar: **akiyama.com.br/suporte** → "Enviar um ticket"

Me conta o que aconteceu!"""

        # ── QUALIDADE / IMAGEM BORRADA ────────────────────────────────────────
        qualidade_kw = ['borrada', 'ilegível', 'ilegivel', 'não captura',
                        'nao captura', 'ruim', 'falha na captura', 'não pega',
                        'nao pega', 'digital não', 'digital nao', 'imagem escura',
                        'imagem clara', 'muito clara', 'muito escura', 'qualidade']
        if any(k in pergunta_lower for k in qualidade_kw):
            return """Vamos resolver o problema de qualidade! Digitais com falha geralmente têm causas específicas:

**🔍 Checklist de diagnóstico — verifique nesta ordem:**

🔹 **O scanner está limpo?**
   → Limpe o visor com gaze **seca** antes de cada dedo
   → Essa é a causa mais comum!

🔹 **Há Vernix (substância branca) no dedo?**
   → Limpe com a solução NATO soro (soro fisiológico + clorexidina + shampoo neutro)
   → Aguarde 1-2 minutos antes de tentar novamente

🔹 **Os dedos estão muito úmidos?** (imagem escura/borrada)
   → Seque bem com gaze antes de capturar
   → Deixe arejar 10 segundos e tente novamente

🔹 **Os dedos estão muito secos?** (imagem muito clara/apagada)
   → Umedeça levemente com a solução, seque antes de capturar

🔹 **Posicionamento correto?**
   → Centralize a **falange distal** no visor
   → Pressão leve — sem pressionar demais

📹 **Vídeo — Captura do RN:** https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link

Após ajustar, refaça a captura. A qualidade melhorou?"""

        # ── ORDEM DOS DEDOS / PROTOCOLO DE COLETA RN ─────────────────────────
        ordem_kw = ['qual ordem', 'ordem dos dedos', 'ordem correta',
                    'ordem de coleta', 'sequência', 'sequencia', 'qual dedo primeiro',
                    'começa por qual', 'começa pelo', 'decadactilar']
        if any(k in pergunta_lower for k in ordem_kw):
            return """A ordem de coleta **decadactilar** do RN é:

**Mão Direita (inicia por):**
1. Polegar direito
2. Indicador direito
3. Médio direito
4. Anelar direito
5. Mínimo direito

**Mão Esquerda (continua com):**
6. Polegar esquerdo
7. Indicador esquerdo
8. Médio esquerdo
9. Anelar esquerdo
10. Mínimo esquerdo

**💡 Pontos-chave:**
→ Foque sempre na **falange distal**
→ Centralize o dedo no visor do scanner
⚠️ Limpe o scanner com gaze seca **entre cada dedo**

📹 **Vídeo — Captura do RN:** https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link

Tem dúvida sobre o posicionamento ou a técnica?"""

        # ── LIMPEZA DO SCANNER / ETAN ─────────────────────────────────────────
        if ('limpar' in pergunta_lower or 'limpeza' in pergunta_lower) and \
           any(k in pergunta_lower for k in ['etan', 'scanner', 'equipamento', 'leitor']):
            return """**Como limpar o scanner ETAN:**

A limpeza correta do scanner é essencial para garantir imagens de qualidade.

**🧹 Limpeza entre cada dedo (obrigatório):**
→ Use uma **gaze seca** (sem qualquer solução líquida no scanner)
→ Passe suavemente sobre a superfície do leitor
→ Aguarde 2 segundos antes de posicionar o próximo dedo

⚠️ **Nunca use:**
→ Álcool diretamente no scanner
→ Gaze molhada ou úmida no leitor
→ Pano, papel toalha ou tecido abrasivo

**✅ Quando limpar:**
→ Antes da primeira coleta do dia
→ Entre cada dedo durante a captura
→ Quando a imagem aparecer borrada ou escurecida
→ Sempre que houver resíduo visível no leitor

**💡 Dica:** A limpeza com gaze seca resolve cerca de **90% dos problemas de qualidade** de imagem!

Ficou claro? Tem mais alguma dúvida sobre o scanner?"""

        # ── PROTOCOLO GERAL / ETAPAS ──────────────────────────────────────────
        protocolo_kw = ['protocolo', 'protocolo etan', 'etapa', 'passo a passo', 'como coletar',
                        'como fazer a coleta', 'procedimento', 'coleta biométrica',
                        'coleta biometrica', 'como funciona a coleta', 'processo']
        if any(k in pergunta_lower for k in protocolo_kw):
            return """O protocolo ETAN tem **5 fases** bem definidas:

**[1] Seleção**
→ Verificar estabilidade clínica de mãe e RN com a equipe médica
📹 https://drive.google.com/file/d/1uOILNO0clQYeP9PFpuvkaP1h4570kaRA/view?usp=sharing

**[2] Preparação**
→ Conforto, coleta de dados biográficos, higienização com solução NATO soro
→ ⚠️ Controle a umidade: nem encharcado, nem ressecado
📹 https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link

**[3] Captura Progenitora**
→ 4 dedos: polegares + indicadores (direito e esquerdo)
→ Mesma técnica de limpeza e posicionamento
📹 https://drive.google.com/file/d/1g55icK4TUhLpQxwsTgPbV0e09td8K8ln/view?usp=drive_link

**[4] Captura RN**
→ 10 dedos (decadactilar): polegar direito → demais direitos → polegar esquerdo → demais esquerdos
→ Pressão LEVE — o scanner faz o trabalho
📹 https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link

**[5] Verificação**
→ Checar qualidade de todas as imagens no sistema; repetir as que ficaram borradas
📹 https://drive.google.com/file/d/1vKSLvP5WolPnjJa4y6ylrP9-rkvPwUqs/view?usp=drive_link

**🔑 Regra de ouro:** Limpe o scanner com gaze seca **antes de cada dedo** — resolve 90% dos problemas de qualidade!

Quer mais detalhes sobre alguma fase específica?"""

        # ── PREPARAÇÃO / HIGIENIZAÇÃO ─────────────────────────────────────────
        prep_kw = ['preparação', 'preparacao', 'higienização', 'higienizacao',
                   'limpar os dedos', 'limpar dedos', 'nato soro', 'soro fisiológico',
                   'soro fisiologico', 'clorexidina', 'shampoo', 'vernix', 'limpeza dos dedos']
        if any(k in pergunta_lower for k in prep_kw):
            return """**Etapa 2 — Preparação e Higienização:**

**Solução NATO soro (para limpeza dos dedos):**
→ Misture: soro fisiológico + clorexidina líquida + shampoo neutro infantil
→ Umedeça uma gaze com essa solução
→ Limpe de maneira **circular** a **primeira falange** da ponta dos dedos a serem coletados

⚠️ **IMPORTANTE — controle de umidade:**
→ Os dedos não podem ficar excessivamente molhados (imagem escurece)
→ Seque levemente com gaze seca antes de capturar

**Se houver Vernix (substância branca):**
→ Limpe DELICADAMENTE com a mesma solução
→ Aguarde 1-2 minutos antes de capturar
→ Não remova a descamação natural (normal em RN)

📹 **Vídeo — Preparação:** https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link

Ficou claro ou quer mais algum detalhe sobre essa etapa?"""

        # ── RN CHORANDO / REFLEXO / CASOS ESPECIAIS ──────────────────────────
        rn_kw = ['chorando', 'chorar', 'choro', 'bebê chorando', 'bebe chorando',
                 'grasping', 'mão fechada', 'mao fechada', 'reflexo', 'prematuro',
                 'recém-nascido', 'recem-nascido', 'rn instável', 'rn instavel',
                 'golden hour', 'primeira hora', 'vernix', 'dedos frágeis',
                 'dedos frageis', 'não abre a mão', 'nao abre a mao']
        if any(k in pergunta_lower for k in rn_kw):
            if any(k in pergunta_lower for k in ['chorando', 'chorar', 'choro']):
                return """RN chorando durante a coleta é comum — aqui está o que fazer:

**Procedimento:**
1. **Pause** a coleta imediatamente — nunca force
2. Deixe a progenitora confortar o bebê (pele a pele funciona muito bem)
3. Aguarde **30 a 60 segundos** para ele se acalmar
4. Retome com calma

**Limite:** máximo 2-3 tentativas. Se o choro persistir em desespero, avalie com o médico antes de continuar.

⚠️ Se o choro for de **agonia** ou o RN apresentar sinais de desconforto extremo → acione a equipe médica imediatamente.

**💡 Dica:** quanto mais calma for a profissional, mais calmo tende a ficar o bebê.

O RN se acalmou? Posso te ajudar com o próximo passo."""
            if any(k in pergunta_lower for k in ['grasping', 'mão fechada', 'mao fechada',
                                                   'não abre', 'nao abre']):
                return """O reflexo de grasping (mão fechada) é **completamente normal** em RNs!

**Técnica para abrir a mão:**
→ Acaricie suavemente o **dorso ou lateral** da mão do bebê
→ Isso estimula o reflexo **oposto** de abertura — é fisiológico
→ Depois, segure os 4 dedos com cuidado e posicione o polegar no scanner

**❌ Não faça:**
→ Não force a abertura dos dedos manualmente
→ Não pressione excessivamente o dedo no scanner

O design ergonômico do scanner ETAN facilita muito o posicionamento mesmo com dedos pequenos.

Conseguiu posicionar o dedo? Tem mais alguma dúvida?"""
            if 'prematuro' in pergunta_lower:
                return """Para bebês **prematuros**, o protocolo é basicamente o mesmo, com alguns cuidados extras:

**✅ Pode coletar normalmente se:**
→ A equipe médica liberou e atestou estabilidade clínica
→ A biometria se forma a partir da 13ª semana de gestação — prematuros já têm digitais formadas

**⚠️ Atenção especial:**
→ Prematuros são **mais instáveis** — monitorar sinais vitais durante toda a coleta
→ Dedos são **ainda mais delicados** — use pressão mínima
→ Vernix pode ser mais abundante — higienize com NATO soro com muito cuidado

**🛑 Pare imediatamente se:**
→ Qualquer sinal de instabilidade (oximetria caindo, palidez, cianose)

📹 **Vídeo — Captura RN:** https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link

Tem mais alguma dúvida sobre a coleta em prematuro?"""

        # ── PROGENITORA / COLETA DA MÃE ──────────────────────────────────────
        progenitora_kw = ['progenitora', 'mãe', 'mae', 'coleta da mãe', 'coleta da mae',
                          'dedos da mãe', 'dedos da mae', 'captura progenitora',
                          'polegar da mãe', 'polegar da mae']
        if any(k in pergunta_lower for k in progenitora_kw):
            return """**Etapa 3 — Captura Progenitora:**

São coletados **4 dedos** no total:
1. Polegar direito
2. Indicador direito
3. Polegar esquerdo
4. Indicador esquerdo

**Técnica:**
→ Mesma solução NATO soro para higienização
→ Limpe o scanner entre cada dedo com gaze seca
→ Falange distal centralizada no visor
→ Pressão leve e natural

⚠️ Se a mãe tiver calosidades ou pele muito seca: umedeça levemente antes de capturar.

📹 **Vídeo — Captura Progenitora:** https://drive.google.com/file/d/1g55icK4TUhLpQxwsTgPbV0e09td8K8ln/view?usp=drive_link

Ficou claro? Tem mais alguma dúvida?"""

        # ── SELEÇÃO (critérios de elegibilidade) ─────────────────────────────
        selecao_kw = ['seleção', 'selecao', 'critério', 'criterio', 'elegível',
                      'elegivel', 'pode coletar', 'quando coletar', 'liberação médica',
                      'liberacao medica', 'quem decide', 'autorização', 'autorizacao']
        if any(k in pergunta_lower for k in selecao_kw):
            return """**Etapa 1 — Seleção:**

A coleta só pode ocorrer quando **mãe e RN estão estáveis e fora de risco**, conforme atestado pela equipe médica.

**Critérios de estabilidade do RN:**
✅ Respiração regular
✅ Frequência cardíaca dentro da normalidade
✅ Boa oxigenação (SpO₂ adequada)
✅ Temperatura corporal estável
✅ Sem sinais de sofrimento

**Critérios para a progenitora:**
✅ Estabilidade clínica pós-parto
✅ Consentimento informado obtido

⚠️ Em caso de **dúvida sobre a estabilidade**, consulte SEMPRE o médico responsável antes de iniciar.

📹 **Vídeo — Seleção:** https://drive.google.com/file/d/1uOILNO0clQYeP9PFpuvkaP1h4570kaRA/view?usp=sharing

Há alguma situação específica que está gerando dúvida?"""

        # ── VERIFICAÇÃO DE QUALIDADE ──────────────────────────────────────────
        verif_kw = ['verificação', 'verificacao', 'checar qualidade', 'verificar qualidade',
                    'imagem aprovada', 'revisar coleta', 'depois da coleta',
                    'finalizar coleta', 'etapa final']
        if any(k in pergunta_lower for k in verif_kw):
            return """**Etapa 5 — Verificação:**

Após capturar os 10 dedos do RN e os 4 da progenitora, verifique no sistema:

**✅ Imagem aprovada quando:**
→ Digital com cristas e sulcos visíveis e nítidos
→ Sem manchas escuras (excesso de umidade)
→ Sem imagem muito apagada (excesso de secura)
→ Centralizada no visor

**❌ Repetir a captura se:**
→ Imagem borrada, ilegível ou cortada
→ Sobreposição de dedos
→ Sistema indicar baixa qualidade

**Procedimento para repetir:**
1. Volte ao dedo específico que ficou com qualidade ruim
2. Limpe o scanner com gaze seca
3. Reposicione e recapture

📹 **Vídeo — Verificação:** https://drive.google.com/file/d/1vKSLvP5WolPnjJa4y6ylrP9-rkvPwUqs/view?usp=drive_link

Todas as imagens ficaram aprovadas ou tem alguma específica com problema?"""

        # ── SEGURANÇA DOS DADOS ───────────────────────────────────────────────
        seguranca_kw = ['segurança', 'seguranca', 'dados seguros', 'privacidade',
                        'lgpd', 'criptografia', 'quem acessa', 'gdpr', 'proteção de dados',
                        'protecao de dados']
        if any(k in pergunta_lower for k in seguranca_kw):
            return """Os dados coletados pelo INFANT.ID são protegidos em múltiplas camadas:

**🔐 Proteção técnica:**
→ Criptografia de ponta a ponta — ninguém acessa no caminho
→ Servidores com múltiplos backups e alta disponibilidade
→ Acesso restrito a profissionais autorizados com log completo de acesso

**📋 Conformidade legal:**
→ LGPD (Lei Geral de Proteção de Dados — Brasil)
→ GDPR (padrão europeu)
→ Certificações internacionais de segurança biométrica
→ Auditorias constantes

**Na prática:** sua responsabilidade é fazer a **coleta de qualidade**. A segurança técnica dos dados fica por conta da plataforma.

Tem alguma dúvida específica sobre privacidade ou sobre quem tem acesso?"""

        # ── RESPOSTA GENÉRICA — tenta ser útil com qualquer pergunta ─────────────
        if any(k in pergunta_lower for k in ['oi', 'olá', 'ola', 'tudo bem', 'bom dia', 'boa tarde', 'boa noite', 'hey']):
            return "Oi! Tudo bem sim, obrigada! Sou a Jade, posso te ajudar com dúvidas sobre coleta biométrica ETAN, equipamento, protocolo, qualidade de imagem — é só perguntar! 😊"

        if any(k in pergunta_lower for k in ['obrigad', 'valeu', 'muito obrigad', 'grat']):
            return "De nada! Fico feliz em ajudar. Qualquer outra dúvida, pode perguntar! 😊"

        if any(k in pergunta_lower for k in ['vida', 'clima', 'comida', 'futebol', 'receita', 'viagem', 'novela']):
            return "Haha, esse eu não sei responder! 😄 Sobre coleta biométrica de recém-nascidos sou especialista. Pode perguntar sobre protocolo ETAN, equipamento, qualidade de imagem — o que precisar!"

        # Análise de tema por palavras-chave da pergunta
        temas_biometria = {
            'dedo':       "No ETAN capturamos todos os 10 dedos do RN (decadactilar) — polegar ao mínimo, mão direita primeiro, depois esquerda. Usamos a técnica tipo pinça para estabilizar o dedo sem pressão. Gaze seca no scanner antes de cada dedo.",
            'digital':    "Para a digital ficar boa: falange distal centralizada no visor, pressão levinha (o scanner faz o trabalho), gaze seca no leitor antes de cada dedo. Se ficar borrada: verifique umidade e limpe o scanner.",
            'scanner':    "O scanner ETAN precisa de gaze seca no leitor antes de cada captura. Nunca use álcool ou gaze molhada diretamente no sensor. Se der problema técnico recorrente, abra chamado em akiyama.com.br/suporte.",
            'rn':         "Para captura do RN: higienize com NATO soro (soro fisiológico + clorexidina + shampoo neutro), seque bem, use pressão levinha. O reflexo de grasping (mão fechada) se resolve acariciando o dorso da mão.",
            'mae':        "Para a progenitora coletamos 4 dedos: polegar direito, indicador direito, polegar esquerdo, indicador esquerdo. Mesma técnica: NATO soro, gaze seca no scanner, pressão leve.",
            'pele':       "Pele a pele é o melhor calmante! Se o bebê estiver agitado, pause a coleta e entregue para a mãe por 1-2 minutos. Funciona muito bem antes de retomar.",
            'etica':      "No contexto da coleta biométrica: obtenha sempre o consentimento informado da progenitora antes de iniciar. Dados são protegidos por LGPD. A equipe médica decide sobre elegibilidade clínica — não inicie sem liberação.",
            'higieniz':   "Higienização dos dedos: solução NATO soro (soro fisiológico + clorexidina líquida + shampoo neutro infantil). Aplique com gaze, movimento circular na primeira falange, seque antes de capturar. Controle a umidade!",
            'sala':       "Para a coleta, o ambiente ideal é tranquilo, com boa iluminação, temperatura confortável. O scanner precisa estar em superfície firme. Verifique conexão USB antes de começar.",
            'connect':    "Problema de conexão: verifique o cabo USB, troque de porta, feche e reabra o software. Se não resolver, reinicie o equipamento. Persiste? Abra chamado em akiyama.com.br/suporte.",
            'driver':     "Problema de driver: verifique se o antivírus está bloqueando. Reinstale o driver pelo portal akiyama.com.br. Se persistir, abra chamado técnico.",
            'consenti':   "O consentimento informado da progenitora é obrigatório antes de qualquer coleta. Explique o propósito (identificação do RN), como os dados serão usados e que ela pode recusar.",
            'identific':  "O sistema INFANT.ID vincula a biometria do recém-nascido à da progenitora, criando um par biométrico único. Isso garante identificação segura do bebê ao longo de toda a internação.",
            'dado':       "Os dados biométricos são criptografados de ponta a ponta, ficam em servidores com backup e acesso restrito a profissionais autorizados. Conformidade com LGPD e padrões internacionais.",
        }

        for palavra, resposta in temas_biometria.items():
            if palavra in pergunta_lower:
                return resposta

        # Fallback final — não sabe o tema, mas tenta ser útil
        return f"""Boa pergunta! Não tenho uma resposta específica para "{pergunta[:60]}{'...' if len(pergunta) > 60 else ''}" aqui na base de conhecimento.

Posso responder sobre:
- Protocolo ETAN (etapas, ordem, técnica)
- Equipamento (scanner, limpeza, problemas)
- Qualidade de imagem (borrada, escurecida, não captura)
- Casos especiais (prematuro, vernix, bebê agitado, reflexo de grasping)
- Suporte técnico (abrir chamado)

Tenta reformular ou me conta com mais detalhes o que está acontecendo! 😊"""

    def _construir_system_prompt(self, curso_id=None):
        """
        Constroi o prompt do sistema com contexto dinâmico por tipo de pergunta.
        Baseado na documentação oficial INFANT.ID + Treinamento de Replicadores.

        Args:
            curso_id (int): ID do curso (opcional)

        Returns:
            str: System prompt
        """
        prompt = """ATENÇÃO: Você DEVE responder SOMENTE em português brasileiro (pt-BR). NUNCA em inglês. Se você responder em inglês, está errado.

Você é a Jade, assistente virtual do sistema INFANT.ID, especializada em coleta biométrica infantil. Você apoia enfermeiras e profissionais de saúde no dia a dia hospitalar.

SEU JEITO DE SER:
- Fale como uma colega experiente e acolhedora, não como um manual técnico
- Seja direta e objetiva — o ambiente hospitalar não tem tempo a perder
- Varie o tom: seja leve quando puder, séria quando precisar (emergências)
- Não repita bullet points longos quando uma frase resolve
- Não use formatação excessiva. Use negrito só quando realmente importa
- Responda no tamanho certo para a pergunta — perguntas simples, respostas curtas

COMO RESPONDER CADA TIPO DE PERGUNTA:

Protocolo / como fazer algo:
- Vá direto ao ponto da etapa perguntada
- Passos numerados, curtos
- Inclua o link do vídeo da etapa se relevante
- Pergunte se ficou claro ou se quer mais detalhes

Problema técnico (scanner, conexão, erro):
- Diagnostique rápido e dê os passos na ordem "faça isso, depois isso"
- Confirme se resolveu antes de ir para o próximo passo
- Se não resolver: orientar abertura de chamado em akiyama.com.br/suporte

Qualidade de imagem (borrada, não captura):
- Pergunte primeiro: scanner limpo? Umidade ok? Posicionamento?
- Responda só a causa provável, não liste tudo de uma vez

Emergência (instabilidade, cianose, risco de vida):
- Responda de forma curta e urgente: pare a coleta, acione o médico agora
- Não dê longas instruções — não é hora

Primeira vez / visão geral:
- Apresente as 5 etapas com brevidade e convide para aprofundar

VÍDEOS DAS ETAPAS (inclua quando pertinente):
- Seleção: https://drive.google.com/file/d/1uOILNO0clQYeP9PFpuvkaP1h4570kaRA/view?usp=sharing
- Preparação e Captura RN: https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link
- Captura Progenitora: https://drive.google.com/file/d/1g55icK4TUhLpQxwsTgPbV0e09td8K8ln/view?usp=drive_link
- Verificação: https://drive.google.com/file/d/1vKSLvP5WolPnjJa4y6ylrP9-rkvPwUqs/view?usp=drive_link

CONHECIMENTO TÉCNICO:

Protocolo ETAN — 5 etapas: Seleção → Preparação → Captura Progenitora → Captura RN → Verificação

Ordem de coleta do RN (decadactilar):
Mão direita: polegar, indicador, médio, anelar, mínimo
Mão esquerda: polegar, indicador, médio, anelar, mínimo

Técnica:
- Falange distal centralizada no visor
- Pressão leve — o scanner faz o trabalho
- Gaze SECA no scanner antes de cada dedo
- Umidade equilibrada: nem encharcado, nem ressecado

Solução NATO soro (limpeza dos dedos): soro fisiológico + shampoo neutro infantil + clorexidina líquida

Limpeza do scanner: use apenas gaze SECA — nunca álcool ou gaze molhada no leitor

Casos especiais:
- Vernix: limpe com NATO soro delicadamente, aguarde 1-2 min antes de capturar
- Prematuro: mesmo protocolo, pressão ainda mais leve, atenção extra à estabilidade
- Reflexo de grasping: acaricie o dorso da mão para estimular abertura natural
- RN chorando: pause 30-60s, máximo 2-3 tentativas, se persistir avalie com médico

Progenitora: 4 dedos — polegares e indicadores (direito e esquerdo)

Pare imediatamente se: cianose, dificuldade respiratória, palidez, choro de agonia → acione o médico

LIMITES:
- Não dê orientações médicas fora do escopo da coleta
- Dúvidas clínicas → médico de plantão
- Problemas técnicos não resolvidos → chamado em akiyama.com.br/suporte

Encerre sempre perguntando se pode ajudar com mais alguma coisa, de forma natural e breve.

LEMBRETE FINAL: Toda a sua resposta deve estar em português brasileiro. Não use inglês em hipótese alguma."""

        return prompt
