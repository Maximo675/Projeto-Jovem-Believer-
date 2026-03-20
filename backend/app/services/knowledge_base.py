"""
Knowledge Base INFANT.ID — Protocolo ETAN de Coleta Biométrica
Conteúdo específico para enfermeiras e profissionais de saúde.
"""

from typing import Optional

# Base de Conhecimento — Protocolo ETAN (Enfermagem)
KNOWLEDGE_BASE = {

    "tipo_captura": {
        "categoria": "Tecnica",
        "sinonimos": ["tipo de captura", "tipo pinça", "tipo pinca", "10 dedos",
                      "dez dedos", "decadactilar", "melhor tipo", "qual tipo",
                      "pinça ou", "pinca ou", "qual é melhor", "qual e melhor",
                      "tipo de coleta", "modalidade de captura", "forma de capturar",
                      "modo de captura", "tecnica de captura"],
        "resposta": """O protocolo ETAN usa exclusivamente a **captura decadactilar** (10 dedos) para o recém-nascido — não existe opção de escolha.

Para o RN, coletamos todos os 10 dedos porque isso garante o máximo de chances de match futuro — se um ou dois dedos ficarem com qualidade ruim, os outros 8 cobrem. É uma decisão de segurança do sistema.

Já a captura **"tipo pinça"** se refere à técnica de segurar o dedo do bebê: você usa o polegar e o indicador para estabilizar o dedo sem pressão, deixando a falange distal livre para o scanner. É a técnica correta justamente para garantir pressão leve e posicionamento certo.

Enton, não é uma coisa ou outra — são complementares: você usa a técnica tipo pinça para posicionar cada um dos 10 dedos no scanner.""",
        "links": []
    },

    "calmar_bebe": {
        "categoria": "Tecnica",
        "sinonimos": ["acalmar", "calmar", "calmo", "tranquilizar", "tranquila",
                      "bebê agitado", "bebe agitado", "facilitar coleta",
                      "facilitar a coleta", "facilitar a coleta do bebe",
                      "bebe chorando", "bebê chorando", "bebê não colabora",
                      "bebe nao colabora", "como acalmar", "bebe inquieto",
                      "bebê inquieto", "agitado", "agitada",
                      "como facilitar", "nao para quieto", "não para quieto",
                      "bebe nao coopera", "bebe resistindo", "bebe resistente",
                      "tornar mais facil", "deixar mais facil", "ajudar na coleta",
                      "bebe nao deixa", "bebê não deixa", "bebe muito agitado",
                      "acalmar o bebe", "calmar o bebe", "sossegar"],
        "resposta": """Isso é bem comum! Aqui está o que funciona na prática:

**Pele a pele** é o melhor calmante que existe. Pause a coleta e entregue o bebê para a mãe por 1-2 minutinhos. Funciona muito bem.

**Reflexo de grasping** (mão fechada): acaricie o *dorso* da mão do bebê — isso ativa o reflexo oposto e ele abre a mão naturalmente. Nunca force.

**Depois que acalmar:** segure os 4 dedos com cuidado, deixe o polegar livre, pressão bem levinha.

**Limite:** 2-3 tentativas por sessão. Se o choro não passar, avalie com o médico antes de continuar.

💡 Uma dica que ajuda muito: quanto mais calma você estiver, mais calmo tende a ficar o bebê.

⚠️ Se o choro for de agonia ou o RN mostrar sinais de sofrimento → acione a equipe médica imediatamente.""",
        "links": []
    },

    "grasping": {
        "categoria": "Tecnica",
        "sinonimos": ["mão fechada", "mao fechada", "grasping", "nao abre a mao",
                      "não abre a mão", "nao abre o dedo", "não abre o dedo",
                      "dedo fechado", "punho fechado", "nao abre a mao",
                      "bebe nao abre", "bebê não abre"],
        "resposta": """Isso é o reflexo de grasping — completamente normal em recém-nascidos, não é resistência, é fisiológico mesmo.

O truque é simples: acaricie suavemente o **dorso ou a lateral** da mão do bebê. Isso ativa o reflexo oposto e ele abre a mão. Depois segure os 4 dedos com cuidado e posicione o polegar no scanner.

O que não fazer: nunca force a abertura dos dedos. Não pressione com força no scanner. O scanner ETAN tem bom design justamente para facilitar mesmo com dedinhos pequenos.

Conseguiu? Se ainda estiver com dificuldade é só me falar.""",
        "links": []
    },

    "protocolo": {
        "categoria": "Protocolo",
        "sinonimos": ["etapas", "passo a passo", "como funciona", "protocolo etan",
                      "como coletar", "como fazer a coleta", "procedimento",
                      "coleta biométrica", "coleta biometrica", "processo",
                      "fases da coleta", "visão geral", "visao geral",
                      "me explica tudo", "por onde começo", "como começa",
                      "resumo do protocolo"],
        "resposta": """O protocolo ETAN tem 5 etapas:

**Seleção** — confirmar com a equipe médica que mãe e RN estão estáveis antes de começar.
📹 https://drive.google.com/file/d/1uOILNO0clQYeP9PFpuvkaP1h4570kaRA/view?usp=sharing

**Preparação** — conforto da mãe, dados biográficos, higienizar os dedos com NATO soro. Atenção à umidade: nem encharcado nem ressecado.
📹 https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link

**Captura da Progenitora** — 4 dedos: polegares + indicadores de cada mão.
📹 https://drive.google.com/file/d/1g55icK4TUhLpQxwsTgPbV0e09td8K8ln/view?usp=drive_link

**Captura do RN** — 10 dedos (decadactilar), pressão levinha, gaze seca entre cada dedo.
📹 https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link

**Verificação** — checar a qualidade de todas as imagens e repetir as borradas.
📹 https://drive.google.com/file/d/1vKSLvP5WolPnjJa4y6ylrP9-rkvPwUqs/view?usp=drive_link

🔑 Regra de ouro: gaze seca no scanner antes de cada dedo — resolve 90% dos problemas. Quer detalhe de alguma etapa específica?""",
        "links": []
    },

    "limpeza_scanner": {
        "categoria": "Equipamento",
        "sinonimos": ["limpar scanner", "limpar o scanner", "limpar etan", "limpar o etan",
                      "limpeza do scanner", "limpeza do equipamento", "limpar leitor",
                      "limpar equipamento", "como limpar", "higienizar scanner",
                      "limpar o equipamento", "limpar o leitor", "limpar meu etan"],
        "resposta": """Use sempre **gaze seca** no leitor — nunca álcool e nem gaze molhada diretamente no scanner.

Limpe antes da primeira coleta do dia, entre cada dedo, e sempre que a imagem aparecer borrada ou escurecida. O processo é simples: passe a gaze seca suavemente na superfície do leitor e aguarde 2 segundos antes de posicionar o próximo dedo.

⚠️ Nunca use álcool direto, gaze molhada, pano de prato ou papel toalha — isso danifica o sensor.

💡 Essa limpeza com gaze seca resolve cerca de 90% dos problemas de qualidade. Vale a pena fazer antes de cada dedo mesmo que não perceba sujeira.""",
        "links": []
    },

    "nato_soro": {
        "categoria": "Preparacao",
        "sinonimos": ["nato soro", "soro fisiológico", "soro fisiologico", "solucao de limpeza",
                      "solução de limpeza", "limpar dedos", "limpar os dedos",
                      "higienizar dedos", "higienização dos dedos", "vernix",
                      "preparacao", "preparação", "higienizacao", "higienização",
                      "clorexidina", "shampoo neutro", "como higienizar"],
        "resposta": """A solução NATO soro é para limpar os **dedos** (não o scanner). Misture: soro fisiológico + clorexidina líquida + shampoo neutro infantil. Umedeça uma gaze e limpe em movimento circular na primeira falange (pontinho dos dedos).

⚠️ Atenção à umidade: dedo encharcado faz a imagem escurecer. Depois de higienizar, seque levemente com gaze seca antes de capturar.

Se tiver vernix (aquela substância branca): limpe com cuidado, aguarde 1-2 minutos e aí captura. Não tente remover a descamação natural, é normal em RN.

📹 https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link""",
        "links": []
    },

    "qualidade_imagem": {
        "categoria": "Qualidade",
        "sinonimos": ["imagem borrada", "imagem ruim", "digital borrada", "não captura",
                      "nao captura", "qualidade baixa", "imagem escura", "imagem apagada",
                      "não reconhece", "nao reconhece", "erro de captura", "falha na captura",
                      "repetir captura", "refazer", "qualidade da imagem",
                      "saiu ruim", "ficou ruim", "nao ficou boa", "ficou borrada",
                      "imagem preta", "imagem branca", "nao capturou"],
        "resposta": """Vamos diagnosticar:

**Imagem escurecida ou manchas escuras** → dedo muito úmido. Seque bem com gaze seca antes de capturar.

**Imagem apagada ou muito clara** → dedo muito seco. Umedeça levemente com NATO soro e seque antes.

**Imagem borrada** → provavelmente o scanner está sujo. Passe gaze seca no leitor. Também verifique o posicionamento: a falange distal precisa estar centralizada no visor.

**Sistema não reconhece** → vernix? Higienize com NATO soro e aguarde 1-2 minutos. Pressão demais também atrapalha — o toque precisa ser bem levinho.

Para repetir: volte ao dedo com problema, limpe o scanner com gaze seca, reposicione e recaptura. Limpeza + umidade certa resolvem 95% dos casos.""",
        "links": []
    },

    "seguranca_dados": {
        "categoria": "Seguranca",
        "sinonimos": ["segurança", "seguranca", "lgpd", "privacidade", "dados seguros",
                      "quem acessa", "proteção de dados", "protecao de dados", "gdpr"],
        "resposta": """
Os dados coletados são protegidos em múltiplas camadas:

→ Criptografia de ponta a ponta
→ Servidores com múltiplos backups
→ Acesso restrito com log completo de auditoria
→ Conformidade com LGPD e padrões internacionais

Sua responsabilidade é fazer a **coleta com qualidade**. A segurança técnica dos dados fica por conta da plataforma.
        """,
        "links": []
    },

    "prematuro": {
        "categoria": "Casos Especiais",
        "sinonimos": ["prematuro", "bebe prematuro", "bebê prematuro", "criança prematura",
                      "nasceu antes", "nascimento prematuro", "bebe pequeno", "bebê pequeno",
                      "nasceu cedo", "prematuro coleta", "coleta prematuro"],
        "resposta": """Para prematuros o protocolo é o mesmo, só com cuidados extras.

Pode coletar normalmente se a equipe médica liberou — a biometria já se forma a partir da 13ª semana, então prematuros têm digitais formadas sim.

Os cuidados adicionais: prematuros são mais instáveis, então monitore sinais vitais durante toda a coleta. Dedos são ainda mais delicadinhos — pressão mínima, quase zero. Vernix tende a ser mais abundante — higienize com NATO soro com muito cuidado. Se possível, espere o bebê estar em sono leve, fica bem mais fácil.

🛑 Pare imediatamente se: oximetria caindo, palidez, cianose. Acione a equipe médica sem demora.

📹 https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link""",
        "links": []
    },

    "selecao": {
        "categoria": "Protocolo",
        "sinonimos": ["seleção", "selecao", "critério", "criterio", "elegível", "elegivel",
                      "pode coletar", "quando coletar", "liberação médica", "liberacao medica",
                      "quem decide", "autorização", "autorizacao", "estabilidade",
                      "quando posso coletar", "quando iniciar", "criterios", "critérios"],
        "resposta": """A coleta só começa quando **mãe e RN estão estáveis e fora de risco**, confirmado pela equipe médica.

Para o RN: respiração regular, frequência cardíaca normal, boa oxigenação, temperatura estável, sem sinais de sofrimento.

Para a progenitora: estabilidade clínica pós-parto e consentimento informado obtido.

⚠️ Qualquer dúvida sobre a estabilidade: consulte o médico responsável antes de iniciar. Não vá em frente se não tiver certeza.

📹 https://drive.google.com/file/d/1uOILNO0clQYeP9PFpuvkaP1h4570kaRA/view?usp=sharing""",
        "links": []
    },

    "chamado": {
        "categoria": "Suporte",
        "sinonimos": ["chamado", "suporte", "ticket", "akiyama", "abrir chamado",
                      "acionar suporte", "contato técnico", "contato tecnico",
                      "problema técnico", "problema tecnico", "scanner não funciona",
                      "scanner nao funciona", "equipamento com problema",
                      "nao consegui resolver", "não consegui resolver", "ligar suporte"],
        "resposta": """Para abrir um chamado técnico:

1. Acesse **akiyama.com.br/suporte**
2. Faça login
3. Clique em "Enviar um ticket"
4. Descreva: o problema, o que já tentou e o número de série do kit ETAN
5. Envie — o suporte retorna conforme o SLA

💡 Enquanto aguarda, use outro equipamento disponível na unidade se tiver.""",
        "links": []
    },

    "captura_rn": {
        "categoria": "Protocolo",
        "sinonimos": ["captura rn", "captura do rn", "coletar do bebe", "coletar do bebê",
                      "digitais do bebe", "digitais do bebê", "10 dedos", "decadactilar",
                      "ordem dos dedos", "qual dedo primeiro", "sequência", "sequencia",
                      "começa por qual dedo", "dedo comecar", "por qual dedo"],
        "resposta": """São 10 dedos no total — aqui vai a ordem:

**Mão direita:** Polegar → Indicador → Médio → Anelar → Mínimo
**Mão esquerda:** Polegar → Indicador → Médio → Anelar → Mínimo

Técnica: foque na **falange distal** (ponta do dedo), centralize no visor, pressão bem levinha — o scanner faz o trabalho. Limpe o scanner com gaze seca entre cada dedo e aguarde a confirmação do sistema antes de passar para o próximo.

📹 https://drive.google.com/file/d/1ZFtokHAzHLuXql2h45Ll3pEemFZqhkos/view?usp=drive_link""",
        "links": []
    },

    "captura_progenitora": {
        "categoria": "Protocolo",
        "sinonimos": ["progenitora", "captura da mãe", "captura da mae", "coleta da mãe",
                      "coleta da mae", "dedos da mãe", "dedos da mae", "4 dedos",
                      "polegares", "indicadores", "mae", "mãe",
                      "coleta da progenitora", "digitais da mae", "digitais da mãe"],
        "resposta": """São 4 dedos da progenitora: polegar direito, indicador direito, polegar esquerdo, indicador esquerdo.

Mesma técnica do RN: NATO soro nos dedos, gaze seca no scanner entre cada dedo, falange distal centralizada, pressão leve.

⚠️ Se a mãe tiver calosidades ou pele muito seca, umedeça levemente antes de capturar.

📹 https://drive.google.com/file/d/1g55icK4TUhLpQxwsTgPbV0e09td8K8ln/view?usp=drive_link""",
        "links": []
    },

    "verificacao": {
        "categoria": "Protocolo",
        "sinonimos": ["verificação", "verificacao", "checar qualidade", "verificar qualidade",
                      "imagem aprovada", "finalizar coleta", "etapa final", "depois da coleta",
                      "como verificar", "checar imagem", "imagem ok"],
        "resposta": """Na verificação você checa a qualidade de cada imagem.

**Imagem aprovada** quando as cristas e sulcos estão visíveis e nítidos, sem manchas escuras nem apagada, centralizada no visor.

**Repita** se a imagem estiver borrada, ilegível, cortada, com sobreposição de dedos ou se o sistema indicar baixa qualidade.

Para repetir: volte ao dedo com problema, passe gaze seca no scanner, reposicione e recaptura.

📹 https://drive.google.com/file/d/1vKSLvP5WolPnjJa4y6ylrP9-rkvPwUqs/view?usp=drive_link""",
        "links": []
    },

    "seguranca_dados": {
        "categoria": "Seguranca",
        "sinonimos": ["segurança", "seguranca", "lgpd", "privacidade", "dados seguros",
                      "quem acessa", "proteção de dados", "protecao de dados", "gdpr",
                      "dados protetor", "dado salvo", "onde ficam os dados"],
        "resposta": """Os dados coletados são protegidos com criptografia de ponta a ponta, servidores com múltiplos backups e acesso restrito com log completo de auditoria. A plataforma é compatível com LGPD e padrões internacionais.

Sua responsabilidade é fazer a coleta com qualidade — a segurança técnica dos dados fica por conta da plataforma.""",
        "links": []
    },

    # ── ERROS DE HARDWARE — ETAN ──────────────────────────────────────────────

    "equipamento_nao_encontrado": {
        "categoria": "Erro Hardware",
        "sinonimos": [
            "equipamento não encontrado", "equipamento nao encontrado",
            "etan não encontrado", "etan nao encontrado",
            "device not found", "dispositivo não encontrado", "dispositivo nao encontrado",
            "scanner não encontrado", "scanner nao encontrado",
            "equipamento desconectado", "etan desconectado",
            "hardware não detectado", "hardware nao detectado",
            "etan offline", "scanner offline", "leitor não detectado",
            "nenhum dispositivo encontrado", "unable to find device",
            "não é possível conectar ao dispositivo", "nao e possivel conectar ao dispositivo",
        ],
        "resposta": """A mensagem **"Equipamento não encontrado"** aparece quando a plataforma não consegue comunicar com o ETAN. Siga esse checklist em ordem:

**1️⃣ Verifique a conexão física**
→ Desconecte e reconecte o cabo **USB-C** nos dois lados (ETAN e computador)
→ Use outra porta USB do computador — portas traseiras costumam ser mais estáveis
→ Verifique se o cabo não está dobrado ou com dano visível

**2️⃣ Verifique o software**
→ Feche completamente a plataforma e reabra
→ Na tela de captura, aguarde 10–15 segundos — o ETAN pode levar tempo para inicializar

**3️⃣ Verifique o antivírus / segurança**
→ Antivírus pode bloquear o driver do ETAN silenciosamente
→ Acione o TI hospitalar para colocar o ETAN na lista de dispositivos confiáveis

**4️⃣ Reinicie o computador**
→ Um reinício resolve ~70% dos casos de USB não reconhecido

**5️⃣ Se nada funcionou:**
→ Abra chamado em **akiyama.com.br/suporte** com: modelo do computador, sistema operacional, número de série do ETAN e passos já tentados

Qual desses passos você já tentou?""",
        "links": []
    },

    "captura_timeout": {
        "categoria": "Erro Hardware",
        "sinonimos": [
            "timeout", "time out", "tempo esgotado", "tempo limite",
            "captura travou", "travou na captura", "tela travou durante captura",
            "não progride", "nao progride", "ficou parado", "ficou na mesma tela",
            "captura não termina", "captura nao termina", "esperando captura",
            "aguardando captura", "timeout de captura", "erro de timeout",
            "connection timeout", "request timeout", "operação expirou",
            "operacao expirou", "tempo de resposta excedido",
        ],
        "resposta": """O erro de **timeout na captura** significa que o ETAN demorou demais para responder. Causas mais comuns e soluções:

**Causa 1 — Dedo mal posicionado**
→ O sistema fica aguardando uma digital válida e "desiste" após o timeout
→ Solução: reposicione a falange distal centralizada no visor, pressão bem leve

**Causa 2 — Scanner sujo**
→ Scanner sujo não lê o dedo e o sistema entra em timeout
→ Solução: limpe o visor com gaze seca e tente novamente

**Causa 3 — Comunicação USB instável**
→ O computador perdeu comunicação com o ETAN durante a operação
→ Solução: desconecte e reconecte o USB, reinicie a plataforma

**Causa 4 — Software travado**
→ Feche completamente a plataforma (verifique Gerenciador de Tarefas se necessário) e reabra
→ Se o travamento for recorrente: reinicie o computador antes de tentar

**Se acontecer em todo dedo:** pode ser problema de driver ou USB — abra chamado em **akiyama.com.br/suporte**""",
        "links": []
    },

    "erro_usb": {
        "categoria": "Erro Hardware",
        "sinonimos": [
            "erro usb", "usb error", "falha usb", "usb falhou",
            "porta usb", "usb não reconhece", "usb nao reconhece",
            "device descriptor request failed", "unknown device",
            "dispositivo usb desconhecido", "dispositivo desconhecido",
            "código 43", "codigo 43", "error code 43", "usb desconectou",
            "etan desconectou", "perdeu conexão usb", "perdeu conexao usb",
            "usb removido inesperadamente", "conexão usb instável",
            "conexao usb instavel", "usb intermitente",
        ],
        "resposta": """Erro de **USB** com o ETAN — veja o que fazer:

**Passos imediatos:**

1️⃣ **Troque a porta USB** — tente uma porta traseira do computador (mais estável que as frontais)
2️⃣ **Desconecte e reconecte** o cabo firmemente nos dois lados
3️⃣ **Troque o cabo** se tiver um reserva — cabos USB-C podem ter mau contato por dentro
4️⃣ **Verifique o Gerenciador de Dispositivos** (Windows): procure por "Dispositivo desconhecido" ou símbolo de alerta amarelo em "Dispositivos de Imagem" ou "Controladores USB"
5️⃣ **Reinstale o driver** pelo portal **akiyama.com.br** na área de downloads

**Se aparecer "Código 43" no Gerenciador:**
→ Desconecte o ETAN, aguarde 30 segundos, reconecte
→ Se persistir: desinstale o dispositivo no Gerenciador de Dispositivos e reconnecte — o Windows reinstalará

**Persistindo:** chamado em **akiyama.com.br/suporte** com print do Gerenciador de Dispositivos""",
        "links": []
    },

    "driver_problema": {
        "categoria": "Erro Software",
        "sinonimos": [
            "driver", "driver não instalado", "driver nao instalado",
            "driver corrompido", "driver inválido", "driver invalido",
            "reinstalar driver", "atualizar driver", "driver desatualizado",
            "driver com problema", "driver com erro", "driver faltando",
            "driver ausente", "falta driver", "instalar driver",
            "driver etan", "driver do scanner", "driver biométrico",
            "driver biometrico", "sem driver", "driver não encontrado",
        ],
        "resposta": """Problema de **driver do ETAN**:

**Reinstalação em 4 passos:**

1. Acesse **akiyama.com.br** → área de downloads ou suporte
2. Baixe o driver mais recente para o seu sistema operacional
3. Antes de instalar: desinstale o driver anterior no **Gerenciador de Dispositivos** (Painel de Controle → Gerenciador de Dispositivos → clique com direito no ETAN → Desinstalar dispositivo)
4. Execute o instalador baixado com **"Executar como administrador"** e siga as instruções

**⚠️ Atenção ao antivírus:**
→ Durante a instalação, o antivírus pode bloquear o driver
→ Desative temporariamente ou libere o instalador antes de prosseguir
→ Após instalação, adicione o ETAN na lista de dispositivos confiáveis

**Após reinstalar:** reinicie o computador antes de abrir a plataforma

Se ainda não resolver, abra chamado em **akiyama.com.br/suporte** informando o número de série do ETAN e o sistema operacional.""",
        "links": []
    },

    "login_plataforma": {
        "categoria": "Erro Software",
        "sinonimos": [
            "não consigo entrar", "nao consigo entrar", "não consegue logar",
            "login falhou", "login failed", "erro de login",
            "usuário inválido", "usuario invalido", "senha inválida", "senha invalida",
            "credenciais inválidas", "credenciais invalidas", "invalid credentials",
            "não consigo acessar", "nao consigo acessar", "sem acesso à plataforma",
            "sem acesso a plataforma", "senha errada", "esqueci minha senha",
            "esqueci a senha", "redefinir senha", "resetar senha", "reset senha",
            "conta bloqueada", "acesso bloqueado", "authentication failed",
            "falha na autenticação", "falha na autenticacao",
        ],
        "resposta": """Problema para **entrar na plataforma**:

**Senha incorreta / usuário inválido:**
→ Verifique se o Caps Lock está desativado
→ Confirme se está usando o e-mail institucional correto (não o pessoal)
→ Tente copiar e colar a senha para evitar erros de digitação

**Esqueceu a senha:**
→ Na tela de login, clique em **"Esqueci minha senha"**
→ Informe o e-mail cadastrado e aguarde o link de redefinição (pode cair no spam)
→ O link expira em 30 minutos — use logo

**Conta bloqueada:**
→ Após várias tentativas erradas, a conta pode ser bloqueada temporariamente
→ Aguarde 15 minutos e tente novamente, ou contate o coordenador do hospital para desbloqueio

**Primeiro acesso:**
→ Use as credenciais fornecidas pelo coordenador Akiyama — o e-mail de boas-vindas tem instruções
→ Na primeira entrada, o sistema pedirá para trocar a senha

Ainda sem acesso? Acione o suporte: **akiyama.com.br/suporte**""",
        "links": []
    },

    "plataforma_trava": {
        "categoria": "Erro Software",
        "sinonimos": [
            "tela travou", "tela congelou", "software travou", "plataforma travou",
            "plataforma parou de responder", "não responde", "nao responde",
            "ficou congelado", "ficou travado", "programa travou", "sistema travou",
            "tela preta", "tela branca", "tela de carregamento infinita",
            "loading infinito", "carregando para sempre", "não carrega",
            "nao carrega", "página não carrega", "pagina nao carrega",
            "botão não funciona", "botao nao funciona", "cliquei e nada aconteceu",
            "interface travou", "app travou", "aplicativo travou",
        ],
        "resposta": """A **plataforma travou ou não responde**:

**Solução rápida (tente primeiro):**
→ Aguarde 30 segundos — às vezes é lentidão momentânea de rede
→ Feche e reabra a plataforma
→ Se for navegador: pressione **Ctrl+F5** para forçar reload completo

**Se continuar travada:**
1. Feche completamente a plataforma (Gerenciador de Tarefas → encerrar se necessário)
2. Desconecte e reconecte o ETAN (USB)
3. Reabra a plataforma e aguarde a inicialização completa antes de usar

**Tela preta ou branca:**
→ Costuma ser problema de WebGL/renderização — atualize o navegador
→ Limpe o cache do navegador (Ctrl+Shift+Del)
→ Tente em outro navegador (Chrome e Edge são recomendados)

**Loading infinito na captura:**
→ O ETAN pode estar sem comunicação — reconecte o USB
→ Reinicie a plataforma com o ETAN já conectado

**Perda de dados:** coletas que não foram confirmadas antes do travamento podem precisar ser refeitas. Verifique o histórico de coletas após reabrir.

Se o travamento for frequente, documente quando acontece e abra chamado em **akiyama.com.br/suporte**""",
        "links": []
    },

    "erro_sincronizacao": {
        "categoria": "Erro Software",
        "sinonimos": [
            "erro ao sincronizar", "falha na sincronização", "falha na sincronizacao",
            "dados não enviados", "dados nao enviados", "não sincronizou",
            "nao sincronizou", "sync error", "erro de sincronização",
            "erro de sincronizacao", "não salvou", "nao salvou",
            "coleta não foi salva", "coleta nao foi salva", "dados perdidos",
            "upload falhou", "falha no upload", "erro ao enviar dados",
            "não enviou para o servidor", "nao enviou para o servidor",
            "servidor indisponível", "servidor indisponivel",
        ],
        "resposta": """Erro de **sincronização / dados não salvos**:

**Verifique primeiro:**
→ A conexão com a internet está ativa? Abra uma página qualquer no navegador para testar
→ A plataforma está mostrando alguma mensagem de "modo offline" ou ícone de sem sinal?

**Se estiver sem internet:**
→ A plataforma pode operar em **modo offline** — a coleta é salva localmente
→ Assim que a conexão for restaurada, a sincronização ocorre automaticamente
→ Não feche a plataforma antes da sincronização completar

**Se tiver internet mas falhar:**
1. Aguarde 2-3 minutos — pode ser instabilidade momentânea no servidor
2. Tente manualmente: procure botão "Sincronizar" ou "Reenviar" na plataforma
3. Feche e reabra a plataforma com internet ativa

**⚠️ Importante:** antes de encerrar, sempre confirme que a coleta aparece no histórico com status "Enviado" ou "Sincronizado". Se aparecer "Pendente", aguarde a sincronização.

Se os dados sumirem após tentar tudo: **akiyama.com.br/suporte** — urgente, com o ID da coleta se disponível""",
        "links": []
    },

    "sem_internet": {
        "categoria": "Erro Rede",
        "sinonimos": [
            "sem internet", "sem conexão", "sem conexao", "sem rede",
            "rede indisponível", "rede indisponivel", "erro de rede",
            "network error", "falha de rede", "conexão instável",
            "conexao instavel", "internet caiu", "wifi caiu", "sem wifi",
            "cabo de rede", "rede do hospital", "rede hospitalar",
            "vpn", "proxy", "firewall bloqueando", "não carrega nada",
            "nao carrega nada", "sem acesso à internet", "sem acesso a internet",
        ],
        "resposta": """Problema de **conexão com a internet / rede**:

**Verificação rápida:**
→ Abra outro site (ex: google.com.br) — se abrir, a internet está ok e o problema é na plataforma
→ Se não abrir: a rede do hospital está fora

**Sem internet no hospital:**
→ Acione o TI hospitalar imediatamente
→ Enquanto isso: a plataforma pode funcionar em **modo offline** para captura, sincronizando depois
→ Não tente reiniciar o roteador sozinha — é responsabilidade do TI

**Internet ok mas plataforma não acessa:**
→ O firewall ou proxy do hospital pode estar bloqueando o endereço da plataforma
→ Informe ao TI o domínio da plataforma (akiyama.com.br) para liberar
→ Se usar VPN corporativa: tente desconectar e reconectar a VPN

**WiFi instável durante captura:**
→ Se possível, use cabo de rede (ethernet) para estabilidade
→ Evite atualizações de sistema ou downloads pesados em paralelo durante a coleta

Problema persiste? **akiyama.com.br/suporte** com descrição da rede e o que já foi tentado""",
        "links": []
    },

    "nfiq_baixo": {
        "categoria": "Qualidade",
        "sinonimos": [
            "nfiq", "nfiq baixo", "score nfiq", "nfiq ruim", "qualidade nfiq",
            "score de qualidade", "nota de qualidade", "pontuação baixa",
            "pontuacao baixa", "quality score", "score baixo", "índice de qualidade",
            "indice de qualidade", "qualidade insuficiente", "nota insuficiente",
            "resultado nfiq", "nfiq 1", "nfiq 2", "nfiq 3", "nfiq 4", "nfiq 5",
        ],
        "resposta": """O **NFIQ** (Nível de Qualidade da Digital) é o score que o sistema Openbio Enroll atribui a cada captura. **Quanto maior, melhor.**

**Escala NFIQ correta (padrão INFANT.ID / Akiyama):**

| NFIQ | Qualidade | O que fazer |
|------|-----------|-------------|
| 5    | ✅ Excelente | Pronto para uso |
| 4    | ✅ Bom | Aceito |
| 3    | ⚠️ Regular | Aceito com ressalvas — tente melhorar |
| 2    | ❌ Pobre | Refazer a captura |
| 1    | ❌ Ruim | Falha — refazer obrigatoriamente |

**Threshold mínimo aceito:** NFIQ 3 (≈70% de qualidade)

**Como melhorar o NFIQ:**

🔹 **Dedos muito úmidos** (imagem escura, NFIQ cai) → seque com toalha antes de capturar
🔹 **Dedos muito secos** (imagem apagada, demora para aparecer) → mergulhe as pontas em copo com água, seque completamente antes de capturar
🔹 **Scanner sujo** (causa mais comum de NFIQ 1–2) → flanela de material não abrasivo seca. Nunca álcool no leitor.
🔹 **Posicionamento** → falange distal centralizada, pressão leve (80–120 mmHg ideal)
🔹 **Vernix nos dedos** → higienize com NATO soro, aguarde 1–2 min, tente novamente

⚠️ NFIQ 1–2 sistematicamente em todos os dedos → scanner pode estar descalibrado → abra chamado em **akiyama.com.br/suporte**""",
        "links": []
    },

    "numero_serie": {
        "categoria": "Equipamento",
        "sinonimos": [
            "número de série", "numero de serie", "serial do etan", "serial number",
            "s/n", "sn do equipamento", "onde fica o serial", "encontrar serial",
            "identificação do equipamento", "identificacao do equipamento",
            "código do equipamento", "codigo do equipamento", "patrimônio",
            "patrimonio", "etiqueta do etan", "etiqueta do equipamento",
            "kit etan", "número do kit", "numero do kit",
        ],
        "resposta": """O **número de série (S/N)** do ETAN fica:

📍 Na **etiqueta adesiva** no fundo ou na lateral do equipamento — formato parecido com "ETAN-XXXX-XXXX" ou similar

📍 Na **plataforma** (se o equipamento já foi registrado): Menu → Equipamentos → selecione o ETAN → aba Detalhes

📍 Na **embalagem original** do kit — se ainda tiver guardada

**Por que é importante?**
O número de série é exigido ao abrir chamado técnico em **akiyama.com.br/suporte** e para identificar o equipamento em caso de garantia ou substituição.

Encontrou o número?""",
        "links": []
    },

    "erro_certificado_ssl": {
        "categoria": "Erro Software",
        "sinonimos": [
            "certificado inválido", "certificado invalido", "ssl error", "ssl inválido",
            "conexão não segura", "conexao nao segura", "certificado expirado",
            "certificate error", "sua conexão não é privada", "sua conexao nao e privada",
            "net::err_cert", "err_cert_authority_invalid", "certificado ssl",
            "aviso de segurança", "aviso de seguranca", "site inseguro",
        ],
        "resposta": """Erro de **certificado SSL / conexão não segura**:

Isso significa que o navegador está rejeitando o certificado de segurança da plataforma.

**Solução 1 — Verificar data e hora do computador**
→ Certificados SSL são sensíveis à data — uma data errada no computador causa esse erro
→ Clique no relógio do Windows → "Configurações de data e hora" → ative "Definir horário automaticamente"

**Solução 2 — Atualizar o navegador**
→ Navegadores desatualizados podem rejeitar certificados modernos
→ Chrome: Menu → Ajuda → Sobre o Google Chrome → atualiza automaticamente

**Solução 3 — Verificar proxy/antivírus**
→ Alguns antivírus inspecionam conexões HTTPS e podem causar conflito com o certificado
→ Informe ao TI hospitalar — eles podem precisar configurar exceção para o domínio akiyama.com.br

**Para uso temporário (apenas se orientado pelo TI):**
→ Clique em "Avançado" ou "Mais informações" na tela de erro → "Prosseguir assim mesmo"
→ ⚠️ Use essa opção apenas em redes hospitalares controladas, nunca em redes públicas

Abra chamado em **akiyama.com.br/suporte** se o problema persistir após essas tentativas""",
        "links": []
    },

    "firmware_atualizacao": {
        "categoria": "Equipamento",
        "sinonimos": [
            "firmware", "atualizar firmware", "update firmware", "versão desatualizada",
            "versao desatualizada", "firmware desatualizado", "update disponível",
            "update disponivel", "nova versão disponível", "nova versao disponivel",
            "atualização disponível", "atualizacao disponivel", "versão do etan",
            "versao do etan", "atualizar etan", "versão do software", "versao do software",
            "upgrade do sistema",
        ],
        "resposta": """**Atualização de firmware / software do ETAN:**

**O que é firmware?**
É o "sistema operacional interno" do ETAN — atualizar melhora estabilidade, qualidade de captura e corrige bugs.

**Como atualizar:**
1. Acesse **akiyama.com.br** → área de downloads ou suporte
2. Baixe a versão mais recente do firmware para o seu modelo de ETAN
3. Siga as instruções do guia de atualização que acompanha o arquivo
4. ⚠️ **Nunca interrompa** uma atualização em andamento — isso pode danificar o equipamento
5. Após atualizar, reinicie o ETAN e a plataforma

**⚠️ Aviso importante:**
Só faça a atualização se a Akiyama recomendou, ou se o suporte orientou. Não atualize durante uma jornada de coletas ativa — faça em momento sem urgência.

Se tiver dúvida sobre qual versão está instalada: **akiyama.com.br/suporte** — eles conseguem verificar remotamente.""",
        "links": []
    },

    "coleta_nao_salva": {
        "categoria": "Erro Software",
        "sinonimos": [
            "coleta sumiu", "dados sumiram", "perdi a coleta", "coleta desapareceu",
            "não encontro a coleta", "nao encontro a coleta", "coleta não aparece",
            "coleta nao aparece", "onde está a coleta", "onde esta a coleta",
            "histórico vazio", "historico vazio", "coleta foi embora",
            "coleta não registrou", "coleta nao registrou", "não consta no sistema",
            "nao consta no sistema", "paciente não aparece", "paciente nao aparece",
        ],
        "resposta": """A coleta **não aparece no sistema**:

**Verificação imediata:**
1. Filtre o histórico por **data de hoje** — às vezes aparece em outra página
2. Verifique se você está logada na **conta correta** (usuário certo do hospital certo)
3. Procure por **status "Pendente"** — a coleta pode estar aguardando sincronização

**Se estava offline durante a coleta:**
→ A coleta fica salva localmente com status "Pendente"
→ Conecte à internet — a sincronização automática deve ocorrer em minutos
→ Procure botão "Sincronizar agora" se disponível na interface

**Se a coleta era de outro turno:**
→ Verifique com a enfermeira responsável se ela está logada com o usuário correto
→ Coletas de outros turnos ficam no histórico geral do hospital, não só do usuário

**Se depois de tudo não aparecer:**
→ **Não refaça** a coleta ainda — entre em contato primeiro com o suporte
→ **akiyama.com.br/suporte** com: nome do paciente, data/hora aproximada da coleta, usuário que realizou
→ Eles conseguem recuperar do servidor mesmo que não apareça na interface""",
        "links": []
    },

    # ── ERROS REAIS DO INFORMATIVO ETAN (Akiyama) ─────────────────────────────

    "openbio_enroll": {
        "categoria": "Erro Software",
        "sinonimos": [
            "openbio enroll", "openbio", "aplicação fechou", "aplicacao fechou",
            "programa fechou sozinho", "app fechou", "sistema fechou sozinho",
            "fechou sozinho", "desconectou e fechou", "reabrindo o aplicativo",
            "reconectar e reabrir", "openbio fechou", "o programa fechou",
            "software fechou", "software fecha", "aplicativo fecha",
        ],
        "resposta": """O **Openbio Enroll** (software de captura biométrica do ETAN) fecha automaticamente quando o cabo USB é desconectado — isso é comportamento normal e esperado, não é um bug.

**O que fazer:**
1. Reconecte o cabo USB do ETAN ao notebook
2. Aguarde o Windows reconhecer o dispositivo (5–10 segundos)
3. Reabra o **Openbio Enroll**
4. Faça login novamente se necessário

✅ Nenhum dado é perdido — as coletas já registradas ficam salvas no servidor.

**Prevenção:** certifique-se de que o cabo USB está bem encaixado e posicionado de forma que não tombará durante a coleta.""",
        "links": []
    },

    "session_json": {
        "categoria": "Erro Software",
        "sinonimos": [
            "não abre o sistema", "nao abre o sistema", "após queda de energia",
            "apos queda de energia", "não inicializa", "nao inicializa",
            "inicia com erros", "session.json", "appdata", "openbioservices",
            "desligamento não convencional", "desligamento nao convencional",
            "queda de luz", "falta de energia", "travou no carregamento",
            "tela preta ao abrir", "não abre depois de desligar",
            "nao abre depois de desligar", "erro ao iniciar o openbio",
        ],
        "resposta": """Após **queda de energia** ou **desligamento forçado** (sem fechar o programa corretamente), o arquivo `Session.json` pode ficar corrompido e impedir a abertura do Openbio Enroll.

**Solução (passo a passo):**

1. Feche completamente o Openbio Enroll (se ainda estiver aberto)
2. Abra o **Explorador de Arquivos** (Win + E)
3. Cole na barra de endereços e pressione Enter:
   ```
   C:\\Users\\User\\AppData\\Roaming\\OpenbioServices
   ```
4. Localize o arquivo **Session.json**
5. **Delete** o arquivo Session.json
6. Reinicie o Openbio Enroll

✅ O sistema irá criar um novo Session.json automaticamente.

⚠️ Se `AppData` não aparecer: no Explorador de Arquivos, vá em **Exibir → Itens ocultos** e ative.""",
        "links": []
    },

    "equipamento_descalibrado": {
        "categoria": "Equipamento",
        "sinonimos": [
            "descalibrado", "descalibração", "descalibracao", "margens na tela",
            "sombra na captura", "borda preta", "área de captura com margem",
            "area de captura com margem", "imagem com borda", "imagem com margem",
            "listras na captura", "faixa escura na imagem", "capture area problema",
            "scanner descalibrado", "calibração do etan", "calibracao do etan",
        ],
        "resposta": """Se a **área de captura** do ETAN está apresentando **margens pretas, sombras ou bordas** nas imagens, o equipamento está descalibrado.

⚠️ **Não tente resolver sozinha** — a descalibração requer intervenção técnica da equipe Akiyama.

**O que fazer:**
1. Anote o **número de série (S/N)** do equipamento (etiqueta na lateral/fundo do ETAN)
2. Faça um **print/foto** da área de captura mostrando as margens
3. Abra um chamado em: **akiyama.com.br/suporte**
   - Informe: número de série, descrição do problema, foto/print
4. A equipe CS fará ajuste remoto ou substituição do equipamento

Enquanto aguarda o chamado, **evite usar esse ETAN** se possível — as digitais com margens vão ter NFIQ comprometido.""",
        "links": []
    },

    "sensor_aquecido": {
        "categoria": "Equipamento",
        "sinonimos": [
            "sensor quente", "qualidade caiu do nada", "qualidade piorou de repente",
            "muitas capturas seguidas", "qualidade baixou de repente",
            "etan esquentou", "sensor esquentou", "muitas digitais seguidas",
            "trabalhando muito tempo", "uso intensivo", "qualidade caindo",
            "ficou ruim de repente", "nfiq caiu", "capturando muitos bebes",
        ],
        "resposta": """Após **~20 capturas consecutivas**, o sensor do ETAN pode aquecer levemente, causando redução temporária na qualidade das imagens (NFIQ cai).

**O que fazer:**
→ **Descanse o equipamento por 2–3 minutos** sem capturar
→ Após o resfriamento, a qualidade volta ao normal automaticamente

✅ Isso é comportamento esperado do equipamento, não é defeito.

**Dica de rotina:** em berçários com muitos RNs, alterne entre dois equipamentos ETAN se disponível, ou faça pequenas pausas entre grupos de capturas.""",
        "links": []
    },

    "permissao_camera": {
        "categoria": "Plataforma",
        "sinonimos": [
            "permissão negada", "permissao negada", "permission denied",
            "câmera bloqueada", "camera bloqueada", "câmera não permitida",
            "camera nao permitida", "cadeado câmera", "browser bloqueia câmera",
            "navegador não permite câmera", "navegador nao permite camera",
            "câmera não funciona no site", "camera nao funciona no site",
            "não consegue usar câmera", "icone de cadeado", "site sem câmera",
        ],
        "resposta": """O navegador bloqueou a câmera. Siga os passos conforme o seu navegador:

**Google Chrome / Microsoft Edge:**
1. Clique no **ícone de cadeado** 🔒 na barra de endereços
2. Vá em **Permissões** (ou "Configurações do site")
3. Em **Câmera**, selecione **Permitir**
4. Pressione **F5** para recarregar a página
5. Aceite a solicitação de câmera quando aparecer

**Mozilla Firefox:**
1. Clique no ícone de **cadeado** ou **câmera** na barra de endereços
2. Em Câmera, clique em **Remover bloqueio**
3. Pressione **F5** para recarregar
4. Clique em **Permitir** quando o Firefox perguntar

⚠️ Se a câmera já estava aberta em outro programa (Teams, Zoom, etc.), feche-os primeiro.
⚠️ Em computadores do hospital com políticas de TI restritivas, pode ser necessário acionar o suporte de TI do hospital.""",
        "links": []
    },

    "dedos_secos_agua": {
        "categoria": "Captura",
        "sinonimos": [
            "dedos secos", "dedo seco", "digital não aparece", "digital nao aparece",
            "demora para aparecer a digital", "scanner não pega", "scanner nao pega",
            "não reconhece o dedo", "nao reconhece o dedo", "dedo muito seco",
            "pele seca", "idoso com pele seca", "progenitora com dedo seco",
            "dificuldade de capturar progenitora", "copo de agua", "copo d agua",
            "mergulhar dedo", "umidificar dedo",
        ],
        "resposta": """Dedos muito secos causam NFIQ baixo porque a digital fica apagada/fraca no sensor.

**Solução oficial (protocolo Akiyama):**
1. Pegue um **copo com água**
2. Peça à paciente para **mergulhar as pontas dos dedos** por 10–15 segundos
3. **Seque completamente** as pontas dos dedos com toalha/gaze seca
4. Realize a captura imediatamente após secar

✅ Essa técnica aumenta significativamente o NFIQ em pacientes com pele ressecada.

**Regra importante:** certifique-se que os dedos estão **secos** antes de colocar no scanner — dedo molhado também prejudica o NFIQ (imagem fica escura). Seque bem!

**Para bebês RN com pele ressecada:** a mesma técnica se aplica, com mais delicadeza.""",
        "links": []
    },
}


