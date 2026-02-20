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
    """Aulas para: Onboarding INFANT.ID - Mdulo 1"""
    return [
        {
            'titulo': 'Bem-vindo ao INFANT.ID',
            'descricao': 'Apresentao do sistema e seus objetivos',
            'ordem': 1,
            'duracao': 15,
            'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
            'conteudo': '''
<div class="aula-container">
    <h1>Bem-vindo ao Sistema INFANT.ID</h1>
    
    <div class="video-container">
        <iframe width="100%" height="400" src="https://www.youtube.com/embed/dQw4w9WgXcQ" 
                frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
    
    <h2>O que voc vai aprender neste mdulo</h2>
    <p>Bem-vindo ao INFANT.ID! Nesta primeira aula, voc conhecer o sistema de identificao biomtrica infantil mais avanado do Brasil.</p>
    
    <h3>Objetivos da Plataforma</h3>
    <ul>
        <li><strong>Segurana Mxima:</strong> Coleta biomtrica segura e LGPD-compliant</li>
        <li><strong>Eficincia:</strong> Reduz tempo de atendimento em hospitais</li>
        <li><strong>Confiabilidade:</strong> Identificao unvoca de pacientes peditricos</li>
        <li><strong>Integrao:</strong> Funciona com sistemas hospitalares existentes</li>
    </ul>
    
    <h3>Pblico-alvo</h3>
    <p>Este treinamento  voltado para:</p>
    <ul>
        <li>Profissionais de sade (mdicos, enfermeiros, tcnicos)</li>
        <li>Administradores de sistemas hospitalares</li>
        <li>Pessoal de TI responsvel pela integrao</li>
        <li>Gestores de qualidade em sade</li>
    </ul>
    
    <h3>Durao Total do Mdulo</h3>
    <p><strong>2 horas</strong> divididas em 6 aulas prticas</p>
    
    <div class="destaque">
        <h4>Prximos Passos</h4>
        <p>Prossiga para a prxima aula: "Princpios de Biometria Infantil"</p>
    </div>
</div>
            '''
        },
        {
            'titulo': 'Princpios de Biometria Infantil',
            'descricao': 'Entenda como funciona a coleta de dados biomtricos em crianas',
            'ordem': 2,
            'duracao': 20,
            'conteudo': '''
<div class="aula-container">
    <h1>Fundamentos da Biometria Infantil</h1>
    
    <h2>O que  Biometria?</h2>
    <p>Biometria  a medio e anlise estatstica dos padres nicos de caractersticas fsicas e de comportamento. 
    No INFANT.ID, usamos mltiplas modalidades biomtricas para identificao infantil segura.</p>
    
    <h3>Modalidades Biomtricas Suportadas</h3>
    <table class="tabela-conteudo">
        <tr>
            <th>Modalidade</th>
            <th>Caractersticas</th>
            <th>Idade Mnima</th>
            <th>Confiabilidade</th>
        </tr>
        <tr>
            <td><strong>Impresso Digital</strong></td>
            <td>Padres nicos das cristas papilares</td>
            <td>6 meses</td>
            <td>99.9%</td>
        </tr>
        <tr>
            <td><strong>ris</strong></td>
            <td>Padro das estruturas da ris</td>
            <td>Nascimento</td>
            <td>99.99%</td>
        </tr>
        <tr>
            <td><strong>Foto Facial</strong></td>
            <td>Geometria e caractersticas faciais</td>
            <td>Nascimento</td>
            <td>98%</td>
        </tr>
        <tr>
            <td><strong>Voz</strong></td>
            <td>Padres acsticos da voz</td>
            <td>3 meses</td>
            <td>97%</td>
        </tr>
    </table>
    
    <h2>Por que Biometria Infantil?</h2>
    <ul>
        <li><strong>Imutvel:</strong> Diferente de documentos, no pode ser falsificada</li>
        <li><strong>Universal:</strong> Todos tm caractersticas biomtricas</li>
        <li><strong>Permanente:</strong> No muda ao longo da vida</li>
        <li><strong>Resistente:</strong> Funciona com variaes de apresentao</li>
    </ul>
    
    <h2>Especificidades da Coleta Infantil</h2>
    <p>A coleta em crianas requer protocolos especiais:</p>
    <ul>
        <li>Consentimento informado dos responsveis</li>
        <li>Equipamento adaptado para pequenas mos</li>
        <li>Ambiente acolhedor e seguro</li>
        <li>Procedimentos rpidos e indolores</li>
        <li>Cumprimento LGPD e resolues ticas</li>
    </ul>
    
    <div class="dica">
        <strong>Dica Importante:</strong> Sempre priorize o bem-estar da criana durante qualquer coleta biomtrica.
    </div>
</div>
            '''
        },
        {
            'titulo': 'Equipamentos e Sensores',
            'descricao': 'Conhea os equipamentos utilizados para coleta biomtrica',
            'ordem': 3,
            'duracao': 25,
            'conteudo': '''
<div class="aula-container">
    <h1>Equipamentos e Sensores do INFANT.ID</h1>
    
    <h2>Scanner de Impresso Digital</h2>
    <p>Captura os padres nicos das cristas papilares das digitais.</p>
    <ul>
        <li><strong>Tecnologia:</strong> Sensor ptico de alta resoluo (1000 DPI)</li>
        <li><strong>Tempo de captura:</strong> 2-3 segundos</li>
        <li><strong>Iluminao:</strong> LED verde para melhor contraste</li>
        <li><strong>Certificao:</strong> ISO/IEC 19794-2</li>
    </ul>
    
    <h2>Cmera Facial</h2>
    <p>Captura a geometria facial para identificao por reconhecimento facial.</p>
    <ul>
        <li><strong>Resoluo:</strong> 8MP, auto-foco</li>
        <li><strong>Distncia:</strong> 30-60cm (ideal para crianas)</li>
        <li><strong>Iluminao:</strong> Sistema IR para funcionar em qualquer condio</li>
        <li><strong>Certificao:</strong> ISO/IEC 39794-5</li>
    </ul>
    
    <h2>Leitor de ris</h2>
    <p>Tecnologia mais avanada de identificao biomtrica.</p>
    <ul>
        <li><strong>Alcance:</strong> 10-35cm (maior liberdade de movimento)</li>
        <li><strong>Anlise:</strong> 400+ pontos de caractersticas nicas</li>
        <li><strong>Velocidade:</strong> Menos de 1 segundo</li>
        <li><strong>Certificao:</strong> ISO/IEC 19794-6</li>
    </ul>
    
    <h2>Microfone Biomtrico</h2>
    <p>Coleta padres acsticos para verificao de voz.</p>
    <ul>
        <li><strong>Frequncia:</strong> 16-48 kHz</li>
        <li><strong>Rudo Ambiente:</strong> Cancelamento ativo at 65dB</li>
        <li><strong>Frase-senha:</strong> 3-5 palavras para mxima segurana</li>
        <li><strong>Certificao:</strong> ISO/IEC 19794-13</li>
    </ul>
    
    <h2>Protocolo de Validao</h2>
    <div class="protocolo">
        <ol>
            <li><strong>Captura:</strong> Obter dados biomtricos de qualidade</li>
            <li><strong>Pr-processamento:</strong> Normalizar e otimizar imagem</li>
            <li><strong>Extrao:</strong> Extrair caractersticas nicas</li>
            <li><strong>Comparao:</strong> Comparar com base de dados</li>
            <li><strong>Deciso:</strong> Gerar score de confiana</li>
        </ol>
    </div>
</div>
            '''
        },
        {
            'titulo': 'Protocolo de Coleta Passo a Passo',
            'descricao': 'Aprenda o protocolo exato para coletar dados biomtricos',
            'ordem': 4,
            'duracao': 30,
            'conteudo': '''
<div class="aula-container">
    <h1>Procedimento de Coleta Biomtrica</h1>
    
    <h2>Preparao</h2>
    <ul class="checklist">
        <li><input type="checkbox"> Verificar se todos os equipamentos esto calibrados</li>
        <li><input type="checkbox"> Confirmar identidade da criana e responsvel</li>
        <li><input type="checkbox"> Obter consentimento informado assinado</li>
        <li><input type="checkbox"> Explicar o procedure  criana de forma amigvel</li>
        <li><input type="checkbox"> Garantir ambiente confortvel e bem iluminado</li>
    </ul>
    
    <h2>Fase 1: Coleta de Impresses Digitais (5 min)</h2>
    <div class="passo">
        <h3>Passo 1: Posicionamento</h3>
        <p>Coloque a mo da criana no scanner com dedo indicador primeiro.</p>
        <p><strong>Dica:</strong> Se a criana estiver nervosa, deixe explorar o equipamento antes.</p>
    </div>
    
    <div class="passo">
        <h3>Passo 2: Captura</h3>
        <p>Pressione suavemente por 2-3 segundos. Sistema confirma com beep sonoro.</p>
        <p><strong>Alerta:</strong> No pressione com fora excessiva!</p>
    </div>
    
    <div class="passo">
        <h3>Passo 3: Validao</h3>
        <p>Sistema exibe qualidade da captura (verde = OK, vermelho = repetir).</p>
    </div>
    
    <h2>Fase 2: Captura de Foto Facial (3 min)</h2>
    <div class="passo">
        <h3>Passo 1: Posicionamento</h3>
        <p>Posicione a criana a 45cm da cmera. Olhos alinhados com linha central.</p>
    </div>
    
    <div class="passo">
        <h3>Passo 2: Captura</h3>
        <p>Sistema captura automaticamente quando detecta rosto frontal com boa iluminao.</p>
    </div>
    
    <div class="passo">
        <h3>Passo 3: Validao</h3>
        <p>Verificar se olhos e boca esto abertos e rosto est claro.</p>
    </div>
    
    <h2>Fase 3: Leitura de ris (2 min)</h2>
    <div class="passo">
        <h3>Passo 1: Orientao</h3>
        <p>"Olhe para o ponto de luz vermelho  sua frente"</p>
    </div>
    
    <div class="passo">
        <h3>Passo 2: Captura</h3>
        <p>Sistema captura quando detecta ris com padres visveis.</p>
        <p><strong>Importante:</strong> Capturar ambos os olhos (esquerdo + direito)</p>
    </div>
    
    <h2>Fase 4: Gravao de Voz (1 min)</h2>
    <div class="passo">
        <h3>Instrues</h3>
        <p>Pea  criana que diga a frase fornecida pelo sistema (ex: "Meu nome ...")</p>
    </div>
    
    <h2>Finalizao</h2>
    <ul>
        <li>Sistema processa e gera ID biomtrico nico</li>
        <li>Imprimir recibo de coleta</li>
        <li>Solicitar assinatura do responsvel</li>
        <li>Registrar observaes especiais (cicatrizes, etc)</li>
        <li>Entregar cpia ao responsvel</li>
    </ul>
    
    <div class="aviso">
        <strong>Importante:</strong> Se qualquer coleta falhar mais de 3 vezes, pausar e tentar outro dia.
    </div>
</div>
            '''
        },
        {
            'titulo': 'Segurana e Conformidade LGPD',
            'descricao': 'Entenda as garantias de segurana e cumprimento regulatrio',
            'ordem': 5,
            'duracao': 20,
            'conteudo': '''
<div class="aula-container">
    <h1>Segurana e Conformidade LGPD</h1>
    
    <h2>Criptografia de Dados</h2>
    <p>Todos os dados biomtricos so criptografados em mltiplas camadas:</p>
    <ul>
        <li><strong>Em Trnsito:</strong> TLS 1.3 (256-bit)</li>
        <li><strong>Em Repouso:</strong> AES-256 (militar grade)</li>
        <li><strong>Hash Biomtrico:</strong> SHA-3 + salting aleatrio</li>
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
            <td>Poltica clara disponvel no sistema</td>
        </tr>
        <tr>
            <td>Art. 30</td>
            <td>Direito de Acesso</td>
            <td>Portal do responsvel com dados digitalizados</td>
        </tr>
        <tr>
            <td>Art. 35</td>
            <td>DIA - Direito de Esquecimento</td>
            <td>Erasure automtico ou sob demanda</td>
        </tr>
    </table>
    
    <h2>Direitos do Titular (Criana)</h2>
    <ul>
        <li><strong>Acesso:</strong> Responsvel pode solicitar dados coletados</li>
        <li><strong>Retificao:</strong> Corrigir dados imprecisos</li>
        <li><strong>Excluso:</strong> Solicitar apagamento permanente</li>
        <li><strong>Portabilidade:</strong> Transferir dados para outro sistema</li>
        <li><strong>Oposio:</strong> Recusar processamento por motivo legtimo</li>
    </ul>
    
    <h2>Reteno de Dados</h2>
    <p>Poltica de reteno conforme regulamentaes:</p>
    <ul>
        <li><strong>Dados Ativas (0-7 anos):</strong> Mantidos para identificao</li>
        <li><strong>Dados Inativas (7-10 anos):</strong> Arquivado, sem acesso regular</li>
        <li><strong>Dados Arquivados (>10 anos):</strong> Apagamento automtico</li>
        <li><strong>Exceo:</strong> Se requerer investigao legal, retm conforme necessrio</li>
    </ul>
    
    <h2>Incidente de Segurana</h2>
    <p>Em caso de violao de dados:</p>
    <ol>
        <li>Notificar responsvel em at 48 horas</li>
        <li>Informar autoridade de proteo de dados</li>
        <li>Fornecer medidas de mitigao</li>
        <li>Auditoria completa para causa raiz</li>
    </ol>
</div>
            '''
        },
        {
            'titulo': 'Troubleshooting e Melhores Prticas',
            'descricao': 'Solucione problemas comuns e aprenda as melhores prticas',
            'ordem': 6,
            'duracao': 15,
            'conteudo': '''
<div class="aula-container">
    <h1>Troubleshooting e Melhores Prticas</h1>
    
    <h2>Problemas Comuns</h2>
    
    <h3>Problema: Dgito no reconhecido</h3>
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
        <li>Pedir  criana para ficar imvel</li>
        <li>Aproximar ou afastar adequadamente</li>
        <li>Limpar lente com pano estril</li>
    </ul>
    
    <h3>Problema: ris no detectada</h3>
    <p><strong>Causa:</strong> Criana com olhos muito fechados ou reflexos muito altos</p>
    <p><strong>Soluo:</strong></p>
    <ul>
        <li>Ajustar ngulo da cmera</li>
        <li>Aumentar iluminao ambiente</li>
        <li>Deixar criana piscar e tentar novamente</li>
        <li>Se uso de culos, remover para captura</li>
    </ul>
    
    <h2>Melhores Prticas</h2>
    
    <h3>Antes da Coleta</h3>
    <ul class="checkmark">
        <li>Testar todos equipamentos no incio do dia</li>
        <li>Revisar lista contatos de emergncia</li>
        <li>Preparar formulrios de consentimento</li>
        <li>Criar ambiente amigvel e ldico</li>
    </ul>
    
    <h3>Durante a Coleta</h3>
    <ul class="checkmark">
        <li>Ser paciente e calmo com criana nervosa</li>
        <li>Explicar cada passo em linguagem infantil</li>
        <li>Dar feedback positivo ("Muito bem!")"></li>
        <li>Manter temperatura ambiente confortvel</li>
        <li>Ter pais/responsveis prximos para conforto</li>
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
    <p><strong> Para crianas muito pequenas (0-3 anos):</strong> Coletar quando dormindo ou imediatamente aps alimentao.</p>
    <p><strong> Para crianas nervosas:</strong> Permitir brincar com equipamento antes, ganhar confiana.</p>
    <p><strong> Para crianas com deficincia:</strong> Adaptar protocolo conforme necessidade individual.</p>
    <p><strong> Dica Geral:</strong> Qualidade > Velocidade. Uma coleta boa vale mais que 10 ruins.</p>
</div>
            '''
        }
    ]

