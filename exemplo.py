"""
Exemplo de Uso Completo do Sistema de Medidas Corporais

Este script demonstra todas as funcionalidades principais do sistema.
"""

from datetime import date, timedelta
from src.models import Usuario, Medidas, Avaliacao
from src.models.usuario import Sexo
from src.services import AnalisadorAvaliacao, ComparadorAvaliacoes
from src.validators import ValidadorMedidas


def exemplo_completo():
    """Exemplo de uso completo do sistema"""
    
    print("=" * 70)
    print("SISTEMA DE ANÁLISE DE MEDIDAS CORPORAIS")
    print("Exemplo de Uso Completo")
    print("=" * 70)
    print()
    
    # ========================================
    # 1. CRIAR USUÁRIO
    # ========================================
    print("1. CRIANDO USUÁRIO")
    print("-" * 70)
    
    usuario = Usuario(
        nome="João Silva",
        sexo=Sexo.MASCULINO,
        data_nascimento=date(1990, 5, 15),
        email="joao.silva@email.com",
        telefone="(11) 98765-4321"
    )
    
    print(f"✓ Usuário criado: {usuario.nome}")
    print(f"  Idade: {usuario.idade} anos")
    print(f"  Sexo: {usuario.sexo.value}")
    print()
    
    # ========================================
    # 2. PRIMEIRA AVALIAÇÃO
    # ========================================
    print("2. REGISTRANDO PRIMEIRA AVALIAÇÃO")
    print("-" * 70)
    
    medidas1 = Medidas(
        altura=178,
        peso=85,
        pescoco=38,
        ombros=120,
        peitoral=105,
        cintura=88,
        abdomen=92,
        quadril=100,
        braco_relaxado=35,
        braco_contraido=38,
        antebraco=30,
        coxa=58,
        panturrilha=38
    )
    
    # Validar medidas
    erros = ValidadorMedidas.validar_todas_medidas({
        'altura': medidas1.altura,
        'peso': medidas1.peso,
        'cintura': medidas1.cintura,
        'quadril': medidas1.quadril
    })
    
    if erros:
        print("⚠ Erros encontrados:", erros)
    else:
        print("✓ Medidas validadas com sucesso")
    
    avaliacao1 = Avaliacao(
        data=date.today() - timedelta(days=90),  # 3 meses atrás
        medidas=medidas1,
        usuario_id="user_001",
        objetivo="Hipertrofia e redução de gordura"
    )
    
    # Processar avaliação
    print("\nProcessando avaliação...")
    resultados1 = AnalisadorAvaliacao.processar_avaliacao(avaliacao1, usuario)
    
    # Adicionar ao usuário
    usuario.adicionar_avaliacao(avaliacao1)
    
    print(f"✓ Avaliação registrada em {avaliacao1.data.strftime('%d/%m/%Y')}")
    print()
    
    # ========================================
    # 3. EXIBIR RELATÓRIO COMPLETO
    # ========================================
    print("3. RELATÓRIO DA PRIMEIRA AVALIAÇÃO")
    print("-" * 70)
    
    relatorio1 = AnalisadorAvaliacao.gerar_relatorio_texto(avaliacao1, usuario)
    print(relatorio1)
    print()
    
    # ========================================
    # 4. SEGUNDA AVALIAÇÃO (após 3 meses)
    # ========================================
    print("4. REGISTRANDO SEGUNDA AVALIAÇÃO (3 MESES DEPOIS)")
    print("-" * 70)
    
    medidas2 = Medidas(
        altura=178,
        peso=83,  # Perdeu 2kg
        pescoco=37,  # Reduziu pescoço
        ombros=122,  # Ganhou ombros
        peitoral=107,  # Ganhou peitoral
        cintura=84,  # Reduziu cintura (-4cm!)
        abdomen=88,  # Reduziu abdômen
        quadril=98,  # Reduziu quadril
        braco_relaxado=36,  # Ganhou braço
        braco_contraido=40,  # Ganhou braço contraído
        antebraco=31,
        coxa=60,  # Ganhou coxa
        panturrilha=39  # Ganhou panturrilha
    )
    
    avaliacao2 = Avaliacao(
        data=date.today(),
        medidas=medidas2,
        usuario_id="user_001",
        objetivo="Manutenção e definição"
    )
    
    # Processar segunda avaliação
    resultados2 = AnalisadorAvaliacao.processar_avaliacao(avaliacao2, usuario)
    usuario.adicionar_avaliacao(avaliacao2)
    
    print(f"✓ Segunda avaliação registrada em {avaliacao2.data.strftime('%d/%m/%Y')}")
    print()
    
    # ========================================
    # 5. COMPARAÇÃO ENTRE AVALIAÇÕES
    # ========================================
    print("5. COMPARAÇÃO ENTRE AVALIAÇÕES")
    print("-" * 70)
    
    comparacao = ComparadorAvaliacoes.comparar_duas_avaliacoes(avaliacao1, avaliacao2)
    relatorio_comparativo = ComparadorAvaliacoes.gerar_relatorio_comparativo(comparacao)
    
    print(relatorio_comparativo)
    print()
    
    # ========================================
    # 6. ANÁLISE DE TENDÊNCIAS
    # ========================================
    print("6. ANÁLISE DE TENDÊNCIAS")
    print("-" * 70)
    
    # Criar mais uma avaliação intermediária para demonstrar tendências
    medidas_intermediaria = Medidas(
        altura=178,
        peso=84,
        pescoco=37.5,
        ombros=121,
        peitoral=106,
        cintura=86,
        abdomen=90,
        quadril=99,
        braco_relaxado=35.5,
        braco_contraido=39,
        coxa=59,
        panturrilha=38.5
    )
    
    avaliacao_intermediaria = Avaliacao(
        data=date.today() - timedelta(days=45),
        medidas=medidas_intermediaria,
        usuario_id="user_001"
    )
    
    AnalisadorAvaliacao.processar_avaliacao(avaliacao_intermediaria, usuario)
    usuario.adicionar_avaliacao(avaliacao_intermediaria)
    
    # Analisar tendências
    tendencias = ComparadorAvaliacoes.analisar_tendencia(usuario.avaliacoes)
    
    print(f"Número de avaliações: {tendencias['numero_avaliacoes']}")
    print(f"Período total: {tendencias['periodo_dias']} dias")
    print(f"Tendência geral: {tendencias['tendencia_geral']}")
    print()
    
    # Evolução do peso
    if tendencias['peso']:
        print("Evolução do Peso:")
        for registro in tendencias['peso']:
            print(f"  {registro['data'].strftime('%d/%m/%Y')}: {registro['valor']} kg")
        print()
    
    # Evolução do percentual de gordura
    if tendencias['percentual_gordura']:
        print("Evolução do % de Gordura:")
        for registro in tendencias['percentual_gordura']:
            print(f"  {registro['data'].strftime('%d/%m/%Y')}: {registro['valor']}%")
        print()
    
    # ========================================
    # 7. RESUMO FINAL
    # ========================================
    print("7. RESUMO FINAL")
    print("-" * 70)
    
    ultima_avaliacao = usuario.obter_ultima_avaliacao()
    
    print(f"Usuário: {usuario.nome}")
    print(f"Total de avaliações: {len(usuario.avaliacoes)}")
    print(f"Última avaliação: {ultima_avaliacao.data.strftime('%d/%m/%Y')}")
    print()
    
    if ultima_avaliacao.tem_resultado('imc'):
        print(f"IMC atual: {ultima_avaliacao.obter_resultado('imc')}")
        print(f"Classificação: {ultima_avaliacao.obter_resultado('imc_descricao')}")
        print()
    
    if ultima_avaliacao.tem_resultado('percentual_gordura'):
        print(f"% Gordura: {ultima_avaliacao.obter_resultado('percentual_gordura')}%")
        print(f"Massa Magra: {ultima_avaliacao.obter_resultado('massa_magra_kg')} kg")
        print(f"Massa Gorda: {ultima_avaliacao.obter_resultado('massa_gorda_kg')} kg")
        print()
    
    if ultima_avaliacao.tem_resultado('somatotipo'):
        print(f"Somatotipo: {ultima_avaliacao.obter_resultado('somatotipo')}")
        print(f"{ultima_avaliacao.obter_resultado('somatotipo_descricao')}")
        print()
    
    if ultima_avaliacao.tem_resultado('pontuacao_estetica'):
        print(f"Pontuação Estética: {ultima_avaliacao.obter_resultado('pontuacao_estetica')}/100")
        print(f"Classificação: {ultima_avaliacao.obter_resultado('classificacao_estetica')}")
        print()
    
    print("=" * 70)
    print("EXEMPLO CONCLUÍDO COM SUCESSO!")
    print("=" * 70)


