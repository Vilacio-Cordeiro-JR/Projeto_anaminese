# ARQUITETURA DO SISTEMA

## Visão Geral

O sistema segue uma arquitetura em camadas bem definida:

```
┌─────────────────────────────────────┐
│         Interface/Exemplo           │  ← exemplo.py
├─────────────────────────────────────┤
│       Camada de Serviços            │  ← services/
│  (Lógica de Negócio)                │
├─────────────────────────────────────┤
│       Camada de Cálculos            │  ← calculations/
│  (Algoritmos e Fórmulas)            │
├─────────────────────────────────────┤
│       Camada de Validação           │  ← validators/
│  (Regras de Negócio)                │
├─────────────────────────────────────┤
│       Camada de Modelo              │  ← models/
│  (Domínio)                          │
└─────────────────────────────────────┘
```

## Fluxo de Dados

### 1. Criação de Avaliação
```
Usuario → Medidas → Avaliacao → AnalisadorAvaliacao → Resultados
```

### 2. Processamento
```
AnalisadorAvaliacao.processar_avaliacao():
  1. Valida medidas (validators)
  2. Calcula IMC (calculations/imc)
  3. Calcula % gordura (calculations/gordura)
  4. Calcula índices (calculations/indices)
  5. Analisa proporções (calculations/proporcoes)
  6. Classifica somatotipo (calculations/somatotipo)
  7. Armazena resultados na avaliacao
  8. Retorna dicionário completo
```

### 3. Comparação
```
ComparadorAvaliacoes.comparar_duas_avaliacoes():
  1. Calcula diferenças de medidas
  2. Calcula diferenças de índices
  3. Analisa evolução qualitativa
  4. Classifica evolução geral
  5. Gera relatório comparativo
```

## Módulos Principais

### models/
Contém as classes de domínio:
- **Usuario**: representa pessoa avaliada
- **Medidas**: armazena medidas antropométricas
- **Avaliacao**: representa uma avaliação em uma data

### calculations/
Funções puras de cálculo:
- **imc.py**: IMC e classificações
- **gordura.py**: % gordura US Navy
- **indices.py**: RCQ, RCA, conicidade
- **proporcoes.py**: análise de proporções e simetria
- **somatotipo.py**: classificação de tipos corporais

### services/
Lógica de negócio:
- **analisador.py**: processa avaliações completas
- **comparador.py**: compara e analisa evolução

### validators/
Validação de dados:
- **validadores.py**: valida medidas, usuários e avaliações

## Princípios de Design

### 1. Separação de Responsabilidades
Cada módulo tem uma responsabilidade única e bem definida.

### 2. Baixo Acoplamento
Módulos dependem apenas de interfaces, não de implementações.

### 3. Alta Coesão
Funcionalidades relacionadas estão agrupadas.

### 4. Extensibilidade
Fácil adicionar novos cálculos ou análises sem modificar código existente.

### 5. Testabilidade
Funções puras facilitam testes unitários.

## Padrões Utilizados

- **Dataclasses**: para modelos de dados imutáveis
- **Type Hints**: para documentação e verificação de tipos
- **Enums**: para valores categóricos (Sexo, Somatotipo)
- **Factory Methods**: para criação de objetos complexos
- **Service Layer**: separação entre domínio e lógica de negócio

## Expansões Futuras

### Persistência
```python
# Interface genérica
class RepositorioUsuarios:
    def salvar(self, usuario: Usuario) -> str
    def buscar(self, id: str) -> Usuario
    def listar_todos(self) -> List[Usuario]
    
# Implementações concretas
class RepositorioSQL(RepositorioUsuarios): ...
class RepositorioNoSQL(RepositorioUsuarios): ...
class RepositorioJSON(RepositorioUsuarios): ...
```

### API Web
```python
# FastAPI example
@app.post("/avaliacoes/")
async def criar_avaliacao(avaliacao_dto: AvaliacaoDTO):
    avaliacao = converter_dto(avaliacao_dto)
    resultado = AnalisadorAvaliacao.processar_avaliacao(avaliacao, usuario)
    return resultado
```

### Interface Gráfica
```python
# Streamlit example
import streamlit as st

st.title("Sistema de Medidas Corporais")
nome = st.text_input("Nome")
peso = st.number_input("Peso (kg)")
# ...
```

## Considerações de Performance

### Otimizações Implementadas
- Cálculos lazy (apenas quando necessário)
- Cache de resultados na avaliação
- Validações progressivas (fail-fast)

### Para Grandes Volumes
- Usar processamento em batch
- Implementar cache de cálculos repetitivos
- Considerar processamento assíncrono

## Segurança

### Validações
- Todos os inputs são validados
- Limites razoáveis para medidas
- Verificação de consistência

### Dados Sensíveis
- Considerar criptografia para dados pessoais
- Implementar controle de acesso
- Logs de auditoria
