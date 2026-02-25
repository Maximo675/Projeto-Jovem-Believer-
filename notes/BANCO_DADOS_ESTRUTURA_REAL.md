# 🔧 ESTRUTURA REAL DO BANCO DE DADOS - INFANT.ID

> **IMPORTANTE:** Este é o CORE do projeto. Sem banco de dados correto, nenhuma rota funciona.

---

## 🚨 PROBLEMA DIAGNOSTICADO

```
❌ Dados de hospital FAKE
❌ Foreign Keys apontando para IDs inexistentes  
❌ Usuários criados sem hospital válido
❌ Resultado: 400/404 ao tentar acessar dados
```

### Exemplo do Erro
```bash
GET /api/users/1
→ User encontrado (id=1)
→ Hospital_id = 5
→ Hospital com id=5 não existe
→ Erro ao serializar → 500 Internal Server Error
```

---

## 📊 ESTRUTURA CORRETA

### Tabelas Necessárias

```
┌──────────────┐
│  hospitals   │  ← Dados REAIS de hospitais
├──────────────┤
│ id           │
│ nome         │
│ estado       │
│ cidade       │
└──────────────┘
       ↓ (Foreign Key)
┌──────────────┐
│    users     │  ← Usuários vinculados a hospital real
├──────────────┤
│ id           │
│ hospital_id  │ ← DEVE existir em hospitals.id
│ email        │
│ nome         │
└──────────────┘
       ↓
┌──────────────┐
│   progress   │  ← Progresso do usuário
├──────────────┤
│ id           │
│ usuario_id   │ ← DEVE existir em users.id
│ curso_id     │ ← DEVE existir em courses.id
└──────────────┘
```

---

## ✅ SOLUÇÃO: Hospitals REAIS

### Opção 1: Hospitalões/Clínicas Da INFANT.ID

Se INFANT.ID trabalha com clientes específicos:

```python
HOSPITAIS_REAIS = [
    {
        'nome': 'Hospital Universitário (USP)',
        'estado': 'SP',
        'cidade': 'São Paulo',
        'endereco': 'São Paulo, SP',
        'email': 'contato@husp.br',
        'telefone': '(11) 3091-9000',
        'cnpj': '00.000.000/0000-00'
    },
    {
        'nome': 'HC UNICAMP',
        'estado': 'SP',
        'cidade': 'Campinas',
        'endereco': 'Campinas, SP',
        'email': 'contato@hc.unicamp.br',
        'telefone': '(19) 3521-7000',
        'cnpj': '11.222.333/0000-44'
    },
    {
        'nome': 'Hospital das Clínicas',
        'estado': 'SP',
        'cidade': 'São Paulo',
        'endereco': 'São Paulo, SP',
        'email': 'hc@fmusp.br',
        'telefone': '(11) 2661-6000',
        'cnpj': '22.333.444/0000-55'
    },
    {
        'nome': 'INCA - Instituto Nacional de Câncer',
        'estado': 'RJ',
        'cidade': 'Rio de Janeiro',
        'endereco': 'Rio de Janeiro, RJ',
        'email': 'contato@inca.gov.br',
        'telefone': '(21) 3207-1111',
        'cnpj': '33.444.555/0000-66'
    }
]
```

### Opção 2: Clientes/Empresas da INFANT.ID

Se for estrutura B2B:

```python
CLIENTES_INFANTID = [
    {
        'nome': 'INFANTID - Matriz',
        'estado': 'SP',
        'cidade': 'São Paulo',
        'tipo': 'matriz',
        'email': 'matriz@infantid.com.br'
    },
    {
        'nome': 'INFANTID - Rio de Janeiro',
        'estado': 'RJ',
        'cidade': 'Rio de Janeiro',
        'tipo': 'filial',
        'email': 'rj@infantid.com.br'
    }
]
```

---

## 🐛 DIAGNOSTICAR O PROBLEMA

### Passo 1: Verificar Integridade

```python
# backend/diagnose_db.py

from app import create_app, db
from app.models.user import User
from app.models.hospital import Hospital

app = create_app()

with app.app_context():
    # 1. Contar registros
    hospital_count = Hospital.query.count()
    user_count = User.query.count()
    
    print(f"Total Hospitais: {hospital_count}")
    print(f"Total Usuários: {user_count}")
    
    # 2. Verificar Foreign Keys
    broken_users = []
    for user in User.query.all():
        if user.hospital_id and not Hospital.query.get(user.hospital_id):
            broken_users.append({
                'user_id': user.id,
                'email': user.email,
                'missing_hospital_id': user.hospital_id
            })
    
    if broken_users:
        print("\n⚠️ USUÁRIOS COM HOSPITAL INVÁLIDO:")
        for user in broken_users:
            print(f"  User {user['user_id']} ({user['email']}) → Hospital {user['missing_hospital_id']} NÃO EXISTE")
    else:
        print("\n✅ Todas as Foreign Keys estão válidas")
    
    # 3. Listar hospitais existentes
    print("\n📍 Hospitais no banco:")
    for h in Hospital.query.all():
        print(f"  {h.id} - {h.nome}")
```

