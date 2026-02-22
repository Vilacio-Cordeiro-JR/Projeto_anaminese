"""
Health Check - Teste de Saúde do Sistema
Testa todas as funcionalidades principais
"""

import requests
import json
from datetime import date

BASE_URL = "http://localhost:5000"

def test_login():
    """Testa login"""
    print("\n🔐 TESTANDO LOGIN...")
    
    # Criar sessão persistente
    session = requests.Session()
    
    response = session.post(f"{BASE_URL}/api/login", 
        json={"nome": "Vilacio", "senha": "123456"})
    
    if response.status_code == 200:
        print("✅ Login bem-sucedido")
        return session
    else:
        print(f"❌ Login falhou: {response.status_code}")
        try:
            print(f"   Erro: {response.json()}")
        except:
            print(f"   Resposta: {response.text}")
        return None

def test_criar_avaliacao(session):
    """Testa criação de avaliação completa"""
    print("\n📝 TESTANDO CRIAÇÃO DE AVALIAÇÃO...")
    
    avaliacao_completa = {
        "data": date.today().isoformat(),
        "objetivo": "Teste de saúde do sistema",
        "peso": 85.5,
        
        # Circunferências principais
        "pescoco": 38.0,
        "ombros": 120.0,  # Campo que estava faltando!
        "peitoral": 105.0,
        "cintura": 85.0,
        "abdomen": 90.0,
        "quadril": 100.0,
        
        # Medidas bilaterais - Braços
        "braco_relaxado_esquerdo": 35.0,
        "braco_relaxado_direito": 35.5,
        "braco_contraido_esquerdo": 38.0,
        "braco_contraido_direito": 38.5,
        "antebraco_esquerdo": 28.0,
        "antebraco_direito": 28.5,
        
        # Medidas bilaterais - Pernas
        "coxa_esquerda": 58.0,
        "coxa_direita": 58.5,
        "panturrilha_esquerda": 38.0,
        "panturrilha_direita": 38.5,
        
        # Larguras ósseas (Camada 1 - Estrutura)
        "largura_ombros": 42.0,
        "largura_quadril": 32.0,
        "largura_punho_esquerdo": 6.5,
        "largura_punho_direito": 6.6,
        "largura_cotovelo_esquerdo": 7.2,
        "largura_cotovelo_direito": 7.3,
        "largura_joelho_esquerdo": 10.0,
        "largura_joelho_direito": 10.1,
        "largura_tornozelo_esquerdo": 7.5,
        "largura_tornozelo_direito": 7.6
    }
    
    response = session.post(
        f"{BASE_URL}/api/avaliacoes",
        json=avaliacao_completa
    )
    
    if response.status_code == 200 or response.status_code == 201:
        print("✅ Avaliação criada com sucesso")
        resultado = response.json()
        print(f"   📊 ID: {resultado.get('id', 'N/A')}")
        return resultado
    else:
        print(f"❌ Criação falhou: {response.status_code}")
        try:
            print(f"   Erro: {response.json()}")
        except:
            print(f"   Resposta: {response.text[:200]}")
        return None

def test_listar_avaliacoes(session):
    """Testa listagem de avaliações"""
    print("\n📋 TESTANDO LISTAGEM DE AVALIAÇÕES...")
    
    response = session.get(f"{BASE_URL}/api/avaliacoes")
    
    if response.status_code == 200:
        avaliacoes = response.json()
        print(f"✅ {len(avaliacoes)} avaliação(ões) encontrada(s)")
        
        # Testar se tem resultados calculados
        if avaliacoes:
            ultima = avaliacoes[-1]
            resultados = ultima.get('resultados', {})
            
            print("\n📊 VERIFICANDO CÁLCULOS DA ÚLTIMA AVALIAÇÃO:")
            
            # Verificar módulos essenciais
            checks = {
                "IMC": resultados.get('imc'),
                "Médias Bilaterais": resultados.get('medias_bilaterais'),
                "Índices Estruturais": resultados.get('indices_estruturais'),
                "Ideais Musculares": resultados.get('ideais_musculares'),
                "Simetrias": resultados.get('simetrias'),
                "Scores Modulares": resultados.get('scores_modulares'),
                "Score Geral": resultados.get('score_geral')
            }
            
            for nome, valor in checks.items():
                status = "✅" if valor is not None else "❌"
                print(f"   {status} {nome}: {'OK' if valor else 'FALTANDO'}")
            
            # Detalhar scores modulares
            if resultados.get('scores_modulares'):
                print("\n   📈 SCORES MODULARES:")
                scores = resultados['scores_modulares']
                for tipo in ['superior', 'inferior', 'posterior', 'proporcional', 'composicao']:
                    score_data = scores.get(tipo, {})
                    score_valor = score_data.get('score', 'N/A')
                    print(f"      • {tipo.capitalize()}: {score_valor}")
            
            # Score geral
            if resultados.get('score_geral'):
                sg = resultados['score_geral']
                print(f"\n   🏆 SCORE GERAL: {sg.get('score', 'N/A')}/100")
                print(f"      Classificação: {sg.get('classificacao', 'N/A')}")
        
        return avaliacoes
    else:
        print(f"❌ Listagem falhou: {response.status_code}")
        return None

def test_comparacao(session):
    """Testa sistema de comparação"""
    print("\n📊 TESTANDO COMPARAÇÃO DE AVALIAÇÕES...")
    
    response = session.get(f"{BASE_URL}/api/comparacao")
    
    if response.status_code == 200:
        print("✅ Endpoint de comparação acessível")
        return True
    else:
        print(f"⚠️ Comparação retornou: {response.status_code}")
        return False

def run_health_check():
    """Executa todos os testes"""
    print("=" * 60)
    print("🏥 HEALTH CHECK - SISTEMA DE MEDIDAS CORPORAIS")
    print("=" * 60)
    
    # Teste 1: Login
    session = test_login()
    if not session:
        print("\n❌ FALHA CRÍTICA: Não foi possível fazer login")
        return
    
    # Teste 2: Criar avaliação
    avaliacao = test_criar_avaliacao(session)
    if not avaliacao:
        print("\n⚠️ AVISO: Falha ao criar avaliação")
    
    # Teste 3: Listar avaliações
    avaliacoes = test_listar_avaliacoes(session)
    
    # Teste 4: Comparação
    test_comparacao(session)
    
    print("\n" + "=" * 60)
    print("✅ HEALTH CHECK CONCLUÍDO")
    print("=" * 60)
    print("\n💡 Verifique os resultados acima para identificar problemas")

if __name__ == "__main__":
    try:
        run_health_check()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar ao servidor")
        print("   Certifique-se que o servidor está rodando em http://localhost:5000")
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
