"""
Cálculos de estimativa de percentual de gordura corporal
"""

import math
from typing import Optional


def calcular_gordura_us_navy(
    altura_cm: float,
    cintura_cm: float,
    pescoco_cm: float,
    sexo: str,
    quadril_cm: Optional[float] = None
) -> float:
    """
    Calcula o percentual de gordura corporal usando o método US Navy.
    
    FÓRMULAS:
    Homens: %G = 86.010 * log10(cintura - pescoço) - 70.041 * log10(altura) + 36.76
    Mulheres: %G = 163.205 * log10(cintura + quadril - pescoço) - 97.684 * log10(altura) - 78.387
    
    Args:
        altura_cm: Altura em centímetros
        cintura_cm: Circunferência da cintura em centímetros
        pescoco_cm: Circunferência do pescoço em centímetros
        sexo: 'M' para masculino ou 'F' para feminino
        quadril_cm: Circunferência do quadril (obrigatório para mulheres)
        
    Returns:
        Percentual de gordura corporal
        
    Raises:
        ValueError: Se dados inválidos ou incompletos
    """
    # Validações básicas
    if altura_cm <= 0 or cintura_cm <= 0 or pescoco_cm <= 0:
        raise ValueError("Todas as medidas devem ser positivas")
    
    sexo = sexo.upper()
    
    if sexo in ['M', 'MASCULINO']:
        # Fórmula para homens
        if cintura_cm <= pescoco_cm:
            raise ValueError("Cintura deve ser maior que pescoço")
        
        gordura = (
            86.010 * math.log10(cintura_cm - pescoco_cm) -
            70.041 * math.log10(altura_cm) +
            36.76
        )
        
    elif sexo in ['F', 'FEMININO']:
        # Fórmula para mulheres - requer medida do quadril
        if quadril_cm is None or quadril_cm <= 0:
            raise ValueError("Quadril é obrigatório para mulheres")
        
        denominador = cintura_cm + quadril_cm - pescoco_cm
        if denominador <= 0:
            raise ValueError("Soma de cintura e quadril deve ser maior que pescoço")
        
        gordura = (
            163.205 * math.log10(denominador) -
            97.684 * math.log10(altura_cm) -
            78.387
        )
    else:
        raise ValueError(f"Sexo inválido: {sexo}. Use 'M' ou 'F'")
    
    # Garante que o resultado está dentro de limites razoáveis
    gordura = max(3, min(60, gordura))
    
    return round(gordura, 1)


def classificar_gordura(percentual: float, sexo: str, idade: int) -> str:
    """
    Classifica o percentual de gordura segundo faixas recomendadas.
    
    Baseado em padrões do American Council on Exercise (ACE).
    
    Args:
        percentual: Percentual de gordura corporal
        sexo: 'M' ou 'F'
        idade: Idade em anos
        
    Returns:
        Classificação do percentual de gordura
    """
    sexo = sexo.upper()
    
    if sexo in ['M', 'MASCULINO']:
        if percentual < 6:
            return "Essencial (muito baixo)"
        elif percentual < 14:
            return "Atleta"
        elif percentual < 18:
            return "Fitness"
        elif percentual < 25:
            return "Aceitável"
        else:
            return "Obesidade"
    
    elif sexo in ['F', 'FEMININO']:
        if percentual < 14:
            return "Essencial (muito baixo)"
        elif percentual < 21:
            return "Atleta"
        elif percentual < 25:
            return "Fitness"
        elif percentual < 32:
            return "Aceitável"
        else:
            return "Obesidade"
    
    return "Desconhecido"


def calcular_massa_gorda(peso: float, percentual_gordura: float) -> float:
    """
    Calcula a massa gorda em kg.
    
    Args:
        peso: Peso total em kg
        percentual_gordura: % de gordura corporal
        
    Returns:
        Massa gorda em kg
    """
    return round(peso * (percentual_gordura / 100), 1)


def calcular_massa_magra(peso: float, percentual_gordura: float) -> float:
    """
    Calcula a massa magra em kg.
    
    Args:
        peso: Peso total em kg
        percentual_gordura: % de gordura corporal
        
    Returns:
        Massa magra em kg
    """
    massa_gorda = peso * (percentual_gordura / 100)
    return round(peso - massa_gorda, 1)