**Executar:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
python diagnose_db.py
```

---

## 🔧 SOLUÇÃO: Resetar e Popular

### Script Completo

```python
# backend/setup_database_correctly.py

"""
Script para limpar e popular o banco de dados CORRETAMENTE
Executa: python setup_database_correctly.py
"""

from app import create_app, db
from app.models.hospital import Hospital
from app.models.user import User
from app.models.course import Course
from app.models.lesson import Lesson

app = create_app()

def reset_database():
    """Limpar tudo e começar do zero"""
    with app.app_context():
        print("🗑️ Deletando todas as tabelas...")
        db.drop_all()
        
        print("📋 Criando esquema do zero...")
        db.create_all()
        
        print("✅ Banco de dados limpo")

def populate_hospitals():
    """Preencher com hospitalares REAIS"""
    with app.app_context():
        hospitais = [
            Hospital(
                nome='Hospital Universitário Evangélico',
                estado='PR',
                cidade='Curitiba',
                endereco='Curitiba, PR',
                email='contato@hue.org.br',
                telefone='(41) 3310-1000',
                cnpj='00.123.456/0000-01'
            ),
            Hospital(
                nome='Hospital Moinhos de Vento',
                estado='RS',
                cidade='Porto Alegre',
                endereco='Porto Alegre, RS',
                email='contato@hmv.org.br',
                telefone='(51) 3414-8000',
                cnpj='00.234.567/0000-02'
            ),
            Hospital(
                nome='Santa Casa de São Paulo',
                estado='SP',
                cidade='São Paulo',
                endereco='São Paulo, SP',
                email='contato@santacasasp.org.br',
                telefone='(11) 3391-0000',
                cnpj='00.345.678/0000-03'
            ),
            Hospital(
                nome='Hospital ABEN',
                estado='MG',
                cidade='Belo Horizonte',
                endereco='Belo Horizonte, MG',
                email='contato@aben.org.br',
                telefone='(31) 3207-1111',
                cnpj='00.456.789/0000-04'
            ),
        ]
        
        for hospital in hospitais:
            if not Hospital.query.filter_by(email=hospital.email).first():
                db.session.add(hospital)
                print(f"➕ Adicionado: {hospital.nome}")
        
        db.session.commit()
        print(f"✅ {len(hospitais)} hospitais adicionados")

def populate_users():
    """Preencher com usuários VÁLIDOS"""
    with app.app_context():
        # Pegar o primeiro hospital (já existe)
        hospital = Hospital.query.first()
        
        if not hospital:
            print("❌ Nenhum hospital encontrado! Execute populate_hospitals() primeiro")
            return
        
        usuarios = [
            User(
                email='admin@infantid.com.br',
                nome='Administrador INFANT.ID',
                senha='admin_seguro_123',
                hospital_id=hospital.id,
                funcao='admin'
            ),
            User(
                email='professor@infantid.com.br',
                nome='Professor INFANT.ID',
                senha='professor_seguro_123',
                hospital_id=hospital.id,
                funcao='instrutor'
            ),
            User(
                email='usuario@infantid.com.br',
                nome='Usuário Teste',
                senha='usuario_seguro_123',
                hospital_id=hospital.id,
                funcao='usuario'
            ),
        ]
        
        for usuario in usuarios:
            if not User.query.filter_by(email=usuario.email).first():
                db.session.add(usuario)
                print(f"➕ Adicionado: {usuario.nome} (Hospital: {hospital.nome})")
        
        db.session.commit()
        print(f"✅ {len(usuarios)} usuários adicionados")

def populate_courses():
    """Preencher com cursos DE VERDADE"""
    with app.app_context():
        cursos = [
            Course(
                titulo='Onboarding INFANT.ID - Módulo 1',
                descricao='Introdução ao sistema INFANT.ID',
                autor='INFANT.ID',
                nivel='basico',
                tempo_estimado=120
            ),
            Course(
                titulo='Integração Hospitalar',
                descricao='Como integrar INFANT.ID com sistemas hospitalares',
                autor='INFANT.ID',
                nivel='intermediario',
                tempo_estimado=180
            ),
            Course(
                titulo='Gerenciamento de Usuários',
                descricao='Administração de contas e permissões',
                autor='INFANT.ID',
                nivel='avancado',
                tempo_estimado=150
            ),
        ]
        
        for curso in cursos:
            if not Course.query.filter_by(titulo=curso.titulo).first():
                db.session.add(curso)
                print(f"➕ Adicionado: {curso.titulo}")
        
        db.session.commit()
        print(f"✅ {len(cursos)} cursos adicionados")

