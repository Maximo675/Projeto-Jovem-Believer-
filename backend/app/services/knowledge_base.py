"""
Knowledge Base para IA do INFANT.ID
Integra conhecimento de cursos + documentos para respostas contextualizadas

A IA pode agora:
- Responder sobre conteúdo específico de cada curso
- Fornecer links diretos para aulas relevantes
- Dar dicas práticas baseadas no treinamento
- Gerar sugestões personalizadas
"""

from typing import Optional

# Base de Conhecimento Estruturada
KNOWLEDGE_BASE = {
    # ===== ONBOARDING INFANT.ID =====
    "biometria": {
        "categoria": "Fundamentos",
        "modulos": ["iri disponível", "impressão digital", "facial", "voz"],
        "aula": 2,
        "resposta": """
A biometria é a medição de características físicas únicas. INFANT.ID usa:

🔹 **Impressão Digital** (99.9% acurácia)
   - Padrões das cristas papilares
   - Coleta a partir de 6 meses

🔹 **Íris** (99.99% acurácia) ← Mais confiável
   - Padrão único de cada olho
   - Funciona desde nascimento

🔹 **Facial** (98% acurácia)
   - Geometria do rosto
   - Rápido e não-invasivo

🔹 **Voz** (97% acurácia)
   - Padrões acústicos
   - Coleta a partir de 3 meses

👉 Próxima aula: "Equipamentos e Sensores" para aprender como usa-se!
        """,
        "links": [
            {"texto": "Fundamentos da Biometria", "aula_id": 2},
            {"texto": "Equipamentos e Sensores", "aula_id": 3}
        ]
    },
    
    "coleta": {
        "categoria": "Procedimentos",
        "sinonimos": ["coletar", "coleta", "captura", "procedimento", "como coletar"],
        "aula": 4,
        "resposta": """
📋 **Protocolo de Coleta Biométrica - 5 FASES**

**Preparação (5 min)**
✓ Calibrar equipamentos
✓ Confirmar identidade
✓ Obter consentimento
✓ Explicar ao criança

**Fase 1: Impressões Digitais (5 min)**
→ Posicionar dedo no scanner
→ Pressionar 2-3 segundos
→ Sistema valida qualidade

**Fase 2: Foto Facial (3 min)**
→ Posicionar a 45cm
→ Captura automática frontal

**Fase 3: Íris (2 min)**
→ "Olhe para o ponto vermelho"
→ Capturar ambos os olhos

**Fase 4: Voz (1 min)**
→ Criança diz frase fornecida

**Próximas Etapas:**
✓ Sistema processa e gera ID
✓ Imprimir recibo
✓ Assinar consentimento
✓ Arquivar documentação

⚠️ Qualidade > Velocidade! Uma boa coleta vale mais que 10 ruins.
        """,
        "links": [
            {"texto": "Ver tutorial completo", "aula_id": 4},
            {"texto": "Troubleshooting comum", "aula_id": 6}
        ]
    },
    
    "segurança": {
        "categoria": "Conformidade",
        "sinonimos": ["segura", "segurança", "criptografia", "lgpd", "privacidade"],
        "aula": 5,
        "resposta": """
🔒 **Segurança INFANT.ID - Múltiplas Camadas**

**Encriptação:**
🔐 Em Trânsito: TLS 1.3 (256-bit)
🔐 Em Repouso: AES-256 (militar grade)
🔐 Hash Biométrico: SHA-3 com salting aleatório

**Conformidade LGPD:**
✅ Consentimento informado
✅ Direito de acesso (responsável pode solicitar dados)
✅ Direito ao esquecimento (deletar dados)
✅ Portabilidade (transferir para outro sistema)
✅ Direito de oposição (recusar processamento)

**Retenção de Dados:**
📅 0-7 anos: Mantido ativo
📅 7-10 anos: Arquivado, sem acesso regular  
📅 >10 anos: Apagado automaticamente
⚖️ Exceção: Investigação legal pode estender

**Incidente de Segurança?**
1. Notificar responsável em 48h
2. Informar autoridade de proteção
3. Fornecer medidas de mitigação
4. Auditoria completa

👉 Aprenda mais em "Segurança e LGPD"!
        """,
        "links": [
            {"texto": "Segurança e Conformidade LGPD", "aula_id": 5}
        ]
    },
    
    "problemas": {
        "categoria": "Troubleshooting",
        "sinonimos": ["problema", "erro", "não funciona", "dificuldade", "ajuda"],
        "aula": 6,
        "resposta": """
🔧 **Problemas Comuns - Soluções Rápidas**

**❌ Dígito não reconhecido**
→ Dedo seco? Hidratar com loção neutra
→ Sujo? Limpar em pano branco úmido
→ Ferimento? Tentar outro dedo
→ Pressão errada? Ajustar leve mente

**❌ Foto facial borrada**
→ Movimento? Pedir para ficar imóvel
→ Pouca luz? Reduzir brilho, iluminar lateralmente
→ Muito perto/longe? Ajustar distância (45cm ideal)
→ Lente suja? Limpar com pano estéril

**❌ Íris não detectada**
→ Olhos fechados? Deixar piscar e tentar depois
→ Reflexos altos? Ajustar ângulo da câmera
→ Óculos? Remover para captura
→ Pouca iluminação? Aumentar luzes do ambiente

**Melhores Práticas:**
✓ Qualidade > Velocidade
✓ Se falhar 3x, pausar e tentar outro dia
✓ Ambiente acolhedor = melhor coleta
✓ Paciência com criança nervosa

👉 Veja guia detalhado em "Troubleshooting e Melhores Práticas"!
        """,
        "links": [
            {"texto": "Guia completo de troubleshooting", "aula_id": 6}
        ]
    },
    
    # ===== INTEGRAÇÃO HOSPITALAR =====
    "integração": {
        "categoria": "Técnico",
        "sinonimos": ["integração", "sistema", "his", "hospital", "conectar"],
        "aula": 1,
        "curso": "Integração Hospitalar",
        "resposta": """
🏥 **Integração INFANT.ID com Seu HIS**

**Arquitetura:**
📌 INFANT.ID Core (processamento biométrico)
📌 Hospital Information System (seu sistema)
📌 Middleware (traduz dados entre sistemas)
📌 API RESTful (comunicação segura)

**Fluxo Integrado:**
1. Paciente chega → HIS cria registro
2. Sistema notifica INFANT.ID
3. Técnico coleta biometria
4. Dados sincronizados automaticamente
5. ID único vinculado ao HIS

**Protocolo HTTP/REST:**
POST /api/v1/pacientes
{
  "nome": "João Silva",
  "data_nascimento": "2020-05-15",
  "responsavel": "Maria Silva"
}

**Segurança na Integração:**
🔐 API Keys com JWT (24h)
🔐 TLS 1.3 para todas requisições
🔐 Assinatura digital (HMAC-SHA256)
🔐 Log completo para auditoria

👉 Quer implementar? Veja "Implementação Técnica"!
        """,
        "links": [
            {"texto": "Arquitetura de Integração", "aula_id": 1},
            {"texto": "Implementação Técnica", "aula_id": 2},
            {"texto": "Troubleshooting", "aula_id": 4}
        ]
    },
    
    "api": {
        "categoria": "Desenvolvimento",
        "sinonimos": ["api", "desenvolvedor", "código", "técnico", "integração"],
        "aula": 2,
        "curso": "Integração Hospitalar",
        "resposta": """
👨‍💻 **SDK INFANT.ID - Rápido Início**

**Instalação:**
pip install infantid-sdk==2.1.0
npm install @infantid/sdk

**Exemplo Python:**
```python
from infantid import InfantIDClient

client = InfantIDClient(
    api_key="sua_chave",
    api_secret="seu_secret"
)

paciente = client.pacientes.create({
    'nome': 'João Silva',
    'data_nascimento': '2020-05-15'
})

print(f"ID gerado: {paciente['infant_id']}")
```

**Exemplo Node.js:**
```javascript
const { InfantID } = require('@infantid/sdk');

const client = new InfantID({
  apiKey: process.env.API_KEY
});

const patient = await client.patients.create({
  name: 'Maria Santos',
  birthDate: '2019-03-20'
});
```

**Testes:**
GET /api/v1/health ← Verificar conexão
GET /api/v1/pacientes ← Listar pacientes
GET /api/v1/mapping/validate/{id} ← Validar dado

👉 Veja documentação completa em "Implementação Técnica"!
        """,
        "links": [
            {"texto": "Guia Técnico Completo", "aula_id": 2}
        ]
    },
    
    "workflow": {
        "categoria": "Clínico",
        "sinonimos": ["workflow", "fluxo", "processo", "rotina", "clínico"],
        "aula": 3,
        "curso": "Integração Hospitalar",
        "resposta": """
🔄 **Fluxo Clínico Completo com INFANT.ID**

**Entrada:**
1️⃣ Responsável chega na recepção
2️⃣ Cria registro no HIS
3️⃣ Notificação automática ao INFANT.ID

**Coleta:**
4️⃣ QR code gerado com dados do paciente
5️⃣ Técnico escaneia e coleta biometria
6️⃣ ID único vinculado automaticamente

**Atendimento:**
7️⃣ Médico acessa registro com identidade verificada
8️⃣ Histórico completo disponível
9️⃣ Alertas automáticos de duplicatas

**Alta:**
🔟 Registro completo salvo
1️⃣1️⃣ Dados arquivados com LGPD
1️⃣2️⃣ Certificado disponível

**Casos Especiais:**

🌟 **Bebê Prematuro (2kg)**
→ Coleta suave de íris + voz
→ Digital completa quando peso adequado
→ 99.99% acurácia mesmo em casos difíceis

🌟 **Criança com Deficiência**
→ Sistema oferece múltiplas modalidades
→ Se digital inadequada, usa íris + facial + voz
→ Igualdade de direitos garantida

👉 Veja detalhes em "Workflow Clínico com INFANT.ID"!
        """,
        "links": [
            {"texto": "Fluxo Clínico Integrado", "aula_id": 3}
        ]
    },
    
    # ===== GERENCIAMENTO DE USUÁRIOS =====
    "usuarios": {
        "categoria": "Admin",
        "sinonimos": ["usuário", "usuários", "conta", "perfil", "acesso"],
        "aula": 1,
        "curso": "Gerenciamento de Usuários",
        "resposta": """
👥 **Gerenciamento de Usuários e Permissões**

**Papéis Disponíveis:**

🔴 **Administrador**
   → Criar, modificar, deletar usuários
   → Acessar configurações
   → Gerar relatórios
   → Todas os pacientes

🟣 **Médico**  
   → Ver prontuários
   → Solicitar coleta
   → Prescrever
   → Seus pacientes atribuidos

🟡 **Técnico Biometria**
   → Coletar dados
   → Validar qualidade
   → Pacientes agendados

🟢 **Recepcionista**
   → Agendar coleta
   → Registrar chegada
   → Calendário de agendamentos

🔵 **Auditor**
   → Visualizar logs
   → Gerar relatórios
   → Todos logs (sem dados sensíveis)

**Princípios de Segurança:**
🔒 Least Privilege: Mínimo acesso necessário
🔒 Separação de Deveres: Técnico não vê dados médicos
🔒 Auditoria Completa: Toda ação registrada
🔒 Revogação Rápida: Desativar remove acesso imediatamente

👉 Saber criar usuários? Veja tutorial em "Controle de Acesso"!
        """,
        "links": [
            {"texto": "Controle de Acesso e Permissões", "aula_id": 1}
        ]
    },
    
    "auditoria": {
        "categoria": "Conformidade",
        "sinonimos": ["auditoria", "compliance", "relatório", "relatórios", "logs"],
        "aula": 3,
        "curso": "Gerenciamento de Usuários",
        "resposta": """
📊 **Auditoria e Compliance**

**Sistema Completo de Logs:**
- Cada ação registrada imutavelmente
- Quem fez, quando, resultado
- Histórico de 3 anos online

**Alertas de Segurança:**
⚠️ Múltiplas tentativas login falhadas → Bloqueia 30min
⚠️ IP incomum → Email de notificação
⚠️ Acesso fora do horário → Alerta
⚠️ Deleção em massa → Requer autorização

**Relatórios Prontos para Auditores:**

📄 **Relatório LGPD**
   → Todos acessos a dados pessoais
   → Quem acessou quando e porquê
   → Conformidade com artigos 30-35

📄 **Relatório de Segurança**
   → Falhas de login
   → Mudanças de permissão
   → Alertas disparados

📄 **Relatório Operacional**
   → Coletas realizadas
   → Processamentos
   → Taxa de erro

📄 **Certificado de Conformidade**
   → ISO/IEC 27001
   → SOC2 Type II
   → NIST Privacy Framework

**Download de Relatório:**
GET /api/v1/reports/compliance?format=pdf&month=2026-02

👉 Saiba mais em "Auditoria e Compliance"!
        """,
        "links": [
            {"texto": "Auditoria e Conformidade", "aula_id": 3}
        ]
    }
}

