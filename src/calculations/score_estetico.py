"""
Sistema de Scores Modulares
Avaliação em 5 dimensões independentes com agregação ponderada.
"""

from typing import Dict, Any, Optional
from .medias_bilaterais import MediasBilaterais
from .ideais_musculares import IdeaisMusculares, calcular_diferenca_do_ideal
from .indices_estruturais import IndicesEstruturais
from .simetria import SimetriaBilateral


def calcular_score_superior(
    medidas: Dict[str, float],
    medias: MediasBilaterais,
    ideais: IdeaisMusculares,
    simetrias: Dict[str, Optional[SimetriaBilateral]],
    largura_ombros: Optional[float]
) -> Dict[str, Any]:
    """
    Calcula Score Superior (0-100).
    
    Base:
    - Ombros (circunferência): 25%
    - Peitoral: 25%
    - Braços (contraído): 25%
    - Largura Escapular: 15%
    - Simetria braços: 10%
    
    Args:
        medidas: Medidas corporais
        medias: Médias bilaterais
        ideais: Ideais musculares ajustados
        simetrias: Análises de simetria
        largura_ombros: Largura biacromial
        
    Returns:
        Dict com score e breakdown
    """
    componentes = {}
    
    # Ombros (circunferência) - 25%
    if medidas.get('ombros') and ideais.ombros:
        diff = calcular_diferenca_do_ideal(medidas['ombros'], ideais.ombros)
        componentes['ombros'] = calcular_score_componente(diff['diferenca_percentual'], 25)
    else:
        componentes['ombros'] = 0
    
    # Peitoral - 25%
    if medidas.get('peitoral') and ideais.peitoral:
        diff = calcular_diferenca_do_ideal(medidas['peitoral'], ideais.peitoral)
        componentes['peitoral'] = calcular_score_componente(diff['diferenca_percentual'], 25)
    else:
        componentes['peitoral'] = 0
    
    # Braços (contraído) - 25%
    if medias.braco_contraido and ideais.braco_contraido:
        diff = calcular_diferenca_do_ideal(medias.braco_contraido, ideais.braco_contraido)
        componentes['bracos'] = calcular_score_componente(diff['diferenca_percentual'], 25)
    else:
        componentes['bracos'] = 0
    
    # Largura Escapular - 15%
    # Avaliar se está na faixa adequada (não penalizar, apenas avaliar desenvolvimento)
    if largura_ombros:
        # Considera adequado se > 35cm para homens, >32cm para mulheres (simplificado)
        if largura_ombros >= 35:
            componentes['largura'] = 15
        elif largura_ombros >= 32:
            componentes['largura'] = 12
        else:
            componentes['largura'] = 8
    else:
        componentes['largura'] = 0
    
    # Simetria braços - 10%
    sim_braco = simetrias.get('braco_contraido')
    if sim_braco:
        if sim_braco.diferenca_percentual < 5:
            componentes['simetria'] = 10
        elif sim_braco.diferenca_percentual <= 10:
            componentes['simetria'] = 7
        else:
            componentes['simetria'] = 4
    else:
        componentes['simetria'] = 0
    
    score_total = sum(componentes.values())
    
    return {
        'score': round(score_total, 1),
        'componentes': componentes,
        'classificacao': classificar_score(score_total)
    }


def calcular_score_inferior(
    medias: MediasBilaterais,
    ideais: IdeaisMusculares,
    simetrias: Dict[str, Optional[SimetriaBilateral]],
    quadril: Optional[float]
) -> Dict[str, Any]:
    """
    Calcula Score Inferior (0-100).
    
    Base:
    - Coxa: 35%
    - Panturrilha: 35%
    - Quadril (proporcionalidade): 20%
    - Simetria inferior: 10%
    
    Args:
        medias: Médias bilaterais
        ideais: Ideais musculares
        simetrias: Análises de simetria
        quadril: Circunferência do quadril
        
    Returns:
        Dict com score e breakdown
    """
    componentes = {}
    
    # Coxa - 35%
    if medias.coxa and ideais.coxa:
        diff = calcular_diferenca_do_ideal(medias.coxa, ideais.coxa)
        componentes['coxa'] = calcular_score_componente(diff['diferenca_percentual'], 35)
    else:
        componentes['coxa'] = 0
    
    # Panturrilha - 35%
    if medias.panturrilha and ideais.panturrilha:
        diff = calcular_diferenca_do_ideal(medias.panturrilha, ideais.panturrilha)
        componentes['panturrilha'] = calcular_score_componente(diff['diferenca_percentual'], 35)
    else:
        componentes['panturrilha'] = 0
    
    # Quadril - 20%
    if quadril:
        # Avaliar proporcionalidade (simplificado)
        if 85 <= quadril <= 110:
            componentes['quadril'] = 20
        elif 80 <= quadril <= 115:
            componentes['quadril'] = 15
        else:
            componentes['quadril'] = 10
    else:
        componentes['quadril'] = 0
    
    # Simetria inferior - 10%
    scores_simetria = []
    for regiao in ['coxa', 'panturrilha']:
        sim = simetrias.get(regiao)
        if sim:
            if sim.diferenca_percentual < 5:
                scores_simetria.append(100)
            elif sim.diferenca_percentual <= 10:
                scores_simetria.append(70)
            else:
                scores_simetria.append(40)
    
    if scores_simetria:
        componentes['simetria'] = round(sum(scores_simetria) / len(scores_simetria) * 0.10, 1)
    else:
        componentes['simetria'] = 0
    
    score_total = sum(componentes.values())
    
    return {
        'score': round(score_total, 1),
        'componentes': componentes,
        'classificacao': classificar_score(score_total)
    }


