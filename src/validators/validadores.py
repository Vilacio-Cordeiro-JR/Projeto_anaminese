"""
Módulo de Validadores
Valida dados de entrada e garante consistência das medidas.
"""

from typing import List, Tuple, Optional
from datetime import date


class ValidadorMedidas:
    """Valida medidas corporais e garante valores dentro de limites razoáveis"""
    
    # Limites aceitáveis para medidas (em cm)
    LIMITES = {
        'altura': (50, 250),
        'peso': (20, 300),
        'pescoco': (20, 60),
        'ombros': (70, 180),
        'peitoral': (60, 180),
        'cintura': (40, 180),
        'abdomen': (45, 200),
        'quadril': (50, 180),
        'braco_relaxado': (15, 60),
        'braco_contraido': (15, 70),
        'antebraco': (15, 50),
        'punho': (10, 30),
        'coxa': (30, 100),
        'joelho': (20, 60),
        'panturrilha': (20, 70),
        'tornozelo': (15, 40)
    }
    
    @classmethod
    def validar_medida(cls, nome: str, valor: float) -> Tuple[bool, Optional[str]]:
        """
        Valida uma medida individual.
        
        Args:
            nome: Nome da medida
            valor: Valor da medida
            
        Returns:
            Tupla (valido, mensagem_erro)
        """
        if valor is None:
            return (True, None)  # Medidas opcionais
        
        if valor <= 0:
            return (False, f"{nome} deve ser positivo")
        
        if nome in cls.LIMITES:
            minimo, maximo = cls.LIMITES[nome]
            if valor < minimo or valor > maximo:
                return (False, f"{nome} fora do intervalo aceitável ({minimo}-{maximo} cm)")
        
        return (True, None)
    
    @classmethod
    def validar_todas_medidas(cls, medidas: dict) -> List[str]:
        """
        Valida todas as medidas fornecidas.
        
        Args:
            medidas: Dicionário com medidas
            
        Returns:
            Lista de erros encontrados (vazia se tudo válido)
        """
        erros = []
        
        for nome, valor in medidas.items():
            if valor is not None:
                valido, erro = cls.validar_medida(nome, valor)
                if not valido:
                    erros.append(erro)
        
        return erros
    
    @classmethod
    def validar_consistencia(cls, medidas: dict) -> List[str]:
        """
        Valida consistência lógica entre medidas.
        
        Args:
            medidas: Dicionário com medidas
            
        Returns:
            Lista de avisos sobre inconsistências
        """
        avisos = []
        
        # Braço contraído deve ser maior que relaxado
        braco_rel = medidas.get('braco_relaxado')
        braco_cont = medidas.get('braco_contraido')
        if braco_rel and braco_cont:
            if braco_cont <= braco_rel:
                avisos.append("Braço contraído deve ser maior que relaxado")
            elif braco_cont > braco_rel * 1.3:
                avisos.append("Diferença entre braço contraído e relaxado muito alta (>30%)")
        
        # Abdômen geralmente é maior ou igual à cintura
        cintura = medidas.get('cintura')
        abdomen = medidas.get('abdomen')
        if cintura and abdomen:
            if abdomen < cintura - 5:  # Tolerância de 5cm
                avisos.append("Abdômen geralmente é maior ou igual à cintura")
        
        # Quadril normalmente é maior que cintura
        quadril = medidas.get('quadril')
        if cintura and quadril:
            if quadril < cintura:
                avisos.append("Quadril geralmente é maior que cintura (especialmente em mulheres)")
        
        # Peitoral deve ser razoavelmente maior que cintura
        peitoral = medidas.get('peitoral')
        if peitoral and cintura:
            if peitoral < cintura:
                avisos.append("Peitoral menor que cintura - verificar medições")
        
        # Coxa normalmente é maior que panturrilha
        coxa = medidas.get('coxa')
        panturrilha = medidas.get('panturrilha')
        if coxa and panturrilha:
            if coxa < panturrilha:
                avisos.append("Coxa menor que panturrilha - verificar medições")
        
        # Relação peso/altura básica
        peso = medidas.get('peso')
        altura = medidas.get('altura')
        if peso and altura:
            imc = peso / ((altura / 100) ** 2)
            if imc < 12:
                avisos.append("IMC extremamente baixo (<12) - verificar medições")
            elif imc > 60:
                avisos.append("IMC extremamente alto (>60) - verificar medições")
        
        return avisos


class ValidadorUsuario:
    """Valida dados de usuário"""
    
    @staticmethod
    def validar_nome(nome: str) -> Tuple[bool, Optional[str]]:
        """Valida nome do usuário"""
        if not nome or len(nome.strip()) == 0:
            return (False, "Nome é obrigatório")
        
        if len(nome) < 3:
            return (False, "Nome deve ter pelo menos 3 caracteres")
        
        if len(nome) > 100:
            return (False, "Nome muito longo (máximo 100 caracteres)")
        
        return (True, None)
    
    @staticmethod
    def validar_data_nascimento(data_nasc: date) -> Tuple[bool, Optional[str]]:
        """Valida data de nascimento"""
        if data_nasc > date.today():
            return (False, "Data de nascimento não pode ser futura")
        
        idade = date.today().year - data_nasc.year
        if idade > 120:
            return (False, "Idade muito alta (>120 anos)")
        
        if idade < 0:
            return (False, "Idade inválida")
        
        return (True, None)
    
    @staticmethod
    def validar_email(email: Optional[str]) -> Tuple[bool, Optional[str]]:
        """Valida email (básico)"""
        if not email:
            return (True, None)  # Email é opcional
        
        if '@' not in email or '.' not in email:
            return (False, "Email inválido")
        
        if len(email) > 100:
            return (False, "Email muito longo")
        
        return (True, None)


class ValidadorAvaliacao:
    """Valida dados de avaliação"""
    
    @staticmethod
    def validar_data(data_aval: date) -> Tuple[bool, Optional[str]]:
        """Valida data da avaliação"""
        if data_aval > date.today():
            return (False, "Data da avaliação não pode ser futura")
        
        # Verifica se não é muito antiga (mais de 100 anos)
        anos_atras = date.today().year - data_aval.year
        if anos_atras > 100:
            return (False, "Data de avaliação muito antiga")
        
        return (True, None)
    
    @staticmethod
    def validar_ordem_avaliacoes(avaliacoes: List) -> List[str]:
        """
        Valida que avaliações estão em ordem cronológica.
        
        Args:
            avaliacoes: Lista de avaliações (com atributo 'data')
            
        Returns:
            Lista de avisos
        """
        avisos = []
        
        if len(avaliacoes) < 2:
            return avisos
        
        # Verifica duplicatas de data
        datas = [a.data for a in avaliacoes]
        if len(datas) != len(set(datas)):
            avisos.append("Existem avaliações com mesma data")
        
        # Verifica intervalo mínimo razoável
        avaliacoes_ordenadas = sorted(avaliacoes, key=lambda x: x.data)
        for i in range(1, len(avaliacoes_ordenadas)):
            dias = (avaliacoes_ordenadas[i].data - avaliacoes_ordenadas[i-1].data).days
            if dias < 1:
                avisos.append("Avaliações muito próximas (mesmo dia)")
        
        return avisos
