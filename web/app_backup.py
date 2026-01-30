"""
Servidor Flask para o Sistema de Medidas Corporais
Fornece API REST e serve a interface web
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import date, datetime
import json
import os
import sys

# Adiciona o diretório raiz ao path para importar módulos src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Usuario, Medidas, Avaliacao
from src.models.usuario import Sexo
from src.services import AnalisadorAvaliacao, ComparadorAvaliacoes
from src.validators import ValidadorMedidas

app = Flask(__name__)
CORS(app)

# Caminho para o arquivo JSON de dados
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'usuarios.json')


def carregar_dados():
    """Carrega dados do arquivo JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def salvar_dados(dados):
    """Salva dados no arquivo JSON"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, default=str)


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/usuario', methods=['GET', 'POST', 'PUT'])
def usuario_api():
    """API para gerenciar usuário"""
    dados = carregar_dados()
    
    if request.method == 'GET':
        # Retorna dados do usuário (por enquanto usuário único)
        return jsonify(dados.get('usuario', None))
    
    elif request.method == 'POST' or request.method == 'PUT':
        # Cria ou atualiza usuário
        data = request.json
        
        # Validações
        if not data.get('nome'):
            return jsonify({'erro': 'Nome é obrigatório'}), 400
        
        if not data.get('data_nascimento'):
            return jsonify({'erro': 'Data de nascimento é obrigatória'}), 400
        
        if not data.get('sexo'):
            return jsonify({'erro': 'Sexo é obrigatório'}), 400
        
        # Calcula idade
        data_nasc = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        hoje = date.today()
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        
        usuario_data = {
            'nome': data['nome'],
            'sexo': data['sexo'],
            'data_nascimento': data['data_nascimento'],
            'email': data.get('email', ''),
            'altura': data.get('altura', 0),
            'idade': idade,
            'tema': data.get('tema', 'light')
        }
        
        dados['usuario'] = usuario_data
        salvar_dados(dados)
        
        return jsonify(usuario_data)


@app.route('/api/avaliacoes', methods=['GET', 'POST'])
def avaliacoes_api():
    """API para gerenciar avaliações"""
    dados = carregar_dados()
    
    if request.method == 'GET':
        # Retorna todas as avaliações
        avaliacoes = dados.get('avaliacoes', [])
        return jsonify(avaliacoes)
    
    elif request.method == 'POST':
        # Cria nova avaliação
        data = request.json
        usuario_data = dados.get('usuario')
        
        if not usuario_data:
            return jsonify({'erro': 'Usuário não cadastrado'}), 400
        
        # Validar medidas
        medidas_dict = {
            'altura': data['medidas'].get('altura', usuario_data.get('altura')),
            'peso': data['medidas']['peso'],
            'pescoco': data['medidas'].get('pescoco'),
            'ombros': data['medidas'].get('ombros'),
            'peitoral': data['medidas'].get('peitoral'),
            'cintura': data['medidas'].get('cintura'),
            'abdomen': data['medidas'].get('abdomen'),
            'quadril': data['medidas'].get('quadril'),
            'braco_relaxado': data['medidas'].get('braco_relaxado'),
            'braco_contraido': data['medidas'].get('braco_contraido'),
            'antebraco': data['medidas'].get('antebraco'),
            'coxa': data['medidas'].get('coxa'),
            'panturrilha': data['medidas'].get('panturrilha'),
            'punho': data['medidas'].get('punho'),
            'joelho': data['medidas'].get('joelho'),
            'tornozelo': data['medidas'].get('tornozelo')
        }
        
        # Validar
        erros = ValidadorMedidas.validar_todas_medidas(medidas_dict)
        if erros:
            return jsonify({'erro': erros}), 400
        
        # Criar objetos do sistema
        try:
            usuario = Usuario(
                nome=usuario_data['nome'],
                sexo=Sexo.MASCULINO if usuario_data['sexo'] == 'M' else Sexo.FEMININO,
                data_nascimento=datetime.strptime(usuario_data['data_nascimento'], '%Y-%m-%d').date(),
                email=usuario_data.get('email')
            )
            
            medidas = Medidas(**{k: v for k, v in medidas_dict.items() if v})
            
            avaliacao = Avaliacao(
                data=date.today(),
                medidas=medidas,
                objetivo=data.get('objetivo', '')
            )
            
            # Processar avaliação
            resultados = AnalisadorAvaliacao.processar_avaliacao(avaliacao, usuario)
            
            # Preparar dados para salvar
            avaliacao_json = {
                'id': datetime.now().isoformat(),
                'data': avaliacao.data.isoformat(),
                'medidas': medidas_dict,
                'objetivo': data.get('objetivo', ''),
                'resultados': {
                    'imc': resultados.get('imc'),
                    'imc_descricao': resultados.get('imc_descricao'),
                    'percentual_gordura': resultados.get('percentual_gordura'),
                    'classificacao_gordura': resultados.get('classificacao_gordura'),
                    'massa_gorda_kg': resultados.get('massa_gorda_kg'),
                    'massa_magra_kg': resultados.get('massa_magra_kg'),
                    'rcq': resultados.get('rcq'),
                    'rcq_descricao': resultados.get('rcq_descricao'),
                    'rca': resultados.get('rca'),
                    'rca_descricao': resultados.get('rca_descricao'),
                    'somatotipo': resultados.get('somatotipo'),
                    'somatotipo_descricao': resultados.get('somatotipo_descricao'),
                    'pontuacao_estetica': resultados.get('pontuacao_estetica'),
                    'classificacao_estetica': resultados.get('classificacao_estetica'),
                    'proporcoes': {
                        'ombro_cintura': resultados.get('proporcoes').ombro_cintura if resultados.get('proporcoes') else None,
                        'peitoral_cintura': resultados.get('proporcoes').peitoral_cintura if resultados.get('proporcoes') else None,
                        'braco_panturrilha': resultados.get('proporcoes').braco_panturrilha if resultados.get('proporcoes') else None,
                    } if resultados.get('proporcoes') else None,
                    'analise_simetria': resultados.get('analise_simetria')
                }
            }
            
            # Salvar
            if 'avaliacoes' not in dados:
                dados['avaliacoes'] = []
            
            dados['avaliacoes'].insert(0, avaliacao_json)  # Mais recente primeiro
            salvar_dados(dados)
            
            return jsonify(avaliacao_json)
            
        except Exception as e:
            return jsonify({'erro': str(e)}), 500


@app.route('/api/avaliacoes/<avaliacao_id>', methods=['DELETE'])
def deletar_avaliacao(avaliacao_id):
    """Deleta uma avaliação"""
    dados = carregar_dados()
    
    avaliacoes = dados.get('avaliacoes', [])
    dados['avaliacoes'] = [a for a in avaliacoes if a['id'] != avaliacao_id]
    
    salvar_dados(dados)
    return jsonify({'sucesso': True})


@app.route('/api/comparar', methods=['POST'])
def comparar_avaliacoes():
    """Compara duas avaliações"""
    data = request.json
    id1 = data.get('id1')
    id2 = data.get('id2')
    
    dados = carregar_dados()
    avaliacoes = dados.get('avaliacoes', [])
    
    aval1_data = next((a for a in avaliacoes if a['id'] == id1), None)
    aval2_data = next((a for a in avaliacoes if a['id'] == id2), None)
    
    if not aval1_data or not aval2_data:
        return jsonify({'erro': 'Avaliações não encontradas'}), 404
    
    # Reconstruir objetos (simplificado para comparação)
    comparacao = {
        'periodo_dias': (datetime.fromisoformat(aval2_data['data']) - 
                        datetime.fromisoformat(aval1_data['data'])).days,
        'peso': {
            'anterior': aval1_data['medidas']['peso'],
            'atual': aval2_data['medidas']['peso'],
            'diferenca': aval2_data['medidas']['peso'] - aval1_data['medidas']['peso']
        }
    }
    
    return jsonify(comparacao)


if __name__ == '__main__':
    import webbrowser
    import threading
    
    print("=" * 60)
    print("🏋️ SISTEMA DE MEDIDAS CORPORAIS")
    print("=" * 60)
    print("\n🌐 Servidor iniciado em: http://localhost:5000")
    print("📁 Dados salvos em:", DATA_FILE)
    print("\nPressione Ctrl+C para encerrar\n")
    
    # Abrir navegador automaticamente após 1.5 segundos
    def abrir_navegador():
        import time
        time.sleep(1.5)
        webbrowser.open('http://localhost:5000')
    
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
