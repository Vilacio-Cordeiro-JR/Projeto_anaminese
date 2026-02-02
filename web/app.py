"""
Servidor Flask para o Sistema de Medidas Corporais com Autenticação
Fornece API REST e serve a interface web
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from datetime import date, datetime
import os
import sys
import hashlib
import traceback

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar módulos de cálculo
from src.models.usuario import Usuario, Sexo
from src.models.medidas import Medidas
from src.models.avaliacao import Avaliacao
from src.services.analisador import AnalisadorAvaliacao

# Verifica se deve usar PostgreSQL ou JSON
USE_DATABASE = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')

if USE_DATABASE:
    try:
        from web import db
    except:
        USE_DATABASE = False
        import json
        DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'usuarios.json')
else:
    import json
    DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'usuarios.json')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave-secreta-dev-12345')
# Usar cookie-based sessions para Vercel (sem filesystem)
app.config['SESSION_TYPE'] = 'null'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
CORS(app)

# Lista de usuários admin (nomes de conta)
ADMINS = ['admin', 'Admin', 'ADMIN', 'Vilacio']


def hash_senha(senha):
    """Gera hash SHA256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()


def is_admin():
    """Verifica se o usuário atual é admin"""
    return session.get('nome') in ADMINS


# ===== MODO JSON (DESENVOLVIMENTO) =====
def carregar_dados():
    """Carrega dados do arquivo JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'contas': {}, 'usuarios': {}, 'avaliacoes': {}}


def salvar_dados(dados):
    """Salva dados no arquivo JSON"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, default=str)


# ===== ROTAS DE AUTENTICAÇÃO =====
@app.route('/login')
def login_page():
    """Página de login"""
    if 'conta_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/api/registro', methods=['POST'])
def registro():
    """Registra nova conta"""
    data = request.json
    nome = data.get('nome')
    senha = data.get('senha')
    
    if not nome or not senha:
        return jsonify({'erro': 'Nome e senha são obrigatórios'}), 400
    
    try:
        if USE_DATABASE:
            # Usar PostgreSQL
            conta_id = db.criar_conta(nome, senha)
        else:
            # Usar JSON
            dados = carregar_dados()
            if nome in dados['contas']:
                return jsonify({'erro': 'Nome já está em uso'}), 400
            
            conta_id = len(dados['contas']) + 1
            dados['contas'][nome] = {
                'id': conta_id,
                'senha_hash': hash_senha(senha),
                'created_at': datetime.now().isoformat()
            }
            salvar_dados(dados)
        
        return jsonify({'sucesso': True, 'conta_id': conta_id})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """Faz login na conta"""
    data = request.json
    nome = data.get('nome')
    senha = data.get('senha')
    
    if not nome or not senha:
        return jsonify({'erro': 'Nome e senha são obrigatórios'}), 400
    
    try:
        if USE_DATABASE:
            # Usar PostgreSQL
            conta_id = db.autenticar(nome, senha)
        else:
            # Usar JSON
            dados = carregar_dados()
            conta = dados['contas'].get(nome)
            if not conta or conta.get('senha_hash') != hash_senha(senha):
                return jsonify({'erro': 'Nome ou senha incorretos'}), 401
            conta_id = conta['id']
        
        if conta_id:
            session['conta_id'] = conta_id
            session['nome'] = nome
            return jsonify({'sucesso': True})
        else:
            return jsonify({'erro': 'Nome ou senha incorretos'}), 401
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    """Faz logout"""
    session.clear()
    return jsonify({'sucesso': True})


