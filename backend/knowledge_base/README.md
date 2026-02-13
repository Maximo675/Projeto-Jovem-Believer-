# Base de Conhecimento - INFANT.ID

## 📁 Estrutura de Documentos

A plataforma utiliza documentos profissionais como base de conhecimento para o currículo de treinamento.

## 📄 Documentos Disponíveis

### 1. Informativo Etan
**Arquivo:** `Informativo Etan.docx`  
**Descrição:** Informações sobre protocolo Etan  
**Uso:** Conteúdo de cursos de treinamento  
**Status:** ✅ Integrado

### 2. Procedimento de Coleta
**Arquivo:** `Procedimento de Coleta.docx`  
**Descrição:** Guia passo a passo para procedimentos de coleta  
**Uso:** Instruções práticas para usuários  
**Status:** ✅ Integrado

### 3. Protocolo de Coleta Passo a Passo
**Arquivo:** `Protocolo de Coleta Passo a Passo.docx`  
**Descrição:** Protocolo detalhado com instruções sequenciais  
**Uso:** Material de referência e treinamento  
**Status:** ✅ Integrado

## 🖼️ Identidade Visual

**Logo:** `logo.png`  
**Uso:** Branding da plataforma  
**Localização:** `/assets/logo/`  
**Integrações:**
- ✅ Navbar da aplicação
- ✅ Página de login
- ✅ Página inicial
- ✅ Documentação

## 🔧 Integração com API

Os documentos estão disponíveis via API em:

### Listar Documentos
```
GET /api/documents
Retorna: Lista de todos os documentos disponíveis
```

### Obter Documento
```
GET /api/documents/<nome-arquivo>
Retorna: Conteúdo do documento específico
```

### Download de Documento
```
GET /api/documents/<nome-arquivo>/download
Retorna: Arquivo Word para download
```

### Índice de Conhecimento
```
GET /api/documents/indice
Retorna: Índice completo da base de conhecimento
```

## 📋 Exemplos de Uso

### JavaScript (Frontend)
```javascript
// Listar documentos
const docs = await fetch('/api/documents').then(r => r.json());

// Download de documento
window.location.href = '/api/documents/Informativo Etan/download';
```

### Python (Backend)
```python
from app.services.document_service import DocumentService

# Listar documentos
docs = DocumentService.listar_documentos()

# Obter conteúdo
doc = DocumentService.obter_documento('Informativo Etan')
```

## 🎓 Criando Cursos a partir de Documentos

Para converter um documento em um curso estruturado:

```python
from app.services.document_service import DocumentService

DocumentService.criar_curso_de_documento(
    nome_documento='Informativo Etan',
    titulo_curso='Treinamento Etan - Módulo Básico',
    descricao='Treinamento sobre protocolo Etan',
    nivel='basico'
)
```

## 🔐 Segurança

- Documentos sensíveis devem ter permissões apropriadas
- Apenas usuários autenzicados podem acessar documentos
- DDownloads são rastreados no sistema
- Implementar LGPD compliance conforme necessário

## 📝 Adicionar Novos Documentos

1. Adicione o arquivo .docx em `/assets/documents/`
2. Execute a sincronização via API:
   ```
   POST /api/documents/sincronizar
   ```
3. O documento será automaticamente indexado

## 🚀 Próximos Passos

- [ ] Extrair conteúdo automático dos documentos Word
- [ ] Criar cursos estruturados baseados nos documentos
- [ ] Implementar busca full-text nos documentos
- [ ] Adicionar suporte a múltiplos formatos (PDF, etc)
- [ ] Criar histórico de versões dos documentos
- [ ] Implementar comentários e anotações nos documentos
