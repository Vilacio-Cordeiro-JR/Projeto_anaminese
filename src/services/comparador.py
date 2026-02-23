"""
Serviço de Comparação de Avaliações
Analisa evolução entre duas ou mais avaliações.
"""

from typing import List, Dict, Any, Tuple
from datetime import date
from ..models.avaliacao import Avaliacao


class ComparadorAvaliacoes:
    """Compara avaliações e analisa evolução temporal"""
    
    @staticmethod
    def comparar_duas_avaliacoes(
        avaliacao_antiga: Avaliacao,
        avaliacao_nova: Avaliacao
    ) -> Dict[str, Any]:
        """
        Compara duas avaliações e calcula diferenças.
        
        Args:
            avaliacao_antiga: Avaliação mais antiga
            avaliacao_nova: Avaliação mais recente
            
        Returns:
            Dicionário com comparações e evolução
        """
        m_antiga = avaliacao_antiga.medidas
        m_nova = avaliacao_nova.medidas
        r_antiga = avaliacao_antiga.resultados
        r_nova = avaliacao_nova.resultados
        
        # Calcula intervalo em dias
        dias = (avaliacao_nova.data - avaliacao_antiga.data).days
        
        comparacao = {
            'dias_entre_avaliacoes': dias,
            'data_antiga': avaliacao_antiga.data,
            'data_nova': avaliacao_nova.data,
            'diferencas_medidas': {},
            'diferencas_indices': {},
            'analise_evolucao': []
        }
        
        # === COMPARAÇÃO DE MEDIDAS ===
        
        # Peso
        if m_antiga.peso and m_nova.peso:
            diff_peso = m_nova.peso - m_antiga.peso
            perc_peso = (diff_peso / m_antiga.peso) * 100
            comparacao['diferencas_medidas']['peso'] = {
                'anterior': m_antiga.peso,
                'atual': m_nova.peso,
                'diferenca': round(diff_peso, 1),
                'percentual': round(perc_peso, 1)
            }
        
        # Circunferências - apenas medidas diretas (não bilaterais)
        medidas_comparar = [
            'pescoco', 'peitoral', 'cintura', 'abdomen', 'quadril', 'ombros'
        ]
        
        for medida in medidas_comparar:
            valor_antigo = getattr(m_antiga, medida, None)
            valor_novo = getattr(m_nova, medida, None)
            
            if valor_antigo and valor_novo:
                diff = valor_novo - valor_antigo
                perc = (diff / valor_antigo) * 100
                comparacao['diferencas_medidas'][medida] = {
                    'anterior': valor_antigo,
                    'atual': valor_novo,
                    'diferenca': round(diff, 1),
                    'percentual': round(perc, 1)
                }
        
        # Comparar médias bilaterais (dos resultados calculados)
        if 'medias_bilaterais' in r_antiga and 'medias_bilaterais' in r_nova:
            medias_antigas = r_antiga['medias_bilaterais']
            medias_novas = r_nova['medias_bilaterais']
            
            medidas_bilaterais = ['braco_relaxado', 'braco_contraido', 'antebraco', 'coxa', 'panturrilha']
            
            for medida in medidas_bilaterais:
                valor_antigo = getattr(medias_antigas, medida, None)
                valor_novo = getattr(medias_novas, medida, None)
                
                if valor_antigo and valor_novo:
                    diff = valor_novo - valor_antigo
                    perc = (diff / valor_antigo) * 100
                    comparacao['diferencas_medidas'][medida] = {
                        'anterior': valor_antigo,
                        'atual': valor_novo,
                        'diferenca': round(diff, 1),
                        'percentual': round(perc, 1)
                    }
        
        # === COMPARAÇÃO DE ÍNDICES ===
        
        indices_comparar = [
            'imc', 'percentual_gordura', 'massa_gorda_kg', 'massa_magra_kg',
            'rcq', 'rca', 'pontuacao_estetica'
        ]
        
        for indice in indices_comparar:
            if indice in r_antiga and indice in r_nova:
                valor_antigo = r_antiga[indice]
                valor_novo = r_nova[indice]
                diff = valor_novo - valor_antigo
                
                # Evita divisão por zero
                if valor_antigo != 0:
                    perc = (diff / valor_antigo) * 100
                else:
                    perc = 0
                
                comparacao['diferencas_indices'][indice] = {
                    'anterior': valor_antigo,
                    'atual': valor_novo,
                    'diferenca': round(diff, 2),
                    'percentual': round(perc, 1)
                }
        
        # === ANÁLISE QUALITATIVA DA EVOLUÇÃO ===
        
        analise = []
        
        # Análise de peso
        if 'peso' in comparacao['diferencas_medidas']:
            diff_peso = comparacao['diferencas_medidas']['peso']['diferenca']
            if diff_peso > 1:
                analise.append(f"Ganho de peso: +{diff_peso} kg")
            elif diff_peso < -1:
                analise.append(f"Perda de peso: {diff_peso} kg")
            else:
                analise.append("Peso mantido estável")
        
        # Análise de gordura
        if 'percentual_gordura' in comparacao['diferencas_indices']:
            diff_gord = comparacao['diferencas_indices']['percentual_gordura']['diferenca']
            if diff_gord < -1:
                analise.append(f"✓ Redução de gordura: {diff_gord}%")
            elif diff_gord > 1:
                analise.append(f"✗ Aumento de gordura: +{diff_gord}%")
        
        # Análise de massa magra
        if 'massa_magra_kg' in comparacao['diferencas_indices']:
            diff_magra = comparacao['diferencas_indices']['massa_magra_kg']['diferenca']
            if diff_magra > 0.5:
                analise.append(f"✓ Ganho de massa magra: +{diff_magra} kg")
            elif diff_magra < -0.5:
                analise.append(f"✗ Perda de massa magra: {diff_magra} kg")
        
        # Análise de cintura
        if 'cintura' in comparacao['diferencas_medidas']:
            diff_cintura = comparacao['diferencas_medidas']['cintura']['diferenca']
            if diff_cintura < -1:
                analise.append(f"✓ Redução de cintura: {diff_cintura} cm")
            elif diff_cintura > 1:
                analise.append(f"Aumento de cintura: +{diff_cintura} cm")
        
        # Análise de membros (hipertrofia)
        medidas_hipertrofia = ['braco_contraido', 'coxa', 'panturrilha']
        ganhos_musculares = []
        
        for medida in medidas_hipertrofia:
            if medida in comparacao['diferencas_medidas']:
                diff = comparacao['diferencas_medidas'][medida]['diferenca']
                if diff > 0.5:
                    nome_bonito = medida.replace('_', ' ').title()
                    ganhos_musculares.append(f"{nome_bonito} (+{diff} cm)")
        
        if ganhos_musculares:
            analise.append(f"✓ Ganhos musculares: {', '.join(ganhos_musculares)}")
        
        # Análise de pontuação estética
        if 'pontuacao_estetica' in comparacao['diferencas_indices']:
            diff_est = comparacao['diferencas_indices']['pontuacao_estetica']['diferenca']
            if diff_est > 5:
                analise.append(f"✓ Melhora estética significativa: +{diff_est} pontos")
            elif diff_est > 2:
                analise.append(f"✓ Melhora estética: +{diff_est} pontos")
        
        comparacao['analise_evolucao'] = analise
        
        # === CLASSIFICAÇÃO GERAL DA EVOLUÇÃO ===
        
        pontos_positivos = sum(1 for a in analise if '✓' in a)
        pontos_negativos = sum(1 for a in analise if '✗' in a)
        
        if pontos_positivos > pontos_negativos + 2:
            comparacao['avaliacao_geral'] = "Excelente evolução"
        elif pontos_positivos > pontos_negativos:
            comparacao['avaliacao_geral'] = "Boa evolução"
        elif pontos_positivos == pontos_negativos:
            comparacao['avaliacao_geral'] = "Evolução moderada"
        else:
            comparacao['avaliacao_geral'] = "Necessita ajustes"
        
        return comparacao
    
    @staticmethod
    def analisar_tendencia(avaliacoes: List[Avaliacao]) -> Dict[str, Any]:
        """
        Analisa tendência ao longo de múltiplas avaliações.
        
        Args:
            avaliacoes: Lista de avaliações ordenadas por data
            
        Returns:
            Análise de tendências
        """
        if len(avaliacoes) < 2:
            return {'erro': 'Necessário pelo menos 2 avaliações'}
        
        # Ordena por data
        avaliacoes_ordenadas = sorted(avaliacoes, key=lambda x: x.data)
        
        tendencias = {
            'numero_avaliacoes': len(avaliacoes_ordenadas),
            'periodo_dias': (avaliacoes_ordenadas[-1].data - avaliacoes_ordenadas[0].data).days,
            'peso': [],
            'percentual_gordura': [],
            'massa_magra': [],
            'cintura': [],
            'tendencia_geral': ''
        }
        
        # Extrai séries temporais
        for aval in avaliacoes_ordenadas:
            tendencias['peso'].append({
                'data': aval.data,
                'valor': aval.medidas.peso
            })
            
            if 'percentual_gordura' in aval.resultados:
                tendencias['percentual_gordura'].append({
                    'data': aval.data,
                    'valor': aval.resultados['percentual_gordura']
                })
            
            if 'massa_magra_kg' in aval.resultados:
                tendencias['massa_magra'].append({
                    'data': aval.data,
                    'valor': aval.resultados['massa_magra_kg']
                })
            
            if aval.medidas.cintura:
                tendencias['cintura'].append({
                    'data': aval.data,
                    'valor': aval.medidas.cintura
                })
        
        # Calcula tendências (crescente, decrescente, estável)
        def calcular_tendencia_simples(serie):
            if len(serie) < 2:
                return "insuficiente"
            
            primeiro = serie[0]['valor']
            ultimo = serie[-1]['valor']
            diff = ultimo - primeiro
            perc = (diff / primeiro) * 100 if primeiro != 0 else 0
            
            if abs(perc) < 2:
                return "estável"
            elif diff > 0:
                return "crescente"
            else:
                return "decrescente"
        
        # Análise geral
        analise_geral = []
        
        if tendencias['peso']:
            tend_peso = calcular_tendencia_simples(tendencias['peso'])
            analise_geral.append(f"Peso: {tend_peso}")
        
        if tendencias['percentual_gordura']:
            tend_gord = calcular_tendencia_simples(tendencias['percentual_gordura'])
            if tend_gord == "decrescente":
                analise_geral.append("✓ Gordura: reduzindo")
            elif tend_gord == "crescente":
                analise_geral.append("Gordura: aumentando")
        
        if tendencias['massa_magra']:
            tend_magra = calcular_tendencia_simples(tendencias['massa_magra'])
            if tend_magra == "crescente":
                analise_geral.append("✓ Massa magra: aumentando")
            elif tend_magra == "decrescente":
                analise_geral.append("Massa magra: reduzindo")
        
        tendencias['tendencia_geral'] = " | ".join(analise_geral)
        
        return tendencias
    
    @staticmethod
    def gerar_relatorio_comparativo(comparacao: Dict[str, Any]) -> str:
        """Gera relatório textual de comparação"""
        relatorio = []
        relatorio.append("=" * 60)
        relatorio.append("RELATÓRIO COMPARATIVO DE AVALIAÇÕES")
        relatorio.append("=" * 60)
        relatorio.append("")
        
        relatorio.append(f"Período: {comparacao['data_antiga'].strftime('%d/%m/%Y')} a {comparacao['data_nova'].strftime('%d/%m/%Y')}")
        relatorio.append(f"Intervalo: {comparacao['dias_entre_avaliacoes']} dias")
        relatorio.append(f"Avaliação Geral: {comparacao['avaliacao_geral']}")
        relatorio.append("")
        
        # Evolução
        if comparacao['analise_evolucao']:
            relatorio.append("PRINCIPAIS MUDANÇAS:")
            for item in comparacao['analise_evolucao']:
                relatorio.append(f"  {item}")
            relatorio.append("")
        
        # Medidas detalhadas
        if comparacao['diferencas_medidas']:
            relatorio.append("DIFERENÇAS NAS MEDIDAS:")
            for medida, dados in comparacao['diferencas_medidas'].items():
                sinal = "+" if dados['diferenca'] > 0 else ""
                relatorio.append(
                    f"  {medida.replace('_', ' ').title()}: "
                    f"{dados['anterior']} → {dados['atual']} "
                    f"({sinal}{dados['diferenca']}, {sinal}{dados['percentual']}%)"
                )
            relatorio.append("")
        
        # Índices detalhados
        if comparacao['diferencas_indices']:
            relatorio.append("DIFERENÇAS NOS ÍNDICES:")
            for indice, dados in comparacao['diferencas_indices'].items():
                sinal = "+" if dados['diferenca'] > 0 else ""
                relatorio.append(
                    f"  {indice.replace('_', ' ').title()}: "
                    f"{dados['anterior']} → {dados['atual']} "
                    f"({sinal}{dados['diferenca']})"
                )
            relatorio.append("")
        
        relatorio.append("=" * 60)
        
        return "\n".join(relatorio)
