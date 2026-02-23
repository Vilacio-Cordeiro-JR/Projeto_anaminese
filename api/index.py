"""
Entrypoint para Vercel
"""
import sys
import os

# Adiciona o diretório raiz ao path (parent do diretório api/)
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

# Importa o app Flask
from web.app import app

# Vercel precisa de uma variável 'app'
# O Flask já está configurado, só exportamos
