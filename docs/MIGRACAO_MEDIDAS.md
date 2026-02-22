# Migração: Medidas Laterais (Esquerda/Direita)

## Data: 2026-02-22

## Descrição
Atualização do sistema para suportar medidas separadas de esquerda e direita para membros que possuem simetria bilateral.

## Mudanças Implementadas

### 1. Modelo de Dados (`src/models/medidas.py`)
**Antes:**
- `braco_relaxado`
- `braco_contraido`
- `antebraco`
- `coxa`
- `panturrilha`

**Depois:**
- `braco_relaxado_esquerdo` / `braco_relaxado_direito`
- `braco_contraido_esquerdo` / `braco_contraido_direito`
- `antebraco_esquerdo` / `antebraco_direito`
- `coxa_esquerda` / `coxa_direita`
- `panturrilha_esquerda` / `panturrilha_direita`

### 2. Interface Web (`web/templates/index.html`)
- Atualizado formulário com campos separados para cada lado
- Mantém labels descritivos (Ex: "Braço Relaxado Esquerdo")

### 3. Frontend JavaScript (`web/static/js/app.js`)
- Coleta de dados atualizada para novos campos
- Limpeza de formulário ajustada
- Navegação com Enter atualizada

### 4. Backend (`web/app.py`)
- Recebi dos dados atualizado para novos campos
- Compatibilidade reversa: suporta avaliações antigas

### 5. Cálculos (`src/calculations/`)
- Funções auxiliares `_obter_media_lateral()` criadas
- Cálculos agora usam média entre esquerda e direita
- Mantém compatibilidade com medidas únicas antigas

### 6. Banco de Dados
**Migração SQL:** `migration_medidas_laterais.sql`
- Adiciona novas colunas (braco_relaxado_esquerdo, etc.)
- Migra dados existentes para novos campos
- Mantém colunas antigas para compatibilidade

## Como Aplicar a Migração

### Se você usa banco de dados PostgreSQL:

```bash
# Execute o script de migração
psql -U seu_usuario -d seu_banco -f migration_medidas_laterais.sql
```

### Se você usa o sistema de arquivos JSON:

Nenhuma ação necessária. O sistema automaticamente:
- Aceita dados com formato antigo
- Aceita dados com formato novo
- Usa funções auxiliares para compatibilidade

## Benefícios

1. **Análise de Simetria**: Detectar desbalanceamentos musculares
2. **Precisão**: Medidas mais detalhadas para acompanhamento
3. **Compatibilidade**: Sistema continua funcionando com dados antigos
4. **Flexibilidade**: Permite análise unilateral ou bilateral

## Compatibilidade Reversa

O sistema mantém 100% de compatibilidade com dados antigos através de:
- Funções `_obter_media_lateral()` que tentam novos campos primeiro
- Fallback para campos antigos se novos não existirem
- Cálculos que funcionam com ambos os formatos

## Testes Recomendados

- [ ] Criar nova avaliação com medidas separadas
- [ ] Visualizar avaliação antiga (deve continuar funcionando)
- [ ] Verificar cálculos de proporções
- [ ] Testar mapa corporal
- [ ] Exportar relatórios

## Arquivos Modificados

- `web/templates/index.html`
- `web/static/js/app.js`
- `web/app.py`
- `src/models/medidas.py`
- `src/calculations/proporcoes.py`
- `src/calculations/mapa_corporal.py`
- `exemplo.py`
- `web/db.py`

## Arquivos Criados

- `migration_medidas_laterais.sql`
- `MIGRACAO_MEDIDAS.md` (este arquivo)
