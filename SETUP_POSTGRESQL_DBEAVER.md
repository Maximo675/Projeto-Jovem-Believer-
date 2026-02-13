# 🐘 DBeaver + PostgreSQL - SETUP RÁPIDO

## ✅ O Que Já Foi Feito

- ✓ Arquivo `.env` criado com variáveis PostgreSQL
- ✓ `config.py` alterado para usar PostgreSQL
- ✓ Driver `psycopg2-binary` instalado
- ✓ Script `setup_postgres.py` criado

---

## 🎯 3 Passos Finais

### Passo 1: Criar o Database no DBeaver

**No DBeaver:**
```
1. Abra DBeaver
2. Clique em: Connections → PostgreSQL (ou New Connection se não tiver)
3. Configure:
   Host: localhost
   Port: 5432
   Username: postgres
   Password: [sua senha do postgres]
   → Test Connection
   → OK

4. Clique direito em "Databases"
5. New Database
   Name: infant_id_platform
   → OK
```

---

### Passo 2: Atualizar o .env

Edite o arquivo `backend/.env`:

```env
# Substitua "YOUR_POSTGRES_PASSWORD" pela SENHA DO SEU POSTGRES
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
```

**Exemplo:**
```env
DB_PASSWORD=minha_senha_do_postgres_123
```

---

### Passo 3: Executar o Setup

**No PowerShell:**
```powershell
cd "c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\backend"

C:\Python314\python.exe setup_postgres.py
```

**Resultado esperado:**
```
✅ DATABASE SETUP CONCLUÍDO COM SUCESSO!
✓ users      (Usuários do sistema)
✓ hospitals  (Hospitais)
✓ courses    (Cursos)
✓ lessons    (Aulas)
✓ documents  (Documentos)
```

---

## 🚀 Depois: Rodar o Servidor

```powershell
cd "c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\backend"

C:\Python314\python.exe run.py
```

**Servidor rodando em:**
```
http://localhost:5000
```

---

## 🔍 Verificar no DBeaver

**No DBeaver:**
1. Expanda: PostgreSQL → Databases → infant_id_platform
2. Expanda: Schemas → public → Tables
3. Você verá:
   - ✓ users
   - ✓ hospitals
   - ✓ courses
   - ✓ lessons
   - ✓ documents

Clique em qualquer tabela → F2 ou direito → View Rows → veja os dados em tempo real!

---

## 💡 Dicas

**Ver estrutura da tabela:**
```
DBeaver → infant_id_platform → public → Tables → users
→ Clique em "Columns" ou "DDL" para ver a estrutura
```

**Executar SQL Query:**
```
DBeaver → SQL Editor (canto superior direito)
→ Escreva seu SQL
→ Ctrl+Enter para executar
```

**Popular com dados de teste:**
```sql
INSERT INTO users (email, password_hash, full_name, created_at)
VALUES ('teste@email.com', 'hash123', 'João Silva', NOW());
```

---

## ✅ Checklist Final

- [ ] DBeaver conectado ao PostgreSQL
- [ ] Database `infant_id_platform` criado
- [ ] `.env` configurado com senha do postgres
- [ ] `setup_postgres.py` executado com sucesso
- [ ] Tabelas aparecem no DBeaver
- [ ] Servidor rodando com `python run.py`
- [ ] Acessando http://localhost:5000

---

## 🤝 Tudo Pronto!

Agora você tem:
✅ Backend Python com Flask
✅ PostgreSQL como banco de dados
✅ DBeaver para gerenciar visualmente
✅ Script automático para criar tabelas
✅ Servidor rodando em tempo real

**Bora testar? 🚀**
