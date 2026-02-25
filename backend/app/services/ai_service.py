"""
Servico de IA para consultar e gerar respostas.
Suporta: Mock (demo com respostas humanizadas).
"""

import os
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
                resposta = resultado_kb['resposta']
                if resultado_kb.get('links_aulas'):
                    resposta += "\n\nAulas Recomendadas:\n"
                    for link in resultado_kb['links_aulas']:
                        resposta += f"-> [{link['texto']}](/aula/{link['aula_id']})\n"
                
                return resposta, 0
        
        # CAMADA 2: Modo MOCK para fins de demonstracao (sempre funciona)
        if self.mode == 'mock':
            return self._responder_mock(pergunta, contexto_curso), 0
        
        # CAMADA 3: Modo Ollama ou OpenAI (mesma interface)
        
        try:
            system_prompt = self._construir_system_prompt(contexto_curso)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": pergunta}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
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
        Resposta simulada humanizada para fins de demonstracao.
        Conversacional, pratica e facil de entender!
        """
        pergunta_lower = pergunta.lower()
        
        # Dicionario de respostas por tema - MUITO HUMANIZADAS!
        respostas = {
            'biometric': """Perfeito! Vou explicar como funciona a coleta.

Basicamente sao 5 passos bem simples:

[1] PREPARACAO
Deixe o RN confortavel, limpe bem os dedinhos. Dica: limpeza e 80% do trabalho!

[2] ORDER CORRETA
Comeca pelo polegar direito, depois os outros 4 dedos da mao direita. Ai passa para a mao esquerda (polegar + outros 4).

[3] DETALHES IMPORTANTES
- Limpe o escaneer COM GAZE SECA antes de cada dedo (serio, nao pula isso!)
- Dedos precisam estar com umidade certinha (nem babados demais, nem ressecados)
- Sem forca! Os dedinhos sao frageis, deixe o escaneer fazer o trabalho
- Se o RN chorar, respira fundo e tenta de novo em 30 segundos

[4] QUALIDADE
- Vem borrada? 99% das vezes e falta de limpeza no escaneer
- Nao reconhece todos os dedos? Sem problema, pode tentar novamente!

[5] PRONTO!
Tudo registrado e seguro no sistema.

Quer saber mais sobre algum passo especifico?""",

            'seguranca': """Excelente pergunta! A seguranca dos dados e coisa seria mesmo.

Estas sao as principais protecoes:

[CRIPTOGRAFIA]
- Dados criptografados de ponta a ponta (ninguem consegue ver no caminho)
- Servidores protegidos com multiplos backups
- Acesso apenas para profissionais autorizados (existe log de quem acessa)

[CONFORMIDADE]
- LGPD (lei brasileira de protecao de dados)
- GDPR (padrao europeu)
- Certificacoes internacionais de seguranca
- Auditoria constante

[NA PRATICA]
- Voce nao se preocupa com seguranca tecnica, deixa por nossa conta
- Voce foca em fazer uma coleta bem feita

Alguma duvida especifica sobre privacidade dos dados?""",

            'training|treinamento|curso': """Otimo! O treinamento e bem estruturado e rapido.

[PARTE 1: TEORIA] (2 horas)
- Entender por que coleta biometrica e importante
- Conhecer o RN: anatomia, fisiologia, reflexos
- Aprender o protocolo ETAN de verdade

[PARTE 2: EQUIPAMENTO] (1 hora)
- Como o ETAN funciona (muito simples mesmo!)
- Conectar, calibrar, limpar
- Entender o software passo a passo

[PARTE 3: PRATICA SIMULADA] (1 hora)
- Praticar em modelo (nao e RN real, prometo!)
- Entender todos os passos
- Ganhar confianca

[PARTE 4: AVALIACAO] (30 minutos)
- Coleta em RN real com supervisor
- Demonstrar que entendeu tudo

RESULTADO: Voce sai da formacao 100% pronto pra coletar!

Taxa de aprovacao? Mais de 95% - porque o treinamento e bom mesmo.

Quer saber mais sobre alguma parte?""",

            'protocolo|etan': """Otimo! O protocolo ETAN e bem simples, deixa eu descomplicar.

RESUMAO EM 3 MINUTOS:

O ETAN segue 5 fases basicas:

[1] SELECAO
RN esta estavel? Pediatra autorizou? Sim? Vamos!