def calcular_score_posterior(
    indices_estruturais: IndicesEstruturais,
    medidas: Dict[str, float]
) -> Dict[str, Any]:
    """
    Calcula Score Posterior (0-100) - Avaliação das costas.
    
    Base:
    - Índice V (ombros/cintura): 40%
    - Índice Posterior (circ/largura): 35%
    - Largura Ombros: 25%
    
    Args:
        indices_estruturais: Índices estruturais calculados
        medidas: Medidas corporais
        
    Returns:
        Dict com score e breakdown
    """
    componentes = {}
    
    # Índice V (ombros/cintura) - 40%
    ombros_circ = medidas.get('ombros')
    cintura = medidas.get('cintura')
    if ombros_circ and cintura and cintura > 0:
        indice_v = ombros_circ / cintura
        # Ideal: > 1.4 para homens, > 1.3 para mulheres (simplificado para 1.35)
        if indice_v >= 1.40:
            componentes['indice_v'] = 40
        elif indice_v >= 1.30:
            componentes['indice_v'] = 32
        elif indice_v >= 1.20:
            componentes['indice_v'] = 24
        else:
            componentes['indice_v'] = 16
    else:
        componentes['indice_v'] = 0
    
    # Índice Posterior - 35%
    if indices_estruturais.indice_posterior:
        if indices_estruturais.classificacao_posterior == "Muito Desenvolvido":
            componentes['indice_posterior'] = 35
        elif indices_estruturais.classificacao_posterior == "Equilibrado":
            componentes['indice_posterior'] = 28
        else:
            componentes['indice_posterior'] = 18
    else:
        componentes['indice_posterior'] = 0
    
    # Largura Ombros - 25%
    if indices_estruturais.indice_estrutural_superior:
        # Avaliar desenvolvimento estrutural (não penalizar genética)
        largura = medidas.get('largura_ombros', 0)
        if largura >= 40:
            componentes['largura'] = 25
        elif largura >= 35:
            componentes['largura'] = 20
        else:
            componentes['largura'] = 15
    else:
        componentes['largura'] = 0
    
    score_total = sum(componentes.values())
    
    return {
        'score': round(score_total, 1),
        'componentes': componentes,
        'classificacao': classificar_score(score_total)
    }


def calcular_score_proporcional(
    medidas: Dict[str, float],
    altura: float
) -> Dict[str, Any]:
    """
    Calcula Score Proporcional (0-100).
    
    Base:
    - RCQ (cintura/quadril): 30%
    - RCA (cintura/altura): 30%
    - Peitoral/Cintura: 25%
    - Ombro/Cintura: 15%
    
    Args:
        medidas: Medidas corporais
        altura: Altura em cm
        
    Returns:
        Dict com score e breakdown
    """
    componentes = {}
    cintura = medidas.get('cintura')
    quadril = medidas.get('quadril')
    peitoral = medidas.get('peitoral')
    ombros = medidas.get('ombros')
    
    # RCQ - 30%
    if cintura and quadril and quadril > 0:
        rcq = cintura / quadril
        # Ideal: < 0.90 homens, < 0.85 mulheres (usar 0.87 como médio)
        if rcq <= 0.85:
            componentes['rcq'] = 30
        elif rcq <= 0.90:
            componentes['rcq'] = 24
        elif rcq <= 0.95:
            componentes['rcq'] = 18
        else:
            componentes['rcq'] = 12
    else:
        componentes['rcq'] = 0
    
    # RCA - 30%
    if cintura and altura > 0:
        rca = cintura / altura
        # Ideal: <= 0.50
        if rca <= 0.50:
            componentes['rca'] = 30
        elif rca <= 0.55:
            componentes['rca'] = 24
        elif rca <= 0.60:
            componentes['rca'] = 18
        else:
            componentes['rca'] = 12
    else:
        componentes['rca'] = 0
    
    # Peitoral/Cintura - 25%
    if peitoral and cintura and cintura > 0:
        ratio = peitoral / cintura
        # Ideal: > 1.3
        if ratio >= 1.40:
            componentes['peitoral_cintura'] = 25
        elif ratio >= 1.30:
            componentes['peitoral_cintura'] = 20
        elif ratio >= 1.20:
            componentes['peitoral_cintura'] = 15
        else:
            componentes['peitoral_cintura'] = 10
    else:
        componentes['peitoral_cintura'] = 0
    
    # Ombro/Cintura - 15%
    if ombros and cintura and cintura > 0:
        ratio = ombros / cintura
        # Ideal: > 1.4
        if ratio >= 1.50:
            componentes['ombro_cintura'] = 15
        elif ratio >= 1.40:
            componentes['ombro_cintura'] = 12
        elif ratio >= 1.30:
            componentes['ombro_cintura'] = 9
        else:
            componentes['ombro_cintura'] = 6
    else:
        componentes['ombro_cintura'] = 0
    
    score_total = sum(componentes.values())
    
    return {
        'score': round(score_total, 1),
        'componentes': componentes,
        'classificacao': classificar_score(score_total)
    }


