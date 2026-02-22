"""
Serviço de Análise de Avaliações
Processa avaliações e calcula todos os índices corporais.
Hierarquia de processamento:
1. Validar inputs
2. Calcular médias bilaterais
3. Calcular índices estruturais
4. Ajustar ideais musculares
5. Calcular proporções
6. Calcular simetria
7. Calcular scores modulares
8. Calcular score geral
"""

from typing import Dict, Any, Optional
from ..models.avaliacao import Avaliacao
from ..models.medidas import Medidas
from ..models.usuario import Usuario, Sexo
from ..calculations import (
    calcular_imc, classificar_imc,
    calcular_gordura_us_navy, classificar_gordura,
    calcular_rcq, calcular_rca, classificar_rcq, classificar_rca,
    calcular_proporcoes, analisar_simetria
)
from ..calculations.gordura import calcular_massa_gorda, calcular_massa_magra
from ..calculations.somatotipo import classificar_somatotipo, obter_recomendacoes_somatotipo
from ..calculations.proporcoes import calcular_pontuacao_estetica
from ..calculations.composicao_tecidual import calcular_composicao_tecidual
from ..calculations.mapa_corporal import gerar_mapa_corporal

# Novos imports do sistema renovado
from ..calculations.medias_bilaterais import calcular_todas_medias
from ..calculations.indices_estruturais import calcular_todos_indices_estruturais
from ..calculations.ideais_musculares import calcular_todos_ideais
from ..calculations.simetria import calcular_todas_simetrias, calcular_score_simetria_geral
from ..calculations.score_estetico import (
    calcular_score_superior,
    calcular_score_inferior,
    calcular_score_posterior,
    calcular_score_proporcional,
    calcular_score_composicao,
    calcular_score_geral
)


