"""
Serviço de Análise de Avaliações
Processa avaliações e calcula todos os índices corporais.
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


class AnalisadorAvaliacao:
    """Processa avaliações e calcula todos os índices corporais possíveis"""
    
    @staticmethod
    def processar_avaliacao(avaliacao: Avaliacao, usuario: Usuario) -> Dict[str, Any]:
        """
        Processa uma avaliação completa e calcula todos os índices possíveis.
        
        Args:
            avaliacao: Objeto Avaliacao a ser processado
            usuario: Usuário sendo avaliado
            
        Returns:
            Dicionário com todos os resultados calculados
        """
        medidas = avaliacao.medidas
        resultados = {}
        
        # === CÁLCULOS BÁSICOS ===
        
        # IMC
        imc = calcular_imc(medidas.peso, medidas.altura)
        classificacao_imc, descricao_imc = classificar_imc(imc)
        
        resultados['imc'] = imc
        resultados['imc_classificacao'] = classificacao_imc
        resultados['imc_descricao'] = descricao_imc
        
        # === PERCENTUAL DE GORDURA (US Navy) ===
        sexo_str = usuario.sexo.value
        
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
        
        # === ÍNDICES CORPORAIS ===
        
        # RCQ
        if medidas.cintura and medidas.quadril:
            rcq = calcular_rcq(medidas.cintura, medidas.quadril)
            classificacao_rcq, desc_rcq = classificar_rcq(rcq, sexo_str)
            
            resultados['rcq'] = rcq
            resultados['rcq_classificacao'] = classificacao_rcq
            resultados['rcq_descricao'] = desc_rcq
        
        # RCA
        if medidas.cintura:
            rca = calcular_rca(medidas.cintura, medidas.altura)
            classificacao_rca, desc_rca = classificar_rca(rca)
            
            resultados['rca'] = rca
            resultados['rca_classificacao'] = classificacao_rca
            resultados['rca_descricao'] = desc_rca
        
        # === PROPORÇÕES E SIMETRIA ===
        
        if medidas.tem_medidas_proporcao():
            medidas_dict = {
                'altura': medidas.altura,
                'cintura': medidas.cintura,
                'peitoral': medidas.peitoral,
                'ombros': medidas.ombros,
                'braco_relaxado': medidas.braco_relaxado,
                'braco_contraido': medidas.braco_contraido,
                'coxa': medidas.coxa,
                'panturrilha': medidas.panturrilha
            }
            
            proporcoes = calcular_proporcoes(medidas_dict)
            analise = analisar_simetria(proporcoes)
            
            resultados['proporcoes'] = proporcoes
            resultados['analise_simetria'] = analise
            
            # Pontuação estética
            pontuacao, classificacao_est = calcular_pontuacao_estetica(proporcoes)
            resultados['pontuacao_estetica'] = pontuacao
            resultados['classificacao_estetica'] = classificacao_est
        
        # === SOMATOTIPO ===
        
        # Precisa de RCQ, RCA e IMC
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
            
            # Recomendações
            recomendacoes = obter_recomendacoes_somatotipo(somatotipo)
            resultados['recomendacoes'] = recomendacoes
        
        # Adiciona resultados à avaliação
        avaliacao.resultados = resultados
        
        return resultados
    
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
