-- Criação do banco de dados para o sistema de medidas corporais

-- Tabela de contas (login)
CREATE TABLE IF NOT EXISTS contas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de usuários (dados pessoais vinculados à conta)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    conta_id INTEGER NOT NULL REFERENCES contas(id) ON DELETE CASCADE,
    data_nascimento DATE NOT NULL,
    sexo VARCHAR(20) NOT NULL,
    altura DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(conta_id)
);

-- Tabela de avaliações
CREATE TABLE IF NOT EXISTS avaliacoes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    data DATE NOT NULL,
    peso DECIMAL(5,2) NOT NULL,
    
    -- Medidas corporais principais
    pescoco DECIMAL(5,2),
    ombros DECIMAL(5,2),  -- circunferência dos ombros
    peitoral DECIMAL(5,2),
    cintura DECIMAL(5,2),
    abdomen DECIMAL(5,2),
    quadril DECIMAL(5,2),
    
    -- Medidas corporais legadas (mantidas para compatibilidade)
    braco_relaxado DECIMAL(5,2),
    braco_contraido DECIMAL(5,2),
    antebraco DECIMAL(5,2),
    punho DECIMAL(5,2),
    coxa_proximal DECIMAL(5,2),
    coxa_medial DECIMAL(5,2),
    coxa_distal DECIMAL(5,2),
    panturrilha DECIMAL(5,2),
    tornozelo DECIMAL(5,2),
    
    -- NOVAS MEDIDAS BILATERAIS (Sistema Renovado 2026)
    braco_relaxado_esquerdo DECIMAL(5,2),
    braco_relaxado_direito DECIMAL(5,2),
    braco_contraido_esquerdo DECIMAL(5,2),
    braco_contraido_direito DECIMAL(5,2),
    antebraco_esquerdo DECIMAL(5,2),
    antebraco_direito DECIMAL(5,2),
    coxa_esquerda DECIMAL(5,2),
    coxa_direita DECIMAL(5,2),
    panturrilha_esquerda DECIMAL(5,2),
    panturrilha_direita DECIMAL(5,2),
    
    -- LARGURAS/DIÂMETROS ÓSSEOS (Camada 1 - Estrutura Genética)
    largura_ombros DECIMAL(5,2),      -- largura biacromial (estrutura óssea)
    largura_quadril DECIMAL(5,2),     -- largura bi-ilíaca
    largura_punho_esquerdo DECIMAL(5,2),
    largura_punho_direito DECIMAL(5,2),
    largura_cotovelo_esquerdo DECIMAL(5,2),
    largura_cotovelo_direito DECIMAL(5,2),
    largura_joelho_esquerdo DECIMAL(5,2),
    largura_joelho_direito DECIMAL(5,2),
    largura_tornozelo_esquerdo DECIMAL(5,2),
    largura_tornozelo_direito DECIMAL(5,2),
    
    -- Resultados calculados (armazenados para histórico)
    imc DECIMAL(5,2),
    gordura_corporal DECIMAL(5,2),
    massa_magra DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(usuario_id, data)
);

-- Índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_usuarios_conta ON usuarios(conta_id);
CREATE INDEX IF NOT EXISTS idx_avaliacoes_usuario ON avaliacoes(usuario_id);
CREATE INDEX IF NOT EXISTS idx_avaliacoes_data ON avaliacoes(data);
-- ============================================================================
-- MIGRAÇÃO PARA SISTEMA RENOVADO (2026)
-- ============================================================================
-- Use este script se você JÁ TEM um banco de dados criado e quer adicionar
-- as novas colunas SEM PERDER DADOS existentes.
-- 
-- ATENÇÃO: Este script NÃO mexe em contas, usuários ou senhas!
-- ============================================================================

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

-- Sucesso! Banco atualizado mantendo todos os dados existentes
-- Contas, usuários e senhas permaneceram intactos