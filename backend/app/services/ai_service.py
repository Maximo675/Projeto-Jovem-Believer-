"""
Serviço de IA para consultar e gerar respostas.
Suporta: OpenAI (remoto), Ollama (local), ou Mock (demo).
"""

import os
from openai import OpenAI
from flask import current_app

class AiService:
    """Serviço para interações com IA."""
    
    def __init__(self):
        """Inicializa o serviço com IA disponível."""
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
                    api_key="not-needed"  # Ollama não requer API key
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
        
        self.model = os.getenv('OPENAI_MODEL', 'llama2')  # llama2 para Ollama, gpt-3.5-turbo para OpenAI
    
    def responder_pergunta(self, pergunta, contexto_curso=None):
        """
        Responde uma pergunta usando IA.
        
        Args:
            pergunta (str): Pergunta do usuário
            contexto_curso (int): ID do curso (opcional, para contexto)
        
        Returns:
            tuple: (resposta, tokens_usados)
        """
        # Modo MOCK para fins de demonstração (sempre funciona)
        if self.mode == 'mock':
            return self._responder_mock(pergunta, contexto_curso), 0
        
        # Modo Ollama ou OpenAI (mesma interface)
        if not self.client:
            return "IA não configurada. Configure OPENAI_API_KEY ou instale Ollama", 0
        
        try:
            # Construir prompt com contexto
            system_prompt = self._construir_system_prompt(contexto_curso)
            
            # Chamar API (Ollama ou OpenAI)
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
            # Se Ollama falhar, fallback automaticamente para mock
            if self.mode == 'ollama':
                print(f"[FALLBACK] Ollama indisponivel. Usando mock...")
                self.mode = 'mock'
                return self._responder_mock(pergunta, contexto_curso), 0
            # Já em outro modo? Just fail
            raise Exception(f"Erro ao consultar IA: {str(e)}")
    
    def _responder_mock(self, pergunta, contexto_curso=None):
        """
        Resposta simulada para fins de demonstração.
        Útil quando IA não está disponível.
        """
        pergunta_lower = pergunta.lower()
        
        # Dicionário de respostas por tema
        respostas = {
            'biométric': 'A coleta biométrica em recém-nascidos deve ser realizada com equipamentos calibrados e protocolos rigorosos. Recomenda-se: 1) Limpeza das mãos com água/álcool gel, 2) Identificação do RN com pulseira apropriada, 3) Coleta de impressões digitais em scanner específico, 4) Registro em base de dados segura. Tempo médio: 2-3 minutos por coleta.',
            'segurança': 'A segurança de dados biométricos é crítica. Implementamos: criptografia end-to-end AES-256, autenticação de dois fatores, logs de auditoria, conformidade LGPD/GDPR, backup automático em múltiplos datacenters. Todos os dados são mantidos isolados e acessados apenas por profissionais autorizados.',
            'training': 'O treinamento de profissionais de saúde envolve: 1) Módulo teórico sobre biometria infantil (2h), 2) Demonstração prática com equipamentos (1h), 3) Simulações de coleta (1h), 4) Avaliação prática (30min). Taxa de aprovação: 95% dos profissionais treinados.',
            'protocolo': 'Nossos protocolos ETAN seguem as diretrizes da WHO e SBP (Sociedade Brasileira de Pediatria). Incluem: identificação segura, coleta não invasiva, armazenamento criptografado, e conformidade com legislação brasileira sobre dados de menores.',
        }
        
        # Buscar resposta mais relevante
        for palavra_chave, resposta in respostas.items():
            if palavra_chave in pergunta_lower:
                return resposta
        
        # Resposta genérica se nenhuma palavra-chave encontrada
        return f"Excelente pergunta sobre '{pergunta}'. A plataforma Winged Mind foi desenvolvida especificamente para otimizar processos de coleta biométrica em ambientes hospitalares, garantindo segurança, eficiência e conformidade regulatória. Como posso ajudá-lo com mais detalhes?"
    
    def _construir_system_prompt(self, curso_id=None):
        """
        Constrói o prompt do sistema com contexto apropriado.
        Especializado para enfermeiras usando o sistema ETAN de coleta biométrica infantil.
        
        Args:
            curso_id (int): ID do curso (opcional)
        
        Returns:
            str: System prompt
        """
        prompt = """Você é um assistente especializado em suporte técnico e treinamento para enfermeiras que utilizam o sistema de coleta biométrica infantil ETAN da Infant.id.

### SUA FUNÇÃO:
- Auxiliar enfermeiras em procedimentos de coleta biométrica de recém-nascidos e progenitoras
- Resolver problemas técnicos com o equipamento ETAN
- Fornecer orientações sobre melhores práticas
- Esclarecer dúvidas sobre o protocolo de coleta
- Instruir sobre abertura de chamados técnicos

### TOM E ESTILO:
- Linguagem clara, objetiva e profissional
- Empática e paciente, considerando que pode haver urgência no ambiente hospitalar
- Use termos técnicos quando apropriado, mas explique quando necessário
- Seja específica nas instruções, seguindo o protocolo à risca
- Em situações de emergência ou dúvida crítica, priorize a segurança do RN e da progenitora

### ESTRUTURA DE RESPOSTA:
1. Reconheça a questão da enfermeira
2. Forneça a solução/orientação de forma direta
3. Se aplicável, cite o passo específico do protocolo
4. Ofereça informações complementares se necessário
5. Pergunte se há mais alguma dúvida

### LIMITAÇÕES IMPORTANTES:
- Não forneça orientações médicas que estejam fora do escopo da coleta biométrica
- Em casos de instabilidade do RN ou progenitora, sempre priorize o encaminhamento à equipe médica
- Para problemas técnicos complexos não resolvidos pelas instruções básicas, oriente a abertura de chamado

### CONHECIMENTO ESPECIALIZADO - PROTOCOLO ETAN:

#### ETAPAS DO PROTOCOLO (5 fases):

**1. SELEÇÃO**
- Escolha de mãe e RN com estabilidade clínica
- Confirmação pela equipe médica
- Documentação inicial

**2. PREPARAÇÃO**
- Conforto da progenitora e RN
- Coleta de dados biográficos
- Higienização: usar solução NATO soro (soro fisiológico + shampoo neutro + clorexidina)
- Limpeza circular da primeira falange dos dedos indicadores e polegares
- ⚠️ **CONTROLE DE UMIDADE**: Dedos não podem ficar excessivamente molhados

**3. CAPTURA PROGENITORA**
- Coleta de 4 dedos (polegares e indicadores de ambas as mãos)
- Foco na falange distal
- Dedo centralizado no visor do scanner
- Sem pressão excessiva

**4. CAPTURA RN (DECADACTILAR)**
Ordem específica:
- **Mão Direita:** Polegar, Indicador, Médio, Anelar, Mínimo
- **Mão Esquerda:** Polegar, Indicador, Médio, Anelar, Mínimo

Técnicas especiais para RN:
- Acaricie suavemente o dorso da mão para combater reflexo de grasping
- Posicione corretamente falange distal
- Limpe o scanner ANTES de cada dedo
- Controle umidade (não muito seco, não muito úmido)

**5. VERIFICAÇÃO**
- Checagem de qualidade no sistema
- Todas as digitais legíveis
- Recoleta se necessário
- Documentação completa

#### SOBRE O EQUIPAMENTO ETAN:
- Dispositivo leve e ergonômico
- Conexão USB-C simples (USB-C no dispositivo, USB-A no computador)
- Não precisa de adaptadores ou fontes externas
- Design especial para coleta neonatal (válido desde 0 dias de vida)
- Requer higiene rigorosa (limpar visor frequentemente)

#### TROUBLESHOOTING EQUIPAMENTO:

**Sintoma: "Equipamento Desconectado"**
1. Verifique antivírus (pode estar bloqueando)
2. Troque a porta USB onde está conectado
3. Desconecte USB-C do dispositivo e reconecte
4. Reinicie o computador
→ Se persistir, abra chamado: akiyama.com.br/suporte

**Sintoma: "Não Reconhecido"**
→ Verifique cabo USB-C e porta USB
→ Tente trocar porta USB
→ Verifique antivírus corporativo
→ Reinicie sistema

**Sintoma: "Descalibrado"**
→ Limpe o visor com gaze úmida
→ Reconecte o dispositivo
→ Se não resolver, abra chamado

#### QUALIDADE DA CAPTURA - DIAGNÓSTICO:

**Digital vem borrada?**
- [ ] Scanner está limpo? (Limpe com gaze umedecida ANTES de cada dedo)
- [ ] Dedos muito úmidos? (Seque bem após limpeza)
- [ ] Dedos muito secos? (Hidrate com solução NATO soro)
- [ ] Vernix residual? (Use solução de limpeza)
- [ ] Posicionamento correto? (Falange distal, centralizado)

**Digital não captura?**
- Verifique se dedos estão próximos demais um do outro
- Posicione melhor no visor
- Tente outra mão/dedo
- Verifique se equipamento recebe comando

#### CASOS ESPECIAIS:

**RN com mãos mais escuras (melanina)?**
- O ETAN funciona com eficiência boa
- Pode exigir ajuste leve de posicionamento
- Solução de limpeza é ainda mais importante
- Limpe scanner com atenção extra

**Progenitora com vernix nas mãos?**
- Não é contraindicação
- Limpe bem com solução NATO soro
- Seque completamente antes da coleta
- Recoleta se primeira tentativa falhar

**Dedos muito pequeninos (RN prematuro)?**
- Use pontas dos dedos com delicadeza extra
- Centralize bem no visor
- Pode exigir múltiplas tentativas
- Priorize segurança sobre velocidade

#### PROTOCOLO DE EMERGÊNCIA:
⚠️ SE RN ou progenitora apresentar sinais de instabilidade:
1. INTERROMPA a coleta IMEDIATAMENTE
2. ACIONE a equipe médica
3. A coleta pode ser realizada posteriormente quando ambos estiverem ESTÁVEIS

A segurança clínica sempre vem ANTES da compliance com protocolo.

#### ABERTURA DE CHAMADOS:
Se problema técnico não for resolvido pelos passos básicos:
1. Acesse: akiyama.com.br/suporte
2. Faça login
3. Clique em "Enviar um ticket"
4. Descreva o problema detalhadamente
5. Informe o que já foi tentado
6. Inclua série do equipamento se aplicável
7. Envie

**Tempo de resposta:** SLA conforme estabelecido

#### LINKS DOS VÍDEOS EDUCATIVOS:
- **Seleção:** https://drive.google.com/file/d/1uOILNO0clQYeP9PFpuvkaP1h4570kaRA/view?usp=sharing
- **Preparação:** https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link
- **Captura Progenitora:** https://drive.google.com/file/d/1g55icK4TUhLpQxwsTgPbV0e09td8K8ln/view?usp=drive_link
- **Captura RN:** https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link
- **Verificação:** https://drive.google.com/file/d/1vKSLvP5WolPnjJa4y6ylrP9-rkvPwUqs/view?usp=drive_link

### RESPOSTA ALWAYS EM PORTUGUÊS DO BRASIL
### SEMPRE PRIORIZE SEGURANÇA CLÍNICA DO PACIENTE
### SEJA EMPÁTICA COM AS DESAFIOS DO AMBIENTE HOSPITALAR"""
        
        if curso_id:
            prompt += f"\n\nO usuário está no contexto do curso ID {curso_id}. Personalize as respostas para esse contexto quando possível."
        
        return prompt
    
    def gerar_recomendacoes(self, usuario_id, progresso_cursos):
        """
        Gera recomendações de cursos baseado no progresso.
        
        Args:
            usuario_id (int): ID do usuário
            progresso_cursos (list): Lista de progresso em cursos
        
        Returns:
            str: Recomendações personalizadas
        """
        try:
            if not self.client:
                return "IA não configurada."
            
            prompt = f"""Com base no progresso do usuário nos cursos:
            {progresso_cursos}
            
            Gere 2-3 recomendações personalizadas de próximos passos de aprendizado."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um recomendador de cursos especializado em onboarding."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Erro ao gerar recomendações: {str(e)}")
    
    def analisar_sentimento(self, texto):
        """
        Analisa o sentimento de um texto (feedback, etc).
        
        Args:
            texto (str): Texto para análise
        
        Returns:
            str: Análise de sentimento (positivo, neutro, negativo)
        """
        try:
            if not self.client:
                return "neutro"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Analise o sentimento do texto e responda apenas com: positivo, neutro ou negativo."},
                    {"role": "user", "content": texto}
                ],
                temperature=0,
                max_tokens=10
            )
            
            content = response.choices[0].message.content
            resultado = content.strip().lower() if content else "neutro"
            
            return resultado
            
        except Exception as e:
            raise Exception(f"Erro ao analisar sentimento: {str(e)}")
