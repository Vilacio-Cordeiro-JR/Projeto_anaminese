# ⚡ INÍCIO RÁPIDO - 5 Minutos

## 🚀 Opção 1: Interface Web (MAIS FÁCIL)

### Windows
1. Duplo clique em: **`iniciar_web.bat`**
2. Aguarde o navegador abrir
3. Pronto! 🎉

### Linux/Mac
```bash
chmod +x iniciar_web.sh
./iniciar_web.sh
```

### Manual
```bash
cd web
pip install flask flask-cors
python app.py
```

Acesse: **http://localhost:5000**

---

## 📝 Primeiro Uso (1 minuto)

1. **Configure seu perfil** (clique no ícone 👤)
   - Nome: `Seu Nome`
   - Data Nascimento: `DD/MM/AAAA`
   - Sexo: `M ou F`
   - Altura: `175` (em cm)
   - Tema: `Claro ou Escuro`
   - Clique: `Salvar Configurações`

2. **Crie sua primeira avaliação**
   - Peso: `75` kg *(obrigatório)*
   - Cintura: `85` cm *(obrigatório)*
   - Quadril: `100` cm *(obrigatório)*
   - Preencha outros campos (opcional)
   - Clique: `Salvar Avaliação`

3. **Veja os resultados!** 📊
   - Cards aparecem do lado direito
   - IMC, % Gordura, RCQ, RCA, Somatotipo
   - Análise de proporções

---

## 🎨 Recursos Principais

✅ **Mapa Anatômico Interativo** - Clique nos pontos azuis  
✅ **Tema Claro/Escuro** - Configure no perfil  
✅ **Salvamento Automático** - Tudo em JSON local  
✅ **Cálculos Instantâneos** - Resultados na hora  
✅ **Histórico Completo** - Todas as avaliações salvas  
✅ **Responsivo** - Funciona em celular  

---

## 🆘 Problemas?

### "Módulo flask não encontrado"
```bash
pip install flask flask-cors
```

### "Porta 5000 já em uso"
Edite `web/app.py`, linha final:
```python
app.run(debug=True, port=8080)  # Mude para 8080
```

### Página em branco
1. Limpe cache: `Ctrl + Shift + Del`
2. Recarregue: `Ctrl + F5`

---

## 📚 Documentação Completa

- [README Principal](../README.md) - Visão geral do sistema
- [Guia Web](web/README_WEB.md) - Detalhes da interface
- [Arquitetura](docs/ARQUITETURA.md) - Estrutura técnica
- [Fórmulas](docs/FORMULAS.md) - Cálculos e classificações
- [Demo Visual](docs/DEMO_VISUAL.md) - Screenshots e layout

---

## 🎯 Próximos Passos

1. ✅ Configure seu perfil
2. ✅ Faça sua primeira avaliação
3. 📈 Adicione avaliações regularmente (a cada 2-4 semanas)
4. 📊 Compare resultados e veja sua evolução
5. 💪 Ajuste treino e dieta baseado nos dados

---

## 💡 Dicas Profissionais

- 🕐 Avalie sempre no mesmo horário (manhã, jejum)
- 📏 Use os mesmos pontos de medição
- 📅 Reavalie a cada 2-4 semanas (não diariamente!)
- 💧 Mantenha-se bem hidratado
- 💾 Faça backup de `data/usuarios.json`

---

**Pronto para começar? Duplo clique em `iniciar_web.bat` agora! 🚀**