# ===== ROTAS PROTEGIDAS =====
def requer_login(f):
    """Decorator para rotas que requerem autenticação"""
    def decorated_function(*args, **kwargs):
        if 'conta_id' not in session:
            return jsonify({'erro': 'Não autorizado'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@app.route('/')
def index():
    """Página principal"""
    if 'conta_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html', is_admin=is_admin())


@app.route('/api/usuario', methods=['GET', 'POST', 'PUT'])
@requer_login
def usuario_api():
    """API para gerenciar usuário"""
    conta_id = session['conta_id']
    
    if request.method == 'GET':
        # Retorna dados do usuário
        if USE_DATABASE:
            usuario = db.obter_usuario_por_conta(conta_id)
        else:
            dados = carregar_dados()
            usuario = dados['usuarios'].get(str(conta_id))
        
        if usuario:
            return jsonify(dict(usuario) if USE_DATABASE else usuario)
        return jsonify(None)
    
    elif request.method == 'POST' or request.method == 'PUT':
        # Cria ou atualiza usuário
        data = request.json
        
        if not data.get('data_nascimento'):
            return jsonify({'erro': 'Data de nascimento é obrigatória'}), 400
        
        if not data.get('sexo'):
            return jsonify({'erro': 'Sexo é obrigatório'}), 400
        
        # Calcula idade
        data_nasc = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        hoje = date.today()
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        
        if USE_DATABASE:
            # Usar PostgreSQL
            db.criar_usuario(conta_id, data['data_nascimento'], data['sexo'], data.get('altura', 0))
        else:
            # Usar JSON
            dados = carregar_dados()
            dados['usuarios'][str(conta_id)] = {
                'conta_id': conta_id,
                'nome': session['nome'],
                'sexo': data['sexo'],
                'data_nascimento': data['data_nascimento'],
                'altura': data.get('altura', 0),
                'idade': idade,
                'created_at': datetime.now().isoformat()
            }
            salvar_dados(dados)
        
        return jsonify({'sucesso': True})


@app.route('/api/avaliacoes', methods=['GET', 'POST'])
@requer_login
def avaliacoes_api():
    """API para gerenciar avaliações"""
    conta_id = session['conta_id']
    
    if request.method == 'GET':
        # Retorna avaliações do usuário
        if USE_DATABASE:
            usuario = db.obter_usuario_por_conta(conta_id)
            if not usuario:
                return jsonify([])
            avaliacoes = db.obter_avaliacoes(usuario['id'])
        else:
            dados = carregar_dados()
            avaliacoes = dados['avaliacoes'].get(str(conta_id), [])
        
        return jsonify([dict(a) for a in avaliacoes] if USE_DATABASE else avaliacoes)
    
    elif request.method == 'POST':
        # Cria nova avaliação
        data = request.json
        
        try:
            # Obter dados do usuário
            if USE_DATABASE:
                usuario = db.obter_usuario_por_conta(conta_id)
                if not usuario:
                    return jsonify({'erro': 'Complete seu cadastro primeiro'}), 400
                usuario_obj = Usuario(
                    nome=usuario['nome'],
                    sexo=Sexo(usuario['sexo']),
                    data_nascimento=datetime.strptime(str(usuario['data_nascimento']), '%Y-%m-%d').date()
                )
            else:
                dados = carregar_dados()
                usuario_data = dados['usuarios'].get(str(conta_id))
                if not usuario_data:
                    return jsonify({'erro': 'Complete seu cadastro primeiro'}), 400
                usuario_obj = Usuario(
                    nome=usuario_data['nome'],
                    sexo=Sexo(usuario_data['sexo']),
                    data_nascimento=datetime.strptime(usuario_data['data_nascimento'], '%Y-%m-%d').date()
                )
            
            # Criar objeto Medidas
            medidas_dict = data['medidas']
            medidas = Medidas(
                altura=medidas_dict['altura'],
                peso=medidas_dict['peso'],
                pescoco=medidas_dict.get('pescoco'),
                ombros=medidas_dict.get('ombros'),
                peitoral=medidas_dict.get('peitoral'),
                cintura=medidas_dict.get('cintura'),
                abdomen=medidas_dict.get('abdomen'),
                quadril=medidas_dict.get('quadril'),
                braco_relaxado=medidas_dict.get('braco_relaxado'),
                braco_contraido=medidas_dict.get('braco_contraido'),
                antebraco=medidas_dict.get('antebraco'),
                coxa_proximal=medidas_dict.get('coxa'),
                panturrilha=medidas_dict.get('panturrilha')
            )
            
            # Criar avaliação
            avaliacao = Avaliacao(
                data=datetime.strptime(data.get('data', date.today().isoformat()), '%Y-%m-%d').date(),
                medidas=medidas,
                objetivo=data.get('objetivo')
            )
            
            # PROCESSAR CÁLCULOS
            resultados = AnalisadorAvaliacao.processar_avaliacao(avaliacao, usuario_obj)
            
            # Salvar com resultados
            avaliacao_completa = {
                'id': datetime.now().isoformat(),
                'data': data.get('data', date.today().isoformat()),
                'medidas': medidas_dict,
                'objetivo': data.get('objetivo', ''),
                'resultados': resultados
            }
            
            if USE_DATABASE:
                db.salvar_avaliacao(
                    usuario['id'],
                    avaliacao_completa['data'],
                    medidas_dict['peso'],
                    medidas_dict
                )
            else:
                if str(conta_id) not in dados['avaliacoes']:
                    dados['avaliacoes'][str(conta_id)] = []
                dados['avaliacoes'][str(conta_id)].insert(0, avaliacao_completa)
                salvar_dados(dados)
            
            return jsonify(avaliacao_completa)
            
        except Exception as e:
            print(f"Erro ao processar avaliação: {e}")
            print(traceback.format_exc())
            return jsonify({'erro': f'Erro ao processar avaliação: {str(e)}'}), 500


@app.route('/api/avaliacoes/<avaliacao_id>', methods=['DELETE'])
@requer_login
def deletar_avaliacao(avaliacao_id):
    """Deleta uma avaliação"""
    conta_id = session['conta_id']
    
    if not USE_DATABASE:
        dados = carregar_dados()
        avaliacoes = dados['avaliacoes'].get(str(conta_id), [])
        dados['avaliacoes'][str(conta_id)] = [a for a in avaliacoes if a['id'] != avaliacao_id]
        salvar_dados(dados)
    
    return jsonify({'sucesso': True})


# ===== ROTAS ADMIN =====
@app.route('/api/admin/check', methods=['GET'])
@requer_login
def check_admin():
    """Verifica se usuário é admin"""
    return jsonify({'is_admin': is_admin()})


@app.route('/api/admin/database', methods=['GET'])
@requer_login
def admin_database():
    """Retorna dados completos do database (apenas admin)"""
    if not is_admin():
        return jsonify({'erro': 'Acesso negado'}), 403
    
    try:
        if USE_DATABASE:
            # TODO: Implementar consulta ao PostgreSQL
            return jsonify({'erro': 'Visualização de PostgreSQL não implementada ainda'}), 501
        else:
            dados = carregar_dados()
            # Remover senhas para segurança
            dados_safe = dados.copy()
            if 'contas' in dados_safe:
                for nome, conta in dados_safe['contas'].items():
                    if 'senha_hash' in conta:
                        conta['senha_hash'] = '***HIDDEN***'
            
            return jsonify(dados_safe)
    except Exception as e:
        print(f"Erro ao carregar database: {e}")
        print(traceback.format_exc())
        return jsonify({'erro': str(e)}), 500


@app.route('/api/admin/stats', methods=['GET'])
@requer_login
def admin_stats():
    """Retorna estatísticas do sistema (apenas admin)"""
    if not is_admin():
        return jsonify({'erro': 'Acesso negado'}), 403
    
    try:
        if USE_DATABASE:
            # TODO: Implementar estatísticas do PostgreSQL
            return jsonify({'erro': 'Estatísticas de PostgreSQL não implementadas ainda'}), 501
        else:
            dados = carregar_dados()
            total_contas = len(dados.get('contas', {}))
            total_usuarios = len(dados.get('usuarios', {}))
            total_avaliacoes = sum(len(avs) for avs in dados.get('avaliacoes', {}).values())
            
            return jsonify({
                'total_contas': total_contas,
                'total_usuarios': total_usuarios,
                'total_avaliacoes': total_avaliacoes,
                'modo': 'JSON'
            })
    except Exception as e:
        print(f"Erro ao carregar estatísticas: {e}")
        return jsonify({'erro': str(e)}), 500


if __name__ == '__main__':
    import webbrowser
    import threading
    
    print("=" * 60)
    print("🏋️ SISTEMA DE MEDIDAS CORPORAIS")
    print("=" * 60)
    print(f"\n🗄️  Modo: {'PostgreSQL' if USE_DATABASE else 'JSON (Desenvolvimento)'}")
    print("\n🌐 Servidor iniciado em: http://localhost:5000")
    print("\nPressione Ctrl+C para encerrar\n")
    
    def abrir_navegador():
        import time
        time.sleep(1.5)
        webbrowser.open('http://localhost:5000')
    
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
