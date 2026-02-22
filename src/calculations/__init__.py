"""
Módulo de Cálculos Corporais
Funções para calcular índices antropométricos e estimativas de composição corporal.
"""

from .imc import calcular_imc, classificar_imc
from .gordura import calcular_gordura_us_navy, classificar_gordura, calcular_massa_gorda, calcular_massa_magra
from .indices import calcular_rcq, calcular_rca, classificar_rcq, classificar_rca
from .proporcoes import calcular_proporcoes, analisar_simetria, calcular_pontuacao_estetica
from .somatotipo import classificar_somatotipo, obter_recomendacoes_somatotipo

# Novos módulos do sistema renovado
from .medias_bilaterais import calcular_todas_medias, calcular_media_bilateral, MediasBilaterais
from .indices_estruturais import (
    calcular_todos_indices_estruturais,
    calcular_indice_estrutural_superior,
    calcular_indice_robustez_ossea,
    calcular_indice_posterior,
    calcular_fator_estrutural_ombros,
    IndicesEstruturais
)
from .ideais_musculares import (
    calcular_todos_ideais,
    calcular_ideais_base_por_altura,
    ajustar_ideais_por_estrutura,
    calcular_diferenca_do_ideal,
    IdeaisMusculares
)
from .simetria import (
    calcular_todas_simetrias,
    calcular_simetria_regiao,
    calcular_score_simetria_geral,
    SimetriaBilateral
)
from .score_estetico import (
    calcular_score_superior,
    calcular_score_inferior,
    calcular_score_posterior,
    calcular_score_proporcional,
    calcular_score_composicao,
    calcular_score_geral
)

__all__ = [
    # Módulos clássicos
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
    'obter_recomendacoes_somatotipo',
    
    # Novos módulos
    'calcular_todas_medias',
    'calcular_media_bilateral',
    'MediasBilaterais',
    'calcular_todos_indices_estruturais',
    'calcular_indice_estrutural_superior',
    'calcular_indice_robustez_ossea',
    'calcular_indice_posterior',
    'calcular_fator_estrutural_ombros',
    'IndicesEstruturais',
    'calcular_todos_ideais',
    'calcular_ideais_base_por_altura',
    'ajustar_ideais_por_estrutura',
    'calcular_diferenca_do_ideal',
    'IdeaisMusculares',
    'calcular_todas_simetrias',
    'calcular_simetria_regiao',
    'calcular_score_simetria_geral',
    'SimetriaBilateral',
    'calcular_score_superior',
    'calcular_score_inferior',
    'calcular_score_posterior',
    'calcular_score_proporcional',
    'calcular_score_composicao',
    'calcular_score_geral',
]
