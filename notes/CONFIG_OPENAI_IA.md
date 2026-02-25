## 🤖 Configuração da IA - OpenAI

Você já tem a chave da API! Vamos configurar agora!

### Passo 1: Adicionar Chave ao .env

Edite o arquivo `backend/.env` e adicione:

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-3.5-turbo
```

**Importante:** Substitua `sua_chave_aqui` pela sua chave real da OpenAI!

### Passo 2: Testar Conexão

Execute no PowerShell:

```powershell
cd "c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\backend"

C:\Python314\python.exe -c "
from app import create_app
from app.services.ai_service import AiService

app = create_app()
with app.app_context():
    ai = AiService()
    resposta, tokens = ai.responder_pergunta('Olá, como você funciona?')
    print('✅ IA Funcionando!')
    print(f'Resposta: {resposta}')
    print(f'Tokens: {tokens}')
"
```

Se ver "IA Funcionando!", tudo OK! ✅

---

## 📋 Prompts Melhorados para Enfermeiras e Papilocopistas

Os prompts já estão configurados para ajudar profissionais de saúde. Aqui está o que você pode fazer:

### Sistema Prompt Atual (em `ai_service.py`):

```
Você é um assistante inteligente especializado em educação e onboarding 
para profissionais de saúde. Você ajuda os usuários a aprender sobre processos de onboarding, 
boas práticas, e responde dúvidas de forma clara e profissional.

Mantenha a simpatia, seja conciso e sempre cite fontes ou referências quando apropriado.
Respostas devem ser em Português do Brasil.
```

### Prompts Específicos por Contexto:

**Para Enfermeiras:**
```
Você é um assistente especializado em educação continuada para enfermeiras. 
Conhece profundamente protocolos de enfermagem, higiene hospitalar, segurança do paciente,
administração de medicamentos, triagem de pacientes, e documentação clínica.

Sempre priorize a segurança do paciente nas respostas.
Cite referências de normas e protocolos quando apropriado.
```

**Para Papilocopistas:**
```
Você é um assistente especializado em educação para papilocopistas e tecnólogos em saúde.
Conhece profundamente citologia, coleta de material, análise de amostras,
identificação de células anormais, documentação de laudos e segurança biológica.

Sempre mantenha foco na qualidade diagnóstica.
Cite referências de protocolos e recomendações técnicas.
```

---

## 🎯 Como Implementar Prompts Customizados

No `backend/app/services/ai_service.py`, modifique o método:

```python
def _construir_system_prompt(self, curso_id=None, tipo_profissional=None):
    # Prompt pode variar por tipo de profissional
    if tipo_profissional == 'enfermeira':
        prompt = """... prompt para enfermeiras ..."""
    elif tipo_profissional == 'papilocopista':
        prompt = """... prompt para papilocopistas ..."""
    else:
        prompt = """... prompt genérico ..."""
    
    return prompt
```

---

## ✅ Próximas Ações

1. Adicione sua chave OpenAI ao `.env`
2. Teste a conexão com o comando acima
3. Customize os prompts conforme necessário
4. Rode o servidor e acesse http://localhost:8000
5. Teste o chat com a IA!

Quando terminar a configuração, avisa! 🚀
