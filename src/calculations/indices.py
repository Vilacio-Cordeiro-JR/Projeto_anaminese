"""
Cálculos de índices corporais: RCQ e RCA
"""

from typing import Tuple


def calcular_rcq(cintura_cm: float, quadril_cm: float) -> float:
    """
    Calcula a Relação Cintura-Quadril (RCQ / WHR - Waist-Hip Ratio).
    
    Indica distribuição de gordura corporal e risco cardiovascular.
    
    Args:
        cintura_cm: Circunferência da cintura em cm
        quadril_cm: Circunferência do quadril em cm
        
    Returns:
        RCQ calculado
        
    Raises:
        ValueError: Se valores inválidos
    """
    if cintura_cm <= 0 or quadril_cm <= 0:
        raise ValueError("Cintura e quadril devem ser positivos")
    
    rcq = cintura_cm / quadril_cm
    return round(rcq, 3)


def classificar_rcq(rcq: float, sexo: str) -> Tuple[str, str]:
    """
    Classifica o RCQ e determina risco de complicações metabólicas.
    
    Args:
        rcq: Relação Cintura-Quadril
        sexo: 'M' para masculino ou 'F' para feminino
        
    Returns:
        Tupla (classificação, descrição_risco)
    """
    sexo = sexo.upper()
    
    if sexo in ['M', 'MASCULINO']:
        if rcq < 0.85:
            return ("BAIXO", "Risco baixo")
        elif rcq < 0.90:
            return ("MODERADO", "Risco moderado")
        else:
            return ("ALTO", "Risco alto")
    
    elif sexo in ['F', 'FEMININO']:
        if rcq < 0.75:
            return ("BAIXO", "Risco baixo")
        elif rcq < 0.85:
            return ("MODERADO", "Risco moderado")
        else:
            return ("ALTO", "Risco alto")
    
    return ("DESCONHECIDO", "Sexo não especificado")


def calcular_rca(cintura_cm: float, altura_cm: float) -> float:
    """
    Calcula a Relação Cintura-Altura (RCA / WHtR - Waist-to-Height Ratio).
    
    Considerado melhor preditor de risco cardiovascular que IMC.
    Regra prática: RCA ideal ≤ 0.50 ("mantenha sua cintura menor que metade da sua altura")
    
    Args:
        cintura_cm: Circunferência da cintura em cm
        altura_cm: Altura em cm
        
    Returns:
        RCA calculado
        
    Raises:
        ValueError: Se valores inválidos
    """
    if cintura_cm <= 0 or altura_cm <= 0:
        raise ValueError("Cintura e altura devem ser positivos")
    
    rca = cintura_cm / altura_cm
    return round(rca, 3)


def classificar_rca(rca: float) -> Tuple[str, str]:
    """
    Classifica o RCA e indica risco para saúde.
    
    Args:
        rca: Relação Cintura-Altura
        
    Returns:
        Tupla (classificação, descrição)
    """
    if rca < 0.40:
        return ("MUITO_BAIXO", "Extremamente magro")
    elif rca < 0.50:
        return ("SAUDAVEL", "Peso saudável")
    elif rca < 0.60:
        return ("SOBREPESO", "Sobrepeso - risco aumentado")
    elif rca < 0.70:
        return ("OBESIDADE", "Obesidade - risco alto")
    else:
        return ("OBESIDADE_MORBIDA", "Obesidade mórbida - risco muito alto")


def calcular_indice_conicidade(cintura_cm: float, peso_kg: float, altura_cm: float) -> float:
    """
    Calcula o Índice de Conicidade (IC).
    
    Avalia a distribuição de gordura corporal e risco cardiovascular.
    Valores mais altos indicam formato mais cônico (acúmulo central de gordura).
    
    Args:
        cintura_cm: Circunferência da cintura em cm
        peso_kg: Peso em kg
        altura_cm: Altura em cm
        
    Returns:
        Índice de conicidade
    """
    import math
    
    altura_m = altura_cm / 100
    
    # IC = (cintura / 0.109) * sqrt(peso / altura)
    ic = (cintura_cm / 0.109) * math.sqrt(peso_kg / altura_m)
    
    return round(ic, 3)
