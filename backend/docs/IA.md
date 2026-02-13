# Documentação de IA - INFANT.ID

## Visão Geral

Implementação de IA para personalizar o aprendizado e responder dúvidas dos usuários.

## Serviços de IA Disponíveis

### 1. Assistente de Dúvidas (Chatbot)

Responde perguntas dos usuários sobre conteúdo dos cursos.

**Funcionalidade:**
- Responde em linguagem natural
- Contextualiza respostas baseado no curso
- Registra histórico de conversas
- Permite avaliação de respostas

**Uso:**
```python
from app.services.ai_service import AiService

ai_service = AiService()
resposta, tokens = ai_service.responder_pergunta(
    "O que é onboarding?",
    contexto_curso=1
)
```

### 2. Recomendação de Conteúdo

Sugere próximos cursos baseado no progresso do usuário.

**Funcionalidade:**
- Analisa progresso em cursos anteriores
- Propõe caminho de aprendizado
- Personaliza recomendações
- Considera dificuldade e tempo de aprendizado

**Uso:**
```python
recomendacoes = ai_service.gerar_recomendacoes(
    usuario_id=1,
    progresso_cursos=[...]
)
```

### 3. Análise de Feedback

Analisa sentimento de respostas do usuário.

**Funcionalidade:**
- Detecta satisfação
- Identifica dúvidas não resolvidas
- Melhora base de conhecimento
- Monitora qualidade do atendimento

**Uso:**
```python
sentimento = ai_service.analisar_sentimento("A resposta foi muito útil!")
# Retorna: "positivo", "neutro", ou "negativo"
```

## Configuração

### OpenAI

1. **Obter Chave de API:**
   - Acesse https://platform.openai.com/
   - Criar chave de API

2. **Configurar Variável de Ambiente:**
   ```
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-3.5-turbo
   ```

### Alternativas

Para melhor privacidade ou custo, considere:

- **Hugging Face**: Modelos open-source
- **Cohere**: API alternativa
- **Llama 2**: Rodando localmente
- **Claude**: Anthropic

## Modelos Recomendados

### Desenvolvimento
```
gpt-3.5-turbo (mais barato)
```

### Produção
```
gpt-4 (mais preciso, mais caro)
```

## Prompts

### System Prompt Padrão
```
Você é um assistente inteligente especializado em educação 
e onboarding para profissionais de saúde. Mantenha a simpatia, 
seja conciso e cite referências quando apropriado.
```

### Personalização por Contexto
```
O usuário está no curso de "Onboarding Básico". 
Personalize as respostas para este contexto.
```

## Histórico de Conversas

Todas as conversas são armazenadas para:

1. **Análise**: Entender padrões de dúvidas
2. **Melhoria**: Ajustar prompts baseado em feedback
3. **Auditoria**: Rastrear interações
4. **Aprendizado**: Melhorar recomendações futuras

**Acesso ao histórico:**
```python
GET /api/ia/historico/<usuario_id>
```

## Avaliação de Respostas

Usuários podem avaliar respostas de 1-5 estrelas:

```python
PUT /api/ia/avaliar/<conversa_id>
{
  "avaliacao": 4
}
```

Essas avaliações ajudam a:
- Identificar respostas ruins
- Treinar modelos melhores
- Melhorar prompts
- Medir satisfação

## Otimizações

### Redução de Custo
1. Cache de respostas frequentes
2. Usar gpt-3.5-turbo em vez de gpt-4
3. Limitar max_tokens
4. Implementar rate limiting

### Melhorar Velocidade
1. Fazer requisições assíncronas
2. Implementar fila de tarefas
3. Cache de respostas

### Melhorar Qualidade
1. Few-shot learning
2. Chain-of-thought prompting
3. Feedback loop
4. Fine-tuning customizado

## Exemplo de Implementação

```python
from flask import Blueprint, request, jsonify
from app.services.ai_service import AiService

bp = Blueprint('ai', __name__, url_prefix='/api/ia')
ai_service = AiService()

@bp.route('/consult', methods=['POST'])
def consult():
    try:
        data = request.get_json()
        pergunta = data.get('pergunta')
        curso_id = data.get('curso_id')
        
        resposta, tokens = ai_service.responder_pergunta(pergunta, curso_id)
        
        # Salvar no banco
        conversa = IAConversation(
            usuario_id=data.get('usuario_id'),
            curso_id=curso_id,
            pergunta=pergunta,
            resposta=resposta,
            tokens_usados=tokens
        )
        db.session.add(conversa)
        db.session.commit()
        
        return jsonify({
            'resposta': resposta,
            'tokens': tokens
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
```

## Monitoramento

### Métricas Importantes

1. **Custo**: Tokens utilizados por mês
2. **Performance**: Tempo de resposta
3. **Qualidade**: Taxa de avaliação positiva
4. **Uso**: Conversas por dia/semana
5. **Satisfação**: Média de avaliações

### Dashboard (Futuro)
- Gráficos de uso de IA
- Custo por usuário
- Satisfação por curso
- Dúvidas mais frequentes

## Roadmap de Melhorias

- [ ] Fine-tuning com dados específicos do INFANT.ID
- [ ] Análise de sentimento em tempo real
- [ ] Sugestões automáticas de conteúdo
- [ ] Multi-idioma (inglês, espanhol)
- [ ] Integração com assistente de voz
- [ ] Geração automática de certificados PDF

## Segurança e Privacidade

1. **Não enviar dados sensíveis**: Evitar CPF, CNPJ, dados de pacientes
2. **Criptografia**: Respostas da IA armazenadas criptografadas
3. **Conformidade**: LGPD, HIPAA (quando aplicável)
4. **Auditoria**: Todas as interações registradas
5. **Retenção**: Política de retenção de dados definida

## Referências

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Best Practices for AI in Healthcare](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7239010/)
- [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)
