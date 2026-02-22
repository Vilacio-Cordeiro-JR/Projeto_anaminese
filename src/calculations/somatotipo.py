"""
Classificador de Somatotipos
Sistema heurístico para classificação de perfis físicos.
"""

from typing import Dict, Tuple
from enum import Enum


class Somatotipo(Enum):
    """Tipos corporais básicos"""
    ECTOMORFO = "ectomorfo"
    MESOMORFO = "mesomorfo"
    ENDOMORFO = "endomorfo"
    ECTO_MESO = "ecto-mesomorfo"
    MESO_ENDO = "meso-endomorfo"
    EQUILIBRADO = "equilibrado"


def classificar_somatotipo(
    rcq: float,
    rca: float,
    imc: float,
    proporcoes: Dict[str, float]
) -> Tuple[Somatotipo, str, Dict[str, float]]:
    """
    Classifica o somatotipo baseado em medidas e índices corporais.
    
    CARACTERÍSTICAS:
    - Ectomorfo: magro, membros longos, dificuldade ganhar peso
      Indicadores: IMC baixo, RCQ baixo, cintura e membros finos
    
    - Mesomorfo: muscular, estrutura atlética, boa resposta ao treino
      Indicadores: Boas proporções, simetria, relação ombro/cintura alta
    
    - Endomorfo: tendência a acumular gordura, estrutura arredondada
      Indicadores: RCQ alto, RCA alto, cintura e quadril maiores
    
    Args:
        rcq: Relação cintura-quadril
        rca: Relação cintura-altura
        imc: Índice de massa corporal
        proporcoes: Dicionário com proporções corporais
            Esperado: ombro_cintura, peitoral_cintura, etc.
    
    Returns:
        Tupla (somatotipo, descricao, scores)
    """
    # Inicializa pontuações para cada tipo
    scores = {
        'ectomorfo': 0.0,
        'mesomorfo': 0.0,
        'endomorfo': 0.0
    }
    
    # === ANÁLISE DO IMC ===
    if imc < 18.5:
        scores['ectomorfo'] += 3
    elif imc < 25:
        scores['mesomorfo'] += 2
        scores['ectomorfo'] += 1
    elif imc < 30:
        scores['mesomorfo'] += 1
        scores['endomorfo'] += 2
    else:
        scores['endomorfo'] += 3
    
    # === ANÁLISE DO RCA ===
    if rca < 0.45:
        scores['ectomorfo'] += 2
    elif rca < 0.50:
        scores['mesomorfo'] += 2
    elif rca < 0.60:
        scores['endomorfo'] += 2
    else:
        scores['endomorfo'] += 3
    
    # === ANÁLISE DO RCQ ===
    # Valores diferentes para homens e mulheres, usando média
    if rcq < 0.80:
        scores['ectomorfo'] += 2
        scores['mesomorfo'] += 1
    elif rcq < 0.90:
        scores['mesomorfo'] += 2
    else:
        scores['endomorfo'] += 3
    
    # === ANÁLISE DE PROPORÇÕES ===
    ombro_cintura = proporcoes.get('ombro_cintura', 0)
    peitoral_cintura = proporcoes.get('peitoral_cintura', 0)
    
    # Relação ombro/cintura (quanto maior, mais mesomorfo)
    if ombro_cintura >= 1.6:
        scores['mesomorfo'] += 3
    elif ombro_cintura >= 1.4:
        scores['mesomorfo'] += 2
    elif ombro_cintura > 0:
        scores['ectomorfo'] += 1
    
    # Relação peitoral/cintura
    if peitoral_cintura >= 1.4:
        scores['mesomorfo'] += 2
    elif peitoral_cintura >= 1.2:
        scores['mesomorfo'] += 1
    
    # === DETERMINA O SOMATOTIPO DOMINANTE ===
    max_score = max(scores.values())
    
    # Verifica se há equilíbrio
    valores_scores = sorted(scores.values(), reverse=True)
    if valores_scores[0] - valores_scores[1] <= 1:
        # Praticamente empatado - tipos mistos
        if scores['ectomorfo'] >= scores['endomorfo']:
            tipo = Somatotipo.ECTO_MESO
            descricao = "Ecto-Mesomorfo: magro com potencial atlético"
        else:
            tipo = Somatotipo.MESO_ENDO
            descricao = "Meso-Endomorfo: estrutura forte com tendência a ganhar gordura"
    else:
        # Um tipo claramente dominante
        if scores['ectomorfo'] == max_score:
            tipo = Somatotipo.ECTOMORFO
            descricao = (
                "Ectomorfo: estrutura delgada, metabolismo acelerado, "
                "dificuldade em ganhar peso"
            )
        elif scores['mesomorfo'] == max_score:
            tipo = Somatotipo.MESOMORFO
            descricao = (
                "Mesomorfo: estrutura atlética natural, boa resposta ao treino, "
                "facilidade para ganhar músculo"
            )
        else:
            tipo = Somatotipo.ENDOMORFO
            descricao = (
                "Endomorfo: estrutura mais arredondada, tendência a acumular gordura, "
                "requer atenção à dieta"
            )
    
    # Normaliza scores para porcentagem
    total = sum(scores.values())
    if total > 0:
        scores = {k: round((v/total) * 100, 1) for k, v in scores.items()}
    
    return (tipo, descricao, scores)


