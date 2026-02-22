#!/bin/bash
# Script de inicialização do sistema web
# Medidas Fit - Sistema de Análise Corporal

echo "========================================"
echo "  MEDIDAS FIT - Sistema Web"
echo "========================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python não encontrado!"
    echo "Instale Python 3.8+ de https://www.python.org/"
    exit 1
fi

echo "[OK] Python encontrado"
echo ""

# Verificar/instalar dependências
echo "Verificando dependências..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "[INSTALANDO] Flask e Flask-CORS..."
    pip3 install flask flask-cors
    echo ""
else
    echo "[OK] Dependências instaladas"
    echo ""
fi

# Navegar para o diretório web
cd web

# Iniciar servidor
echo "========================================"
echo "  Iniciando servidor..."
echo "========================================"
echo ""
echo "Acesse: http://localhost:5000"
echo ""
echo "Pressione Ctrl+C para encerrar"
echo "========================================"
echo ""

python3 app.py
