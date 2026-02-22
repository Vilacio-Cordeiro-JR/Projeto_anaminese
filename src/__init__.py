"""
Sistema de Gerenciamento e Análise de Medidas Corporais
"""

__version__ = "1.0.0"
__author__ = "Sistema de Medidas Fit"

from .models import Usuario, Medidas, Avaliacao
from .services import AnalisadorAvaliacao, ComparadorAvaliacoes
from .calculations import (
    calcular_imc,
    calcular_gordura_us_navy,
    calcular_rcq,
    calcular_rca,
    calcular_proporcoes
)

__all__ = [
    'Usuario',
    'Medidas',
    'Avaliacao',
    'AnalisadorAvaliacao',
    'ComparadorAvaliacoes',
    'calcular_imc',
    'calcular_gordura_us_navy',
    'calcular_rcq',
    'calcular_rca',
    'calcular_proporcoes'
]
