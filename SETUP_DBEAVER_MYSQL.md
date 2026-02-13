# 🗄️ SETUP: MySQL + DBeaver

## Passo 1: Instalar MySQL Server

### Windows - Download
1. Acesse: https://dev.mysql.com/downloads/mysql/
2. Baixe: **MySQL 8.0.x** (recomendado)
3. Escolha: **Windows (x86, 64-bit)**
4. MSI Installer (mais fácil)

### Windows - Instalação
1. Execute o instalador MSI
2. Choose Setup Type: **Developer Default** ✅
3. MySQL Server Configuration: 
   - Port: **3306** (padrão)
   - Config Type: **Development Computer**
4. MySQL Server User Accounts:
   - Root Password: **coloque uma senha segura** (ex: `root123`)
   - Anote essa senha! ⚠️
5. Windows Service: ✅ (Configure MySQL como serviço)
6. Complete a instalação

### Verificar se MySQL está rodando
```powershell
# No PowerShell, teste a conexão:
mysql -u root -p

# Ele vai pedir a senha que você configurou
# Se funcionar, digitar:
exit
```

---

## Passo 2: Instalar DBeaver

### Download
1. Acesse: https://dbeaver.io/download/
2. Baixe: **DBeaver Community Edition** (Windows)
3. Escolha versão **Portable** (sem instalação) ou **Installer** (padrão)

### Instalação
1. Execute o instalador
2. Next → Next → Finish
3. Pronto! DBeaver instalado ✅

---

## Passo 3: Conectar DBeaver ao MySQL

### 1. Abrir DBeaver
```
Arquivo → Nova Conexão de Database
```

### 2. Escolher MySQL
```
Procurar por "MySQL" na lista
Clicar em MySQL → Próximo
```

### 3. Configurar Conexão
```
Configurações:
┌─────────────────────────────────┐
│ Host/IP:        localhost        │
│ Port:           3306            │
│ Database:       [deixar em branco]│
│ Username:       root            │
│ Password:       [sua senha]      │
│ Save password:  ✅               │
└─────────────────────────────────┘
```

### 4. Testar Conexão
```
Botão: "Test Connection..."
Se sucesso: ✅ "Database connection successful!"
```

### 5. Finalizar
```
Clique: "Finish"
```

**Pronto!** MySQL conectado no DBeaver! 🎉

---

## Passo 4: Criar o Banco de Dados

### Opção A: Via DBeaver (Visual)
1. No painel esquerdo, expanda **Connections → MySQL**
2. Clique direito em **MySQL**
3. **New → Database**
4. Nome: `infant_id_platform`
5. Character Set: `utf8mb4`
6. Charset: `utf8mb4_unicode_ci`
7. Clique: **Finish**

### Opção B: Via SQL (Terminal)
```sql
CREATE DATABASE infant_id_platform 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

---

## Passo 5: Criar as Tabelas

### Via Python (Recomendado)
```powershell
# No PowerShell, vá até a pasta backend:
cd "c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\backend"

# Execute:
C:\Python314\python.exe -c "
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Tabelas criadas com sucesso!')
"
```

### Via DBeaver (SQL Script)
1. Clique direito em **infant_id_platform** → **SQL Editor**
2. Execute o script em `backend/database/schema.sql`

---

## Passo 6: Verificar Tabelas no DBeaver

1. Expanda: **Connections → MySQL → infant_id_platform → Tables**
2. Você deve ver:
   - ✅ users
   - ✅ courses
   - ✅ lessons
   - ✅ hospitals
   - ✅ documents
   - ✅ etc...

---

## Passo 7: Rodar o Servidor com Banco Real

```powershell
# Terminal PowerShell:
cd "c:\Users\maximo.silva\Desktop\Desevolvimento\Alura Jovem Believer\backend"

# Rodar servidor:
C:\Python314\python.exe run.py
```

**Pronto!** Servidor rodando com MySQL! ✅

---

## 📝 Arquivo .env (Checklist)

Garantir que o `.env` tem estas variáveis:

```env
# .env na pasta backend/
FLASK_ENV=development
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_NAME=infant_id_platform
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET=jwt-secret-key-change
```

Arquivo deve estar em:
```
backend/
├── .env              ← AQUI!
├── app/
├── run.py
└── ...
```

---

## 🔧 Troubleshooting

### Erro: "Access denied for user 'root'@'localhost'"
- Verificar senha no `.env`
- Verificar senha no DBeaver

### Erro: "Can't connect to MySQL server"
- MySQL está rodando? (Services → MySQL80)
- Porta 3306 correta?
- Firewall bloqueando?

### Erro: "Database 'infant_id_platform' doesn't exist"
- Criar database via DBeaver ou SQL
- Verificar em: **DBeaver → Connections → MySQL → Databases**

---

## ✅ Checklist Final

- [ ] MySQL Server instalado
- [ ] MySQL rodando (Services)
- [ ] DBeaver instalado
- [ ] DBeaver conectado ao MySQL
- [ ] Database `infant_id_platform` criado
- [ ] Tabelas criadas (via Python ou SQL)
- [ ] `.env` configurado
- [ ] Servidor rodando com `python run.py`
- [ ] DBeaver mostrando as tabelas

---

## 🎯 Próximo Passo

Uma vez que tudo estiver configurado:

```
1. Abra http://localhost:5000
2. Registre um novo usuário
3. Veja os dados aparecendo em tempo real no DBeaver!
```

**DBeaver pronto para monitora seu banco em tempo real!** 🚀

