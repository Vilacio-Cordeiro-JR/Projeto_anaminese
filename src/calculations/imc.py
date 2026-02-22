"""
Cálculos relacionados ao Índice de Massa Corporal (IMC)
"""

from typing import Tuple


def calcular_imc(peso: float, altura_cm: float) -> float:
    """
    Calcula o Índice de Massa Corporal (IMC).
    
    Fórmula: IMC = peso / (altura_metros)²
    
    Args:
        peso: Peso em quilogramas
        altura_cm: Altura em centímetros
        
    Returns:
        IMC calculado
        
    Raises:
        ValueError: Se peso ou altura forem inválidos
    """
    if peso <= 0:
        raise ValueError(f"Peso deve ser positivo: {peso}")
    
    if altura_cm <= 0 or altura_cm > 300:
        raise ValueError(f"Altura inválida: {altura_cm} cm")
    
    altura_m = altura_cm / 100
    imc = peso / (altura_m ** 2)
    
    return round(imc, 2)


def classificar_imc(imc: float) -> Tuple[str, str]:
    """
    Classifica o IMC segundo padrões da OMS.
    
    Args:
        imc: Índice de Massa Corporal
        
    Returns:
        Tupla (classificação, descrição)
    """
    if imc < 16:
        return ("MAGREZA_GRAVE", "Magreza grau III")
    elif imc < 17:
        return ("MAGREZA_MODERADA", "Magreza grau II")
    elif imc < 18.5:
        return ("MAGREZA_LEVE", "Magreza grau I")
    elif imc < 25:
        return ("NORMAL", "Peso normal")
    elif imc < 30:
        return ("SOBREPESO", "Sobrepeso (pré-obesidade)")
    elif imc < 35:
        return ("OBESIDADE_I", "Obesidade grau I")
    elif imc < 40:
        return ("OBESIDADE_II", "Obesidade grau II")
    else:
        return ("OBESIDADE_III", "Obesidade grau III (mórbida)")


def obter_imc_ideal(altura_cm: float) -> Tuple[float, float]:
    """
    Calcula a faixa de peso ideal para a altura (IMC entre 18.5 e 25).
    
    Args:
        altura_cm: Altura em centímetros
        
    Returns:
        Tupla (peso_minimo, peso_maximo) em kg
    """
    altura_m = altura_cm / 100
    peso_min = 18.5 * (altura_m ** 2)
    peso_max = 25 * (altura_m ** 2)
    
    return (round(peso_min, 1), round(peso_max, 1))
