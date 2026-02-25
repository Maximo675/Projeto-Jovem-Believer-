"""
Script para POPULAR AULAS COM CONTEDO PROFISSIONAL
- Cria aulas didticas com HTML estruturado
- Integra conhecimento baseado em documentos do INFANT.ID
- Torna a plataforma COMPLETA como uma Alura real

Executar: python populate_lessons_content.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.course import Course
from app.models.lesson import Lesson

# Cores
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_section(title):
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}{title:^70}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

def get_curso_1_aulas():
    """Aulas para: Onboarding INFANT.ID - Módulo 1"""
    return [
        {
            'titulo': 'Bem-vindo ao INFANT.ID',
            'descricao': 'Apresentação do sistema e seus objetivos',
            'ordem': 1,
            'duracao': 15,
            'video_url': '',
            'conteudo': '''
<div class="aula-container">
    <h1>Bem-vindo ao Sistema INFANT.ID</h1>
    
    <h2>O que você vai aprender neste módulo</h2>
    <p>Bem-vindo ao INFANT.ID! Nesta primeira aula, você conhecerá o sistema de identificação biométrica infantil mais avançado do Brasil.</p>
    
    <h3>Objetivos da Plataforma</h3>
    <ul>
        <li><strong>Segurança Máxima:</strong> Coleta biométrica segura e LGPD-compliant</li>
        <li><strong>Eficincia:</strong> Reduz tempo de atendimento em hospitais</li>
        <li><strong>Confiabilidade:</strong> Identificação unívoca de pacientes pediátricos</li>
        <li><strong>Integração:</strong> Funciona com sistemas hospitalares existentes</li>
    </ul>
    
    <h3>Público-alvo</h3>
    <p>Este treinamento  voltado para:</p>
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
        <p>Prossiga para a prxima aula: "Princípios de Biometria Infantil"</p>
    </div>
</div>
            '''
        },
        {
            'titulo': 'Princípios de Biometria Infantil',
            'descricao': 'Entenda como funciona a coleta de dados biométricos em crianças',
            'ordem': 2,
            'duracao': 20,
            'conteudo': '''
<div class="aula-container">
    <h1>Fundamentos da Biometria Infantil</h1>
    
    <h2>O que é Biometria?</h2>
    <p>Biometria é a medição e análise estatística dos padrões úúnicos de características físicas e de comportamento. 
    Não INFANT.ID, usamos múltiplas modalidades biométricas para identificação infantil segura.</p>
    
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
            <td>99.9%</td>
        </tr>
        <tr>
            <td><strong>Íris</strong></td>
            <td>Padrão das estruturas da Íris</td>
            <td>Nascimento</td>
            <td>99.99%</td>
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
        <li>Cumprimento LGPD e resoluções éticas</li>
    </ul>
    
    <div class="dica">
        <strong>Dica Importante:</strong> Sempre priorize o bem-estar da criança durante qualquer coleta biométrica.
    </div>
</div>
            '''
        },
        {
            'titulo': 'Equipamentos e Sensores',
            'descricao': 'Conheça os equipamentos utilizados para coleta biométrica',
            'ordem': 3,
            'duracao': 25,
            'conteudo': '''
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
    <p>Tecnologia mais avanada de identificação biométrica.</p>
    <ul>
        <li><strong>Alcance:</strong> 10-35cm (maior liberdade de movimento)</li>
        <li><strong>Análise:</strong> 400+ pontos de características únicas</li>
        <li><strong>Velocidade:</strong> Menos de 1 segundo</li>
        <li><strong>Certificação:</strong> ISO/IEC 19794-6</li>
    </ul>
    
    <h2>Microfone Biométrico</h2>
    <p>Coleta padrões acústicos para verificação de voz.</p>
    <ul>
        <li><strong>Frequncia:</strong> 16-48 kHz</li>
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
            <li><strong>Deciso:</strong> Gerar score de confiança</li>
        </ol>
    </div>
</div>
            '''
        },
        {
            'titulo': 'Protocolo de Coleta Passo a Passo',
            'descricao': 'Aprenda o protocolo exato para coletar dados biométricos',
            'ordem': 4,
            'duracao': 30,
            'conteudo': '''
<div class="aula-container">
    <h1>Procedimento de Coleta Biométrica</h1>
    
    <h2>Preparação</h2>
    <ul class="checklist">
        <li><input type="checkbox"> Verificar se todos os equipamentos estão calibrados</li>
        <li><input type="checkbox"> Confirmar identidade da criança e responsável</li>
        <li><input type="checkbox"> Obter consentimento informado assinado</li>
        <li><input type="checkbox"> Explicar o procedimento  criança de forma amigvel</li>
        <li><input type="checkbox"> Garantir ambiente confortável e bem iluminado</li>
    </ul>
    
    <h2>Fase 1: Coleta de Impressões Digitais (5 min)</h2>
    <div class="passo">
        <h3>Passo 1: Posicionamento</h3>
        <p>Coloque a mo da criança não scanner com dedo indicador primeiro.</p>
        <p><strong>Dica:</strong> Se a criança estiver nervosa, deixe explorar o equipamento antes.</p>
    </div>
    
    <div class="passo">
        <h3>Passo 2: Captura</h3>
        <p>Pressione suavemente por 2-3 segundos. Sistema confirma com beep sonoro.</p>
        <p><strong>Alerta:</strong> Não pressione com fora excessiva!</p>
    </div>
    
    <div class="passo">
        <h3>Passo 3: Validação</h3>
        <p>Sistema exibe qualidade da captura (verde = OK, vermelho = repetir).</p>
    </div>
    
    <h2>Fase 2: Captura de Foto Facial (3 min)</h2>
    <div class="passo">
        <h3>Passo 1: Posicionamento</h3>
        <p>Posicione a criança a 45cm da câmera. Olhos alinhados com linha central.</p>
    </div>
    
    <div class="passo">
        <h3>Passo 2: Captura</h3>
        <p>Sistema captura automaticamente quando detecta rosto frontal com boa iluminação.</p>
    </div>
    
    <div class="passo">
        <h3>Passo 3: Validação</h3>
        <p>Verificar se olhos e boca estão abertos e rosto est claro.</p>
    </div>
    
    <h2>Fase 3: Leitura de Íris (2 min)</h2>
    <div class="passo">
        <h3>Passo 1: Orientação</h3>
        <p>"Olhe para o ponto de luz vermelho  sua frente"</p>
    </div>
    
    <div class="passo">
        <h3>Passo 2: Captura</h3>
        <p>Sistema captura quando detecta Íris com padrões visíveis.</p>
        <p><strong>Importante:</strong> Capturar ambos os olhos (esquerdo + direito)</p>
    </div>
    
    <h2>Fase 4: Gravao de Voz (1 min)</h2>
    <div class="passo">
        <h3>Instruções</h3>
        <p>Peça  criança que diga a frase fornecida pelo sistema (ex: "Meu nome ...")</p>
    </div>
    
    <h2>Finalização</h2>
    <ul>
        <li>Sistema processa e gera ID biométrico único</li>
        <li>Imprimir recibo de coleta</li>
        <li>Solicitar assinatura do responsável</li>
        <li>Registrar observações especiais (cicatrizes, etc)</li>
        <li>Entregar cpia ao responsável</li>
    </ul>
    
    <div class="aviso">
        <strong>Importante:</strong> Se qualquer coleta falhar mais de 3 vezes, pausar e tentar outro dia.
    </div>
</div>
            '''
        },
        {
            'titulo': 'Segurança e Conformidade LGPD',
            'descricao': 'Entenda as garantias de segurança e cumprimento regulatrio',
            'ordem': 5,
            'duracao': 20,
            'conteudo': '''
<div class="aula-container">
    <h1>Segurança e Conformidade LGPD</h1>
    
    <h2>Criptografia de Dados</h2>
    <p>Todos os dados biométricos so criptografados em múltiplas camadas:</p>
    <ul>
        <li><strong>Em Trânsito:</strong> TLS 1.3 (256-bit)</li>
        <li><strong>Em Repouso:</strong> AES-256 (militar grade)</li>
        <li><strong>Hash Biométrico:</strong> SHA-3 + salting aleatrio</li>
        <li><strong>Backup:</strong> Replicado em datacenters SEC-3</li>
    </ul>
    
    <h2>Conformidade LGPD</h2>
    <p>INFANT.ID opera em total conformidade com a Lei Geral de Proteo de Dados:</p>
    <table class="tabela-conformidade">
        <tr>
            <th>Artigo LGPD</th>
            <th>Requisito</th>
            <th>Implementao INFANT.ID</th>
        </tr>
        <tr>
            <td>Art. 5</td>
            <td>Consentimento</td>
            <td>Formulrio de consentimento digital assinado</td>
        </tr>
        <tr>
            <td>Art. 7</td>
            <td>Base Legal</td>
            <td>Consentimento + exerccio direitos</td>
        </tr>
        <tr>
            <td>Art. 13</td>
            <td>Transparncia</td>
            <td>Poltica clara disponvel não sistema</td>
        </tr>
        <tr>
            <td>Art. 30</td>
            <td>Direito de Acesso</td>
            <td>Portal do responsável com dados digitalizados</td>
        </tr>
        <tr>
            <td>Art. 35</td>
            <td>DIA - Direito de Esquecimento</td>
            <td>Erasure automtico ou sob demanda</td>
        </tr>
    </table>
    
    <h2>Direitos do Titular (Criança)</h2>
    <ul>
        <li><strong>Acesso:</strong> Responsável pode solicitar dados coletados</li>
        <li><strong>Retificao:</strong> Corrigir dados imprecisos</li>
        <li><strong>Excluso:</strong> Solicitar apagamento permanente</li>
        <li><strong>Portabilidade:</strong> Transferir dados para outro sistema</li>
        <li><strong>Oposio:</strong> Recusar processamento por motivo legtimo</li>
    </ul>
    
    <h2>Reteno de Dados</h2>
    <p>Poltica de reteno conforme regulamentaes:</p>
    <ul>
        <li><strong>Dados Ativas (0-7 anos):</strong> Mantidos para identificação</li>
        <li><strong>Dados Inativas (7-10 anos):</strong> Arquivado, sem acesso regular</li>
        <li><strong>Dados Arquivados (>10 anos):</strong> Apagamento automtico</li>
        <li><strong>Exceo:</strong> Se requerer investigao legal, retm conforme necessrio</li>
    </ul>
    
    <h2>Incidente de Segurança</h2>
    <p>Em caso de violao de dados:</p>
    <ol>
        <li>Notificar responsável em até 48 horas</li>
        <li>Informar autoridade de proteo de dados</li>
        <li>Fornecer medidas de mitigao</li>
        <li>Auditoria completa para causa raiz</li>
    </ol>
</div>
            '''
        },
        {
            'titulo': 'Troubleshooting e Melhores Práticas',
            'descricao': 'Solucione problemas comuns e aprenda as melhores práticas',
            'ordem': 6,
            'duracao': 15,
            'conteudo': '''
<div class="aula-container">
    <h1>Troubleshooting e Melhores Práticas</h1>
    
    <h2>Problemas Comuns</h2>
    
    <h3>Problema: Dgito não reconhecido</h3>
    <p><strong>Causa:</strong> Dedo muito seco, sujo ou com ferimento</p>
    <p><strong>Soluo:</strong></p>
    <ul>
        <li>Hidratar a ponta do dedo com loo neutra</li>
        <li>Limpar dedo em pano mido branco</li>
        <li>Se h ferimento, tentar outro dedo</li>
        <li>Ajustar presso levemente</li>
    </ul>
    
    <h3>Problema: Foto facial borrada</h3>
    <p><strong>Causa:</strong> Movimento da cabea, luz insuficiente ou muito brilho</p>
    <p><strong>Soluo:</strong></p>
    <ul>
        <li>Reduzir brilho incidindo luz lateralmente</li>
        <li>Pedir  criança para ficar imvel</li>
        <li>Aproximar ou afastar adequadamente</li>
        <li>Limpar lente com pano estril</li>
    </ul>
    
    <h3>Problema: Íris não detectada</h3>
    <p><strong>Causa:</strong> Criança com olhos muito fechados ou reflexos muito altos</p>
    <p><strong>Soluo:</strong></p>
    <ul>
        <li>Ajustar ngulo da câmera</li>
        <li>Aumentar iluminação ambiente</li>
        <li>Deixar criança piscar e tentar novamente</li>
        <li>Se uso de culos, remover para captura</li>
    </ul>
    
    <h2>Melhores Práticas</h2>
    
    <h3>Antes da Coleta</h3>
    <ul class="checkmark">
        <li>Testar todos equipamentos não incio do dia</li>
        <li>Revisar lista contatos de emergncia</li>
        <li>Preparar formulrios de consentimento</li>
        <li>Criar ambiente amigvel e ldico</li>
    </ul>
    
    <h3>Durante a Coleta</h3>
    <ul class="checkmark">
        <li>Ser paciente e calmo com criança nervosa</li>
        <li>Explicar cada passo em linguagem infantil</li>
        <li>Dar feedback positivo ("Muito bem!")"></li>
        <li>Manter temperatura ambiente confortável</li>
        <li>Ter pais/responsáveis próximos para conforto</li>
    </ul>
    
    <h3>Aps a Coleta</h3>
    <ul class="checkmark">
        <li>Revisar qualidade de todos os dados capturados</li>
        <li>Documentar qualquer situao anormal</li>
        <li>Fazer upload seguro ao sistema aps reviso</li>
        <li>Arquivar documentao assinada</li>
        <li>Fazer backup de dados crticos</li>
    </ul>
    
    <h2>Dicas de Ouro</h2>
    <p><strong> Para crianças muito pequenas (0-3 anos):</strong> Coletar quando dormindo ou imediatamente aps alimentao.</p>
    <p><strong> Para crianças nervosas:</strong> Permitir brincar com equipamento antes, ganhar confiança.</p>
    <p><strong> Para crianças com deficincia:</strong> Adaptar protocolo conforme necessidade individual.</p>
    <p><strong> Dica Geral:</strong> Qualidade > Velocidade. Uma coleta boa vale mais que 10 ruins.</p>
</div>
            '''
        }
    ]

def get_curso_2_aulas():
    """Aulas para: Integração Hospitalar"""
    return [
        {
            'titulo': 'Architectura de Integração',
            'descricao': 'Entenda a arquitetura tcnica da integração com sistemas hospitalares',
            'ordem': 1,
            'duracao': 25,
            'conteudo': '''
<div class="aula-container">
    <h1>Arquitetura de Integração INFANT.ID</h1>
    
    <h2>Viso Geral</h2>
    <p>O INFANT.ID foi projetado para integrar-se perfeitamente a sistemas hospitalares existentes, permitindo 
    adicionar biometria infantil sem interromper operaes.</p>
    
    <h2>Componentes Principais</h2>
    <img src="https://via.placeholder.com/800x400?text=Arquitetura%20INFANT.ID" alt="Arquitetura" class="img-large">
    
    <h3>1. INFANT.ID Core</h3>
    <ul>
        <li>Engine de processamento biométrico</li>
        <li>Banco de dados seguro com criptografia</li>
        <li>API RESTful para integração</li>
        <li>Dashboard administrativo</li>
    </ul>
    
    <h3>2. Hospital Information System (HIS)</h3>
    <ul>
        <li>Sua plataforma hospitalar existente</li>
        <li>INFANT.ID se integra via API-bridge</li>
        <li>Sem modificaes não seu cdigo core</li>
    </ul>
    
    <h3>3. Integração Middleware</h3>
    <ul>
        <li>Traduz dados entre sistemas</li>
        <li>Sincroniza pacientes automaticamente</li>
        <li>Gerencia filas de processamento</li>
        <li>Logs e auditoria completa</li>
    </ul>
    
    <h2>Fluxo de Integração</h2>
    <div class="fluxo">
        <div class="passo-fluxo">1. Paciente chega ao hospital</div>
        <div class="seta"></div>
        <div class="passo-fluxo">2. HIS cria registro</div>
        <div class="seta"></div>
        <div class="passo-fluxo">3. INFANT.ID coleta biometria</div>
        <div class="seta"></div>
        <div class="passo-fluxo">4. Dados sincronizados</div>
        <div class="seta"></div>
        <div class="passo-fluxo">5. ID único gerado</div>
    </div>
    
    <h2>Protocolo HTTP/REST</h2>
    <pre><code>
POST /api/v1/pacientes
{
  "nome": "Joo Silva",
  "data_nascimento": "2020-05-15",
  "responsavel": "Maria Silva",
  "hospital_id": 123
}

Response 201:
{
  "id": 456,
  "infant_id": "INF-2026-001234567",
  "status": "aguardando_biometria"
}
    </code></pre>
    
    <h2>Segurança na Integração</h2>
    <ul>
        <li><strong>API Keys:</strong> Autenticao via tokens JWT com 24h validade</li>
        <li><strong>Encriptao:</strong> TLS 1.3 para todas as requisies</li>
        <li><strong>Validação:</strong> Assinatura digital (HMAC-SHA256) em cada payload</li>
        <li><strong>Auditoria:</strong> Log completo em blockchain-style para rastreabilidade</li>
    </ul>
</div>
            '''
        },
        {
            'titulo': 'Implementao Tcnica',
            'descricao': 'Como implementar a integração não seu HIS',
            'ordem': 2,
            'duracao': 30,
            'conteudo': '''
<div class="aula-container">
    <h1>Guia de Implementao Tcnica</h1>
    
    <h2>Pr-requisitos</h2>
    <ul>
        <li>Node.js 16+ ou Python 3.8+</li>
        <li>Acesso ao banco de dados do HIS</li>
        <li>INFANT.ID API credentials (fornecidas)</li>
        <li>Certificado SSL vlido</li>
    </ul>
    
    <h2>Instalao do Cliente SDK</h2>
    <h3>Python</h3>
    <pre><code>pip install infantid-sdk==2.1.0</code></pre>
    
    <h3>Node.js</h3>
    <pre><code>npm install @infantid/sdk</code></pre>
    
    <h2>Exemplo de Integração - Python</h2>
    <pre><code>
from infantid import InfantIDClient

# Inicializar
client = InfantIDClient(
    api_key="seu_api_key_aqui",
    api_secret="seu_secret_aqui",
    environment="production"
)

# Registrar novo paciente
paciente = client.pacientes.crear({
    'nome': 'Joo Silva',
    'data_nascimento': '2020-05-15',
    'hospital_id': 123
})

print(f"ID único: {paciente['infant_id']}")

# Sincronizar com HIS
def sync_to_his(infant_id, his_patient_id):
    # Mapear IDs
    client.mapping.criar({
        'infant_id': infant_id,
        'sistema_externo_id': his_patient_id,
        'sistema': 'seu_his_name'
    })
    </code></pre>
    
    <h2>Exemplo de Integração - Node.js</h2>
    <pre><code>
const { InfantID } = require('@infantid/sdk');

const client = new InfantID({
  apiKey: process.env.INFANTID_API_KEY,
  apiSecret: process.env.INFANTID_SECRET
});

// Registrar paciente
async function registerPatient() {
  const response = await client.patients.create({
    name: 'Maria Santos',
    birthDate: '2019-03-20',
    hospitalId: 123
  });
  
  console.log(`ID criado: ${response.infantId}`);
  return response;
}

registerPatient().catch(console.error);
    </code></pre>
    
    <h2>Mapeamento de Dados</h2>
    <p>INFANT.ID oferece mapeamento automtico para campos comuns:</p>
    <table class="tabela-mapeamento">
        <tr>
            <th>INFANT.ID</th>
            <th>HL7 (Padrão Hospitalar)</th>
            <th>FHIR</th>
        </tr>
        <tr>
            <td>infant_id</td>
            <td>CX.1</td>
            <td>Patient.identifier.value</td>
        </tr>
        <tr>
            <td>nome</td>
            <td>XPN.1</td>
            <td>Patient.name.text</td>
        </tr>
        <tr>
            <td>data_nascimento</td>
            <td>TS.1</td>
            <td>Patient.birthDate</td>
        </tr>
    </table>
    
    <h2>Testes de Integração</h2>
    <pre><code>
# Testar conexo
GET /api/v1/health

# Listar pacientes integrados
GET /api/v1/pacientes?hospital_id=123

# Validar mapeamento
GET /api/v1/mapping/validate/{infant_id}
    </code></pre>
</div>
            '''
        },
        {
            'titulo': 'Workflow Clnico com INFANT.ID',
            'descricao': 'Entenda o fluxo clnico com integração biométrica',
            'ordem': 3,
            'duracao': 20,
            'conteudo': '''
<div class="aula-container">
    <h1>Workflow Clnico Integrado</h1>
    
    <h2>Entrada do Paciente</h2>
    <div class="fluxo-clinico">
        <div class="etapa">
            <h3>1. Recepo</h3>
            <p> Responsável chega com criança</p>
            <p> Funcionrio cria registro não HIS</p>
            <p> Sistema notifica INFANT.ID automaticamente</p>
        </div>
        
        <div class="etapa">
            <h3>2. Coleta Biométrica</h3>
            <p> QR code gerado com dados do paciente</p>
            <p> Tcnico escaneia e coleta biometria</p>
            <p> ID único vinculado automaticamente ao HIS</p>
        </div>
        
        <div class="etapa">
            <h3>3. Processamento Clnico</h3>
            <p> Mdico acessa registro com identidade verificada</p>
            <p> Histrico biométrico disponvel</p>
            <p> Alertas para duplicatas reduzem erros</p>
        </div>
        
        <div class="etapa">
            <h3>4. Alta</h3>
            <p> Registro completo não INFANT.ID e HIS</p>
            <p> Dados biométricos arquivados com segurança LGPD</p>
            <p> Certificado de coleta disponvel</p>
        </div>
    </div>
    
    <h2>Casos de Uso Prticos</h2>
    
    <h3>Caso 1: Beb Prematuro</h3>
    <p><strong>Cenrio:</strong> Criança de 2 kg internada em UTI neonatal</p>
    <p><strong>Soluo INFANT.ID:</strong></p>
    <ul>
        <li>Coleta suave de Íris e voz</li>
        <li>Dados armazenados para conferncia posterior</li>
        <li>Quando criança tiver peso adequado, coleta digital completa</li>
        <li>Biometria multi-modal garante 99.99% de acurcia</li>
    </ul>
    
    <h3>Caso 2: Criança com Deficincia</h3>
    <p><strong>Cenrio:</strong> Criança com sndrome gentica que afeta padro digital</p>
    <p><strong>Soluo INFANT.ID:</strong></p>
    <ul>
        <li>Sistema oferece múltiplas modalidades</li>
        <li>Se digital inadequada, usa Íris + facial + voz</li>
        <li>Certificação de igualdade de direitos e acessibilidade</li>
    </ul>
    
    <h3>Caso 3: Mltiplas Admisses</h3>
    <p><strong>Cenrio:</strong> Criança que frequenta diferentes hospitais</p>
    <p><strong>Soluo INFANT.ID:</strong></p>
    <ul>
        <li>Registro único nacional vinculado</li>
        <li>Histrico mdico completo acessvel</li>
        <li>Reduz testes duplicados e custos</li>
    </ul>
    
    <h2>Relatrios de Conformidade</h2>
    <p>INFANT.ID gera relatrios automticos para:</p>
    <ul>
        <li><strong>Acreditao:</strong> JCI, AABB, CNAS</li>
        <li><strong>Regulamentao:</strong> ANVISA, CFM, COREN</li>
        <li><strong>Segurança:</strong> ISO/IEC 27001, NIST</li>
        <li><strong>Dados:</strong> LGPD, NIST Privacy Framework</li>
    </ul>
</div>
            '''
        },
        {
            'titulo': 'Troubleshooting de Integração',
            'descricao': 'Resolva problemas mais comuns de integração',
            'ordem': 4,
            'duracao': 15,
            'conteudo': '''
<div class="aula-container">
    <h1>Troubleshooting de Integração</h1>
    
    <h2>Problemas de Conexo</h2>
    
    <h3> Erro: "Connection Refused"</h3>
    <p><strong>Diagnstico:</strong> INFANT.ID não alcanvel</p>
    <pre><code>
# Testar conectividade
curl -v https://api.infantid.com/v1/health

# Verificar DNS
nslookup api.infantid.com

# Verificar firewall
telnet api.infantid.com 443
    </code></pre>
    
    <divclass="solucao">
        <strong>Soluo:</strong> Verificar firewall corporativo, VPN, ou endereo IP da API
    </div>
    
    <h3> Erro: "Unauthorized - Invalid API Key"</h3>
    <p><strong>Diagnstico:</strong> Credenciais incorretas ou expiradas</p>
    <p><strong>Soluo:</strong></p>
    <ul>
        <li>Verificar variveis de ambiente ($INFANTID_API_KEY)</li>
        <li>Confirmar formato: "INFANTID-XXX"</li>
        <li>Se expirada, solicitar nova chave não admin portal</li>
        <li>Testar com cURL primeiro antes de cdigo</li>
    </ul>
    
    <h3> Erro: "Rate Limited - Too Many Requests"</h3>
    <p><strong>Diagnstico:</strong> Excedeu limite de chamadas</p>
    <p><strong>Limite padro:</strong> 1000 req/min por API key</p>
    <p><strong>Soluo:</strong></p>
    <ul>
        <li>Implementar backoff exponencial (espera progressiva)</li>
        <li>Usar batch endpoints para múltiplas operaes</li>
        <li>Solicitar upgrade do plano se necessrio</li>
    </ul>
    
    <h2>Problemas de Dados</h2>
    
    <h3> Erro: "Duplicate Patient"</h3>
    <p><strong>Diagnstico:</strong> Mesmo paciente registrado 2x</p>
    <p><strong>Soluo:</strong></p>
    <ul>
        <li>INFANT.ID detecta automaticamente duplicatas via biometria</li>
        <li>Admin pode mesclar registros manualmente</li>
        <li>Implementar verificação não HIS antes de criar novo registro</li>
    </ul>
    
    <h3> Erro: "Invalid Date Format"</h3>
    <p><strong>Diagnstico:</strong> Data em formato incorreto</p>
    <p><strong>Formato aceito:</strong> YYYY-MM-DD (ISO 8601)</p>
    <pre><code>
# Errado
{ "data_nascimento": "15/05/2020" }

# Certo
{ "data_nascimento": "2020-05-15" }
    </code></pre>
    
    <h2>Logs e Monitoramento</h2>
    <p>Ativar logs detalhados para debugging:</p>
    <pre><code>
# Python
import logging
logging.basicConfig(level=logging.DEBUG)

# Node.js
const client = new InfantID({
  debug: true
});
    </code></pre>
    
    <p><strong>Verificar logs em:</strong> Admin Portal  Logs  Filtrar por hospital_id/timestamp</p>
</div>
            '''
        }
    ]

def get_curso_3_aulas():
    """Aulas para: Gerenciamento de Usurios"""
    return [
        {
            'titulo': 'Controle de Acesso e Permisses',
            'descricao': 'Como gerenciar usurios e suas permisses',
            'ordem': 1,
            'duracao': 20,
            'conteudo': '''
<div class="aula-container">
    <h1>Controle de Acesso e Permisses</h1>
    
    <h2>Modelos de Acesso</h2>
    
    <h3>Role-Based Access Control (RBAC)</h3>
    <p>Sistema de permisses baseado em papis pr-definidos.</p>
    
    <table class="tabela-roles">
        <tr>
            <th>Funo</th>
            <th>Permisses</th>
            <th>Acesso a Dados</th>
        </tr>
        <tr>
            <td><strong>Administrador</strong></td>
            <td>Criar, modificar, deletar usurios, relatrios, configuraes</td>
            <td>Todos os pacientes do hospital</td>
        </tr>
        <tr>
            <td><strong>Mdico</strong></td>
            <td>Ver pronturio, solicitar coleta, prescrever</td>
            <td>Seus pacientes atribudos</td>
        </tr>
        <tr>
            <td><strong>Tcnico Biometria</strong></td>
            <td>Coletar dados, validar qualidade</td>
            <td>Pacientes agendados para coleta</td>
        </tr>
        <tr>
            <td><strong>Recepcionista</strong></td>
            <td>Agendar coleta, registrar chegada</td>
            <td>Calendrio de agendamentos</td>
        </tr>
        <tr>
            <td><strong>Auditor</strong></td>
            <td>Visualizar logs, gerar relatrios</td>
            <td>Todos os logs (sem dados sensveis)</td>
        </tr>
    </table>
    
    <h2>Implementao Tcnica</h2>
    <pre><code>
# Criar novo usurio com role
POST /api/v1/users
{
  "email": "medico@hospital.com.br",
  "nome": "Dr. Silva",
  "role": "medico",
  "hospital_id": 123
}

# Response
{
  "id": 456,
  "email": "medico@hospital.com.br",
  "role": "medico",
  "created_at": "2026-02-20",
  "status": "ativo"
}
    </code></pre>
    
    <h2>Princípios de Segurança</h2>
    <ul>
        <li><strong>Least Privilege:</strong> Cada usurio s acessa o necessrio</li>
        <li><strong>Separao de Deveres:</strong> Tcnico não pode ver dados médicos</li>
        <li><strong>Auditoria Completa:</strong> Toda ao  registrada com quem fez quando</li>
        <li><strong>Revogao Rpida:</strong> Desativar usurio remove acesso imediatamente</li>
    </ul>
</div>
            '''
        },
        {
            'titulo': 'Gerenciamento de Lojistas e Hospitais',
            'descricao': 'Configure mltiplos hospitais e lojistas',
            'ordem': 2,
            'duracao': 25,
            'conteudo': '''
<div class="aula-container">
    <h1>Gerenciamento Multi-Institucional</h1>
    
    <h2>Modelo Multi-Tenant</h2>
    <p>INFANT.ID suporta mltiplos hospitais/clnicas em uma nica plataforma,com dados isolados.</p>
    
    <h3>Hierarquia Organizacional</h3>
    <pre><code>
Rede INFANT.ID
 Grupo Hospitalar A
     Hospital A1 (So Paulo)
        Ala Peditrica
           Medico 1
           Tecnico 1
        UTI Neonatal
            Medico 2
            Tecnico 2
     Hospital A2 (Rio de Janeiro)
         Medico 3
         Tecnico 3
</code></pre>
    
    <h2>Onboarding de Novo Hospital</h2>
    <ol>
        <li>Admin cria conta do hospital
        <li>Selecionador endpoint de login dedicado
        <li>Importar usurios via CSV ou LDAP
        <li>Configurar permisses padro
        <li>Testar com dados fictcios
        <li>Ativar produo
    </ol>
    
    <h3>Checklist de Ativao</h3>
    <ul class="checklist">
        <li><input type="checkbox"> Equipamentos calibrados e testados</li>
        <li><input type="checkbox"> Todos os usurios criados e treinados</li>
        <li><input type="checkbox"> Integração HIS validada</li>
        <li><input type="checkbox"> Backup e recuperao testados</li>
        <li><input type="checkbox"> LGPD e conformidade verificados</li>
        <li><input type="checkbox"> Go-live authorized</li>
    </ul>
    
    <h2>Controle de Custos</h2>
    <p>Rastrear uso por hospital:</p>
    <ul>
        <li>Nmero de coletas realizadas</li>
        <li>Armazenamento utilizado</li>
        <li>APIs chamadas</li>
        <li>Usurios ativos</li>
    </ul>
    
    <p>Dashboard de custos mostra projeo mensal.</p>
</div>
            '''
        },
        {
            'titulo': 'Auditoria e Compliance',
            'descricao': 'Rastreie aes e cumpra com regulamentaes',
            'ordem': 3,
            'duracao': 20,
            'conteudo': '''
<div class="aula-container">
    <h1>Auditoria e Compliance</h1>
    
    <h2>Sistema de Auditoria</h2>
    <p>Cada ao  registrada imutavelmente:</p>
    
    <table class="tabela-auditoria">
        <tr>
            <th>Ao</th>
            <th>Quem</th>
            <th>Quando</th>
            <th>Resultado</th>
        </tr>
        <tr>
            <td>Criar usurio</td>
            <td>admin@hospital.com</td>
            <td>2026-02-20 09:15:00</td>
            <td> Sucesso</td>
        </tr>
        <tr>
            <td>Coletar biometria</td>
            <td>tecnico@hospital.com</td>
            <td>2026-02-20 10:30:00</td>
            <td> Sucesso</td>
        </tr>
        <tr>
            <td>Acessar pronturio</td>
            <td>medico@hospital.com</td>
            <td>2026-02-20 14:45:00</td>
            <td> Sucesso</td>
        </tr>
        <tr>
            <td>Tentar login com senha errada</td>
            <td>usuario_desconhecido</td>
            <td>2026-02-20 16:20:00</td>
            <td> Falha</td>
        </tr>
    </table>
    
    <h2>Alertas de Segurança</h2>
    <ul>
        <li>Mltiplas tentativas de login falhadas  Bloqueia temporariamente</li>
        <li>Acesso de IP incomum  Notificao por email</li>
        <li>Operao em horrio fora do normal  Alerta</li>
        <li>Deleo em massa de dados  Requer autorizao</li>
    </ul>
    
    <h2>Relatrios de Conformidade</h2>
    <p>INFANT.ID gera relatrios prontos para auditores:</p>
    <ul>
        <li><strong>Relatrio LGPD:</strong> Acessos a dados pessoais</li>
        <li><strong>Relatrio de Segurança:</strong> Falhas de login, alertas</li>
        <li><strong>Relatrio Operacional:</strong> Coletas, processamentos, erros</li>
        <li><strong>Certificado de Conformidade:</strong> ISO, SOC2, NIST</li>
    </ul>
    
    <h3>Download de Relatrios</h3>
    <pre><code>
GET /api/v1/reports/compliance?format=pdf&month=2026-02
    </code></pre>
</div>
            '''
        }
    ]

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
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Vernix (substância branca)</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Cobre os dedos ao nascer</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Limpeza com solução ETAN antes</td>
        </tr>
    </table>
    
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
        <li><strong>Preparar Material</strong>
            <ul>
                <li>Solução ETAN (soro fisiológico + shampoo neutro infantil)</li>
                <li>Gaze estéril (múltiplas unidades)</li>
                <li>Scanner ETAN (conectado e funcionando)</li>
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
                <li>Use movimento suave (não esfregue)</li>
            </ul>
        </li>
        <li><strong>Enxugue com Gaze Estéril</strong>
            <ul>
                <li>Gaze SECA (não úmida)</li>
                <li>Seque completamente cada dedo</li>
            </ul>
        </li>
    </ol>
    
    <h2>FASE 3-5: Captura do Bebê E Verificação</h2>
    <p>Colete 10 dedos seguindo a ordem correta, aguarde acalmia se necessário, e verifique qualidade final.</p>
    
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
    
    <h3>Protocolo Modificado:</h3>
    <ol>
        <li><strong>Verificação Clínica EXTRA:</strong>
            <ul>
                <li>Confirme com médico/enfermeiro antes de coletar</li>
                <li>Verificar suporte respiratório</li>
            </ul>
        </li>
        <li><strong>Dedos são EXTREMAMENTE Frágeis:</strong>
            <ul>
                <li>Pressão deve ser mínima (praticamente nenhuma)</li>
                <li>Deixe scanner fazer 100% do trabalho</li>
            </ul>
        </li>
        <li><strong>Pode levar 15-20 minutos (mais longo = normal!)</strong></li>
    </ol>
    
    <h2>CASO 2: BEBÊ COM VERNIX ESPESSO</h2>
    <p><strong>O que é:</strong> Substância branca que cobre RN ao nascer</p>
    
    <h3>Solução:</h3>
    <ol>
        <li><strong>Primera Limpeza:</strong>
            <ul>
                <li>Use solução ETAN</li>
                <li>Pode levar 2-3 minutos por mão</li>
            </ul>
        </li>
        <li><strong>Persistência é chave:</strong>
            <ul>
                <li>99% dos casos se resolvem com paciência</li>
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
                <li>RN chorando = qualidade ruim</li>
            </ul>
        </li>
        <li><strong>PAUSA Imediata</strong>
            <ul>
                <li>Quando começar choro PARE</li>
                <li>Deixe progenitora confortar</li>
            </ul>
        </li>
        <li><strong>Máximo 2 pausas por sessão</strong></li>
    </ol>
    
    <h2>CASO 4-6: Dedos Secos, Úmidos, Grasping</h2>
    <p>Use técnicas de ajuste de umidade, espera de acalmia, e posicionamento suave para resolver.</p>
    
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
    
    <h2>PROBLEMA 1: Imagem Sempre Borrada</h2>
    
    <h3>Diagnóstico:</h3>
    <ul>
        <li>Imagem visualizada no scanner é pouco clara</li>
        <li>Sistema rejeita com mensagem de qualidade baixa</li>
    </ul>
    
    <h3>Causas (em ordem de probabilidade):</h3>
    <ol>
        <li><strong>MAIS COMUM (99%):</strong> Scanner não está limpo!
            <ul>
                <li>Restos de pele anterior acumulado</li>
            </ul>
        </li>
        <li><strong>Dedos do bebê sujos</strong>
            <ul>
                <li>Vernix não foi removido completamente</li>
            </ul>
        </li>
    </ol>
    
    <h3>Solução Passo a Passo:</h3>
    <ol>
        <li><strong>LIMPE O SCANNER!</strong>
            <ul>
                <li>Pegue gaze SECA</li>
                <li>Limpe a área de captura suavemente</li>
            </ul>
        </li>
        <li><strong>Repita captura</strong></li>
        <li><strong>Se ainda borrrado: Verifique dedos do bebê</strong></li>
    </ol>
    
    <h2>PROBLEMA 2: Sistema Diz "Impressão Rejeitada"</h2>
    
    <h3>O Que Fazer:</h3>
    <ol>
        <li><strong>Não Desista!</strong> Rejeição é normal às vezes</li>
        <li><strong>Siga Checklist:</strong>
            <ul>
                <li>Scanner limpo? ✓</li>
                <li>Dedo bem posicionado? ✓</li>
                <li>Umidade OK? ✓</li>
            </ul>
        </li>
        <li><strong>Tente Novamente</strong></li>
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
    </table>
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
    <p>É fácil pensar: "Preciso ser rápido!" Mas PARE e pense: Uma coleta de má qualidade gera problemas futuros MUITO maiores.</p>
    
    <h2>Impacto de Qualidade Ruim</h2>
    
    <h3>Em Curto Prazo (Hoje):</h3>
    <ul>
        <li>❌ Sistema não reconhece impressão</li>
        <li>❌ Documento não pode ser emitido</li>
        <li>❌ Bebê coleta NOVAMENTE (trauma desnecessário)</li>
    </ul>
    
    <h3>Em Longo Prazo (Futuro):</h3>
    <ul>
        <li>❌ ID biométrico fraco = problemas de verificação</li>
        <li>❌ Segurança comprometida</li>
        <li>❌ Criança prejudicada documentalmente</li>
    </ul>
    
    <h2>Benefício de Fazer Certo</h2>
    
    <h3>Fazer coleta de QUALIDADE significa:</h3>
    <ul>
        <li>✅ Criança tem identidade civil segura PARA A VIDA</li>
        <li>✅ Documento emitido na primeira vez</li>
        <li>✅ Você ganha reputação de profissional competente</li>
    </ul>
    
    <h2>Golden Rules</h2>
    <ol>
        <li><strong>Uma coleta perfeita > 10 coletas ruins</strong></li>
        <li><strong>Qualidade no scanner > Velocidade</strong></li>
        <li><strong>Limpeza bem feita = 80% do sucesso</strong></li>
        <li><strong>RN calmo = coleta melhor</strong></li>
        <li><strong>Melhor esperar 30 seg do que refazer tudo</strong></li>
    </ol>
    
    <h2>Seu Poder Como Profissional</h2>
    
    <p>Você tem o PODER de:</p>
    <ul>
        <li>✅ Dar à criança uma identidade civil segura</li>
        <li>✅ Protegê-la contra tráfico infantil</li>
        <li>✅ Criar um documento que a acompanhará POR TODA a vida</li>
    </ul>
    
    <p><strong>Isso é muito maior que uma coleta biométrica rápida!</strong></p>
</div>
''',
        },
    ]

def main():
    """Executar populao de aulas"""
    app = create_app()
    
    with app.app_context():
        print_section(" POPULANDO AULAS COM CONTEDO PROFISSIONAL")
        
        # Curso 1
        print(f"{BLUE}Processando: Onboarding INFANT.ID - Módulo 1{RESET}")
        curso1 = Course.query.filter_by(titulo='Onboarding INFANT.ID - Módulo 1').first()
        if curso1:
            # Limpar aulas antigas
            Lesson.query.filter_by(curso_id=curso1.id).delete()
            db.session.commit()
            
            # Adicionar novas
            for aula_data in get_curso_1_aulas():
                aula = Lesson(
                    curso_id=curso1.id,
                    titulo=aula_data['titulo'],
                    descricao=aula_data['descricao'],
                    conteudo=aula_data['conteudo'],
                    ordem=aula_data['ordem'],
                    duracao=aula_data['duracao'],
                    video_url=aula_data.get('video_url'),
                    ativo=True
                )
                db.session.add(aula)
                print(f"  {GREEN}{RESET} {aula_data['titulo']}")
            
            db.session.commit()
            print(f"{GREEN} Curso 1 completo com 6 aulas{RESET}")
        else:
            print(f"{RED} Curso não encontrado{RESET}")
        
        # Curso 2
        print(f"\n{BLUE}Processando: Integração Hospitalar{RESET}")
        curso2 = Course.query.filter_by(titulo='Integração Hospitalar').first()
        if curso2:
            Lesson.query.filter_by(curso_id=curso2.id).delete()
            db.session.commit()
            
            for aula_data in get_curso_2_aulas():
                aula = Lesson(
                    curso_id=curso2.id,
                    titulo=aula_data['titulo'],
                    descricao=aula_data['descricao'],
                    conteudo=aula_data['conteudo'],
                    ordem=aula_data['ordem'],
                    duracao=aula_data['duracao'],
                    ativo=True
                )
                db.session.add(aula)
                print(f"  {GREEN}{RESET} {aula_data['titulo']}")
            
            db.session.commit()
            print(f"{GREEN} Curso 2 completo com 4 aulas{RESET}")
        else:
            print(f"{RED} Curso não encontrado{RESET}")
        
        # Curso 3
        print(f"\n{BLUE}Processando: Gerenciamento de Usurios{RESET}")
        curso3 = Course.query.filter_by(titulo='Gerenciamento de Usurios').first()
        if curso3:
            Lesson.query.filter_by(curso_id=curso3.id).delete()
            db.session.commit()
            
            for aula_data in get_curso_3_aulas():
                aula = Lesson(
                    curso_id=curso3.id,
                    titulo=aula_data['titulo'],
                    descricao=aula_data['descricao'],
                    conteudo=aula_data['conteudo'],
                    ordem=aula_data['ordem'],
                    duracao=aula_data['duracao'],
                    ativo=True
                )
                db.session.add(aula)
                print(f"  {GREEN}{RESET} {aula_data['titulo']}")
            
            db.session.commit()
            print(f"{GREEN} Curso 3 completo com 3 aulas{RESET}")
        else:
            print(f"{RED} Curso não encontrado{RESET}")
        
        # Curso 4 - NOVO CURSO
        print(f"\n{BLUE}Processando: Biometria Infantil - Protocolo ETAN Avançado{RESET}")
        curso4 = Course.query.filter_by(titulo='Biometria Infantil - Protocolo ETAN Avançado').first()
        if curso4:
            # Limpar aulas antigas
            Lesson.query.filter_by(curso_id=curso4.id).delete()
            db.session.commit()
            
            # Adicionar novas
            for aula_data in get_curso_4_aulas():
                aula = Lesson(
                    curso_id=curso4.id,
                    titulo=aula_data['titulo'],
                    descricao=aula_data['descricao'],
                    conteudo=aula_data['conteudo'],
                    ordem=aula_data['ordem'],
                    duracao=aula_data['duracao'],
                    video_url=aula_data.get('video_url'),
                    ativo=True
                )
                db.session.add(aula)
                print(f"  {GREEN}{RESET} {aula_data['titulo']}")
            
            db.session.commit()
            print(f"{GREEN} Curso 4 completo com 5 aulas{RESET}")
        else:
            print(f"{YELLOW} Curso 4 não encontrado - será criado automaticamente{RESET}")
            # Criar o curso se não existir
            novo_curso = Course(
                titulo='Biometria Infantil - Protocolo ETAN Avançado',
                descricao='Aprofunde seus conhecimentos em biometria infantil com foco no protocolo ETAN, casos especiais, troubleshooting e melhores práticas para coleta de alta qualidade em recém-nascidos.',
                tempo_estimado=130,
                nivel='avancado',
                autor='INFANT.ID Training Team',
                ativo=True
            )
            db.session.add(novo_curso)
            db.session.flush()
            
            for aula_data in get_curso_4_aulas():
                aula = Lesson(
                    curso_id=novo_curso.id,
                    titulo=aula_data['titulo'],
                    descricao=aula_data['descricao'],
                    conteudo=aula_data['conteudo'],
                    ordem=aula_data['ordem'],
                    duracao=aula_data['duracao'],
                    video_url=aula_data.get('video_url'),
                    ativo=True
                )
                db.session.add(aula)
                print(f"  {GREEN}{RESET} {aula_data['titulo']}")
            
            db.session.commit()
            print(f"{GREEN} Novo Curso 4 criado completo com 5 aulas{RESET}")
        
        # Resumo final
        print_section(" POPULAO CONCLUDA")
        total_cursos = Course.query.count()
        total_aulas = Lesson.query.count()
        
        print(f"{GREEN} Total de Cursos: {total_cursos}{RESET}")
        print(f"{GREEN} Total de Aulas: {total_aulas}{RESET}")
        print(f"\n{BLUE}Aulas disponveis por curso:{RESET}")
        
        for curso in Course.query.all():
            aulas = Lesson.query.filter_by(curso_id=curso.id).count()
            print(f"   {curso.titulo}: {aulas} aulas")
        
print(f"{GREEN} Plataforma agora est COMPLETA!{RESET}")

if __name__ == '__main__':
    main()