# Função para buscar resposta contextualizada
def buscar_resposta(pergunta: str, atual_curso_id: Optional[int] = None) -> dict:
    """
    Busca a melhor resposta na knowledge base
    
    Args:
        pergunta (str): Pergunta do usuário
        atual_curso_id (int|None): ID do curso atual (opcional, para contexto)
        
    Returns:
        dict: Resposta com texto, links para aulas, confiança (0-1)
    """
    pergunta_lower = pergunta.lower()
    
    melhor_resultado = None
    melhor_score = 0
    
    # Buscar por palavra-chave
    for chave, info in KNOWLEDGE_BASE.items():
        # Verificar match direto
        if chave in pergunta_lower:
            score = 1.0
        # Verificar sinônimos
        elif 'sinonimos' in info:
            for sinonimo in info['sinonimos']:
                if sinonimo in pergunta_lower:
                    score = 0.9
                    break
            else:
                continue
        else:
            continue
        
        if score > melhor_score:
            melhor_score = score
            melhor_resultado = (chave, info)
    
    if melhor_resultado:
        chave, info = melhor_resultado
        return {
            'resposta': info['resposta'],
            'links_aulas': info.get('links', []),
            'confianca': melhor_score,
            'categoria': info.get('categoria'),
            'aula_id': info.get('aula'),
            'curso': info.get('curso', 'Onboarding INFANT.ID'),
            'sucesso': True
        }
    
    # Se não achou, retornar resposta genérica
    return {
        'resposta': f"""
Entendi sua pergunta sobre "{pergunta}", mas não tenho uma resposta específica no momento.

Posso ajudar com:
• 🧬 **Biometria**: Tipos, como funciona, modalidades
• 📋 **Coleta**: Protocolo passo a passo
• 🔒 **Segurança**: Criptografia, LGPD, conformidade
• 🔧 **Problemas**: Troubleshooting comum
• 🏥 **Integração**: HIS, API, implementação técnica
• 👥 **Usuários**: Papéis, permissões, gerenciamento
• 📊 **Auditoria**: Logs, relatórios, compliance

👉 Experimente perguntar sobre um dos tópicos acima!
        """,
        'sucesso': False,
        'confianca': 0,
        'sugestoes': [
            'biometria',
            'coleta',
            'segurança',
            'integração',
            'problemas'
        ]
    }


if __name__ == '__main__':
    # Teste simples
    print("🤖 Knowledge Base IA INFANT.ID")
    print("=" * 50)
    
    test_perguntas = [
        "Como coletar biometria?",
        "Qual módulo fala sobre LGPD?",
        "Tenho problema com dígito não reconhecido",
        "Como integrar com meu HIS?",
        "Quais são os papéis de usuário?"
    ]
    
    for pergunta in test_perguntas:
        print(f"\n❓ {pergunta}")
        resultado = buscar_resposta(pergunta)
        print(f"✅ Confiança: {resultado['confianca']*100:.0f}%")
        print(f"   Categoria: {resultado.get('categoria', 'N/A')}")
        if resultado.get('links_aulas'):
            print(f"   Links: {resultado['links_aulas']}")
