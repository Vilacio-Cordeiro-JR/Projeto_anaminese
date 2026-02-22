# Configuração do Banco de Dados no Vercel

## Problema Atual
As avaliações são perdidas após refresh porque o Vercel é **serverless** e **stateless**. Arquivos locais (como `usuarios.json`) não persistem.

## Solução: Configurar PostgreSQL

### Opção 1: Vercel Postgres (Recomendado)

1. **Acesse o projeto no Vercel:**
   - https://vercel.com/dashboard

2. **Vá para a aba "Storage":**
   - Clique no projeto `projeto-anaminese`
   - Clique em "Storage" no menu lateral
   - Clique em "Create Database"
   - Selecione "Postgres"

3. **Crie o banco:**
   - Nome: `medidas-fit-db`
   - Region: `São Paulo` ou mais próxima
   - Clique em "Create"

4. **O Vercel criará automaticamente:**
   - `POSTGRES_URL` (variável de ambiente)
   - Conexão SSL configurada

5. **Execute o SQL de inicialização:**
   - Na aba "Data" do banco, clique em "Query"
   - Cole o conteúdo do arquivo `database.sql`
   - Execute

6. **Redeploy o projeto:**
   ```bash
   git commit --allow-empty -m "Trigger redeploy with database"
   git push origin main
   ```

### Opção 2: Supabase (Grátis)

1. **Crie conta no Supabase:**
   - https://supabase.com/

2. **Crie novo projeto:**
   - Nome: `medidas-fit`
   - Database Password: [escolha uma senha forte]
   - Region: South America

3. **Execute o SQL:**
   - Vá para SQL Editor
   - Cole o conteúdo de `database.sql`
   - Execute

4. **Copie a connection string:**
   - Settings → Database → Connection string → URI
   - Formato: `postgresql://postgres:[senha]@[host]:5432/postgres`

5. **Configure no Vercel:**
   - Vá para Settings → Environment Variables
   - Adicione:
     - Name: `DATABASE_URL`
     - Value: [cole a connection string]
   - Scope: Production, Preview, Development

6. **Redeploy:**
   ```bash
   git commit --allow-empty -m "Trigger redeploy with Supabase"
   git push origin main
   ```

### Opção 3: Railway (Grátis temporário)

1. **Acesse Railway.app:**
   - https://railway.app/

2. **Crie novo projeto:**
   - "+ New Project"
   - "Provision PostgreSQL"

3. **Copie a connection string:**
   - Clique no banco
   - Connect → Copy Connection String

4. **Configure no Vercel** (mesma forma que Supabase)

## Verificar se o Banco está Funcionando

Após configurar, acesse:
```
https://projeto-anaminese.vercel.app/
```

1. Faça login
2. Crie uma avaliação
3. **Pressione F5** (refresh)
4. A avaliação deve permanecer visível ✅

## Comandos Úteis

### Verificar logs no Vercel:
```bash
vercel logs https://projeto-anaminese.vercel.app/
```

### Testar localmente com banco:
```bash
# No terminal, defina a variável de ambiente
export DATABASE_URL="postgresql://usuario:senha@host:5432/database"

# Inicie o servidor
python web/app.py
```

## Troubleshooting

### Erro: "relation 'contas' does not exist"
- Execute o arquivo `database.sql` no banco

### Erro: "could not connect to server"
- Verifique se DATABASE_URL está configurada corretamente
- Teste a conexão: `psql $DATABASE_URL`

### Ainda perde dados após F5
- Verifique se USE_DATABASE está True:
  - Adicione print em `app.py`: `print("USE_DATABASE:", USE_DATABASE)`
  - Veja logs no Vercel

### Avaliações não aparecem
- Verifique se a tabela `avaliacoes` tem dados:
```sql
SELECT * FROM avaliacoes;
```

## Status Atual

🔴 **Sem banco configurado** - Dados perdidos no refresh  
🟡 **Banco configurado, sem dados** - Execute `database.sql`  
🟢 **Funcionando** - Dados persistem após refresh

## Suporte

Se tiver problemas, verifique:
1. Variável `DATABASE_URL` está no Vercel?
2. O arquivo `database.sql` foi executado?
3. Os logs do Vercel mostram erros de conexão?
