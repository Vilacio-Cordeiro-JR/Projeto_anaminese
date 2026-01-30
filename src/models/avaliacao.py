"""
Modelo de dados: Avaliação
Representa uma avaliação física completa realizada em uma data específica.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional, Dict, Any
from .medidas import Medidas


@dataclass
class Avaliacao:
    """
    Representa uma avaliação física completa.
    
    Attributes:
        data: Data da avaliação
        medidas: Objeto com todas as medidas corporais
        id: Identificador único
        usuario_id: ID do usuário avaliado
        objetivo: Objetivo da avaliação (ganho muscular, emagrecimento, etc)
        observacoes: Observações do avaliador
        resultados: Dicionário com resultados calculados (IMC, %gordura, etc)
    """
    data: date
    medidas: Medidas
    id: Optional[str] = None
    usuario_id: Optional[str] = None
    objetivo: Optional[str] = None
    observacoes: Optional[str] = None
    resultados: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validações após inicialização"""
        if self.data > date.today():
            raise ValueError("Data da avaliação não pode ser futura")
        
        if not isinstance(self.medidas, Medidas):
            raise TypeError("medidas deve ser uma instância de Medidas")
    
    def adicionar_resultado(self, chave: str, valor: Any) -> None:
        """Adiciona um resultado calculado"""
        self.resultados[chave] = valor
    
    def obter_resultado(self, chave: str, padrao: Any = None) -> Any:
        """Obtém um resultado calculado"""
        return self.resultados.get(chave, padrao)
    
    def tem_resultado(self, chave: str) -> bool:
        """Verifica se um resultado foi calculado"""
        return chave in self.resultados
    
    def resumo(self) -> str:
        """Retorna resumo da avaliação"""
        imc = self.obter_resultado('imc')
        gordura = self.obter_resultado('percentual_gordura')
        
        texto = f"Avaliação de {self.data.strftime('%d/%m/%Y')}\n"
        texto += f"Peso: {self.medidas.peso} kg | Altura: {self.medidas.altura} cm\n"
        
        if imc:
            texto += f"IMC: {imc:.1f}\n"
        if gordura:
            texto += f"% Gordura: {gordura:.1f}%\n"
        
        return texto
    
    def __repr__(self) -> str:
        return f"Avaliacao(data={self.data}, peso={self.medidas.peso}kg, resultados={len(self.resultados)})"
