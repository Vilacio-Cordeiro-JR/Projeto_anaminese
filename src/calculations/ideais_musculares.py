"""
Ideais Musculares Ajustados por Estrutura
Sistema adaptativo que considera a base óssea do indivíduo.
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class IdeaisMusculares:
    """Armazena os ideais musculares calculados"""
    
    # Ideais ajustados por estrutura
    pescoco: Optional[float] = None
    ombros: Optional[float] = None  # circunferência
    peitoral: Optional[float] = None
    braco_contraido: Optional[float] = None
    antebraco: Optional[float] = None
    coxa: Optional[float] = None
    panturrilha: Optional[float] = None
    
    # Metadados
    fator_estrutural_aplicado: Optional[float] = None
    baseado_em: str = "altura"  # "altura" ou "estrutura"


def calcular_ideais_base_por_altura(altura: float, sexo: str) -> Dict[str, float]:
    """
    Calcula ideais musculares básicos baseados apenas na altura.
    Usa proporções clássicas de bodybuilding.
    
    Args:
        altura: Altura em cm
        sexo: 'M' ou 'F'
        
    Returns:
        Dicionário com ideais base
    """
    # Proporções clássicas (John McCallum e outros)
    # Referência: punho como base
    
    if sexo.upper() in ['M', 'MASCULINO']:
        # Proporções masculinas
        punho_base = altura * 0.100  # ~10% da altura
        
        return {
            'pescoco': round(punho_base * 2.52, 1),      # 2.52x punho
            'ombros': round(altura * 0.629, 1),           # 62.9% altura
            'peitoral': round(altura * 0.577, 1),         # 57.7% altura
            'braco_contraido': round(punho_base * 2.52, 1),  # igual pescoço
            'antebraco': round(punho_base * 2.10, 1),     # 2.1x punho
            'coxa': round(punho_base * 3.52, 1),          # 3.52x punho
            'panturrilha': round(punho_base * 2.52, 1),   # igual pescoço/braço
        }
    else:
        # Proporções femininas (mais conservadoras)
        punho_base = altura * 0.095
        
        return {
            'pescoco': round(punho_base * 2.30, 1),
            'ombros': round(altura * 0.600, 1),
            'peitoral': round(altura * 0.550, 1),
            'braco_contraido': round(punho_base * 2.30, 1),
            'antebraco': round(punho_base * 1.95, 1),
            'coxa': round(punho_base * 3.20, 1),
            'panturrilha': round(punho_base * 2.30, 1),
        }


def ajustar_ideais_por_estrutura(
    ideais_base: Dict[str, float],
    fator_estrutural: Optional[float]
) -> Dict[str, float]:
    """
    Ajusta os ideais musculares baseado no fator estrutural do indivíduo.
    
    Se o indivíduo tem estrutura óssea maior que a média (fator > 1.0),
    os ideais musculares devem ser proporcionalmente maiores.
    
    Args:
        ideais_base: Ideais calculados por altura
        fator_estrutural: Fator multiplicador (1.0 = estrutura média)
        
    Returns:
        Ideais ajustados
    """
    if not fator_estrutural or fator_estrutural == 1.0:
        return ideais_base
    
    # Ajustar todos os ideais proporcionalmente
    ideais_ajustados = {}
    for regiao, valor_base in ideais_base.items():
        ideais_ajustados[regiao] = round(valor_base * fator_estrutural, 1)
    
    return ideais_ajustados


def calcular_todos_ideais(
    altura: float,
    sexo: str,
    fator_estrutural: Optional[float] = None
) -> IdeaisMusculares:
    """
    Calcula todos os ideais musculares, ajustando pela estrutura se disponível.
    
    Args:
        altura: Altura em cm
        sexo: 'M' ou 'F'
        fator_estrutural: Fator estrutural calculado (opcional)
        
    Returns:
        Objeto IdeaisMusculares completo
    """
    # 1. Calcular ideais base por altura
    ideais_base = calcular_ideais_base_por_altura(altura, sexo)
    
    # 2. Ajustar pela estrutura se disponível
    if fator_estrutural:
        ideais_finais = ajustar_ideais_por_estrutura(ideais_base, fator_estrutural)
        baseado_em = "estrutura"
    else:
        ideais_finais = ideais_base
        baseado_em = "altura"
    
    return IdeaisMusculares(
        pescoco=ideais_finais['pescoco'],
        ombros=ideais_finais['ombros'],
        peitoral=ideais_finais['peitoral'],
        braco_contraido=ideais_finais['braco_contraido'],
        antebraco=ideais_finais['antebraco'],
        coxa=ideais_finais['coxa'],
        panturrilha=ideais_finais['panturrilha'],
        fator_estrutural_aplicado=fator_estrutural,
        baseado_em=baseado_em
    )


def calcular_diferenca_do_ideal(
    valor_real: Optional[float],
    valor_ideal: Optional[float]
) -> Dict[str, Optional[float]]:
    """
    Calcula a diferença entre o valor real e o ideal.
    
    Args:
        valor_real: Medida real do indivíduo
        valor_ideal: Medida ideal calculada
        
    Returns:
        Dicionário com diferença absoluta, percentual e classificação
    """
    if not valor_real or not valor_ideal:
        return {
            'diferenca_absoluta': None,
            'diferenca_percentual': None,
            'classificacao': 'Não Medido',
            'status': 'neutro'
        }
    
    diferenca_absoluta = round(valor_real - valor_ideal, 1)
    diferenca_percentual = round(((valor_real - valor_ideal) / valor_ideal) * 100, 1)
    
    # Classificação e status
    if abs(diferenca_percentual) <= 5:
        classificacao = "Ideal"
        status = "excelente"
    elif diferenca_percentual < -5:
        # Abaixo do ideal
        if diferenca_percentual < -15:
            classificacao = "Muito Subdesenvolvido"
            status = "subdesenvolvido"
        else:
            classificacao = "Subdesenvolvido"
            status = "atencao"
    else:
        # Acima do ideal
        if diferenca_percentual > 15:
            classificacao = "Muito Acima"
            status = "excesso"
        else:
            classificacao = "Acima do Ideal"
            status = "bom"
    
    return {
        'diferenca_absoluta': diferenca_absoluta,
        'diferenca_percentual': diferenca_percentual,
        'classificacao': classificacao,
        'status': status
    }
