"""
Análise de proporções corporais e simetria
"""

from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
from ..utils import obter_media_lateral


@dataclass
class Proporcoes:
    """Armazena as proporções corporais calculadas"""
    # Relações entre circunferências
    ombro_cintura: Optional[float] = None
    peitoral_cintura: Optional[float] = None
    braco_panturrilha: Optional[float] = None
    coxa_panturrilha: Optional[float] = None
    
    # Proporções baseadas na altura
    cintura_altura: Optional[float] = None  # % da altura
    peitoral_altura: Optional[float] = None
    coxa_altura: Optional[float] = None
    panturrilha_altura: Optional[float] = None
    
    # Simetria (diferença entre lados)
    simetria_bracos: Optional[float] = None  # contraído vs relaxado


def calcular_proporcoes(medidas: Dict[str, float]) -> Proporcoes:
    """
    Calcula todas as proporções corporais possíveis com as medidas disponíveis.
    
    Args:
        medidas: Dicionário com as medidas corporais
            Chaves esperadas: altura, cintura, peitoral, ombros, 
            braco_relaxado_esquerdo, braco_relaxado_direito,
            braco_contraido_esquerdo, braco_contraido_direito,
            coxa_esquerda, coxa_direita, panturrilha_esquerda, panturrilha_direita, etc.
    
    Returns:
        Objeto Proporcoes com todos os cálculos possíveis
    """
    prop = Proporcoes()
    
    altura = medidas.get('altura')
    cintura = medidas.get('cintura')
    peitoral = medidas.get('peitoral')
    ombros = medidas.get('ombros')
    braco_rel = obter_media_lateral(medidas, 'braco_relaxado')
    braco_cont = obter_media_lateral(medidas, 'braco_contraido')
    coxa = obter_media_lateral(medidas, 'coxa')
    panturrilha = obter_media_lateral(medidas, 'panturrilha')
    
    # Relações entre circunferências
    if ombros and cintura and cintura > 0:
        prop.ombro_cintura = round(ombros / cintura, 2)
    
    if peitoral and cintura and cintura > 0:
        prop.peitoral_cintura = round(peitoral / cintura, 2)
    
    if braco_cont and panturrilha and panturrilha > 0:
        prop.braco_panturrilha = round(braco_cont / panturrilha, 2)
    
    if coxa and panturrilha and panturrilha > 0:
        prop.coxa_panturrilha = round(coxa / panturrilha, 2)
    
    # Proporções baseadas na altura
    if altura and altura > 0:
        if cintura:
            prop.cintura_altura = round((cintura / altura) * 100, 1)
        if peitoral:
            prop.peitoral_altura = round((peitoral / altura) * 100, 1)
        if coxa:
            prop.coxa_altura = round((coxa / altura) * 100, 1)
        if panturrilha:
            prop.panturrilha_altura = round((panturrilha / altura) * 100, 1)
    
    # Simetria dos braços
    if braco_cont and braco_rel and braco_rel > 0:
        prop.simetria_bracos = round(braco_cont / braco_rel, 2)
    
    return prop


