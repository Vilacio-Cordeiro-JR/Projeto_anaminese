# 📊 Guia de Banco de Dados - Sistema Renovado

## 📁 Arquivos SQL Disponíveis

### 1. `database.sql` (Banco Completo)
**Quando usar:** Criação inicial do banco de dados do zero

```bash
psql -d seu_banco -f database.sql
```

**O que faz:**
- ✅ Cria tabela `contas` (login e senha)
- ✅ Cria tabela `usuarios` (dados pessoais)
- ✅ Cria tabela `avaliacoes` (medidas corporais + novas features)
- ✅ Cria índices de performance
- ✅ Inclui script de migração no final

**Contém:**
- Todas as medidas bilaterais (esq/dir)
- Todas as larguras ósseas (10 campos novos)
- Compatibilidade com campos legados

---

### 2. `migration_sistema_renovado.sql` (Migração Segura)
**Quando usar:** Você JÁ tem um banco e quer atualizar SEM PERDER DADOS

```bash
psql -d seu_banco -f migration_sistema_renovado.sql
```

**O que faz:**
- ✅ Adiciona 10 colunas de medidas bilaterais
- ✅ Adiciona 10 colunas de larguras ósseas
- ⚠️ **NÃO mexe em contas, usuários ou senhas**
- ⚠️ **Preserva TODOS os dados existentes**

**Seguro para produção!**

---

### 3. `migration_medidas_laterais.sql` (Migração Antiga)
**Status:** Legado - use `migration_sistema_renovado.sql` que é mais completo

**O que faz:**
- Adiciona apenas medidas bilaterais (sem larguras ósseas)
- Migra dados antigos para o novo formato
- Mantido para compatibilidade

---

## 🚀 Como Usar no Vercel

### Opção 1: Via Dashboard Vercel
1. Acesse: https://vercel.com/dashboard
2. Entre no seu projeto
3. Vá em **Storage** → **Postgres**
4. Clique em **Query**
5. Cole o conteúdo de `migration_sistema_renovado.sql`
6. Clique em **Run**

### Opção 2: Via CLI Vercel
```bash
# Conectar ao banco
vercel postgres connect

# Rodar migração
\i migration_sistema_renovado.sql
```

---

## 🔄 Estrutura das Novas Colunas

### Medidas Bilaterais (Circunferências)
```
braco_relaxado_esquerdo      DECIMAL(5,2)
braco_relaxado_direito       DECIMAL(5,2)
braco_contraido_esquerdo     DECIMAL(5,2)
braco_contraido_direito      DECIMAL(5,2)
antebraco_esquerdo          DECIMAL(5,2)
antebraco_direito           DECIMAL(5,2)
coxa_esquerda               DECIMAL(5,2)
coxa_direita                DECIMAL(5,2)
panturrilha_esquerda        DECIMAL(5,2)
panturrilha_direita         DECIMAL(5,2)
```

### Larguras Ósseas (Estrutura Genética)
```
largura_ombros              DECIMAL(5,2)  -- biacromial
largura_quadril             DECIMAL(5,2)  -- bi-ilíaca
largura_punho_esquerdo      DECIMAL(5,2)
largura_punho_direito       DECIMAL(5,2)
largura_cotovelo_esquerdo   DECIMAL(5,2)
largura_cotovelo_direito    DECIMAL(5,2)
largura_joelho_esquerdo     DECIMAL(5,2)
largura_joelho_direito      DECIMAL(5,2)
largura_tornozelo_esquerdo  DECIMAL(5,2)
largura_tornozelo_direito   DECIMAL(5,2)
```

---

## ⚠️ IMPORTANTE

### ✅ O que é SEGURO fazer:
- Rodar `migration_sistema_renovado.sql` em produção
- Adicionar novas colunas com `ALTER TABLE ... IF NOT EXISTS`
- Consultar dados existentes
- Fazer backup antes de qualquer alteração

### ❌ O que NÃO fazer:
- Rodar `database.sql` em banco existente (vai dar erro de tabelas duplicadas)
- Deletar colunas antigas (pode quebrar histórico)
- Alterar tipos de dados sem migração
- Mexer nas tabelas `contas` ou `usuarios` sem necessidade

---

## 🔍 Verificar Migração

Após rodar a migração, verifique se deu certo:

```sql
-- Ver todas as colunas da tabela avaliacoes
SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns 
WHERE table_name = 'avaliacoes' 
ORDER BY ordinal_position;

-- Contar registros preservados
SELECT COUNT(*) as total_avaliacoes FROM avaliacoes;

-- Verificar se as novas colunas existem
SELECT 
    COUNT(braco_relaxado_esquerdo) as tem_bilateral,
    COUNT(largura_ombros) as tem_larguras
FROM avaliacoes;
```

---

## 📦 Backup Antes de Migrar

**SEMPRE faça backup antes de qualquer alteração em produção!**

```bash
# PostgreSQL local
pg_dump seu_banco > backup_antes_migracao.sql

# Vercel (export via dashboard)
# Storage → Postgres → Export → Download SQL
```

---

## 🐛 Resolver Problemas

### Erro: "column already exists"
**Solução:** Já está atualizado! Pode ignorar.

### Erro: "relation avaliacoes does not exist"
**Solução:** Use `database.sql` para criar o banco do zero.

### Erro: "permission denied"
**Solução:** Verifique se tem permissão de ALTER TABLE.

---

## 📞 Suporte

Documentação completa: `SISTEMA_RENOVADO.md`

**Features implementadas:**
- ✅ Scores modulares (5 dimensões)
- ✅ Ideais musculares adaptativos
- ✅ Índices estruturais (genética)
- ✅ Análise de simetria bilateral
- ✅ Sistema de classificação inteligente
