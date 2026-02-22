"""
Modelo de dados: Usuário
Representa uma pessoa que terá suas medidas corporais acompanhadas.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List
from enum import Enum


class Sexo(Enum):
    """Sexo biológico - importante para cálculos de percentual de gordura"""
    MASCULINO = "M"
    FEMININO = "F"


@dataclass
class Usuario:
    """
    Representa um usuário do sistema.
    
    Attributes:
        id: Identificador único
        nome: Nome completo
        sexo: Sexo biológico (M/F)
        data_nascimento: Data de nascimento
        email: Email (opcional)
        telefone: Telefone (opcional)
        observacoes: Observações gerais (opcional)
        avaliacoes: Lista de avaliações realizadas
        data_cadastro: Data de cadastro no sistema
        ativo: Indica se o usuário está ativo
    """
    nome: str
    sexo: Sexo
    data_nascimento: date
    id: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    observacoes: Optional[str] = None
    avaliacoes: List['Avaliacao'] = field(default_factory=list)
    data_cadastro: date = field(default_factory=date.today)
    ativo: bool = True
    
    def __post_init__(self):
        """Validações após inicialização"""
        if not self.nome or len(self.nome.strip()) == 0:
            raise ValueError("Nome é obrigatório")
        
        if self.data_nascimento > date.today():
            raise ValueError("Data de nascimento não pode ser futura")
    
    @property
    def idade(self) -> int:
        """Calcula a idade atual em anos"""
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        
        # Ajusta se ainda não fez aniversário este ano
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        
        return idade
    
    def adicionar_avaliacao(self, avaliacao: 'Avaliacao') -> None:
        """Adiciona uma nova avaliação ao histórico"""
        self.avaliacoes.append(avaliacao)
        # Ordena por data (mais recente primeiro)
        self.avaliacoes.sort(key=lambda x: x.data, reverse=True)
    
    def obter_ultima_avaliacao(self) -> Optional['Avaliacao']:
        """Retorna a avaliação mais recente"""
        return self.avaliacoes[0] if self.avaliacoes else None
    
    def obter_avaliacoes_periodo(self, data_inicio: date, data_fim: date) -> List['Avaliacao']:
        """Retorna avaliações dentro de um período"""
        return [
            avaliacao for avaliacao in self.avaliacoes
            if data_inicio <= avaliacao.data <= data_fim
        ]
    
    def __repr__(self) -> str:
        return f"Usuario(id={self.id}, nome='{self.nome}', sexo={self.sexo.value}, idade={self.idade})"