def calcular_score_composicao(
    percentual_gordura: Optional[float],
    sexo: str,
    imc: float
) -> Dict[str, Any]:
    """
    Calcula Score de Composição Corporal (0-100).
    
    Base:
    - Percentual de gordura: 70%
    - IMC: 30%
    
    Args:
        percentual_gordura: % de gordura corporal
        sexo: 'M' ou 'F'
        imc: Índice de massa corporal
        
    Returns:
        Dict com score e breakdown
    """
    componentes = {}
    
    # Percentual de gordura - 70%
    if percentual_gordura:
        if sexo.upper() in ['M', 'MASCULINO']:
            ideal_min, ideal_max = 10, 15
        else:
            ideal_min, ideal_max = 18, 23
        
        if ideal_min <= percentual_gordura <= ideal_max:
            componentes['gordura'] = 70
        elif percentual_gordura < ideal_min:
            diff = ideal_min - percentual_gordura
            componentes['gordura'] = max(35, 70 - (diff * 4))
        else:
            diff = percentual_gordura - ideal_max
            componentes['gordura'] = max(20, 70 - (diff * 3))
    else:
        componentes['gordura'] = 0
    
    # IMC - 30%
    if 18.5 <= imc <= 24.9:
        componentes['imc'] = 30
    elif 17.0 <= imc < 18.5 or 25.0 <= imc <= 27.0:
        componentes['imc'] = 24
    elif 16.0 <= imc < 17.0 or 27.0 < imc <= 30.0:
        componentes['imc'] = 18
    else:
        componentes['imc'] = 12
    
    score_total = sum(componentes.values())
    
    return {
        'score': round(score_total, 1),
        'componentes': componentes,
        'classificacao': classificar_score(score_total)
    }


def calcular_score_geral(
    score_composicao: float,
    score_proporcional: float,
    score_superior: float,
    score_inferior: float,
    score_posterior: float
) -> Dict[str, Any]:
    """
    Calcula o Score Geral ponderado.
    
    Ponderação:
    - 30% Composição
    - 25% Proporção
    - 20% Superior
    - 15% Inferior
    - 10% Posterior
    
    Returns:
        Dict com score geral e breakdown
    """
    score_geral = (
        score_composicao * 0.30 +
        score_proporcional * 0.25 +
        score_superior * 0.20 +
        score_inferior * 0.15 +
        score_posterior * 0.10
    )
    
    return {
        'score_geral': round(score_geral, 1),
        'classificacao': classificar_score(score_geral),
        'breakdown': {
            'composicao': round(score_composicao, 1),
            'proporcional': round(score_proporcional, 1),
            'superior': round(score_superior, 1),
            'inferior': round(score_inferior, 1),
            'posterior': round(score_posterior, 1)
        },
        'pesos': {
            'composicao': '30%',
            'proporcional': '25%',
            'superior': '20%',
            'inferior': '15%',
            'posterior': '10%'
        }
    }


def calcular_score_componente(diferenca_percentual: float, peso_maximo: float) -> float:
    """
    Calcula score de um componente baseado na diferença percentual do ideal.
    
    Args:
        diferenca_percentual: Diferença % em relação ao ideal
        peso_maximo: Peso máximo deste componente no score total
        
    Returns:
        Score do componente
    """
    if abs(diferenca_percentual) <= 5:
        return peso_maximo
    elif abs(diferenca_percentual) <= 10:
        return peso_maximo * 0.80
    elif abs(diferenca_percentual) <= 15:
        return peso_maximo * 0.60
    elif abs(diferenca_percentual) <= 20:
        return peso_maximo * 0.40
    else:
        return peso_maximo * 0.20


def classificar_score(score: float) -> str:
    """Classifica um score em categorias"""
    if score >= 85:
        return 'Atlético'
    elif score >= 70:
        return 'Estético'
    elif score >= 50:
        return 'Intermediário'
    elif score >= 30:
        return 'Em Desenvolvimento'
    else:
        return 'Iniciante'
