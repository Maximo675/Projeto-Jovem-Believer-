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
    }
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