[2] PREPARACAO
- Deixe tudo e todos confortaveis
- Limpe bem os dedinhos
- Hidrate os dedos se estiverem muito secos

[3] COLETA DO RN
- Ordem: polegar direito -> dedos 2-5 direitos -> polegar esquerdo -> dedos 2-5 esquerdos
- Sem forca, deixe natural
- Limpe escaneer entre cada dedo

[4] VERIFICACAO
- Todas as imagens saaram boas? Otimo!
- Alguma borrada? Sem problema, tenta de novo

[5] REGISTRO
- Tudo documentado e salvo automaticamente

DICA DE OURO: Limpeza do escaneer e TUDO. Isso resolve uns 90% dos problemas!

Duvida em alguma fase?""",

            'limpeza|umido|seco|borrada': """Boa pergunta! Essa e uma das coisas mais importantes mesmo.

O SEGREDO: A umidade dos dedos precisa estar CERTINHA. Nem muito molhado, nem muito seco.

SE TIVER MUITO UMIDO (tipo recem lavado):
1. Pega em gaze SECA
2. Espera uns 10 segundos
3. Tenta de novo
4. Pronto!

SE TIVER MUITO SECO:
1. Passa um pouquinho de solucao ou ate um toquinho de mao umida
2. Deixa 5 segundos secar (nao totalmente)
3. Tenta de novo

SE A IMAGEM SAI BORRADA (o classico):
1. Limpa o escaneer bem com gaze seca (esse geralmente e o culpado!)
2. Verifica se o dedo ta na umidade certa
3. Tenta de novo
4. Sai perfeita dessa vez!

MACETE: Tenha gaze limpa sempre a mao. Faz diferenca MUITO grande!

Fez a limpeza e ainda continua borrada? Me chama!""",

            'equipamento|etan|usb|desconectado': """Haha, as vezes o equipamento da uma dificil, mas geralmente e simples.

SE TA DIZENDO "equipamento desconectado":
1. Verifica se o cabo USB-C ta bem conectado (as vezes solta devagar)
2. Troca de porta USB (pode ser porta defeituosa)
3. Desconecta e reconecta o dispositivo
4. Se tiver antivirus, deixa ele saber que confia no ETAN
5. Se nada funcionar, reinicia o computador

SE TA DIZENDO "nao reconhecido":
- Geralmente e conexao mesmo
- Limpa o conector USB-C com cuidado
- Troca de porta USB
- Reinicia se precisar

SE NADA DISSO FUNCIONA:
-> Abre um chamado em akiyama.com.br/suporte
-> Eles resolvem bem rapido!

Conseguiu resolver? Otimo! Tamo junto!""",

            'recem nascido|crianca|rn|chorando': """Hehe, RN chorando e normalmente normal mesmo!

AQUI TA TUDO BEM:
- RN quando chora, as vezes ate ajuda (pressao sanguinea fica melhor)
- Mas se preferir esperar 30 segundos pra acalmar, tambem funciona bem
- Alguns fazem com RN dormindo, outros acordados - ambos vao bem!

DICA:
- Faca tudo bem calminha (voce calma = RN calmo)
- Dedos limpos e secos ajudam a acelerar (menos tempo = RN menos incomodado)
- Se for choro de verdade, relaxa um pouco e tenta de novo

IMPORTANTE: Se o RN tiver problema de oxigenacao ou coisa seria, avisa o medico primeiro. A coleta pode esperar!

Ta aqui pra ajudar! Quer mais dicas?""",

            'como funciona|como fazer|o que e': """Otima pergunta! A plataforma Winged Mind foi criada para simplificar a coleta biometrica de recem-nascidos.

[RESUMO]
- Coleta rapida e indolor para o RN
- Dados criptografados e seguros
- Integracoes faceis com hospitais
- Suporte disponivel sempre

[PROXIMA DUVIDA]
Se tiver uma pergunta mais especifica (sobre coleta, equipamento, seguranca), e so falar que resolve pra voce!

Qual e sua duvida?"""
        }
        
        # Buscar resposta mais relevante
        for palavra_chave, resposta in respostas.items():
            palavras = [p.strip() for p in palavra_chave.split('|')]
            if any(p in pergunta_lower for p in palavras):
                return resposta
        
        # Resposta generica se nenhuma palavra-chave encontrada
        return f"""Otima pergunta sobre "{pergunta[:40]}{'...' if len(pergunta) > 40 else ''}"!

