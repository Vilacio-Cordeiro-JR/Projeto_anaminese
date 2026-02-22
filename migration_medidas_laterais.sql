-- Migração: Adiciona medidas separadas de esquerda e direita
-- Data: 2026-02-22
-- Descrição: Adiciona colunas para medidas separadas de braços, antebraços, coxas e panturrilhas

-- Adicionar novas colunas para medidas separadas
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

-- Migrar dados existentes (duplicar valores únicos para ambos os lados)
UPDATE avaliacoes SET braco_relaxado_esquerdo = braco_relaxado WHERE braco_relaxado IS NOT NULL AND braco_relaxado_esquerdo IS NULL;
UPDATE avaliacoes SET braco_relaxado_direito = braco_relaxado WHERE braco_relaxado IS NOT NULL AND braco_relaxado_direito IS NULL;
UPDATE avaliacoes SET braco_contraido_esquerdo = braco_contraido WHERE braco_contraido IS NOT NULL AND braco_contraido_esquerdo IS NULL;
UPDATE avaliacoes SET braco_contraido_direito = braco_contraido WHERE braco_contraido IS NOT NULL AND braco_contraido_direito IS NULL;
UPDATE avaliacoes SET antebraco_esquerdo = antebraco WHERE antebraco IS NOT NULL AND antebraco_esquerdo IS NULL;
UPDATE avaliacoes SET antebraco_direito = antebraco WHERE antebraco IS NOT NULL AND antebraco_direito IS NULL;
UPDATE avaliacoes SET coxa_esquerda = coxa_proximal WHERE coxa_proximal IS NOT NULL AND coxa_esquerda IS NULL;
UPDATE avaliacoes SET coxa_direita = coxa_proximal WHERE coxa_proximal IS NOT NULL AND coxa_direita IS NULL;
UPDATE avaliacoes SET panturrilha_esquerda = panturrilha WHERE panturrilha IS NOT NULL AND panturrilha_esquerda IS NULL;
UPDATE avaliacoes SET panturrilha_direita = panturrilha WHERE panturrilha IS NOT NULL AND panturrilha_direita IS NULL;

-- Nota: As colunas antigas (braco_relaxado, braco_contraido, antebraco, coxa_proximal, panturrilha)
-- são mantidas para compatibilidade com dados históricos.
-- Novos registros devem usar as colunas separadas.