class AnalisadorAvaliacao:
    """Processa avaliações e calcula todos os índices corporais possíveis"""
    
    @staticmethod
    def processar_avaliacao(avaliacao: Avaliacao, usuario: Usuario) -> Dict[str, Any]:
        """
        Processa uma avaliação completa e calcula todos os índices possíveis.
        Segue hierarquia de processamento estrita.
        
        Args:
            avaliacao: Objeto Avaliacao a ser processado
            usuario: Usuário sendo avaliado
            
        Returns:
            Dicionário com todos os resultados calculados
        """
        medidas = avaliacao.medidas
        resultados = {}
        sexo_str = usuario.sexo.value
        
        # === ETAPA 1: CÁLCULOS BÁSICOS ===
        
        # IMC
        imc = calcular_imc(medidas.peso, medidas.altura)
        classificacao_imc, descricao_imc = classificar_imc(imc)
        
        resultados['imc'] = imc
        resultados['imc_classificacao'] = classificacao_imc
        resultados['imc_descricao'] = descricao_imc
        
        # Percentual de Gordura (US Navy)
        if medidas.tem_medidas_minimas_us_navy(sexo_str):
            try:
                percentual_gordura = calcular_gordura_us_navy(
                    altura_cm=medidas.altura,
                    cintura_cm=medidas.cintura,
                    pescoco_cm=medidas.pescoco,
                    sexo=sexo_str,
                    quadril_cm=medidas.quadril
                )
                
                resultados['percentual_gordura'] = percentual_gordura
                resultados['classificacao_gordura'] = classificar_gordura(
                    percentual_gordura, sexo_str, usuario.idade
                )
                
                # Massas
                resultados['massa_gorda_kg'] = calcular_massa_gorda(
                    medidas.peso, percentual_gordura
                )
                resultados['massa_magra_kg'] = calcular_massa_magra(
                    medidas.peso, percentual_gordura
                )
            except ValueError as e:
                resultados['erro_gordura'] = str(e)
        
        # RCQ e RCA
        if medidas.cintura and medidas.quadril:
            rcq = calcular_rcq(medidas.cintura, medidas.quadril)
            classificacao_rcq, desc_rcq = classificar_rcq(rcq, sexo_str)
            
            resultados['rcq'] = rcq
            resultados['rcq_classificacao'] = classificacao_rcq
            resultados['rcq_descricao'] = desc_rcq
        
        if medidas.cintura:
            rca = calcular_rca(medidas.cintura, medidas.altura)
            classificacao_rca, desc_rca = classificar_rca(rca)
            
            resultados['rca'] = rca
            resultados['rca_classificacao'] = classificacao_rca
            resultados['rca_descricao'] = desc_rca
        
        # === ETAPA 2: MÉDIAS BILATERAIS ===
        
        medidas_dict = AnalisadorAvaliacao._medidas_para_dict(medidas)
        medias_bilaterais = calcular_todas_medias(medidas_dict)
        resultados['medias_bilaterais'] = medias_bilaterais
        
        # === ETAPA 3: ÍNDICES ESTRUTURAIS (Camada 1) ===
        
        indices_estruturais = calcular_todos_indices_estruturais(
            medidas_dict,
            medias_bilaterais,
            medidas.altura,
            sexo_str
        )
        resultados['indices_estruturais'] = indices_estruturais
        
        # === ETAPA 4: AJUSTAR IDEAIS MUSCULARES ===
        
        ideais_musculares = calcular_todos_ideais(
            altura=medidas.altura,
            sexo=sexo_str,
            fator_estrutural=indices_estruturais.fator_estrutural_ombros
        )
        resultados['ideais_musculares'] = ideais_musculares
        
        # === ETAPA 5: PROPORÇÕES (Legado mantido para compatibilidade) ===
        
        if medidas.tem_medidas_proporcao():
            proporcoes = calcular_proporcoes(medidas_dict)
            analise = analisar_simetria(proporcoes)
            
            resultados['proporcoes'] = proporcoes
            resultados['analise_simetria'] = analise
            
            pontuacao, classificacao_est = calcular_pontuacao_estetica(proporcoes)
            resultados['pontuacao_estetica'] = pontuacao
            resultados['classificacao_estetica'] = classificacao_est
        
        # === ETAPA 6: SIMETRIA BILATERAL ===
        
        simetrias = calcular_todas_simetrias(medidas_dict)
        score_simetria_geral = calcular_score_simetria_geral(simetrias)
        resultados['simetrias'] = simetrias
        resultados['score_simetria_geral'] = score_simetria_geral
        
        # === ETAPA 7: SCORES MODULARES ===
        
        scores_modulares = {}
        
        # Score Superior
        scores_modulares['superior'] = calcular_score_superior(
            medidas=medidas_dict,
            medias=medias_bilaterais,
            ideais=ideais_musculares,
            simetrias=simetrias,
            largura_ombros=medidas_dict.get('largura_ombros')
        )
        
        # Score Inferior
        scores_modulares['inferior'] = calcular_score_inferior(
            medias=medias_bilaterais,
            ideais=ideais_musculares,
            simetrias=simetrias,
            quadril=medidas.quadril
        )
        
        # Score Posterior
        scores_modulares['posterior'] = calcular_score_posterior(
            indices_estruturais=indices_estruturais,
            medidas=medidas_dict
        )
        
        # Score Proporcional
        scores_modulares['proporcional'] = calcular_score_proporcional(
            medidas=medidas_dict,
            altura=medidas.altura
        )
        
        # Score Composição
        scores_modulares['composicao'] = calcular_score_composicao(
            percentual_gordura=resultados.get('percentual_gordura'),
            sexo=sexo_str,
            imc=imc
        )
        
        resultados['scores_modulares'] = scores_modulares
        
        # === ETAPA 8: SCORE GERAL ===
        
        score_geral_resultado = calcular_score_geral(
            score_composicao=scores_modulares['composicao']['score'],
            score_proporcional=scores_modulares['proporcional']['score'],
            score_superior=scores_modulares['superior']['score'],
            score_inferior=scores_modulares['inferior']['score'],
            score_posterior=scores_modulares['posterior']['score']
        )
        resultados['score_geral'] = score_geral_resultado
        
        # === MÓDULOS LEGADOS (Mantidos para compatibilidade) ===
        
        # Composição Tecidual
        if 'percentual_gordura' in resultados:
            composicao = calcular_composicao_tecidual(
                peso=medidas.peso,
                percentual_gordura=resultados['percentual_gordura'],
                sexo=sexo_str
            )
            resultados['composicao_tecidual'] = composicao
        
        # Mapa Corporal
        if medidas.cintura:
            mapa = gerar_mapa_corporal(medidas_dict, medidas.altura, sexo_str)
            resultados['mapa_corporal'] = mapa
        
        # Somatotipo
        if 'rcq' in resultados and 'rca' in resultados:
            proporcoes_dict = {}
            if 'proporcoes' in resultados:
                prop = resultados['proporcoes']
                proporcoes_dict = {
                    'ombro_cintura': prop.ombro_cintura,
                    'peitoral_cintura': prop.peitoral_cintura
                }
            
            somatotipo, desc_somato, scores_somato = classificar_somatotipo(
                rcq=resultados['rcq'],
                rca=resultados['rca'],
                imc=imc,
                proporcoes=proporcoes_dict
            )
            
            resultados['somatotipo'] = somatotipo.value
            resultados['somatotipo_descricao'] = desc_somato
            resultados['somatotipo_scores'] = scores_somato
            
            recomendacoes = obter_recomendacoes_somatotipo(somatotipo)
            resultados['recomendacoes'] = recomendacoes
        
        # Adiciona resultados à avaliação
        avaliacao.resultados = resultados
        
        return resultados
    
    @staticmethod
    def _medidas_para_dict(medidas: Medidas) -> Dict[str, float]:
        """
        Converte objeto Medidas em dicionário.
        
        Args:
            medidas: Objeto Medidas
            
        Returns:
            Dicionário com todas as medidas
        """
        return {
            'altura': medidas.altura,
            'peso': medidas.peso,
            'pescoco': medidas.pescoco,
            'peitoral': medidas.peitoral,
            'cintura': medidas.cintura,
            'abdomen': medidas.abdomen,
            'quadril': medidas.quadril,
            'ombros': medidas.ombros,
            # Bilaterais - circunferências
            'braco_relaxado_esquerdo': medidas.braco_relaxado_esquerdo,
            'braco_relaxado_direito': medidas.braco_relaxado_direito,
            'braco_contraido_esquerdo': medidas.braco_contraido_esquerdo,
            'braco_contraido_direito': medidas.braco_contraido_direito,
            'antebraco_esquerdo': medidas.antebraco_esquerdo,
            'antebraco_direito': medidas.antebraco_direito,
            'coxa_esquerda': medidas.coxa_esquerda,
            'coxa_direita': medidas.coxa_direita,
            'panturrilha_esquerda': medidas.panturrilha_esquerda,
            'panturrilha_direita': medidas.panturrilha_direita,
            # Larguras ósseas
            'largura_ombros': medidas.largura_ombros,
            'largura_quadril': medidas.largura_quadril,
            'largura_punho_esquerdo': medidas.largura_punho_esquerdo,
            'largura_punho_direito': medidas.largura_punho_direito,
            'largura_cotovelo_esquerdo': medidas.largura_cotovelo_esquerdo,
            'largura_cotovelo_direito': medidas.largura_cotovelo_direito,
            'largura_joelho_esquerdo': medidas.largura_joelho_esquerdo,
            'largura_joelho_direito': medidas.largura_joelho_direito,
            'largura_tornozelo_esquerdo': medidas.largura_tornozelo_esquerdo,
            'largura_tornozelo_direito': medidas.largura_tornozelo_direito,
        }
    
    @staticmethod
    def gerar_relatorio_texto(avaliacao: Avaliacao, usuario: Usuario) -> str:
        """
        Gera um relatório textual completo da avaliação.
        
        Args:
            avaliacao: Avaliação processada
            usuario: Usuário avaliado
            
        Returns:
            Relatório em formato texto
        """
        r = avaliacao.resultados
        m = avaliacao.medidas
        
        relatorio = []
        relatorio.append("=" * 60)
        relatorio.append("RELATÓRIO DE AVALIAÇÃO CORPORAL")
        relatorio.append("=" * 60)
        relatorio.append("")
        
        # Dados do usuário
        relatorio.append(f"Nome: {usuario.nome}")
        relatorio.append(f"Sexo: {usuario.sexo.value}")
        relatorio.append(f"Idade: {usuario.idade} anos")
        relatorio.append(f"Data da Avaliação: {avaliacao.data.strftime('%d/%m/%Y')}")
        relatorio.append("")
        
        # Medidas básicas
        relatorio.append("MEDIDAS BÁSICAS:")
        relatorio.append(f"  Altura: {m.altura} cm")
        relatorio.append(f"  Peso: {m.peso} kg")
        relatorio.append("")
        
        # Circunferências
        relatorio.append("CIRCUNFERÊNCIAS (cm):")
        if m.pescoco:
            relatorio.append(f"  Pescoço: {m.pescoco}")
        if m.ombros:
            relatorio.append(f"  Ombros: {m.ombros}")
        if m.peitoral:
            relatorio.append(f"  Peitoral: {m.peitoral}")
        if m.cintura:
            relatorio.append(f"  Cintura: {m.cintura}")
        if m.abdomen:
            relatorio.append(f"  Abdômen: {m.abdomen}")
        if m.quadril:
            relatorio.append(f"  Quadril: {m.quadril}")
        if m.braco_relaxado:
            relatorio.append(f"  Braço (relaxado): {m.braco_relaxado}")
        if m.braco_contraido:
            relatorio.append(f"  Braço (contraído): {m.braco_contraido}")
        if m.coxa:
            relatorio.append(f"  Coxa: {m.coxa}")
        if m.panturrilha:
            relatorio.append(f"  Panturrilha: {m.panturrilha}")
        relatorio.append("")
        
        # Índices calculados
        relatorio.append("ÍNDICES CORPORAIS:")
        relatorio.append(f"  IMC: {r['imc']} - {r['imc_descricao']}")
        
        if 'percentual_gordura' in r:
            relatorio.append(f"  % Gordura: {r['percentual_gordura']}% - {r['classificacao_gordura']}")
            relatorio.append(f"  Massa Gorda: {r['massa_gorda_kg']} kg")
            relatorio.append(f"  Massa Magra: {r['massa_magra_kg']} kg")
        
        if 'rcq' in r:
            relatorio.append(f"  RCQ: {r['rcq']} - {r['rcq_descricao']}")
        
        if 'rca' in r:
            relatorio.append(f"  RCA: {r['rca']} - {r['rca_descricao']}")
        
        relatorio.append("")
        
        # Proporções
        if 'proporcoes' in r:
            relatorio.append("PROPORÇÕES CORPORAIS:")
            prop = r['proporcoes']
            
            if prop.ombro_cintura:
                relatorio.append(f"  Ombros/Cintura: {prop.ombro_cintura}")
            if prop.peitoral_cintura:
                relatorio.append(f"  Peitoral/Cintura: {prop.peitoral_cintura}")
            if prop.braco_panturrilha:
                relatorio.append(f"  Braço/Panturrilha: {prop.braco_panturrilha}")
            
            relatorio.append("")
            
            if 'analise_simetria' in r:
                relatorio.append("ANÁLISE DE SIMETRIA:")
                for chave, feedback in r['analise_simetria'].items():
                    relatorio.append(f"  {chave}: {feedback}")
                relatorio.append("")
            
            if 'pontuacao_estetica' in r:
                relatorio.append(f"PONTUAÇÃO ESTÉTICA: {r['pontuacao_estetica']}/100 - {r['classificacao_estetica']}")
                relatorio.append("")
        
        # Somatotipo
        if 'somatotipo' in r:
            relatorio.append("CLASSIFICAÇÃO DE SOMATOTIPO:")
            relatorio.append(f"  Tipo: {r['somatotipo'].upper()}")
            relatorio.append(f"  {r['somatotipo_descricao']}")
            relatorio.append("")
            relatorio.append("  Distribuição:")
            for tipo, score in r['somatotipo_scores'].items():
                relatorio.append(f"    {tipo.capitalize()}: {score}%")
            relatorio.append("")
        
        # Recomendações
        if 'recomendacoes' in r:
            relatorio.append("RECOMENDAÇÕES:")
            rec = r['recomendacoes']
            relatorio.append(f"\nTREINO:")
            relatorio.append(f"  {rec['treino']}")
            relatorio.append(f"\nDIETA:")
            relatorio.append(f"  {rec['dieta']}")
            relatorio.append(f"\nDICAS:")
            relatorio.append(f"  {rec['dicas']}")
            relatorio.append("")
        
        relatorio.append("=" * 60)
        
        return "\n".join(relatorio)
