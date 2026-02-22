"""
Cálculo de Médias Bilaterais
Centraliza o cálculo de médias entre medidas esquerda/direita.
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class MediasBilaterais:
    """Armazena todas as médias calculadas de medidas bilaterais"""
    
    # Circunferências musculares
    braco_relaxado: Optional[float] = None
    braco_contraido: Optional[float] = None
    antebraco: Optional[float] = None
    coxa: Optional[float] = None
    panturrilha: Optional[float] = None
    
    # Larguras ósseas
    largura_punho: Optional[float] = None
    largura_cotovelo: Optional[float] = None
    largura_joelho: Optional[float] = None
    largura_tornozelo: Optional[float] = None


def calcular_media_bilateral(esquerda: Optional[float], direita: Optional[float]) -> Optional[float]:
    """
    Calcula a média entre duas medidas laterais.
    
    Args:
        esquerda: Medida do lado esquerdo
        direita: Medida do lado direito
        
    Returns:
        Média arredondada para 1 casa decimal, ou None se ambas forem None
    """
    if esquerda is not None and direita is not None:
        return round((esquerda + direita) / 2, 1)
    elif esquerda is not None:
        return esquerda
    elif direita is not None:
        return direita
    
    return None


def calcular_todas_medias(medidas: Dict[str, float]) -> MediasBilaterais:
    """
    Calcula todas as médias bilaterais possíveis.
    
    Args:
        medidas: Dicionário com todas as medidas corporais
        
    Returns:
        Objeto MediasBilaterais com todas as médias calculadas
    """
    return MediasBilaterais(
        # Circunferências musculares
        braco_relaxado=calcular_media_bilateral(
            medidas.get('braco_relaxado_esquerdo'),
            medidas.get('braco_relaxado_direito')
        ),
        braco_contraido=calcular_media_bilateral(
            medidas.get('braco_contraido_esquerdo'),
            medidas.get('braco_contraido_direito')
        ),
        antebraco=calcular_media_bilateral(
            medidas.get('antebraco_esquerdo'),
            medidas.get('antebraco_direito')
        ),
        coxa=calcular_media_bilateral(
            medidas.get('coxa_esquerda'),
            medidas.get('coxa_direita')
        ),
        panturrilha=calcular_media_bilateral(
            medidas.get('panturrilha_esquerda'),
            medidas.get('panturrilha_direita')
        ),
        
        # Larguras ósseas
        largura_punho=calcular_media_bilateral(
            medidas.get('largura_punho_esquerdo'),
            medidas.get('largura_punho_direito')
        ),
        largura_cotovelo=calcular_media_bilateral(
            medidas.get('largura_cotovelo_esquerdo'),
            medidas.get('largura_cotovelo_direito')
        ),
        largura_joelho=calcular_media_bilateral(
            medidas.get('largura_joelho_esquerdo'),
            medidas.get('largura_joelho_direito')
        ),
        largura_tornozelo=calcular_media_bilateral(
            medidas.get('largura_tornozelo_esquerdo'),
            medidas.get('largura_tornozelo_direito')
        ),
    )
