-- ============================================================================
-- MIGRAÇÃO: SISTEMA RENOVADO (22/02/2026)
-- ============================================================================
-- Script para atualizar banco de dados EXISTENTE com novas features
-- 
-- ⚠️  IMPORTANTE:
-- - Este script NÃO mexe em contas, usuários ou senhas
-- - Apenas adiciona novas colunas na tabela 'avaliacoes'
-- - Dados existentes são preservados
-- - Seguro para rodar em produção
-- 
-- 📊 O QUE SERÁ ADICIONADO:
-- - 10 colunas de medidas bilaterais (esquerda/direita)
-- - 10 colunas de larguras ósseas (estrutura genética)
-- 
-- 🚀 COMO USAR:
-- No PostgreSQL (Vercel/Neon/local):
--   psql -d seu_banco -f migration_sistema_renovado.sql
-- 
-- Ou copie e cole no console do Vercel Postgres
-- ============================================================================

BEGIN;

-- Adicionar colunas bilaterais (se não existirem)
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS braco_relaxado_esquerdo DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS braco_relaxado_direito DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS braco_contraido_esquerdo DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS braco_contraido_direito DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS antebraco_esquerdo DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS antebraco_direito DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS coxa_esquerda DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS coxa_direita DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS panturrilha_esquerda DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS panturrilha_direita DECIMAL(5,2);

-- Adicionar colunas de larguras ósseas (se não existirem)
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS largura_ombros DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS largura_quadril DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS largura_punho_esquerdo DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS largura_punho_direito DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS largura_cotovelo_esquerdo DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS largura_cotovelo_direito DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS largura_joelho_esquerdo DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS largura_joelho_direito DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS largura_tornozelo_esquerdo DECIMAL(5,2);
ALTER TABLE avaliacoes ADD COLUMN IF NOT EXISTS largura_tornozelo_direito DECIMAL(5,2);

COMMIT;

-- ✅ Migração concluída com sucesso!
-- ✅ Banco atualizado mantendo todos os dados existentes
-- ✅ Contas, usuários e senhas permaneceram intactos
-- ✅ Sistema pronto para as novas features

-- Para verificar as novas colunas:
-- SELECT column_name, data_type FROM information_schema.columns 
-- WHERE table_name = 'avaliacoes' ORDER BY ordinal_position;