def obter_recomendacoes_somatotipo(somatotipo: Somatotipo) -> Dict[str, str]:
    """
    Fornece recomendações de treino e nutrição baseadas no somatotipo.
    
    Args:
        somatotipo: Tipo corporal classificado
        
    Returns:
        Dicionário com recomendações de treino, dieta e dicas
    """
    recomendacoes = {
        Somatotipo.ECTOMORFO: {
            'treino': (
                "Foco em exercícios compostos (agachamento, supino, levantamento terra). "
                "Treinos mais curtos e intensos (45-60min). Cardio moderado. "
                "Priorizar hipertrofia com 8-12 repetições."
            ),
            'dieta': (
                "Dieta hipercalórica com superávit calórico. "
                "Carboidratos abundantes (50-60% das calorias). "
                "Proteína moderada a alta (1.8-2.2g/kg). "
                "Não temer gorduras saudáveis. Refeições frequentes (5-6x/dia)."
            ),
            'dicas': (
                "Durma bem (8+ horas). Evite cardio excessivo. "
                "Seja paciente - ganhos serão mais lentos mas duradouros. "
                "Suplementação: whey protein, creatina, hipercalóricos."
            )
        },
        Somatotipo.MESOMORFO: {
            'treino': (
                "Variedade de estímulos. Combine força (5-8 reps) e hipertrofia (8-12 reps). "
                "Cardio moderado para definição. Responde bem a periodização. "
                "Pode treinar com maior volume."
            ),
            'dieta': (
                "Dieta balanceada e flexível. "
                "Carboidratos moderados (40-50% das calorias). "
                "Proteína moderada (1.6-2.0g/kg). "
                "Ajustar calorias conforme objetivo (bulking ou cutting)."
            ),
            'dicas': (
                "Aproveite a genética favorável mas não descuide da dieta. "
                "Varie os treinos para evitar estagnação. "
                "Fácil ganhar mas também fácil perder forma - mantenha consistência."
            )
        },
        Somatotipo.ENDOMORFO: {
            'treino': (
                "Combine musculação com cardio regular. "
                "HIIT eficiente para queima de gordura. "
                "Treinos com maior volume e frequência. "
                "Foco em compostos + exercícios metabólicos."
            ),
            'dieta': (
                "Controle calórico rigoroso. Déficit para perda de gordura. "
                "Carboidratos controlados (30-40% das calorias), preferir baixo IG. "
                "Proteína alta (2.0-2.5g/kg) para preservar massa magra. "
                "Atenção ao timing dos carboidratos (pré/pós-treino)."
            ),
            'dicas': (
                "A genética pode ser desafiadora mas não é limitante. "
                "Monitore calorias e macros de perto. "
                "Sono e gestão de estresse são críticos (afetam hormônios). "
                "Evite períodos longos sem atividade."
            )
        },
        Somatotipo.ECTO_MESO: {
            'treino': (
                "Treinos de força e hipertrofia, volume moderado. "
                "Cardio leve a moderado. Foco em construir massa muscular "
                "sem cardio excessivo que prejudique ganhos."
            ),
            'dieta': (
                "Leve superávit calórico para construção muscular. "
                "Carboidratos moderados a altos. Proteína alta (1.8-2.2g/kg). "
                "Mais flexibilidade que ectomorfo puro."
            ),
            'dicas': (
                "Boa capacidade de definição com dieta adequada. "
                "Aproveite facilidade para construir físico atlético e definido."
            )
        },
        Somatotipo.MESO_ENDO: {
            'treino': (
                "Musculação pesada + cardio regular para controle de gordura. "
                "HIIT 2-3x/semana. Volume alto de treino. "
                "Bom potencial para ganho de força e massa."
            ),
            'dieta': (
                "Atenção ao excesso calórico. Carboidratos moderados. "
                "Proteína alta. Monitorar percentual de gordura regularmente. "
                "Ciclos de bulking/cutting bem estruturados."
            ),
            'dicas': (
                "Facilidade para ganhar massa mas também gordura. "
                "Disciplina alimentar é chave. Potencial para físicos imponentes "
                "se bem trabalhado."
            )
        },
        Somatotipo.EQUILIBRADO: {
            'treino': (
                "Abordagem balanceada. Variar entre fases de força, "
                "hipertrofia e resistência. Cardio moderado."
            ),
            'dieta': (
                "Dieta equilibrada e flexível. Ajustar conforme objetivos. "
                "Proteína moderada (1.6-2.0g/kg)."
            ),
            'dicas': (
                "Versatilidade é seu ponto forte. Pode adaptar-se a diferentes "
                "objetivos com relativa facilidade."
            )
        }
    }
    
    return recomendacoes.get(somatotipo, recomendacoes[Somatotipo.EQUILIBRADO])