def get_curso_2_aulas():
    """Aulas para: Integrao Hospitalar"""
    return [
        {
            'titulo': 'Architectura de Integrao',
            'descricao': 'Entenda a arquitetura tcnica da integrao com sistemas hospitalares',
            'ordem': 1,
            'duracao': 25,
            'conteudo': '''
<div class="aula-container">
    <h1>Arquitetura de Integrao INFANT.ID</h1>
    
    <h2>Viso Geral</h2>
    <p>O INFANT.ID foi projetado para integrar-se perfeitamente a sistemas hospitalares existentes, permitindo 
    adicionar biometria infantil sem interromper operaes.</p>
    
    <h2>Componentes Principais</h2>
    <img src="https://via.placeholder.com/800x400?text=Arquitetura%20INFANT.ID" alt="Arquitetura" class="img-large">
    
    <h3>1. INFANT.ID Core</h3>
    <ul>
        <li>Engine de processamento biomtrico</li>
        <li>Banco de dados seguro com criptografia</li>
        <li>API RESTful para integrao</li>
        <li>Dashboard administrativo</li>
    </ul>
    
    <h3>2. Hospital Information System (HIS)</h3>
    <ul>
        <li>Sua plataforma hospitalar existente</li>
        <li>INFANT.ID se integra via API-bridge</li>
        <li>Sem modificaes no seu cdigo core</li>
    </ul>
    
    <h3>3. Integrao Middleware</h3>
    <ul>
        <li>Traduz dados entre sistemas</li>
        <li>Sincroniza pacientes automaticamente</li>
        <li>Gerencia filas de processamento</li>
        <li>Logs e auditoria completa</li>
    </ul>
    
    <h2>Fluxo de Integrao</h2>
    <div class="fluxo">
        <div class="passo-fluxo">1. Paciente chega ao hospital</div>
        <div class="seta"></div>
        <div class="passo-fluxo">2. HIS cria registro</div>
        <div class="seta"></div>
        <div class="passo-fluxo">3. INFANT.ID coleta biometria</div>
        <div class="seta"></div>
        <div class="passo-fluxo">4. Dados sincronizados</div>
        <div class="seta"></div>
        <div class="passo-fluxo">5. ID nico gerado</div>
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
    
    <h2>Segurana na Integrao</h2>
    <ul>
        <li><strong>API Keys:</strong> Autenticao via tokens JWT com 24h validade</li>
        <li><strong>Encriptao:</strong> TLS 1.3 para todas as requisies</li>
        <li><strong>Validao:</strong> Assinatura digital (HMAC-SHA256) em cada payload</li>
        <li><strong>Auditoria:</strong> Log completo em blockchain-style para rastreabilidade</li>
    </ul>
</div>
            '''
        },
        {
            'titulo': 'Implementao Tcnica',
            'descricao': 'Como implementar a integrao no seu HIS',
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
    
    <h2>Exemplo de Integrao - Python</h2>
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

print(f"ID nico: {paciente['infant_id']}")

# Sincronizar com HIS
def sync_to_his(infant_id, his_patient_id):
    # Mapear IDs
    client.mapping.criar({
        'infant_id': infant_id,
        'sistema_externo_id': his_patient_id,
        'sistema': 'seu_his_name'
    })
    </code></pre>
    
    <h2>Exemplo de Integrao - Node.js</h2>
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
            <th>HL7 (Padro Hospitalar)</th>
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
    
    <h2>Testes de Integrao</h2>
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
            'descricao': 'Entenda o fluxo clnico com integrao biomtrica',
            'ordem': 3,
            'duracao': 20,
            'conteudo': '''
<div class="aula-container">
    <h1>Workflow Clnico Integrado</h1>
    
    <h2>Entrada do Paciente</h2>
    <div class="fluxo-clinico">
        <div class="etapa">
            <h3>1. Recepo</h3>
            <p> Responsvel chega com criana</p>
            <p> Funcionrio cria registro no HIS</p>
            <p> Sistema notifica INFANT.ID automaticamente</p>
        </div>
        
        <div class="etapa">
            <h3>2. Coleta Biomtrica</h3>
            <p> QR code gerado com dados do paciente</p>
            <p> Tcnico escaneia e coleta biometria</p>
            <p> ID nico vinculado automaticamente ao HIS</p>
        </div>
        
        <div class="etapa">
            <h3>3. Processamento Clnico</h3>
            <p> Mdico acessa registro com identidade verificada</p>
            <p> Histrico biomtrico disponvel</p>
            <p> Alertas para duplicatas reduzem erros</p>
        </div>
        
        <div class="etapa">
            <h3>4. Alta</h3>
            <p> Registro completo no INFANT.ID e HIS</p>
            <p> Dados biomtricos arquivados com segurana LGPD</p>
            <p> Certificado de coleta disponvel</p>
        </div>
    </div>
    
    <h2>Casos de Uso Prticos</h2>
    
    <h3>Caso 1: Beb Prematuro</h3>
    <p><strong>Cenrio:</strong> Criana de 2 kg internada em UTI neonatal</p>
    <p><strong>Soluo INFANT.ID:</strong></p>
    <ul>
        <li>Coleta suave de ris e voz</li>
        <li>Dados armazenados para conferncia posterior</li>
        <li>Quando criana tiver peso adequado, coleta digital completa</li>
        <li>Biometria multi-modal garante 99.99% de acurcia</li>
    </ul>
    
    <h3>Caso 2: Criana com Deficincia</h3>
    <p><strong>Cenrio:</strong> Criana com sndrome gentica que afeta padro digital</p>
    <p><strong>Soluo INFANT.ID:</strong></p>
    <ul>
        <li>Sistema oferece mltiplas modalidades</li>
        <li>Se digital inadequada, usa ris + facial + voz</li>
        <li>Certificao de igualdade de direitos e acessibilidade</li>
    </ul>
    
    <h3>Caso 3: Mltiplas Admisses</h3>
    <p><strong>Cenrio:</strong> Criana que frequenta diferentes hospitais</p>
    <p><strong>Soluo INFANT.ID:</strong></p>
    <ul>
        <li>Registro nico nacional vinculado</li>
        <li>Histrico mdico completo acessvel</li>
        <li>Reduz testes duplicados e custos</li>
    </ul>
    
    <h2>Relatrios de Conformidade</h2>
    <p>INFANT.ID gera relatrios automticos para:</p>
    <ul>
        <li><strong>Acreditao:</strong> JCI, AABB, CNAS</li>
        <li><strong>Regulamentao:</strong> ANVISA, CFM, COREN</li>
        <li><strong>Segurana:</strong> ISO/IEC 27001, NIST</li>
        <li><strong>Dados:</strong> LGPD, NIST Privacy Framework</li>
    </ul>
</div>
            '''
        },
        {
            'titulo': 'Troubleshooting de Integrao',
            'descricao': 'Resolva problemas mais comuns de integrao',
            'ordem': 4,
            'duracao': 15,
            'conteudo': '''
<div class="aula-container">
    <h1>Troubleshooting de Integrao</h1>
    
    <h2>Problemas de Conexo</h2>
    
    <h3> Erro: "Connection Refused"</h3>
    <p><strong>Diagnstico:</strong> INFANT.ID no alcanvel</p>
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
        <li>Se expirada, solicitar nova chave no admin portal</li>
        <li>Testar com cURL primeiro antes de cdigo</li>
    </ul>
    
    <h3> Erro: "Rate Limited - Too Many Requests"</h3>
    <p><strong>Diagnstico:</strong> Excedeu limite de chamadas</p>
    <p><strong>Limite padro:</strong> 1000 req/min por API key</p>
    <p><strong>Soluo:</strong></p>
    <ul>
        <li>Implementar backoff exponencial (espera progressiva)</li>
        <li>Usar batch endpoints para mltiplas operaes</li>
        <li>Solicitar upgrade do plano se necessrio</li>
    </ul>
    
    <h2>Problemas de Dados</h2>
    
    <h3> Erro: "Duplicate Patient"</h3>
    <p><strong>Diagnstico:</strong> Mesmo paciente registrado 2x</p>
    <p><strong>Soluo:</strong></p>
    <ul>
        <li>INFANT.ID detecta automaticamente duplicatas via biometria</li>
        <li>Admin pode mesclar registros manualmente</li>
        <li>Implementar verificao no HIS antes de criar novo registro</li>
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
    
    <h2>Princpios de Segurana</h2>
    <ul>
        <li><strong>Least Privilege:</strong> Cada usurio s acessa o necessrio</li>
        <li><strong>Separao de Deveres:</strong> Tcnico no pode ver dados mdicos</li>
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
        <li><input type="checkbox"> Integrao HIS validada</li>
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
    
    <h2>Alertas de Segurana</h2>
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
        <li><strong>Relatrio de Segurana:</strong> Falhas de login, alertas</li>
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

def main():
    """Executar populao de aulas"""
    app = create_app()
    
    with app.app_context():
        print_section(" POPULANDO AULAS COM CONTEDO PROFISSIONAL")
        
        # Curso 1
        print(f"{BLUE}Processando: Onboarding INFANT.ID - Mdulo 1{RESET}")
        curso1 = Course.query.filter_by(titulo='Onboarding INFANT.ID - Mdulo 1').first()
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
            print(f"{RED} Curso no encontrado{RESET}")
        
        # Curso 2
        print(f"\n{BLUE}Processando: Integrao Hospitalar{RESET}")
        curso2 = Course.query.filter_by(titulo='Integrao Hospitalar').first()
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
            print(f"{RED} Curso no encontrado{RESET}")
        
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
            print(f"{RED} Curso no encontrado{RESET}")
        
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
