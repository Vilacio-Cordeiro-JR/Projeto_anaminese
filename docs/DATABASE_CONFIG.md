# 🗄️ Configuração do Banco de Dados PostgreSQL

## Opções de Hospedagem Gratuita

### 1. **Vercel Postgres** (Recomendado - Integrado)
- Acesse: https://vercel.com/docs/storage/vercel-postgres
- No dashboard do Vercel, vá em "Storage" → "Create Database" → "Postgres"
- Conecte ao seu projeto
- A variável `POSTGRES_URL` será configurada automaticamente

### 2. **Supabase** (Alternativa Gratuita)
- Acesse: https://supabase.com
- Crie uma conta e um novo projeto
- Em Settings → Database, copie a Connection String (Session Mode)
- Adicione como variável de ambiente `DATABASE_URL` no Vercel

### 3. **Neon** (Alternativa Gratuita)
- Acesse: https://neon.tech
- Crie uma conta e um projeto
- Copie a connection string
- Adicione como variável de ambiente `DATABASE_URL` no Vercel

## Configuração no Vercel

1. **Adicione a variável de ambiente:**
   - Vá em Settings → Environment Variables
   - Adicione: `POSTGRES_URL` ou `DATABASE_URL`
   - Valor: sua connection string do PostgreSQL

2. **Formato da Connection String:**
   ```
   postgresql://usuario:senha@host:5432/database?sslmode=require
   ```

3. **Inicialização do Banco:**
   - Execute o script `database.sql` no seu banco PostgreSQL
   - Você pode fazer isso através do painel do Supabase, Neon ou usando o `psql`

## Executando o Script SQL

### Via Supabase:
1. No dashboard, vá em "SQL Editor"
2. Copie e cole o conteúdo de `database.sql`
3. Clique em "Run"

### Via psql (linha de comando):
```bash
psql "sua-connection-string" -f database.sql
```

## Testando Localmente

1. Crie um arquivo `.env` na raiz do projeto:
   ```
   POSTGRES_URL=sua-connection-string
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   python web/app.py
   ```

## Estrutura do Banco

### Tabela `usuarios`
- `id`: ID único do usuário
- `nome`: Nome completo
- `data_nascimento`: Data de nascimento
- `sexo`: Masculino/Feminino
- `altura`: Altura em cm
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### Tabela `avaliacoes`
- `id`: ID único da avaliação
- `usuario_id`: FK para usuarios
- `data`: Data da avaliação
- `peso`: Peso em kg
- Todas as medidas corporais em cm
- Resultados calculados (IMC, gordura, etc.)

## Migração dos Dados Existentes

Se você tem dados no `data/usuarios.json`, pode migrar manualmente ou criar um script Python para isso.
