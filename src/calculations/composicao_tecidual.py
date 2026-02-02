"""
Módulo de Composição Tecidual
Calcula e divide o peso corporal em diferentes componentes teciduais
"""

from typing import Dict, Any


def calcular_composicao_tecidual(peso: float, percentual_gordura: float, sexo: str) -> Dict[str, Any]:
    """
    Calcula a composição tecidual do corpo.
    
    Args:
        peso: Peso corporal em kg
        percentual_gordura: Percentual de gordura corporal
        sexo: 'M' para masculino, 'F' para feminino
        
    Returns:
        Dicionário com massas em kg e percentuais
    """
    # Massa gorda
    massa_gorda = peso * (percentual_gordura / 100)
    
    # Massa magra (tudo que não é gordura)
    massa_magra = peso - massa_gorda
    
    # Massa óssea (15% massa magra para homens, 12% para mulheres)
    percentual_osseo = 0.15 if sexo == 'M' else 0.12
    massa_ossea = massa_magra * percentual_osseo
    
    # Massa muscular (massa magra - massa óssea)
    massa_muscular = massa_magra - massa_ossea
    
    # Outros tecidos (órgãos, pele, água extracelular, etc)
    outros_tecidos = peso - (massa_gorda + massa_muscular + massa_ossea)
    
    # Calcular percentuais
    percentual_muscular = (massa_muscular / peso) * 100
    percentual_osseo_total = (massa_ossea / peso) * 100
    percentual_outros = (outros_tecidos / peso) * 100
    
    return {
        'massa_gorda_kg': round(massa_gorda, 2),
        'massa_muscular_kg': round(massa_muscular, 2),
        'massa_ossea_kg': round(massa_ossea, 2),
        'outros_tecidos_kg': round(outros_tecidos, 2),
        'percentual_gordura': round(percentual_gordura, 2),
        'percentual_muscular': round(percentual_muscular, 2),
        'percentual_osseo': round(percentual_osseo_total, 2),
        'percentual_outros': round(percentual_outros, 2),
        'peso_total': peso
    }
