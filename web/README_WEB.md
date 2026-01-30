# 🌐 Interface Web - Medidas Fit

Sistema web completo para gerenciamento de medidas corporais com interface moderna e intuitiva.

## 🎨 Características da Interface

### Design
- ✅ Layout responsivo e moderno
- ✅ Tema claro e escuro (alternável)
- ✅ Cores azul e branco
- ✅ Mapa anatômico interativo
- ✅ Animações suaves

### Funcionalidades
- ✅ Cadastro de usuário com perfil completo
- ✅ Formulário de medidas com validação
- ✅ Cálculo automático de idade
- ✅ Salvamento em JSON local
- ✅ Visualização de avaliações em cards
- ✅ Análise completa com todos os índices
- ✅ Sistema de notificações (toast)
- ✅ Modo offline-first

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
# No diretório raiz do projeto
pip install flask flask-cors
```

Ou use o arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Iniciar o Servidor

```bash
# Entre no diretório web
cd web

# Execute o servidor Flask
python app.py
```

O servidor iniciará em: **http://localhost:5000**

### 3. Acessar a Interface

Abra seu navegador e acesse:
```
http://localhost:5000
```

## 📖 Guia de Uso

### Primeiro Acesso

1. **Configurar Perfil**
   - Clique no ícone de usuário (canto superior direito)
   - Preencha: nome, data de nascimento, sexo, altura, email
   - A idade é calculada automaticamente
   - Escolha o tema (claro ou escuro)
   - Clique em "Salvar Configurações"

2. **Criar Primeira Avaliação**
   - Preencha os campos de medidas (peso, cintura e quadril são obrigatórios)
   - Clique nos pontos do mapa anatômico para focar no campo correspondente
   - Adicione um objetivo (opcional)
   - Clique em "Salvar Avaliação"

3. **Visualizar Resultados**
   - Os cards com as avaliações aparecerão do lado direito
   - Cada card mostra: IMC, % Gordura, RCQ, RCA, Somatotipo, etc.
   - Análise de simetria aparece no final do card

### Funcionalidades

#### Mapa Anatômico Interativo
- Pontos clicáveis indicam onde medir
- Ao clicar em um ponto, o campo correspondente recebe foco
- Representação visual das circunferências

#### Temas
- **Claro**: fundo branco, ideal para ambientes iluminados
- **Escuro**: fundo escuro, confortável para uso noturno
- A preferência é salva com o perfil do usuário

#### Cards de Avaliação
Cada card exibe:
- Data da avaliação
- Peso atual
- IMC e classificação
- Percentual de gordura e classificação
- Massa gorda e magra
- RCQ (Relação Cintura-Quadril)
- RCA (Relação Cintura-Altura)
- Somatotipo (tipo corporal)
- Pontuação estética
- Análise de simetria e proporções

#### Gerenciamento
- **Deletar**: clique no ícone de lixeira no card
- **Histórico**: todas as avaliações ficam salvas

## 🗂️ Estrutura de Arquivos

```
web/
├── app.py                  # Servidor Flask (backend)
├── templates/
│   └── index.html         # HTML principal
├── static/
│   ├── css/
│   │   └── style.css      # Estilos e temas
│   └── js/
│       └── app.js         # Lógica JavaScript
└── README_WEB.md          # Este arquivo
```

## 💾 Armazenamento de Dados

Os dados são salvos em:
```
data/usuarios.json
```

Estrutura do JSON:
```json
{
  "usuario": {
    "nome": "João Silva",
    "sexo": "M",
    "data_nascimento": "1990-05-15",
    "email": "joao@email.com",
    "altura": 178,
    "idade": 35,
    "tema": "light"
  },
  "avaliacoes": [
    {
      "id": "2026-01-29T10:30:00",
      "data": "2026-01-29",
      "medidas": { ... },
      "resultados": { ... }
    }
  ]
}
```

## 🎨 Personalização de Cores

### Tema Claro
```css
--primary-color: #1976d2;  /* Azul principal */
--background: #f5f7fa;      /* Fundo claro */
--surface: #ffffff;         /* Cards brancos */
```

### Tema Escuro
```css
--primary-color: #42a5f5;  /* Azul claro */
--background: #121212;      /* Fundo escuro */
--surface: #1e1e1e;         /* Cards escuros */
```

Para personalizar, edite: `web/static/css/style.css`

## 🔌 API Endpoints

### GET /api/usuario
Retorna dados do usuário atual

### POST /api/usuario
Cria novo usuário

### PUT /api/usuario
Atualiza dados do usuário

### GET /api/avaliacoes
Lista todas as avaliações

### POST /api/avaliacoes
Cria nova avaliação
```json
{
  "medidas": {
    "peso": 75.5,
    "cintura": 85,
    "quadril": 100,
    ...
  },
  "objetivo": "Hipertrofia"
}
```

### DELETE /api/avaliacoes/:id
Deleta uma avaliação

## 📱 Responsividade

A interface é totalmente responsiva:
- **Desktop**: layout em 2 colunas (formulário | cards)
- **Tablet**: layout adaptativo
- **Mobile**: layout em coluna única

## 🔒 Segurança

⚠️ **Nota**: Esta é uma versão inicial focada em funcionalidade local.

Para produção, considere:
- Adicionar autenticação de usuários
- HTTPS
- Validação mais robusta no backend
- Sanitização de inputs
- Rate limiting
- CSRF protection

## 🚧 Futuras Implementações

- [ ] Sistema de múltiplos usuários com login
- [ ] Comparação visual entre avaliações
- [ ] Gráficos de evolução temporal
- [ ] Exportação de relatórios em PDF
- [ ] Fotos de progresso
- [ ] Integração com wearables
- [ ] Lembretes de avaliação
- [ ] Metas e objetivos personalizados

## 🐛 Troubleshooting

### Erro: "Módulo flask não encontrado"
```bash
pip install flask flask-cors
```

### Porta 5000 já em uso
Edite `app.py` e mude a porta:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Dados não salvam
Verifique permissões na pasta `data/`:
```bash
# No diretório raiz
mkdir -p data
chmod 755 data
```

### Tema não muda
Limpe o cache do navegador (Ctrl + Shift + Del)

## 💡 Dicas

1. **Padronização**: Meça sempre no mesmo horário (manhã, em jejum)
2. **Consistência**: Use os mesmos pontos de medição
3. **Frequência**: Avalie a cada 2-4 semanas
4. **Hidratação**: Mantenha-se hidratado para medidas precisas
5. **Backup**: Faça backup do arquivo `data/usuarios.json`

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este guia
2. Consulte os logs do servidor no terminal
3. Verifique o console do navegador (F12)

---

**Desenvolvido com ❤️ para profissionais da saúde e fitness**
