"""
Módulo de Cálculos Corporais
Funções para calcular índices antropométricos e estimativas de composição corporal.
"""

from .imc import calcular_imc, classificar_imc
from .gordura import calcular_gordura_us_navy, classificar_gordura, calcular_massa_gorda, calcular_massa_magra
from .indices import calcular_rcq, calcular_rca, classificar_rcq, classificar_rca
from .proporcoes import calcular_proporcoes, analisar_simetria, calcular_pontuacao_estetica
from .somatotipo import classificar_somatotipo, obter_recomendacoes_somatotipo

__all__ = [
    'calcular_imc',
    'classificar_imc',
    'calcular_gordura_us_navy',
    'classificar_gordura',
    'calcular_massa_gorda',
    'calcular_massa_magra',
    'calcular_rcq',
    'calcular_rca',
    'classificar_rcq',
    'classificar_rca',
    'calcular_proporcoes',
    'analisar_simetria',
    'calcular_pontuacao_estetica',
    'classificar_somatotipo',
    'obter_recomendacoes_somatotipo'
]
