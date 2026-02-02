"""
Módulo de Score Estético Corporal
Calcula pontuação 0-100 baseada em múltiplos fatores corporais
"""

from typing import Dict, Any


def calcular_score_gordura(percentual_gordura: float, sexo: str) -> float:
    """
    Calcula score baseado no percentual de gordura (30% do total).
    Faixa ideal: 10-15% homens, 18-23% mulheres
    """
    if sexo == 'M':
        ideal_min, ideal_max = 10, 15
    else:
        ideal_min, ideal_max = 18, 23
    
    if ideal_min <= percentual_gordura <= ideal_max:
        return 30.0  # Score máximo
    elif percentual_gordura < ideal_min:
        # Penalização por estar muito baixo
        diferenca = ideal_min - percentual_gordura
        return max(0, 30 - (diferenca * 2))
    else:
        # Penalização por estar acima
        diferenca = percentual_gordura - ideal_max
        return max(0, 30 - (diferenca * 1.5))


def calcular_score_proporcao(medida_real: float, medida_ideal: float, peso_maximo: float) -> float:
    """
    Calcula score de uma proporção específica.
    """
    if not medida_real:
        return 0
    
    ratio = medida_real / medida_ideal
    
    # Score máximo quando ratio entre 0.95 e 1.05
    if 0.95 <= ratio <= 1.05:
        return peso_maximo
    elif 0.90 <= ratio <= 1.10:
        return peso_maximo * 0.8
    elif 0.85 <= ratio <= 1.15:
        return peso_maximo * 0.6
    elif 0.80 <= ratio <= 1.20:
        return peso_maximo * 0.4
    else:
        return peso_maximo * 0.2


def calcular_score_simetria(regioes: Dict[str, Dict]) -> float:
    """
    Calcula score de simetria e equilíbrio (15% do total).
    Baseado na média das diferenças entre real e ideal.
    """
    diferencas = []
    
    for regiao, dados in regioes.items():
        if dados.get('real') and dados.get('ratio'):
            # Quanto mais próximo de 1.0, melhor
            diferenca_abs = abs(1.0 - dados['ratio'])
            diferencas.append(diferenca_abs)
    
    if not diferencas:
        return 0
    
    # Média das diferenças
    media_diferenca = sum(diferencas) / len(diferencas)
    
    # Converter para score (0.0 = perfeito, quanto menor melhor)
    if media_diferenca <= 0.05:
        return 15.0
    elif media_diferenca <= 0.10:
        return 12.0
    elif media_diferenca <= 0.15:
        return 9.0
    elif media_diferenca <= 0.20:
        return 6.0
    else:
        return max(0, 15 - (media_diferenca * 50))


def calcular_score_gordura_central(cintura: float, altura: float) -> float:
    """
    Calcula score de gordura central (10% do total).
    Baseado no índice cintura/altura.
    """
    rca = cintura / altura
    
    if rca <= 0.45:
        return 10.0
    elif rca <= 0.49:
        return 8.0
    elif rca <= 0.54:
        return 5.0
    elif rca <= 0.60:
        return 2.0
    else:
        return 0


def calcular_score_estetico(
    percentual_gordura: float,
    medidas: Dict[str, float],
    altura: float,
    sexo: str,
    mapa_corporal: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calcula score estético corporal completo (0-100).
    
    Componentes:
    - 30%: Percentual de gordura
    - 25%: Relação ombro/cintura
    - 20%: Relação peitoral/cintura
    - 15%: Simetria e equilíbrio
    - 10%: Gordura central
    
    Args:
        percentual_gordura: Percentual de gordura corporal
        medidas: Dicionário com medidas corporais
        altura: Altura em cm
        sexo: 'M' ou 'F'
        mapa_corporal: Dados do mapa corporal
        
    Returns:
        Dicionário com score total e breakdown
    """
    cintura = medidas.get('cintura', 0)
    ombros = medidas.get('ombros', 0)
    peitoral = medidas.get('peitoral', 0)
    
    # 1. Score de Gordura (30%)
    score_gordura = calcular_score_gordura(percentual_gordura, sexo)
    
    # 2. Score Ombro/Cintura (25%)
    ombro_ideal = cintura * (1.60 if sexo == 'M' else 1.40)
    score_ombro = calcular_score_proporcao(ombros, ombro_ideal, 25.0) if ombros else 0
    
    # 3. Score Peitoral/Cintura (20%)
    peitoral_ideal = cintura * (1.40 if sexo == 'M' else 1.30)
    score_peitoral = calcular_score_proporcao(peitoral, peitoral_ideal, 20.0) if peitoral else 0
    
    # 4. Score Simetria (15%)
    regioes = mapa_corporal.get('regioes', {})
    score_simetria = calcular_score_simetria(regioes)
    
    # 5. Score Gordura Central (10%)
    score_central = calcular_score_gordura_central(cintura, altura) if cintura else 0
    
    # Score total
    score_total = score_gordura + score_ombro + score_peitoral + score_simetria + score_central
    score_total = min(100, max(0, score_total))  # Limitar entre 0 e 100
    
    # Classificação
    if score_total >= 85:
        classificacao = 'Atlético'
        cor = '#20c997'
    elif score_total >= 61:
        classificacao = 'Estético'
        cor = '#51cf66'
    elif score_total >= 31:
        classificacao = 'Intermediário'
        cor = '#ffa94d'
    else:
        classificacao = 'A Desenvolver'
        cor = '#ff6b6b'
    
    return {
        'score_total': round(score_total, 1),
        'classificacao': classificacao,
        'cor': cor,
        'breakdown': {
            'gordura': round(score_gordura, 1),
            'ombro_cintura': round(score_ombro, 1),
            'peitoral_cintura': round(score_peitoral, 1),
            'simetria': round(score_simetria, 1),
            'gordura_central': round(score_central, 1)
        },
        'pesos': {
            'gordura': '30%',
            'ombro_cintura': '25%',
            'peitoral_cintura': '20%',
            'simetria': '15%',
            'gordura_central': '10%'
        }
    }
