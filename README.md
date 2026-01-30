# Sistema de Gerenciamento e Análise de Medidas Corporais

Sistema completo para registro, análise e acompanhamento de medidas antropométricas corporais, voltado para profissionais de educação física, nutricionistas e acompanhamento estético.

## 📋 Funcionalidades

### ✅ Gerenciamento de Usuários
- Cadastro completo com dados pessoais
- Histórico de avaliações
- Cálculo automático de idade

### 📏 Registro de Medidas
- **Medidas básicas**: altura, peso
- **Circunferências principais**: pescoço, peitoral, cintura, abdômen, quadril, braços, coxa, panturrilha
- **Circunferências complementares**: antebraço, ombros, punho, joelho, tornozelo

### 🧮 Cálculos Automáticos
- **IMC** (Índice de Massa Corporal)
- **% Gordura** (método US Navy)
- **RCQ** (Relação Cintura-Quadril)
- **RCA** (Relação Cintura-Altura)
- **Massa gorda e magra**
- **Proporções corporais**
- **Índice de conicidade**

### 📊 Análises Avançadas
- Classificação de somatotipos (ectomorfo, mesomorfo, endomorfo)
- Análise de simetria e proporções
- Pontuação estética baseada em proporções clássicas
- Comparação entre avaliações
- Análise de tendências temporais
- Identificação de ganhos musculares e perda de gordura

### 📈 Relatórios
- Relatório completo de avaliação individual
- Relatório comparativo entre avaliações
- Análise de evolução temporal
- Recomendações personalizadas de treino e dieta

## 🏗️ Arquitetura do Projeto

```
Projeto Medidas Fit/
│
├── src/
│   ├── models/              # Modelos de dados
│   │   ├── usuario.py       # Classe Usuario
│   │   ├── medidas.py       # Classe Medidas
│   │   └── avaliacao.py     # Classe Avaliacao
│   │
│   ├── calculations/        # Módulos de cálculo
│   │   ├── imc.py          # Cálculos de IMC
│   │   ├── gordura.py      # % de gordura (US Navy)
│   │   ├── indices.py      # RCQ, RCA, conicidade
│   │   ├── proporcoes.py   # Análise de proporções
│   │   └── somatotipo.py   # Classificação de somatotipos
│   │
│   ├── services/           # Lógica de negócio
│   │   ├── analisador.py   # Análise de avaliações
│   │   └── comparador.py   # Comparação e evolução
│   │
│   └── validators/         # Validadores
│       └── validadores.py  # Validação de dados
│
├── tests/                  # Testes unitários
├── data/                   # Dados persistidos
├── docs/                   # Documentação adicional
├── exemplo.py             # Exemplos de uso
└── README.md              # Este arquivo
```

## 🚀 Como Usar

### Opção 1: Interface Web (Recomendado) 🌐

A maneira mais fácil de usar o sistema é através da interface web moderna:

```bash
# Windows - Duplo clique ou execute:
iniciar_web.bat

# Linux/Mac:
chmod +x iniciar_web.sh
./iniciar_web.sh

# Ou manualmente:
cd web
pip install flask flask-cors
python app.py
```

Acesse: **http://localhost:5000**

**Recursos da Interface Web:**
- ✅ Mapa anatômico interativo
- ✅ Tema claro e escuro
- ✅ Salvamento automático em JSON
- ✅ Visualização de resultados em cards
- ✅ Cálculos em tempo real
- ✅ Responsivo (funciona em celular)

📖 [Guia completo da interface web](web/README_WEB.md)

### Opção 2: Python (Programático)

Para uso programático ou integração com outros sistemas:

```bash
# Não requer dependências externas - Python puro!
cd "Projeto Medidas Fit"
```

### Exemplo Básico

