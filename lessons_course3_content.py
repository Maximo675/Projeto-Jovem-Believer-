"""
Aulas do Curso 3: Gerenciamento de Usuarios
Foco em: Seguranca, Controle de Acesso, Limpeza e Manutencao
"""

LESSONS_COURSE3 = {
    13: {
        "id": 13,
        "course_id": 3,
        "title": "Controle de Acesso e Uso Seguro",
        "content": """
<h1>Seguranca: Controle de Acesso ao Equipamento</h1>

<h2>Importancia do Controle de Acesso</h2>
<p>O equipamento ETAN eh um dispositivo critico que mantem dados biometricos sensíveis. Por isso:</p>
<ul>
    <li>Apenas pessoal treinado deve operar o equipamento</li>
    <li>Acesso deve ser controlado e monitorado</li>
    <li>Cada uso deve ser registrado</li>
    <li>Ninguem sem autorizacao pode manipular</li>
</ul>

<h2>Quem pode usar o ETAN?</h2>
<p><strong>Usuarios Autorizados:</strong></p>
<ul>
    <li>Enfermeiras treinadas no procedimento</li>
    <li>Tecnicos de TI designados</li>
    <li>Supervisores do programa</li>
    <li>Pessoal de manutencao certificado</li>
</ul>

<p><strong>Quem NAO pode usar:</strong></p>
<ul>
    <li>Visitantes ou publico geral</li>
    <li>Pessoal sem treinamento</li>
    <li>Usuarios nao-autorizados</li>
    <li>Criancas ou menores de idade</li>
</ul>

<h2>Localizacao Segura do Equipamento</h2>
<p>O equipamento deve ser armazenado em:</p>
<ul>
    <li><strong>Area restrita</strong> do hospital</li>
    <li><strong>Sala fechada</strong> quando nao em uso</li>
    <li><strong>Local seguro</strong> contra roubo ou danos</li>
    <li><strong>Temperatura controlada</strong> (ambiente normal)</li>
    <li><strong>Longe de umidade excessiva</strong></li>
</ul>

<h2>Rastreamento de Uso</h2>
<p>Mantenha registro de:</p>
<ul>
    <li>Quem usou o equipamento</li>
    <li>Quando foi usado (data/hora)</li>
    <li>Qual procedimento foi realizado</li>
    <li>Incidentes ou problemas</li>
</ul>

<p><strong>Documentacao:</strong> Use um livro de registro ou sistema digital para rastreamento.</p>

<h2>Regras de Utilizacao</h2>
<ol>
    <li><strong>Sempre autenticar-se</strong> antes de usar</li>
    <li><strong>Usar apenas em procedimentos autorizados</strong></li>
    <li><strong>Nao compartilhar credenciais</strong></li>
    <li><strong>Realizar logout</strong> ao terminar</li>
    <li><strong>Relatar anomalias</strong> imediatamente</li>
    <li><strong>Nao tentar reparos</strong> nao-autorizados</li>
</ol>

<h2>Resposta a Violacoes de Seguranca</h2>
<p>Se suspeitar de acesso nao-autorizado:</p>
<ol>
    <li>Desconectar o equipamento imediatamente</li>
    <li>Informar supervisor ou gerente de TI</li>
    <li>Iniciar investigacao de seguranca</li>
    <li>Documentar o incidente</li>
    <li>Revisar logs de acesso</li>
</ol>

<h2>Duracao estimada: 10 minutos</h2>
        """,
        "duration": "10 minutos"
    },

    14: {
        "id": 14,
        "course_id": 3,
        "title": "Limpeza, Higiene e Manutencao Preventiva",
        "content": """
<h1>Manutencao do Equipamento ETAN</h1>

<h2>Por que Manutencao eh Importante?</h2>
<p>Limpeza e manutencao regular garantem:</p>
<ul>
    <li>Longevidade do equipamento</li>
    <li>Qualidade consistente de captura</li>
    <li>Seguranca higiênica para usar com bebes</li>
    <li>Cumprimento de normas hospitalares</li>
    <li>Reducao de problemas tecnicos</li>
</ul>

<h2>Limpeza Diaria do Scanner</h2>
<p><strong>Materiais Necessarios:</strong></p>
<ul>
    <li>Gaze ou pano macio (material nao-abrasivo)</li>
    <li>Solucao de limpeza (álcool 70% ou solucao fornecida)</li>
    <li>Recipiente para materiais descartaveis</li>
</ul>

<h2>Procedimento de Limpeza</h2>
<p><strong>Apos CADA uso:</strong></p>
<ol>
    <li>Desconectar o equipamento do computador</li>
    <li>Umedecer levemente a gaze com solucao de limpeza</li>
    <li>Limpar a area de captura (visor) com movimentos suaves</li>
    <li>Secar completamente com gaze seca</li>
    <li>Reconectar apenas apos estar completamente seco</li>
</ol>

<p><strong>Apos CADA coleta (dentro do mesmo dia):</strong></p>
<ol>
    <li>Limpar o visor com gaze macia</li>
    <li>Evitar deixar residuos ou sujeira</li>
    <li>Permitir secar ao ar antes da proxima coleta</li>
</ol>

<h2>Limpeza Semanal Aprofundada</h2>
<p>Uma vez por semana, realizar limpeza mais completa:</p>
<ol>
    <li>Desconectar equipamento completamente</li>
    <li>Limpar visor principal</li>
    <li>Limpar conectores USB (externamente apenas)</li>
    <li>Limpar corpo do dispositivo e cabo</li>
    <li>Inspeção visual de danos</li>
    <li>Secar bem antes de reconectar</li>
</ol>

<h2>O que NUNCA fazer</h2>
<ul>
    <li><strong>NUNCA</strong> imerger em agua</li>
    <li><strong>NUNCA</strong> usar produtos abrasivos</li>
    <li><strong>NUNCA</strong> usar agua quente</li>
    <li><strong>NUNCA</strong> forcar conexoes</li>
    <li><strong>NUNCA</strong> abrir o dispositivo</li>
    <li><strong>NUNCA</strong> reparar pessoalmente</li>
</ul>

<h2>Limpeza do Visor</h2>
<p><strong>CRITICO para qualidade de captura:</strong></p>
<ol>
    <li>Usar apenas materiais nao-abrasivos</li>
    <li>Limpar em movimentos circulares suaves</li>
    <li>NAO esfregar vigorosamente</li>
    <li>Secar completamente</li>
    <li>Verificar se ficou limpo (sem manchas)</li>
</ol>

<h2>Manutencao Mensal</h2>
<p>Uma vez por mês, verificar:</p>
<ul>
    <li>Estado geral do equipamento</li>
    <li>Sinais de desgaste ou dano</li>
    <li>Funcionamento de LED (se houver)</li>
    <li>Integridade do cabo USB</li>
    <li>Conexoes firmes</li>
</ul>

<p>Se encontrar qualquer problema, contactar suporte tecnico.</p>

<h2>Materiais de Limpeza Recomendados</h2>
<table border="1" cellpadding="10">
    <tr>
        <th>Material</th>
        <th>Uso</th>
        <th>Frequencia</th>
    </tr>
    <tr>
        <td>Gaze macia (nao-abrasiva)</td>
        <td>Limpeza principal</td>
        <td>Sempre</td>
    </tr>
    <tr>
        <td>Álcool 70%</td>
        <td>Desinfeccao leve</td>
        <td>Diaria</td>
    </tr>
    <tr>
        <td>Pano de microfibra (opcional)</td>
        <td>Secagem final</td>
        <td>Conforme necessario</td>
    </tr>
    <tr>
        <td>Destilador/spray de ar (opcional)</td>
        <td>Remover pó</td>
        <td>Semanal</td>
    </tr>
</table>

<h2>Registro de Manutencao</h2>
<p>Mantenha um registro com:</p>
<ul>
    <li>Data e hora da limpeza</li>
    <li>Pessoa responsavel</li>
    <li>Tipo de limpeza realizada</li>
    <li>Qualquer problema detectado</li>
    <li>Proxima manutencao programada</li>
</ul>

<h2>Duracao estimada: 12 minutos</h2>
        """,
        "duration": "12 minutos"
    },

    15: {
        "id": 15,
        "course_id": 3,
        "title": "Conformidade e Auditoria",
        "content": """
<h1>Conformidade, Regulamentacoes e Auditoria</h1>

<h2>O que eh Conformidade?</h2>
<p>Conformidade significa que todas as operacoes com o ETAN seguem:</p>
<ul>
    <li>Regulamentacoes legais (LGPD, lei de protecao de dados)</li>
    <li>Normas hospitalares e clinicas</li>
    <li>Protocolos internacionais de seguranca biometrica</li>
    <li>Diretrizes da INFANT.ID</li>
</ul>

<h2>Protecao de Dados - LGPD</h2>
<p><strong>Lei Geral de Protecao de Dados (LGPD - Lei 13.709/2018)</strong></p>

<p>Seus dados biometricos sao extremamente sensíveis. A LGPD garante:</p>
<ul>
    <li><strong>Direito a privacidade:</strong> Seus dados nao sao compartilhados</li>
    <li><strong>Direito a informacao:</strong> Saber como dados sao usados</li>
    <li><strong>Direito a acesso:</strong> Solicitar ver seus dados</li>
    <li><strong>Direito a remocao:</strong> Solicitar que dados sejam apagados</li>
</ul>

<p><strong>Como o INFANT.ID assegura LGPD:</strong></p>
<ul>
    <li>Dados sao criptografados em transito e em repouso</li>
    <li>Acesso restrito apenas a pessoal treinado</li>
    <li>Consentimento informado obrigatorio</li>
    <li>Auditagem regular de acesso</li>
    <li>Retencao de dados por periodo limitado</li>
</ul>

<h2>Consentimento Informado</h2>
<p>Antes de realizar coleta biometrica, deve-se ter:</p>
<ol>
    <li><strong>Consentimento da progenitora</strong> (em nome do RN)</li>
    <li><strong>Explicacao clara</strong> do procedimento</li>
    <li><strong>Informacao sobre como dados serao usados</strong></li>
    <li><strong>Opcao de rejeitar</strong> se desejar</li>
</ol>

<p><strong>Documentacao:</strong> Consentimento deve ser registrado no sistema e arquivado.</p>

<h2>Seguranca de Dados Biometricos</h2>
<p>Medidas essenciais de seguranca:</p>
<ul>
    <li><strong>Criptografia:</strong> Dados sempre criptografados</li>
    <li><strong>Controle de Acesso:</strong> Apenas usuarios autorizados</li>
    <li><strong>Auditagem:</strong> Todos os acessos registrados</li>
    <li><strong>Backup:</strong> Dados duplicados em local seguro</li>
    <li><strong>Seguranca Fisica:</strong> Equipamento em local protegido</li>
</ul>

<h2>Retencao de Dados</h2>
<ul>
    <li>Dados sao retidos pelo periodo necessario para o servico</li>
    <li>Apos termino do servico, dados podem ser apagados</li>
    <li>Retencao minima obrigatoria por lei pode variar</li>
    <li>Procedimentos de destruicao segura estao em place</li>
</ul>

<h2>Auditagem de Acesso</h2>
<p>Todas as operacoes sao registradas em logs de auditoria:</p>
<ul>
    <li>Quem acessou o sistema</li>
    <li>Quando acessou (data/hora exata)</li>
    <li>Qual operacao realizou</li>
    <li>Se foi bem-sucedida ou falhou</li>
</ul>

<p><strong>Auditores</strong> revisam esses logs regularmente para detectar anomalias.</p>

<h2>Checklist de Conformidade Diaria</h2>
<p>Cada operador deve verificar diariamente:</p>
<table border="1" cellpadding="10">
    <tr>
        <th>Item</th>
        <th>Verificar</th>
    </tr>
    <tr>
        <td>Consentimento</td>
        <td>Todos os participantes consentiram?</td>
    </tr>
    <tr>
        <td>Autorizacao</td>
        <td>Sou operador autorizado para este procedimento?</td>
    </tr>
    <tr>
        <td>Privacidade</td>
        <td>Area eh privada? Dados sao confidenciais?</td>
    </tr>
    <tr>
        <td>Documentacao</td>
        <td>Registro de coleta foi feito corretamente?</td>
    </tr>
    <tr>
        <td>Seguranca</td>
        <td>Dados foram salvos em ambiente seguro?</td>
    </tr>
    <tr>
        <td>Higiene</td>
        <td>Equipamento foi limpo apropriadamente?</td>
    </tr>
</table>

<h2>Relatorio de Incidentes</h2>
<p>Se acontecer qualquer incidente de seguranca ou privacidade:</p>
<ol>
    <li>Documentar exatamente o que aconteceu</li>
    <li>Informar supervisor imediatamente</li>
    <li>Nao tentar "corrigir" sem autorizacao</li>
    <li>Seguir procedimento de resposta a incidentes</li>
    <li>Revisar o que causou para prevenir no futuro</li>
</ol>

<h2>Certificado de Conformidade</h2>
<p>Periodicamente, o programa passa por auditoria externa para:</p>
<ul>
    <li>Verificar conformidade com LGPD</li>
    <li>Avaliar seguranca de dados</li>
    <li>Auditar protocolos clinicos</li>
    <li>Validar treinamento de pessoal</li>
</ul>

<h2>Recursos de Conformidade</h2>
<ul>
    <li><strong>Politica de Privacidade:</strong> Disponivel no portal INFANT.ID</li>
    <li><strong>Documentacao LGPD:</strong> Solicitar ao departamento de conformidade</li>
    <li><strong>Contato - DPO (Data Protection Officer):</strong> dpo@infantid.com.br</li>
</ul>

<h2>Duracao estimada: 15 minutos</h2>
        """,
        "duration": "15 minutos"
    },
}

print("="*70)
print("Aulas do Curso 3: Gerenciamento de Usuarios")
print("="*70)

for lesson_id, lesson in LESSONS_COURSE3.items():
    print(f"\nAula {lesson_id}: {lesson['title']}")
    print(f"  Curso {lesson['course_id']}")
    print(f"  Duracao: {lesson['duration']}")
    print(f"  Caracteres: {len(lesson['content'])}")

print("\n" + "="*70)
print(f"Total de {len(LESSONS_COURSE3)} aulas do Curso 3 criadas")
print("="*70)
