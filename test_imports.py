"""
Teste de importações do sistema
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testando importações...")

try:
    from src.models.usuario import Usuario, Sexo
    print("✓ Usuario e Sexo importados")
except Exception as e:
    print(f"✗ Erro ao importar Usuario: {e}")

try:
    from src.models.medidas import Medidas
    print("✓ Medidas importado")
except Exception as e:
    print(f"✗ Erro ao importar Medidas: {e}")

try:
    from src.models.avaliacao import Avaliacao
    print("✓ Avaliacao importado")
except Exception as e:
    print(f"✗ Erro ao importar Avaliacao: {e}")

try:
    from src.services.analisador import AnalisadorAvaliacao
    print("✓ AnalisadorAvaliacao importado")
except Exception as e:
    print(f"✗ Erro ao importar AnalisadorAvaliacao: {e}")

print("\nTeste de criação de objetos...")

try:
    from datetime import date
    
    # Criar usuário
    usuario = Usuario(
        nome="Teste",
        sexo=Sexo.MASCULINO,
        data_nascimento=date(2000, 1, 1)
    )
    print(f"✓ Usuário criado: {usuario.nome}, {usuario.idade} anos")
    
    # Criar medidas
    medidas = Medidas(
        altura=175,
        peso=75,
        cintura=85,
        quadril=95,
        pescoco=38
    )
    print(f"✓ Medidas criadas: Peso {medidas.peso}kg, Altura {medidas.altura}cm")
    
    # Criar avaliação
    avaliacao = Avaliacao(
        data=date.today(),
        medidas=medidas
    )
    print(f"✓ Avaliação criada: {avaliacao.data}")
    
    # Processar avaliação
    resultados = AnalisadorAvaliacao.processar_avaliacao(avaliacao, usuario)
    print(f"✓ Avaliação processada: {len(resultados)} resultados calculados")
    print(f"  - IMC: {resultados.get('imc', 'N/A')}")
    print(f"  - % Gordura: {resultados.get('percentual_gordura', 'N/A')}")
    print(f"  - RCQ: {resultados.get('rcq', 'N/A')}")
    
except Exception as e:
    print(f"✗ Erro ao testar objetos: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Testes concluídos!")