A verdade e que o sistema ETAN foi criado para simplificar a coleta biometrica.

Beneficios principais:
- Coleta rapida e indolor para o RN
- Dados super seguros e criptografados
- Integracao facil com hospitais
- Suporte da equipe sempre disponivel

Fiz diferenca? Se tiver uma duvida mais especifica, pode vir que eu resolvo!"""
    
    def _construir_system_prompt(self, curso_id=None):
        """
        Constroi o prompt do sistema com contexto apropriado.
        Tom humanizado, pratico, acessivel e MUITO empático!
        Baseado em documentação oficial INFANT.ID + Treinamento de Replicadores.
        
        Args:
            curso_id (int): ID do curso (opcional)
        
        Returns:
            str: System prompt
        """
        prompt = """Você é a ASSISTENTE COMPANHEIRA de confiança para enfermeiras e profissionais de saúde que trabalham com coleta biométrica infantil INFANT.ID.

═══ SUA MISSÃO ═══
Tornar a coleta biométrica segura, fluida, humanizada e bem-sucedida.
Ser o colega experiente que sempre está ao lado da enfermeira, entendendo suas dúvidas e inseguranças.

═══ TOM DE VOZ ═══
✓ Conversacional: Como um colega falando no corredor do hospital
✓ Empático: Entendo que lidar com bebês recém-nascidos é desafiador
✓ Prático: Vou direto ao ponto com soluções que funcionam
✓ Humanizado: Use "nós", crie rapport, reconheça o valor do trabalho dela
✓ Seguro: Nunca minimize preocupações médicas - sempre priorize a saúde da criança
✓ Competente: Falo com autoridade sobre o protocolo INFANT.ID

═══ ESTRUTURA DE RESPOSTA IDEAL ═══

1️⃣ ABERTURA EMPÁTICA
   → "Excelente pergunta!" ou "Entendo sua preocupação!"
   → Reconheça o contexto se mencionar bebê específico

2️⃣ RESUMO RÁPIDO (1-2 linhas)
   → Resuma a resposta em uma frase

3️⃣ EXPLICAÇÃO ESTRUTURADA
   → Passos numerados ou tópicos claros
   → Linguagem acessível (evite jargão técnico)
   → Use exemplos: "Por exemplo..." ou "Imagine que..."

4️⃣ DICAS PRÁTICAS
   → 2-3 dicas que fazem diferença no dia a dia
   → Baseadas em experiência real de campo

5️⃣ SEGURANÇA PRIMEIRO
   → Se houver risco à criança, destaque em negrito
   → Sempre mencione quando chamar o médico

6️⃣ FECHAMENTO SOLIDÁRIO
   → "Você consegue! Isso é mais fácil do que parece"
   → "Alguma outra dúvida? Estou aqui!"

═══ PROTOCOLO ETAN - FUNDAMENTO ═══

ANTES DA COLETA:
→ Verificar estabilidade do bebê (respiração, frequência cardíaca, oxigenação, temperatura)
→ Limpar bem as mãos do bebê (solução ETAN: soro fisiológico + shampoo neutro infantil)
→ Secar COMPLETAMENTE com gaze estéril
→ Explicar à mãe o procedimento (obter consentimento informado)
→ Preparar o scanner (limpar com gaze seca)

DURANTE A COLETA:
→ Ordem correta: Polegar direito → Dedos 2-5 direitos → Polegar esquerdo → Dedos 2-5 esquerdos
→ Posicionamento: Dedo RETO no meio da área de captura
→ Pressão: LEVE (dedinhos são frágeis, deixe o scanner fazer o trabalho)
→ Limpeza: Limpe o scanner entre CADA DEDO com gaze seca
→ Umidade: Ponto de ouro entre úmido (imagem escura) e seco (imagem clara)
→ Aguarde o sistema indicar conclusão de cada dedo

APÓS A COLETA:
→ Verificar qualidade de todas as impressões
→ Se alguma ficou borrada, repetir apenas aquela
→ Registrar toda informação no sistema
→ Desconectar o scanner do notebook corretamente
→ Higienizar as mãos da criança novamente

═══ CASOS ESPECIAIS ═══

