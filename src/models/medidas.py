"""
Modelo de dados: Medidas Corporais
Armazena todas as medidas antropométricas de uma avaliação.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Medidas:
    """
    Representa o conjunto completo de medidas corporais.
    
    MEDIDAS OBRIGATÓRIAS:
        altura: Altura em centímetros
        peso: Peso em quilogramas
    
    CIRCUNFERÊNCIAS PRINCIPAIS (em centímetros):
        pescoco: Circunferência do pescoço
        peitoral: Circunferência do tórax/peitoral
        cintura: Menor circunferência entre costelas e crista ilíaca
        abdomen: Circunferência na linha do umbigo
        quadril: Maior projeção glútea
        braco_relaxado: Braço em repouso
        braco_contraido: Braço contraído (biceps flexionado)
        coxa: Ponto médio entre virilha e joelho
        panturrilha: Maior circunferência da panturrilha
    
    CIRCUNFERÊNCIAS COMPLEMENTARES (opcionais, em centímetros):
        antebraco: Maior circunferência do antebraço
        ombros: Circunferência dos ombros
        punho: Circunferência do pulso
        joelho: Circunferência do joelho
        tornozelo: Circunferência do tornozelo
    """
    
    # Medidas básicas obrigatórias
    altura: float  # cm
    peso: float    # kg
    
    # Circunferências principais
    pescoco: Optional[float] = None       # cm
    peitoral: Optional[float] = None      # cm
    cintura: Optional[float] = None       # cm
    abdomen: Optional[float] = None       # cm
    quadril: Optional[float] = None       # cm
    braco_relaxado: Optional[float] = None   # cm
    braco_contraido: Optional[float] = None  # cm
    coxa: Optional[float] = None          # cm
    panturrilha: Optional[float] = None   # cm
    
    # Circunferências complementares
    antebraco: Optional[float] = None     # cm
    ombros: Optional[float] = None        # cm
    punho: Optional[float] = None         # cm
    joelho: Optional[float] = None        # cm
    tornozelo: Optional[float] = None     # cm
    
    def __post_init__(self):
        """Validações após inicialização"""
        if self.altura <= 0 or self.altura > 300:
            raise ValueError(f"Altura inválida: {self.altura} cm")
        
        if self.peso <= 0 or self.peso > 500:
            raise ValueError(f"Peso inválido: {self.peso} kg")
        
        # Valida circunferências se informadas
        self._validar_medidas_positivas()
    
    def _validar_medidas_positivas(self):
        """Garante que todas as medidas informadas são positivas"""
        medidas = {
            'pescoco': self.pescoco,
            'peitoral': self.peitoral,
            'cintura': self.cintura,
            'abdomen': self.abdomen,
            'quadril': self.quadril,
            'braco_relaxado': self.braco_relaxado,
            'braco_contraido': self.braco_contraido,
            'coxa': self.coxa,
            'panturrilha': self.panturrilha,
            'antebraco': self.antebraco,
            'ombros': self.ombros,
            'punho': self.punho,
            'joelho': self.joelho,
            'tornozelo': self.tornozelo
        }
        
        for nome, valor in medidas.items():
            if valor is not None and valor <= 0:
                raise ValueError(f"{nome} deve ser positivo: {valor}")
    
    @property
    def altura_metros(self) -> float:
        """Retorna altura em metros"""
        return self.altura / 100
    
    def tem_medidas_minimas_us_navy(self, sexo: str) -> bool:
        """
        Verifica se tem as medidas mínimas para cálculo US Navy.
        
        Homens: altura, cintura, pescoço
        Mulheres: altura, cintura, quadril, pescoço
        """
        basico = self.altura and self.cintura and self.pescoco
        
        if sexo.upper() in ['M', 'MASCULINO']:
            return basico is not None
        elif sexo.upper() in ['F', 'FEMININO']:
            return basico and self.quadril is not None
        
        return False
    
    def tem_medidas_proporcao(self) -> bool:
        """Verifica se tem medidas suficientes para análise de proporção"""
        return (
            self.altura is not None and
            self.cintura is not None and
            (self.peitoral is not None or self.ombros is not None)
        )
    
    def __repr__(self) -> str:
        return (
            f"Medidas(altura={self.altura}cm, peso={self.peso}kg, "
            f"cintura={self.cintura}cm, quadril={self.quadril}cm)"
        )
