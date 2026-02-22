"""
Análise de Simetria Bilateral
Avalia o equilíbrio entre os lados esquerdo e direito do corpo.
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class SimetriaBilateral:
    """Resultado da análise de simetria de uma região"""
    esquerda: float
    direita: float
    diferenca_absoluta: float
    diferenca_percentual: float
    classificacao: str  # "Ideal", "Atenção", "Assimetria Relevante"
    status: str  # "excelente", "atencao", "alerta"


def calcular_simetria_regiao(
    valor_esquerdo: Optional[float],
    valor_direito: Optional[float]
) -> Optional[SimetriaBilateral]:
    """
    Calcula a simetria entre duas medidas laterais.
    
    Fórmula: |Direita - Esquerda| ÷ Maior Valor × 100
    
    Classificação:
    - < 5% = Ideal
    - 5-10% = Atenção
    - > 10% = Assimetria Relevante
    
    Args:
        valor_esquerdo: Medida do lado esquerdo
        valor_direito: Medida do lado direito
        
    Returns:
        Objeto SimetriaBilateral ou None se medidas não disponíveis
    """
    if not valor_esquerdo or not valor_direito:
        return None
    
    diferenca_abs = abs(valor_direito - valor_esquerdo)
    maior_valor = max(valor_esquerdo, valor_direito)
    diferenca_pct = round((diferenca_abs / maior_valor) * 100, 2)
    
    # Classificação
    if diferenca_pct < 5:
        classificacao = "Ideal"
        status = "excelente"
    elif diferenca_pct <= 10:
        classificacao = "Atenção"
        status = "atencao"
    else:
        classificacao = "Assimetria Relevante"
        status = "alerta"
    
    return SimetriaBilateral(
        esquerda=valor_esquerdo,
        direita=valor_direito,
        diferenca_absoluta=round(diferenca_abs, 1),
        diferenca_percentual=diferenca_pct,
        classificacao=classificacao,
        status=status
    )


def calcular_todas_simetrias(medidas: Dict[str, float]) -> Dict[str, Optional[SimetriaBilateral]]:
    """
    Calcula a simetria de todas as regiões bilaterais.
    
    Args:
        medidas: Dicionário com todas as medidas corporais
        
    Returns:
        Dicionário com análises de simetria por região
    """
    simetrias = {}
    
    # Braços relaxados
    simetrias['braco_relaxado'] = calcular_simetria_regiao(
        medidas.get('braco_relaxado_esquerdo'),
        medidas.get('braco_relaxado_direito')
    )
    
    # Braços contraídos
    simetrias['braco_contraido'] = calcular_simetria_regiao(
        medidas.get('braco_contraido_esquerdo'),
        medidas.get('braco_contraido_direito')
    )
    
    # Antebraços
    simetrias['antebraco'] = calcular_simetria_regiao(
        medidas.get('antebraco_esquerdo'),
        medidas.get('antebraco_direito')
    )
    
    # Coxas
    simetrias['coxa'] = calcular_simetria_regiao(
        medidas.get('coxa_esquerda'),
        medidas.get('coxa_direita')
    )
    
    # Panturrilhas
    simetrias['panturrilha'] = calcular_simetria_regiao(
        medidas.get('panturrilha_esquerda'),
        medidas.get('panturrilha_direita')
    )
    
    # Larguras ósseas
    simetrias['largura_punho'] = calcular_simetria_regiao(
        medidas.get('largura_punho_esquerdo'),
        medidas.get('largura_punho_direito')
    )
    
    simetrias['largura_cotovelo'] = calcular_simetria_regiao(
        medidas.get('largura_cotovelo_esquerdo'),
        medidas.get('largura_cotovelo_direito')
    )
    
    simetrias['largura_joelho'] = calcular_simetria_regiao(
        medidas.get('largura_joelho_esquerdo'),
        medidas.get('largura_joelho_direito')
    )
    
    simetrias['largura_tornozelo'] = calcular_simetria_regiao(
        medidas.get('largura_tornozelo_esquerdo'),
        medidas.get('largura_tornozelo_direito')
    )
    
    return simetrias


def calcular_score_simetria_geral(simetrias: Dict[str, Optional[SimetriaBilateral]]) -> float:
    """
    Calcula um score geral de simetria (0-100).
    
    Penaliza assimetrias acima de 10%.
    
    Args:
        simetrias: Dicionário com análises de simetria
        
    Returns:
        Score de 0 a 100
    """
    scores = []
    
    for regiao, simetria in simetrias.items():
        if simetria is None:
            continue
        
        # Calcular score da região
        if simetria.diferenca_percentual < 5:
            score_regiao = 100
        elif simetria.diferenca_percentual <= 10:
            # Interpolação linear: 5% = 100, 10% = 70
            score_regiao = 100 - ((simetria.diferenca_percentual - 5) * 6)
        else:
            # Penalização progressiva acima de 10%
            score_regiao = max(0, 70 - ((simetria.diferenca_percentual - 10) * 5))
        
        scores.append(score_regiao)
    
    if not scores:
        return 0
    
    score_medio = sum(scores) / len(scores)
    return round(score_medio, 1)