```python
from datetime import date
from src.models import Usuario, Medidas, Avaliacao
from src.models.usuario import Sexo
from src.services import AnalisadorAvaliacao

# 1. Criar usuário
usuario = Usuario(
    nome="João Silva",
    sexo=Sexo.MASCULINO,
    data_nascimento=date(1990, 5, 15)
)

# 2. Registrar medidas
medidas = Medidas(
    altura=178,
    peso=85,
    pescoco=38,
    cintura=88,
    quadril=100,
    peitoral=105,
    braco_contraido=38,
    panturrilha=38
)

# 3. Criar avaliação
avaliacao = Avaliacao(
    data=date.today(),
    medidas=medidas
)

# 4. Processar e obter resultados
AnalisadorAvaliacao.processar_avaliacao(avaliacao, usuario)

# 5. Gerar relatório
relatorio = AnalisadorAvaliacao.gerar_relatorio_texto(avaliacao, usuario)
print(relatorio)
```

### Exemplo Completo

Execute o arquivo de exemplo:

```bash
python exemplo.py
```

Este script demonstra:
- Criação de usuário
- Múltiplas avaliações
- Comparação entre avaliações
- Análise de tendências
- Relatórios completos

## 📐 Padronização de Medidas

### Pontos de Medição

- **Cintura**: menor circunferência entre costelas e crista ilíaca
- **Abdômen**: na linha do umbigo
- **Quadril**: maior projeção glútea
- **Braço**: ponto médio entre acrômio e olécrano
- **Coxa**: ponto médio entre virilha e joelho
- **Panturrilha**: maior circunferência

### Fórmulas Utilizadas

#### IMC
```
IMC = peso (kg) / altura² (m)
```

#### % Gordura (US Navy)
**Homens:**
```
%G = 86.010 × log10(cintura - pescoço) - 70.041 × log10(altura) + 36.76
```

**Mulheres:**
```
%G = 163.205 × log10(cintura + quadril - pescoço) - 97.684 × log10(altura) - 78.387
```

#### RCQ e RCA
```
RCQ = cintura / quadril
RCA = cintura / altura
```

## 🎯 Classificações

### IMC
- < 18.5: Abaixo do peso
- 18.5 - 24.9: Peso normal
- 25.0 - 29.9: Sobrepeso
- 30.0 - 34.9: Obesidade grau I
- 35.0 - 39.9: Obesidade grau II
- ≥ 40.0: Obesidade grau III

### RCA (Risco Cardiovascular)
- < 0.50: Saudável
- 0.50 - 0.59: Sobrepeso
- 0.60 - 0.69: Obesidade
- ≥ 0.70: Obesidade mórbida

### Somatotipos
- **Ectomorfo**: magro, metabolismo rápido
- **Mesomorfo**: atlético, boa resposta ao treino
- **Endomorfo**: tendência a acumular gordura

## 🔧 Validações

O sistema inclui validações para:
- Intervalos aceitáveis de medidas
- Consistência entre medidas relacionadas
- Datas válidas
- Dados obrigatórios

## 📱 Integração Futura

Este sistema foi projetado para fácil integração com:
- Aplicativos web (Flask, Django, FastAPI)
- Aplicativos mobile (Kivy, React Native via API)
- Dashboards (Streamlit, Dash)
- Bancos de dados (SQL, NoSQL)

## 🧪 Testes

```python
# Execute os testes (quando implementados)
python -m pytest tests/
```

## 📝 Dependências

**Nenhuma dependência externa!** O sistema usa apenas bibliotecas padrão do Python:
- `dataclasses`
- `datetime`
- `typing`
- `enum`
- `math`

## 🤝 Contribuindo

Sugestões de melhorias futuras:
- [ ] Adicionar cálculo de dobras cutâneas
- [ ] Integrar bioimpedância
- [ ] Gráficos de evolução (matplotlib/plotly)
- [ ] Persistência em banco de dados
- [ ] Interface web
- [ ] Exportação para PDF
- [ ] API REST

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente para fins educacionais e profissionais.

## ✉️ Contato

Para dúvidas ou sugestões, entre em contato.

---

**Desenvolvido com ❤️ para profissionais da saúde e fitness**
