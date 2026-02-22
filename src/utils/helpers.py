"""
Funções utilitárias compartilhadas
Evita duplicação de código entre módulos
"""

from typing import Dict, Optional


def obter_media_lateral(medidas: Dict[str, float], nome_base: str) -> Optional[float]:
    """
    Obtém a média das medidas laterais (esquerda/direita) ou a medida única se existir.
    
    Args:
        medidas: Dicionário com as medidas
        nome_base: Nome base da medida (ex: 'braco_relaxado', 'coxa', 'panturrilha')
    
    Returns:
        Média das medidas laterais ou medida única, ou None se não existir
    
    Examples:
        >>> obter_media_lateral({'braco_relaxado_esquerdo': 35, 'braco_relaxado_direito': 36}, 'braco_relaxado')
        35.5
        >>> obter_media_lateral({'coxa': 60}, 'coxa')
        60
    """
    # Tentar obter medidas separadas
    esquerda = medidas.get(f'{nome_base}_esquerdo') or medidas.get(f'{nome_base}_esquerda')
    direita = medidas.get(f'{nome_base}_direito') or medidas.get(f'{nome_base}_direita')
    
    if esquerda and direita:
        return round((esquerda + direita) / 2, 1)
    elif esquerda:
        return esquerda
    elif direita:
        return direita
    
    # Fallback para medida única (compatibilidade com dados antigos)
    return medidas.get(nome_base)