def analisar_simetria(proporcoes: Proporcoes) -> Dict[str, str]:
    """
    Analisa as proporções e fornece feedback sobre simetria corporal.
    
    PROPORÇÕES IDEAIS (referências):
    - Ombros: ~1.6x cintura
    - Peitoral: ~1.4x cintura
    - Braço ≈ Panturrilha (1.0)
    - Cintura: 45-47% da altura
    - Peitoral: 55-60% da altura
    - Coxa: 30-33% da altura
    - Panturrilha: 20-22% da altura
    - Simetria braço: 1.05-1.15 (5-15% maior quando contraído)
    
    Args:
        proporcoes: Objeto Proporcoes calculado
        
    Returns:
        Dicionário com análises e feedbacks
    """
    analise = {}
    
    # Análise ombro/cintura
    if proporcoes.ombro_cintura:
        if proporcoes.ombro_cintura >= 1.6:
            analise['ombro_cintura'] = "Excelente proporção (formato V)"
        elif proporcoes.ombro_cintura >= 1.4:
            analise['ombro_cintura'] = "Boa proporção"
        else:
            analise['ombro_cintura'] = "Desenvolver ombros ou reduzir cintura"
    
    # Análise peitoral/cintura
    if proporcoes.peitoral_cintura:
        if proporcoes.peitoral_cintura >= 1.4:
            analise['peitoral_cintura'] = "Excelente desenvolvimento torácico"
        elif proporcoes.peitoral_cintura >= 1.2:
            analise['peitoral_cintura'] = "Bom desenvolvimento"
        else:
            analise['peitoral_cintura'] = "Desenvolver peitoral"
    
    # Análise braço/panturrilha (simetria)
    if proporcoes.braco_panturrilha:
        diff = abs(proporcoes.braco_panturrilha - 1.0)
        if diff <= 0.05:
            analise['braco_panturrilha'] = "Simetria perfeita"
        elif diff <= 0.10:
            analise['braco_panturrilha'] = "Boa simetria"
        elif proporcoes.braco_panturrilha > 1.0:
            analise['braco_panturrilha'] = "Braços dominantes - treinar panturrilhas"
        else:
            analise['braco_panturrilha'] = "Panturrilhas dominantes - treinar braços"
    
    # Análise proporções baseadas em altura
    if proporcoes.cintura_altura:
        if 45 <= proporcoes.cintura_altura <= 47:
            analise['cintura_altura'] = "Proporção ideal"
        elif proporcoes.cintura_altura < 45:
            analise['cintura_altura'] = "Cintura fina (excelente)"
        else:
            analise['cintura_altura'] = "Reduzir gordura abdominal"
    
    if proporcoes.peitoral_altura:
        if 55 <= proporcoes.peitoral_altura <= 60:
            analise['peitoral_altura'] = "Proporção ideal"
        elif proporcoes.peitoral_altura < 55:
            analise['peitoral_altura'] = "Desenvolver peitoral"
        else:
            analise['peitoral_altura'] = "Desenvolvimento acima do ideal"
    
    # Análise contração do braço
    if proporcoes.simetria_bracos:
        ganho_percentual = (proporcoes.simetria_bracos - 1) * 100
        if 5 <= ganho_percentual <= 15:
            analise['simetria_bracos'] = f"Contração normal ({ganho_percentual:.1f}%)"
        elif ganho_percentual < 5:
            analise['simetria_bracos'] = f"Pouca hipertrofia ({ganho_percentual:.1f}%)"
        else:
            analise['simetria_bracos'] = f"Excelente hipertrofia ({ganho_percentual:.1f}%)"
    
    return analise


def calcular_pontuacao_estetica(proporcoes: Proporcoes) -> Tuple[float, str]:
    """
    Calcula uma pontuação estética baseada nas proporções corporais.
    
    Sistema de pontos baseado em proximidade dos ideais clássicos.
    
    Args:
        proporcoes: Objeto Proporcoes calculado
        
    Returns:
        Tupla (pontuacao, classificacao)
        Pontuação de 0 a 100
    """
    pontos = 0
    total_metricas = 0
    
    # Ombro/Cintura (peso 25%)
    if proporcoes.ombro_cintura:
        total_metricas += 1
        if proporcoes.ombro_cintura >= 1.6:
            pontos += 25
        elif proporcoes.ombro_cintura >= 1.5:
            pontos += 20
        elif proporcoes.ombro_cintura >= 1.4:
            pontos += 15
        else:
            pontos += max(0, (proporcoes.ombro_cintura / 1.6) * 25)
    
    # Peitoral/Cintura (peso 20%)
    if proporcoes.peitoral_cintura:
        total_metricas += 1
        if proporcoes.peitoral_cintura >= 1.4:
            pontos += 20
        elif proporcoes.peitoral_cintura >= 1.3:
            pontos += 15
        else:
            pontos += max(0, (proporcoes.peitoral_cintura / 1.4) * 20)
    
    # Braço/Panturrilha (peso 15%)
    if proporcoes.braco_panturrilha:
        total_metricas += 1
        diff = abs(proporcoes.braco_panturrilha - 1.0)
        pontos += max(0, 15 * (1 - diff * 2))
    
    # Cintura/Altura (peso 20%)
    if proporcoes.cintura_altura:
        total_metricas += 1
        if 45 <= proporcoes.cintura_altura <= 47:
            pontos += 20
        else:
            desvio = min(abs(proporcoes.cintura_altura - 46), 10)
            pontos += max(0, 20 - desvio * 2)
    
    # Simetria braços (peso 20%)
    if proporcoes.simetria_bracos:
        total_metricas += 1
        ganho = (proporcoes.simetria_bracos - 1) * 100
        if 5 <= ganho <= 15:
            pontos += 20
        else:
            desvio = min(abs(ganho - 10), 10)
            pontos += max(0, 20 - desvio * 2)
    
    # Normaliza para 0-100
    if total_metricas > 0:
        pontuacao = (pontos / total_metricas) * (100 / 100)
    else:
        pontuacao = 0
    
    # Classificação
    if pontuacao >= 90:
        classificacao = "Excepcional"
    elif pontuacao >= 80:
        classificacao = "Excelente"
    elif pontuacao >= 70:
        classificacao = "Muito Bom"
    elif pontuacao >= 60:
        classificacao = "Bom"
    elif pontuacao >= 50:
        classificacao = "Médio"
    else:
        classificacao = "A Desenvolver"
    
    return (round(pontuacao, 1), classificacao)
