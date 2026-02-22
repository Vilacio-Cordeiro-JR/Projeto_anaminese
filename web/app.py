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
        print("✅ Usando PostgreSQL - dados serão persistidos")
    except Exception as e:
        print(f"⚠️ Erro ao conectar PostgreSQL: {e}")
        print("⚠️ Voltando para modo JSON (dados não persistem no Vercel!)")
        USE_DATABASE = False
        import json
        DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'usuarios.json')
else:
    print("⚠️ DATABASE_URL não configurada - usando JSON local")
    print("⚠️ ATENÇÃO: No Vercel, os dados serão perdidos após cada deploy/restart!")
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
ADMINS = ['admin', 'Admin', 'ADMIN', 'Vilacio', 'vilacio', 'VILACIO']


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


@app.route('/api/mudar-senha', methods=['POST'])
def mudar_senha():
    """Muda a senha do usuário logado"""
    if 'conta_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 401
    
    data = request.json
    senha_atual = data.get('senha_atual')
    nova_senha = data.get('nova_senha')
    
    if not senha_atual or not nova_senha:
        return jsonify({'erro': 'Senha atual e nova senha são obrigatórias'}), 400
    
    if len(nova_senha) < 6:
        return jsonify({'erro': 'A senha deve ter pelo menos 6 caracteres'}), 400
    
    try:
        nome = session.get('nome')
        
        if USE_DATABASE:
            # Verificar senha atual e atualizar no PostgreSQL
            if not db.autenticar(nome, senha_atual):
                return jsonify({'erro': 'Senha atual incorreta'}), 401
            
            # Atualizar senha
            nova_senha_hash = db.hash_senha(nova_senha)
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE contas SET senha_hash = %s WHERE nome = %s",
                (nova_senha_hash, nome)
            )
            conn.commit()
            cursor.close()
            conn.close()
        else:
            # Usar JSON
            dados = carregar_dados()
            conta = dados['contas'].get(nome)
            
            if not conta or conta.get('senha_hash') != hash_senha(senha_atual):
                return jsonify({'erro': 'Senha atual incorreta'}), 401
            
            # Atualizar senha
            conta['senha_hash'] = hash_senha(nova_senha)
            salvar_dados(dados)
        
        return jsonify({'sucesso': True, 'mensagem': 'Senha alterada com sucesso'})
    
    except Exception as e:
        print(f"Erro ao mudar senha: {e}")
        traceback.print_exc()
        return jsonify({'erro': 'Erro ao mudar senha'}), 500


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