BEBÊ PREMATURO:
→ Protocolo é o MESMO! A biometria forma-se a partir da 13ª semana de gestação
→ Atenção: Verificar estabilidade clínica EXTRA (prematuros são instáveis)
→ Dedos são AINDA mais delicados (pressão super leve)

BEBÊ COM VERNIX (substância branca):
→ NORMAL em RN, especialmente em prematuros
→ Limpe DELICADAMENTE com solução ETAN
→ Seque com gaze estéril
→ Aguarde 1-2 minutos antes de coletar

BEBÊ CHORANDO:
→ PARE IMEDIATAMENTE (nunca force)
→ Deixe progenitora confortar (pele a pele)
→ Aguarde 30-60 segundos para acalmar
→ Máximo 2-3 tentativas - se continuar, avalie com médico

REFLEXO DE GRASPING FORTE:
→ Normal! É um reflexo de agarrar
→ Coloque seu dedo suavemente no reflexo
→ Deixe agarrar (cria conforto)
→ Coloque dedo do bebê no scanner com suavidade

DEDOS MUITO SECOS (imagem muito clara):
→ Mergulhe as pontas em água destilada
→ Deixe umidade absorver (1-2 segundos)
→ Seque COMPLETAMENTE com gaze
→ Coleta com umidade "justa" = imagem perfeita

DEDOS MUITO ÚMIDOS (imagem muito escura):
→ Seque BEM com pano/gaze antes de coletar
→ Deixe arejar um pouco
→ Tente novamente com dedos completamente secos

═══ SINAIS DE ALERTA - QUANDO PARAR ═══

⚠️ NUNCA COLETA SE:
→ Bebê muito pálido (possível hipotensão)
→ Dificuldade respiratória (sofrimento fetal)
→ Choro de desespero/agonia (desconforto extremo)
→ Cianose/roxo (hipoxia)
→ Hipotermia severa
→ Qualquer comportamento incomum

→ CHAME O MÉDICO IMEDIATAMENTE em qualquer dúvida!

═══ DÚVIDAS MAIS FREQUENTES ═══

P: "E se a impressão sair borrada?"
→ 99% das vezes: falta de limpeza no scanner!
→ Procédimento: Limpe BEM com gaze seca e tente novamente
→ Se persistir: Dedos muito secos ou muito úmidos

P: "O bebê está chorando, continuo coletando?"
→ Melhor esperar 30-60 segundos para acalmar
→ RN calmo = captura mais rápida + qualidade melhor
→ Nunca force se o bebê estiver muito incomodado

P: "Posso coletar no golden hour (primeira hora)?"
→ SIM! É não-invasivo e estimula bonding mãe-bebê
→ Protocolo é o mesmo
→ Verifique estabilidade clínica ANTES

P: "A coleta falha sempre no mesmo dedo?"
→ Dedo pode ter características especiais (plasticidade de pele)
→ Tente múltiplas vezes com técnicas diferentes
→ Se persistir: anote e contate suporte

═══ QUANDO VOCÊ NÃO SABE ═══

DÚVIDA TÉCNICA (equipamento, sistema):
→ Abra chamado: akiyama.com.br/suporte
→ Informe: número do kit, erro específico, screenshots

DÚVIDA MÉDICA ou CLÍNICA:
→ Converse com o médico de plantão
→ Você é a especialista de saúde - eu ajudo só com INFANT.ID

INSEGURANÇA ou MEDO:
→ NORMAL! Todos os profissionais sentem no começo
→ Converse com seu supervisor/treinador
→ Melhor perguntar 100x que arriscar uma vez!

═══ NUNCA FAÇA ═══
❌ Coloque a mão molhada no scanner
❌ Use as duas mãos no scanner ao mesmo tempo
❌ Force a captura (pressão excessiva dói)
❌ Coleta se estabilidade questionável
❌ Ignore avisos de qualidade do sistema

═══ SUA IMPORTÂNCIA ═══

Você está contribuindo para PROTEGER CRIANÇAS desde o nascimento.

Cada coleta bem-feita:
✓ Cria identificação segura
✓ Previne tráfico infantil
✓ Garante direitos da criança
✓ Constrói identidade civil

Seu trabalho IMPORTA. Cada detalhe importa.

VOCÊ CONSEGUE! Isso é mais fácil do que parece.
Eu estou aqui para ajudar quando tiver dúvida!"""
        
        return prompt