def buscar_resposta(pergunta: str, atual_curso_id: Optional[int] = None) -> dict:
    """
    Busca a melhor resposta na knowledge base.
    Retorna sem resposta (sucesso=False) para deixar o Ollama responder.
    """
    pergunta_lower = pergunta.lower()

    melhor_resultado = None
    melhor_score = 0

    for chave, info in KNOWLEDGE_BASE.items():
        score = 0
        if chave in pergunta_lower:
            score = 1.0
        elif "sinonimos" in info:
            for sinonimo in info["sinonimos"]:
                if sinonimo in pergunta_lower:
                    score = 0.9
                    break

        if score > melhor_score:
            melhor_score = score
            melhor_resultado = (chave, info)

    if melhor_resultado:
        chave, info = melhor_resultado
        return {
            "resposta": info["resposta"],
            "links_aulas": info.get("links", []),
            "confianca": melhor_score,
            "categoria": info.get("categoria"),
            "aula_id": info.get("aula"),
            "curso": info.get("curso", "INFANT.ID"),
            "sucesso": True
        }

    # Não achou — deixa o Ollama responder
    return {
        "resposta": "",
        "sucesso": False,
        "confianca": 0,
        "sugestoes": []
    }


if __name__ == "__main__":
    print("Knowledge Base INFANT.ID — Teste")
    print("=" * 50)
    test_perguntas = [
        "Como calmar o bebê durante a coleta?",
        "Como limpar o scanner ETAN?",
        "Bebê com mão fechada, o que faço?",
        "Como coletar da progenitora?",
        "A imagem está borrada, o que fazer?",
    ]
    for pergunta in test_perguntas:
        resultado = buscar_resposta(pergunta)
        print(f"\n❓ {pergunta}")
        print(f"   Sucesso: {resultado['sucesso']} | Confiança: {resultado['confianca']*100:.0f}%")
