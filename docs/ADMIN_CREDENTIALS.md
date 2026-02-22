# Credenciais de Administrador

## Conta Admin Criada

**Nome de usuário:** Vilacio  
**Senha:** 123456  

Esta conta tem privilégios de administrador e pode:
- Ver estatísticas do sistema
- Visualizar o banco de dados completo
- Acessar o painel de administração clicando no ícone de engrenagem (⚙️) no header

## Como Logar

1. Acesse a página de login
2. Digite o nome de usuário: `Vilacio`
3. Digite a senha: `123456`
4. Clique em "Entrar"

## Funcionalidades Admin

Após o login, você verá um botão roxo com ícone de engrenagem no header. Clique nele para:

### Aba Estatísticas
- Total de contas cadastradas
- Total de avaliações realizadas
- Modo de armazenamento (JSON ou PostgreSQL)

### Aba Banco de Dados
- Visualização completa do arquivo `usuarios.json`
- Todas as contas (senhas ocultadas por segurança)
- Todos os usuários cadastrados
- Todas as avaliações com resultados

## Outros Admins

Os seguintes nomes de usuário também têm privilégios de admin:
- admin
- Admin
- ADMIN
- Vilacio

Para adicionar mais admins, edite a lista `ADMINS` no arquivo `web/app.py`.
