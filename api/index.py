"""
Entrypoint para Vercel
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa o app Flask
from web.app import app

# Vercel precisa de uma variável 'app'
# O Flask já está configurado, só exportamos
