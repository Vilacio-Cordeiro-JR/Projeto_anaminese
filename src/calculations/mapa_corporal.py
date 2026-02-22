"""
Módulo de Mapa Corporal
Analisa distribuição de gordura e desenvolvimento muscular por região
"""

from typing import Dict, Any, Optional


def _obter_media_lateral(medidas: Dict[str, float], nome_base: str) -> Optional[float]:
    """
    Obtém a média das medidas laterais (esquerda/direita) ou a medida única se existir.
    
    Args:
        medidas: Dicionário com as medidas
        nome_base: Nome base da medida (ex: 'braco_relaxado', 'coxa', 'panturrilha')
    
    Returns:
        Média das medidas laterais ou medida única, ou None se não existir
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
    
    # Fallback para medida única (compatibilidade)
    return medidas.get(nome_base)


def calcular_proporcoes_ideais(cintura: float, sexo: str) -> Dict[str, float]:
    """
    Calcula medidas ideais baseadas na cintura.
    
    Args:
        cintura: Circunferência da cintura em cm
        sexo: 'M' para masculino, 'F' para feminino
        
    Returns:
        Dicionário com medidas ideais em cm
    """
    if sexo == 'M':
        # Proporções masculinas
        return {
            'pescoco': round(cintura * 0.42, 1),
            'ombros': round(cintura * 1.60, 1),
            'peitoral': round(cintura * 1.40, 1),
            'cintura': round(cintura, 1),  # Referência base
            'abdomen': round(cintura * 1.05, 1),  # Abdômen ligeiramente maior
            'braco': round(cintura * 0.36, 1),
            'antebraco': round(cintura * 0.36 * 0.85, 1),
            'quadril': round(cintura * 1.12, 1),
            'coxa': round(cintura * 0.75, 1),
            'panturrilha': round(cintura * 0.36, 1)  # Igual ao braço
        }
    else:
        # Proporções femininas
        braco_ideal = cintura * 0.32
        return {
            'pescoco': round(cintura * 0.38, 1),
            'ombros': round(cintura * 1.40, 1),
            'peitoral': round(cintura * 1.30, 1),
            'cintura': round(cintura, 1),  # Referência base
            'abdomen': round(cintura * 1.03, 1),  # Abdômen próximo à cintura
            'braco': round(braco_ideal, 1),
            'antebraco': round(braco_ideal * 0.85, 1),
            'quadril': round(cintura * 1.38, 1),
            'coxa': round(cintura * 0.80, 1),
            'panturrilha': round(braco_ideal * 0.95, 1)
        }


def classificar_desenvolvimento(medida_real: float, medida_ideal: float) -> Dict[str, Any]:
    """
    Classifica o desenvolvimento muscular de uma região.
    
    Args:
        medida_real: Medida real em cm
        medida_ideal: Medida ideal em cm
        
    Returns:
        Dicionário com ratio, classificação e cor
    """
    ratio = medida_real / medida_ideal
    
    if ratio < 0.90:
        classificacao = 'subdesenvolvido'
        cor = '#ff6b6b'  # Vermelho
        descricao = 'Subdesenvolvido'
    elif ratio <= 1.10:
        classificacao = 'equilibrado'
        cor = '#51cf66'  # Verde
        descricao = 'Equilibrado'
    else:
        classificacao = 'excesso'
        cor = '#ffa94d'  # Laranja
        descricao = 'Excesso'
    
    return {
        'ratio': round(ratio, 2),
        'classificacao': classificacao,
        'descricao': descricao,
        'cor': cor,
        'diferenca_cm': round(medida_real - medida_ideal, 1)
    }


def avaliar_gordura_central(cintura: float, altura: float, quadril: float, sexo: str) -> Dict[str, Any]:
    """
    Avalia a distribuição de gordura central.
    
    Args:
        cintura: Circunferência da cintura em cm
        altura: Altura em cm
        quadril: Circunferência do quadril em cm
        sexo: 'M' para masculino, 'F' para feminino
        
    Returns:
        Dicionário com índices e classificações
    """
    # Índice cintura/altura
    rca = cintura / altura
    
    if rca <= 0.49:
        rca_status = 'saudavel'
        rca_descricao = 'Saudável'
        rca_cor = '#51cf66'
    elif rca <= 0.54:
        rca_status = 'moderado'
        rca_descricao = 'Risco Moderado'
        rca_cor = '#ffa94d'
    else:
        rca_status = 'elevado'
        rca_descricao = 'Risco Elevado'
        rca_cor = '#ff6b6b'
    
    # Relação cintura/quadril
    rcq = cintura / quadril
    limite_rcq = 0.90 if sexo == 'M' else 0.85
    
    if rcq <= limite_rcq:
        rcq_status = 'normal'
        rcq_descricao = 'Normal'
        rcq_cor = '#51cf66'
    else:
        rcq_status = 'elevado'
        rcq_descricao = 'Elevado'
        rcq_cor = '#ff6b6b'
    
    return {
        'rca': round(rca, 3),
        'rca_status': rca_status,
        'rca_descricao': rca_descricao,
        'rca_cor': rca_cor,
        'rcq': round(rcq, 3),
        'rcq_status': rcq_status,
        'rcq_descricao': rcq_descricao,
        'rcq_cor': rcq_cor
    }


def gerar_mapa_corporal(medidas: Dict[str, float], altura: float, sexo: str) -> Dict[str, Any]:
    """
    Gera mapa corporal completo com análise de todas as regiões.
    
    Args:
        medidas: Dicionário com medidas corporais (cintura, ombros, peitoral, etc)
        altura: Altura em cm
        sexo: 'M' para masculino, 'F' para feminino
        
    Returns:
        Dicionário com análise completa do mapa corporal
    """
    # Debug: imprimir medidas recebidas
    print(f"🔍 MAPA CORPORAL - Medidas recebidas: {list(medidas.keys())}")
    print(f"📏 Valores: pescoco={medidas.get('pescoco')}, ombros={medidas.get('ombros')}, "
          f"abdomen={medidas.get('abdomen')}, coxa={medidas.get('coxa')}")
    
    cintura = medidas.get('cintura')
    quadril = medidas.get('quadril')
    
    if not cintura:
        return {'erro': 'Cintura é obrigatória para análise corporal'}
    
    # Calcular proporções ideais
    ideais = calcular_proporcoes_ideais(cintura, sexo)
    
    # Analisar cada região
    regioes = {}
    
    for parte, ideal in ideais.items():
        real = None
        
        # Mapear nomes das medidas
        if parte == 'pescoco':
            real = medidas.get('pescoco')
        elif parte == 'ombros':
            real = medidas.get('ombros')
        elif parte == 'peitoral':
            real = medidas.get('peitoral')
        elif parte == 'cintura':
            real = medidas.get('cintura')
        elif parte == 'abdomen':
            real = medidas.get('abdomen')
        elif parte == 'braco':
            real = _obter_media_lateral(medidas, 'braco_contraido') or _obter_media_lateral(medidas, 'braco_relaxado')
        elif parte == 'antebraco':
            real = _obter_media_lateral(medidas, 'antebraco')
        elif parte == 'quadril':
            real = medidas.get('quadril')
        elif parte == 'coxa':
            real = _obter_media_lateral(medidas, 'coxa')
            print(f"🔍 COXA - Valor médio encontrado: {real}")
        elif parte == 'panturrilha':
            real = _obter_media_lateral(medidas, 'panturrilha')
        
        if real:
            regioes[parte] = {
                'real': real,
                'ideal': ideal,
                **classificar_desenvolvimento(real, ideal)
            }
        else:
            regioes[parte] = {
                'real': None,
                'ideal': ideal,
                'classificacao': 'nao_medido',
                'descricao': 'Não medido',
                'cor': '#868e96'
            }
    
    # Avaliar gordura central
    gordura_central = None
    if quadril:
        gordura_central = avaliar_gordura_central(cintura, altura, quadril, sexo)
    
    return {
        'regioes': regioes,
        'gordura_central': gordura_central,
        'proporcoes_ideais': ideais
    }
