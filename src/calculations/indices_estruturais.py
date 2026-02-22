"""
Índices Estruturais (Camada 1)
Avalia a base óssea/esquelética do indivíduo.
Não penaliza genética, apenas classifica a estrutura.
"""

from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from .medias_bilaterais import MediasBilaterais


@dataclass
class IndicesEstruturais:
    """Armazena todos os índices estruturais calculados"""
    
    # Índice estrutural superior
    indice_estrutural_superior: Optional[float] = None
    classificacao_estrutural: Optional[str] = None  # Invertida/Neutra/Triangular
    
    # Índice de robustez óssea
    indice_robustez_ossea: Optional[float] = None
    classificacao_robustez: Optional[str] = None  # Leve/Média/Robusta
    
    # Índice posterior (costas)
    indice_posterior: Optional[float] = None
    classificacao_posterior: Optional[str] = None
    
    # Fator estrutural para ajuste de ideais
    fator_estrutural_ombros: Optional[float] = None


def calcular_indice_estrutural_superior(
    largura_ombros: Optional[float],
    largura_quadril: Optional[float]
) -> Tuple[Optional[float], Optional[str]]:
    """
    Calcula o Índice Estrutural Superior (formato do corpo).
    
    Fórmula: Largura Ombros ÷ Largura Quadril
    
    Classificação:
    - > 1.10 = Estrutura Invertida (ombros muito largos)
    - 0.95 - 1.10 = Neutra (equilibrada)
    - < 0.95 = Triangular (quadril mais largo)
    
    Args:
        largura_ombros: Largura biacromial em cm
        largura_quadril: Largura bi-ilíaca em cm
        
    Returns:
        Tupla (índice, classificação)
    """
    if not largura_ombros or not largura_quadril or largura_quadril == 0:
        return None, None
    
    indice = round(largura_ombros / largura_quadril, 3)
    
    if indice > 1.10:
        classificacao = "Estrutura Invertida"
    elif indice >= 0.95:
        classificacao = "Estrutura Neutra"
    else:
        classificacao = "Estrutura Triangular"
    
    return indice, classificacao


def calcular_indice_robustez_ossea(
    medias: MediasBilaterais,
    altura: float
) -> Tuple[Optional[float], Optional[str]]:
    """
    Calcula o Índice de Robustez Óssea.
    
    Fórmula: (Punho Médio + Tornozelo Médio) ÷ Altura
    
    Define se a estrutura óssea é leve, média ou robusta.
    Valores de referência (ajustar conforme população):
    - < 0.105 = Estrutura Leve
    - 0.105 - 0.115 = Estrutura Média
    - > 0.115 = Estrutura Robusta
    
    Args:
        medias: Objeto com médias bilaterais calculadas
        altura: Altura em cm
        
    Returns:
        Tupla (índice, classificação)
    """
    if not medias.largura_punho or not medias.largura_tornozelo or altura == 0:
        return None, None
    
    indice = round((medias.largura_punho + medias.largura_tornozelo) / altura, 4)
    
    if indice < 0.105:
        classificacao = "Estrutura Leve"
    elif indice <= 0.115:
        classificacao = "Estrutura Média"
    else:
        classificacao = "Estrutura Robusta"
    
    return indice, classificacao


def calcular_indice_posterior(
    circunferencia_ombros: Optional[float],
    largura_ombros: Optional[float]
) -> Tuple[Optional[float], Optional[str]]:
    """
    Calcula o Índice Posterior (desenvolvimento das costas).
    
    Fórmula: Circunferência Ombros ÷ Largura Ombros
    
    Mede o volume muscular real sobre a base estrutural óssea.
    Quanto maior, mais desenvolvido está o dorso.
    
    Valores de referência:
    - < 2.8 = Subdesenvolvido
    - 2.8 - 3.2 = Equilibrado
    - > 3.2 = Muito Desenvolvido
    
    Args:
        circunferencia_ombros: Circunferência dos ombros em cm
        largura_ombros: Largura biacromial em cm
        
    Returns:
        Tupla (índice, classificação)
    """
    if not circunferencia_ombros or not largura_ombros or largura_ombros == 0:
        return None, None
    
    indice = round(circunferencia_ombros / largura_ombros, 2)
    
    if indice < 2.8:
        classificacao = "Subdesenvolvido"
    elif indice <= 3.2:
        classificacao = "Equilibrado"
    else:
        classificacao = "Muito Desenvolvido"
    
    return indice, classificacao


def calcular_fator_estrutural_ombros(
    largura_ombros: Optional[float],
    altura: float,
    sexo: str
) -> Optional[float]:
    """
    Calcula o fator estrutural dos ombros para ajuste de ideais musculares.
    
    Fórmula: Largura Ombros Real ÷ Largura Média Populacional Estimada
    
    Estimativas de largura média populacional por altura e sexo:
    - Homens: altura * 0.23
    - Mulheres: altura * 0.21
    
    Args:
        largura_ombros: Largura biacromial real em cm
        altura: Altura em cm
        sexo: 'M' ou 'F'
        
    Returns:
        Fator multiplicador (1.0 = estrutura média)
    """
    if not largura_ombros or altura == 0:
        return None
    
    # Estimativa de largura média populacional
    if sexo.upper() in ['M', 'MASCULINO']:
        largura_media_estimada = altura * 0.23
    else:
        largura_media_estimada = altura * 0.21
    
    fator = round(largura_ombros / largura_media_estimada, 3)
    
    return fator


def calcular_todos_indices_estruturais(
    medidas: Dict[str, float],
    medias: MediasBilaterais,
    altura: float,
    sexo: str
) -> IndicesEstruturais:
    """
    Calcula todos os índices estruturais.
    
    Args:
        medidas: Dicionário com medidas corporais
        medias: Médias bilaterais calculadas
        altura: Altura em cm
        sexo: 'M' ou 'F'
        
    Returns:
        Objeto IndicesEstruturais com todos os cálculos
    """
    # Índice Estrutural Superior
    indice_sup, class_sup = calcular_indice_estrutural_superior(
        medidas.get('largura_ombros'),
        medidas.get('largura_quadril')
    )
    
    # Robustez Óssea
    indice_rob, class_rob = calcular_indice_robustez_ossea(medias, altura)
    
    # Índice Posterior
    indice_post, class_post = calcular_indice_posterior(
        medidas.get('ombros'),  # circunferência
        medidas.get('largura_ombros')
    )
    
    # Fator Estrutural
    fator_estrutural = calcular_fator_estrutural_ombros(
        medidas.get('largura_ombros'),
        altura,
        sexo
    )
    
    return IndicesEstruturais(
        indice_estrutural_superior=indice_sup,
        classificacao_estrutural=class_sup,
        indice_robustez_ossea=indice_rob,
        classificacao_robustez=class_rob,
        indice_posterior=indice_post,
        classificacao_posterior=class_post,
        fator_estrutural_ombros=fator_estrutural
    )
