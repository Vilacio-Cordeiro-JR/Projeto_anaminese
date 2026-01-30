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
    
    -- Medidas corporais
    pescoco DECIMAL(5,2),
    ombros DECIMAL(5,2),
    peitoral DECIMAL(5,2),
    cintura DECIMAL(5,2),
    abdomen DECIMAL(5,2),
    quadril DECIMAL(5,2),
    braco_relaxado DECIMAL(5,2),
    braco_contraido DECIMAL(5,2),
    antebraco DECIMAL(5,2),
    punho DECIMAL(5,2),
    coxa_proximal DECIMAL(5,2),
    coxa_medial DECIMAL(5,2),
    coxa_distal DECIMAL(5,2),
    panturrilha DECIMAL(5,2),
    tornozelo DECIMAL(5,2),
    
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