@app.route('/api/status')
def status():
    """Retorna status do sistema e configuração do banco"""
    return jsonify({
        'status': 'online',
        'database': {
            'type': 'PostgreSQL' if USE_DATABASE else 'JSON (Local File)',
            'persistent': USE_DATABASE,
            'warning': None if USE_DATABASE else 'Dados serão perdidos no Vercel sem banco configurado'
        },
        'environment': 'production' if os.environ.get('VERCEL') else 'development'
    })


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
        
        # Validar e converter altura
        try:
            altura = float(data.get('altura', 0))
            if altura <= 0:
                return jsonify({'erro': 'Altura deve ser maior que zero'}), 400
        except (ValueError, TypeError):
            return jsonify({'erro': 'Altura inválida'}), 400
        
        # Calcula idade
        data_nasc = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        hoje = date.today()
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        
        if USE_DATABASE:
            # Usar PostgreSQL
            db.criar_usuario(conta_id, data['data_nascimento'], data['sexo'], altura)
        else:
            # Usar JSON
            dados = carregar_dados()
            dados['usuarios'][str(conta_id)] = {
                'conta_id': conta_id,
                'nome': session['nome'],
                'sexo': data['sexo'],
                'data_nascimento': data['data_nascimento'],
                'altura': altura,
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
            avaliacoes_db = db.obter_avaliacoes(usuario['id'])
            
            # Recalcular resultados para cada avaliação
            usuario_obj = Usuario(
                nome=usuario['nome'],
                sexo=Sexo(usuario['sexo']),
                data_nascimento=usuario['data_nascimento']
            )
            
            avaliacoes_completas = []
            for av in avaliacoes_db:
                # Compatibilidade com medidas antigas e novas
                def obter_medida_lateral(dados, nome_base):
                    """Obtém medidas laterais ou fallback para medida única"""
                    esquerda = dados.get(f'{nome_base}_esquerdo') or dados.get(f'{nome_base}_esquerda')
                    direita = dados.get(f'{nome_base}_direito') or dados.get(f'{nome_base}_direita')
                    if esquerda:
                        return float(esquerda)
                    if direita:
                        return float(direita)
                    # Fallback para medida única antiga
                    if dados.get(nome_base):
                        return float(dados[nome_base])
                    return None
                
                medidas = Medidas(
                    altura=float(usuario['altura']),
                    peso=float(av['peso']),
                    pescoco=float(av['pescoco']) if av.get('pescoco') else None,
                    ombros=float(av['ombros']) if av.get('ombros') else None,
                    peitoral=float(av['peitoral']) if av.get('peitoral') else None,
                    cintura=float(av['cintura']) if av.get('cintura') else None,
                    abdomen=float(av['abdomen']) if av.get('abdomen') else None,
                    quadril=float(av['quadril']) if av.get('quadril') else None,
                    braco_relaxado_esquerdo=obter_medida_lateral(av, 'braco_relaxado') or obter_medida_lateral(av, 'braco_relaxado_esquerdo'),
                    braco_relaxado_direito=obter_medida_lateral(av, 'braco_relaxado_direito'),
                    braco_contraido_esquerdo=obter_medida_lateral(av, 'braco_contraido') or obter_medida_lateral(av, 'braco_contraido_esquerdo'),
                    braco_contraido_direito=obter_medida_lateral(av, 'braco_contraido_direito'),
                    antebraco_esquerdo=obter_medida_lateral(av, 'antebraco') or obter_medida_lateral(av, 'antebraco_esquerdo'),
                    antebraco_direito=obter_medida_lateral(av, 'antebraco_direito'),
                    coxa_esquerda=obter_medida_lateral(av, 'coxa') or obter_medida_lateral(av, 'coxa_esquerda') or (float(av['coxa_proximal']) if av.get('coxa_proximal') else None),
                    coxa_direita=obter_medida_lateral(av, 'coxa_direita'),
                    panturrilha_esquerda=obter_medida_lateral(av, 'panturrilha') or obter_medida_lateral(av, 'panturrilha_esquerda'),
                    panturrilha_direita=obter_medida_lateral(av, 'panturrilha_direita'),
                    # Larguras ósseas
                    largura_ombros=float(av['largura_ombros']) if av.get('largura_ombros') else None,
                    largura_quadril=float(av['largura_quadril']) if av.get('largura_quadril') else None,
                    largura_punho_esquerdo=float(av['largura_punho_esquerdo']) if av.get('largura_punho_esquerdo') else None,
                    largura_punho_direito=float(av['largura_punho_direito']) if av.get('largura_punho_direito') else None,
                    largura_cotovelo_esquerdo=float(av['largura_cotovelo_esquerdo']) if av.get('largura_cotovelo_esquerdo') else None,
                    largura_cotovelo_direito=float(av['largura_cotovelo_direito']) if av.get('largura_cotovelo_direito') else None,
                    largura_joelho_esquerdo=float(av['largura_joelho_esquerdo']) if av.get('largura_joelho_esquerdo') else None,
                    largura_joelho_direito=float(av['largura_joelho_direito']) if av.get('largura_joelho_direito') else None,
                    largura_tornozelo_esquerdo=float(av['largura_tornozelo_esquerdo']) if av.get('largura_tornozelo_esquerdo') else None,
                    largura_tornozelo_direito=float(av['largura_tornozelo_direito']) if av.get('largura_tornozelo_direito') else None
                )
                
                avaliacao = Avaliacao(
                    data=av['data'],
                    medidas=medidas,
                    objetivo=''
                )
                
                resultados = AnalisadorAvaliacao.processar_avaliacao(avaliacao, usuario_obj)
                
                avaliacoes_completas.append({
                    'id': str(av['id']),
                    'data': str(av['data']),
                    'medidas': {
                        'altura': float(usuario['altura']),
                        'peso': float(av['peso']),
                        'pescoco': float(av['pescoco']) if av.get('pescoco') else None,
                        'ombros': float(av['ombros']) if av.get('ombros') else None,
                        'peitoral': float(av['peitoral']) if av.get('peitoral') else None,
                        'cintura': float(av['cintura']) if av.get('cintura') else None,
                        'abdomen': float(av['abdomen']) if av.get('abdomen') else None,
                        'quadril': float(av['quadril']) if av.get('quadril') else None,
                        'braco_relaxado_esquerdo': obter_medida_lateral(av, 'braco_relaxado') or obter_medida_lateral(av, 'braco_relaxado_esquerdo'),
                        'braco_relaxado_direito': obter_medida_lateral(av, 'braco_relaxado_direito'),
                        'braco_contraido_esquerdo': obter_medida_lateral(av, 'braco_contraido') or obter_medida_lateral(av, 'braco_contraido_esquerdo'),
                        'braco_contraido_direito': obter_medida_lateral(av, 'braco_contraido_direito'),
                        'antebraco_esquerdo': obter_medida_lateral(av, 'antebraco') or obter_medida_lateral(av, 'antebraco_esquerdo'),
                        'antebraco_direito': obter_medida_lateral(av, 'antebraco_direito'),
                        'coxa_esquerda': obter_medida_lateral(av, 'coxa') or obter_medida_lateral(av, 'coxa_esquerda') or (float(av['coxa_proximal']) if av.get('coxa_proximal') else None),
                        'coxa_direita': obter_medida_lateral(av, 'coxa_direita'),
                        'panturrilha_esquerda': obter_medida_lateral(av, 'panturrilha') or obter_medida_lateral(av, 'panturrilha_esquerda'),
                        'panturrilha_direita': obter_medida_lateral(av, 'panturrilha_direita')
                    },
                    'resultados': resultados
                })
            
            return jsonify(avaliacoes_completas)
        else:
            dados = carregar_dados()
            print(f"🔍 GET Avaliações - conta_id: {conta_id}")
            print(f"🔍 Chaves em avaliacoes: {list(dados['avaliacoes'].keys())}")
            avaliacoes = dados['avaliacoes'].get(str(conta_id), [])
            print(f"🔍 Total de avaliações encontradas: {len(avaliacoes)}")
            return jsonify(avaliacoes)
    
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
            
            # Criar objeto Medidas (converter valores para float)
            medidas_dict = data['medidas']
            
            # Debug: log da coxa
            print(f"🔍 APP.PY - Coxa recebida no medidas_dict: {medidas_dict.get('coxa')}")
            
            def to_float(value):
                """Converte valor para float, retorna None se vazio"""
                if value is None or value == '':
                    return None
                return float(value)
            
            medidas = Medidas(
                altura=float(medidas_dict['altura']),
                peso=float(medidas_dict['peso']),
                pescoco=to_float(medidas_dict.get('pescoco')),
                ombros=to_float(medidas_dict.get('ombros')),
                peitoral=to_float(medidas_dict.get('peitoral')),
                cintura=to_float(medidas_dict.get('cintura')),
                abdomen=to_float(medidas_dict.get('abdomen')),
                quadril=to_float(medidas_dict.get('quadril')),
                braco_relaxado_esquerdo=to_float(medidas_dict.get('braco_relaxado_esquerdo')),
                braco_relaxado_direito=to_float(medidas_dict.get('braco_relaxado_direito')),
                braco_contraido_esquerdo=to_float(medidas_dict.get('braco_contraido_esquerdo')),
                braco_contraido_direito=to_float(medidas_dict.get('braco_contraido_direito')),
                antebraco_esquerdo=to_float(medidas_dict.get('antebraco_esquerdo')),
                antebraco_direito=to_float(medidas_dict.get('antebraco_direito')),
                coxa_esquerda=to_float(medidas_dict.get('coxa_esquerda')),
                coxa_direita=to_float(medidas_dict.get('coxa_direita')),
                panturrilha_esquerda=to_float(medidas_dict.get('panturrilha_esquerda')),
                panturrilha_direita=to_float(medidas_dict.get('panturrilha_direita')),
                # Larguras ósseas
                largura_ombros=to_float(medidas_dict.get('largura_ombros')),
                largura_quadril=to_float(medidas_dict.get('largura_quadril')),
                largura_punho_esquerdo=to_float(medidas_dict.get('largura_punho_esquerdo')),
                largura_punho_direito=to_float(medidas_dict.get('largura_punho_direito')),
                largura_cotovelo_esquerdo=to_float(medidas_dict.get('largura_cotovelo_esquerdo')),
                largura_cotovelo_direito=to_float(medidas_dict.get('largura_cotovelo_direito')),
                largura_joelho_esquerdo=to_float(medidas_dict.get('largura_joelho_esquerdo')),
                largura_joelho_direito=to_float(medidas_dict.get('largura_joelho_direito')),
                largura_tornozelo_esquerdo=to_float(medidas_dict.get('largura_tornozelo_esquerdo')),
                largura_tornozelo_direito=to_float(medidas_dict.get('largura_tornozelo_direito'))
            )
            
            print(f"🔍 APP.PY - Objeto Medidas criado com coxas: E={medidas.coxa_esquerda}, D={medidas.coxa_direita}")
            
            # Criar avaliação
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
    
    try:
        if USE_DATABASE:
            sucesso = db.deletar_avaliacao(int(avaliacao_id))
            return jsonify({'sucesso': sucesso})
        else:
            dados = carregar_dados()
            avaliacoes = dados['avaliacoes'].get(str(conta_id), [])
            dados['avaliacoes'][str(conta_id)] = [a for a in avaliacoes if a['id'] != avaliacao_id]
            salvar_dados(dados)
            return jsonify({'sucesso': True})
    except Exception as e:
        print(f"Erro ao deletar avaliação: {e}")
        return jsonify({'erro': str(e)}), 500


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
    
    table = request.args.get('table', 'all')  # all, contas, usuarios, avaliacoes
    
    try:
        if USE_DATABASE:
            # Implementar consulta ao PostgreSQL por tabela
            with db.get_db_connection() as conn:
                with conn.cursor() as cur:
                    result = {}
                    
                    if table == 'all' or table == 'contas':
                        cur.execute("SELECT id, nome, email FROM contas ORDER BY id")
                        result['contas'] = cur.fetchall()
                    
                    if table == 'all' or table == 'usuarios':
                        cur.execute("""
                            SELECT u.*, c.nome 
                            FROM usuarios u 
                            JOIN contas c ON u.conta_id = c.id 
                            ORDER BY u.id
                        """)
                        result['usuarios'] = cur.fetchall()
                    
                    if table == 'all' or table == 'avaliacoes':
                        cur.execute("""
                            SELECT a.*, c.nome 
                            FROM avaliacoes a 
                            JOIN usuarios u ON a.usuario_id = u.id 
                            JOIN contas c ON u.conta_id = c.id 
                            ORDER BY a.data DESC 
                            LIMIT 100
                        """)
                        result['avaliacoes'] = cur.fetchall()
                    
                    # Se for tabela específica, retornar array direto
                    if table != 'all':
                        return jsonify(result.get(table, []))
                    
                    return jsonify(result)
        else:
            dados = carregar_dados()
            
            # Filtrar por tabela se necessário
            if table == 'contas':
                contas_safe = {}
                for nome, conta in dados.get('contas', {}).items():
                    conta_copy = conta.copy()
                    if 'senha_hash' in conta_copy:
                        conta_copy['senha_hash'] = '***HIDDEN***'
                    contas_safe[nome] = conta_copy
                return jsonify(contas_safe)
            
            elif table == 'usuarios':
                return jsonify(dados.get('usuarios', {}))
            
            elif table == 'avaliacoes':
                return jsonify(dados.get('avaliacoes', {}))
            
            else:  # all
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
            with db.get_db_connection() as conn:
                with conn.cursor() as cur:
                    # Contar contas
                    cur.execute("SELECT COUNT(*) FROM contas")
                    total_contas = cur.fetchone()['count']
                    
                    # Contar usuários
                    cur.execute("SELECT COUNT(*) FROM usuarios")
                    total_usuarios = cur.fetchone()['count']
                    
                    # Contar avaliações
                    cur.execute("SELECT COUNT(*) FROM avaliacoes")
                    total_avaliacoes = cur.fetchone()['count']
                    
                    return jsonify({
                        'total_contas': total_contas,
                        'total_usuarios': total_usuarios,
                        'total_avaliacoes': total_avaliacoes,
                        'modo': 'PostgreSQL'
                    })
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