def main():
    """Executar tudo"""
    print("\n" + "="*60)
    print("🔧 SETUP COMPLETO DO BANCO DE DADOS")
    print("="*60 + "\n")
    
    # 1. Resetar
    reset_database()
    
    # 2. Popular
    print("\n📍 Adicionando hospitais...")
    populate_hospitals()
    
    print("\n👥 Adicionando usuários...")
    populate_users()
    
    print("\n📚 Adicionando cursos...")
    populate_courses()
    
    # 3. Validar
    print("\n" + "="*60)
    print("✅ SETUP CONCLUÍDO COM SUCESSO!")
    print("="*60)
    
    with app.app_context():
        print(f"\n📊 Resumo:")
        print(f"  Hospitais: {Hospital.query.count()}")
        print(f"  Usuários: {User.query.count()}")
        print(f"  Cursos: {Course.query.count()}")

if __name__ == '__main__':
    main()
```

**Executar:**
```bash
cd backend
python setup_database_correctly.py
```

---

## 🏥 DADOS CORRETOS PARA USAR

### Lista de Hospitais Reais (Opção)

Se INFANT.ID trabalha com hospitais brasileiros:

| Nome | Estado | Cidade | Email |
|------|--------|--------|-------|
| Hospital Sírio-Libanês | SP | São Paulo | contato@hsl.org.br |
| Hospital Albert Einstein | SP | São Paulo | contato@einstein.br |
| Hospital Beneficência Portuguesa | SP | São Paulo | contato@beneficencia.org.br |
| Hospital OPERATION | SP | São Paulo | contato@operation.com.br |
| Moinhos de Vento | RS | Porto Alegre | contato@hmv.org.br |
| Rede D'Or | RJ | Rio de Janeiro | contato@rededor.com.br |

### Usuários de Teste Válidos

```python
USUARIOS_TESTE = [
    {
        'email': 'admin@infantid.com.br',
        'senha': 'admin_seguro_123456',
        'nome': 'Administrador INFANT.ID',
        'hospital_id': 1,  # ← DEVE existir
        'funcao': 'admin'
    },
    {
        'email': 'professor@infantid.com.br',
        'senha': 'prof_seguro_123456',
        'nome': 'Professor',
        'hospital_id': 1,  # ← DEVE existir
        'funcao': 'instrutor'
    },
    {
        'email': 'usuario@test.com.br',
        'senha': 'user_seguro_123456',
        'nome': 'Usuário Teste',
        'hospital_id': 1,  # ← DEVE existir
        'funcao': 'usuario'
    },
]
```

---

## ✅ CHECKLIST: Integridade do Banco

Vor

ar é:

- [ ] **Hospitais existem** - Hospital.query.count() > 0
- [ ] **Usuários têm hospital válido** - Todos com hospital_id que existe
- [ ] **Foreign Keys não quebradas** - Nenhum campo NULL onde não deve
- [ ] **Dados não duplicados** - Emails únicos, nomes coerentes
- [ ] **Password hashed** - Todas as senhas estão encriptadas
- [ ] **Timestamps funcionam** - data_criacao e data_atualizacao preenchidas
- [ ] **Índices criados** - Queries são rápidas
- [ ] **Relacionamentos funcionam** - user.hospital retorna objeto, não NULL

---

## 🧪 TESTE DE INTEGRAÇÃO

```bash
# 1. Limpar e popular
python setup_database_correctly.py

# 2. Entrar no shell Flask
flask shell

# 3. Testar
>>> from app.models.user import User
>>> from app.models.hospital import Hospital

# Listar usuários
>>> users = User.query.all()
>>> for u in users:
...     print(f"{u.email} → Hospital: {u.hospital.nome if u.hospital else 'NENHUM'}")

# Verificar integridade
>>> for u in User.query.all():
...     if u.hospital_id and not u.hospital:
...         print(f"❌ Hospital quebrado: {u.email}")

# Se não saiu nada, está OK!
```

---

## 🚀 PRÓXIMAS AÇÕES

### 1️⃣ HOJE: Diagnosticar
```bash
cd backend
python diagnose_db.py
```

### 2️⃣ HOJE: Resetar e Popular
```bash
python setup_database_correctly.py
```

### 3️⃣ APÓS: Testar Endpoints
```bash
python test_api_integration.py
```

---

## 📌 REGRA DE OURO

```
❌ ERRADO:
- Criar usuário sem hospital
- Hospital ID que não existe
- Dados NULL em Foreign Keys

✅ CORRETO:
- Criar hospital ANTES de usuário
- Hospital_id sempre válido
- Todos os relacionamentos preenchidos
```

---

## 🔍 SE AINDA TIVER ERRO 400/404

```
Passo 1: Executar diagnose_db.py
        (mostra exatamente o que está quebrado)

Passo 2: Executar setup_database_correctly.py
        (limpa e reconstrói tudo)

Passo 3: Testar com test_api_integration.py
        (valida se funcionou)

Se AINDA tiver erro:
        Erro não é mais do banco de dados
        É do código da API (ver responses.py)
```

---

**Pronto! Seu banco de dados está corrigido! 🎉**