def exemplo_basico():
    """Exemplo básico rápido"""
    
    print("\n" + "=" * 70)
    print("EXEMPLO BÁSICO - USO RÁPIDO")
    print("=" * 70 + "\n")
    
    # Criar usuário
    usuario = Usuario(
        nome="Maria Santos",
        sexo=Sexo.FEMININO,
        data_nascimento=date(1995, 8, 20)
    )
    
    # Criar medidas
    medidas = Medidas(
        altura=165,
        peso=62,
        pescoco=32,
        cintura=68,
        quadril=95,
        peitoral=88,
        braco_contraido=30,
        panturrilha=36
    )
    
    # Criar avaliação
    avaliacao = Avaliacao(
        data=date.today(),
        medidas=medidas
    )
    
    # Processar
    AnalisadorAvaliacao.processar_avaliacao(avaliacao, usuario)
    
    # Exibir resultados principais
    print(f"Nome: {usuario.nome}")
    print(f"Peso: {medidas.peso} kg | Altura: {medidas.altura} cm")
    print(f"IMC: {avaliacao.obter_resultado('imc')} - {avaliacao.obter_resultado('imc_descricao')}")
    print(f"% Gordura: {avaliacao.obter_resultado('percentual_gordura')}%")
    print(f"Somatotipo: {avaliacao.obter_resultado('somatotipo')}")
    print(f"RCA: {avaliacao.obter_resultado('rca')} - {avaliacao.obter_resultado('rca_descricao')}")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    # Executar exemplo completo
    exemplo_completo()
    
    # Executar exemplo básico
    exemplo_basico()
