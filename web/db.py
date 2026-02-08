"""
Módulo de conexão com banco de dados PostgreSQL
"""
import os
import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

# URL de conexão do PostgreSQL (será configurada no Vercel)
DATABASE_URL = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')

@contextmanager
def get_db_connection():
    """Context manager para conexão com banco de dados"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def hash_senha(senha):
    """Gera hash SHA256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_conta(nome, senha):
    """Cria uma nova conta de usuário"""
    senha_hash = hash_senha(senha)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO contas (nome, senha_hash) VALUES (%s, %s) RETURNING id",
                (nome, senha_hash)
            )
            return cur.fetchone()['id']

def autenticar(nome, senha):
    """Autentica um usuário e retorna o ID da conta"""
    senha_hash = hash_senha(senha)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM contas WHERE nome = %s AND senha_hash = %s",
                (nome, senha_hash)
            )
            result = cur.fetchone()
            return result['id'] if result else None

def criar_usuario(conta_id, data_nascimento, sexo, altura):
    """Cria ou atualiza dados pessoais do usuário vinculado à conta"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO usuarios (conta_id, data_nascimento, sexo, altura) 
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (conta_id) DO UPDATE SET
                       data_nascimento = EXCLUDED.data_nascimento,
                       sexo = EXCLUDED.sexo,
                       altura = EXCLUDED.altura
                   RETURNING id""",
                (conta_id, data_nascimento, sexo, altura)
            )
            return cur.fetchone()['id']

def obter_usuario_por_conta(conta_id):
    """Obtém dados do usuário pela conta"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT u.*, c.nome 
                   FROM usuarios u 
                   JOIN contas c ON u.conta_id = c.id 
                   WHERE u.conta_id = %s""",
                (conta_id,)
            )
            return cur.fetchone()

def salvar_avaliacao(usuario_id, data, peso, medidas):
    """Salva uma nova avaliação"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO avaliacoes (
                    usuario_id, data, peso, pescoco, ombros, peitoral, cintura, 
                    abdomen, quadril, braco_relaxado, braco_contraido, antebraco, 
                    punho, coxa_proximal, coxa_medial, coxa_distal, panturrilha, tornozelo
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (usuario_id, data) DO UPDATE SET
                    peso = EXCLUDED.peso,
                    pescoco = EXCLUDED.pescoco,
                    ombros = EXCLUDED.ombros,
                    peitoral = EXCLUDED.peitoral,
                    cintura = EXCLUDED.cintura,
                    abdomen = EXCLUDED.abdomen,
                    quadril = EXCLUDED.quadril,
                    braco_relaxado = EXCLUDED.braco_relaxado,
                    braco_contraido = EXCLUDED.braco_contraido,
                    antebraco = EXCLUDED.antebraco,
                    punho = EXCLUDED.punho,
                    coxa_proximal = EXCLUDED.coxa_proximal,
                    coxa_medial = EXCLUDED.coxa_medial,
                    coxa_distal = EXCLUDED.coxa_distal,
                    panturrilha = EXCLUDED.panturrilha,
                    tornozelo = EXCLUDED.tornozelo
                RETURNING id""",
                (usuario_id, data, peso, medidas.get('pescoco'), medidas.get('ombros'),
                 medidas.get('peitoral'), medidas.get('cintura'), medidas.get('abdomen'),
                 medidas.get('quadril'), medidas.get('braco_relaxado'), medidas.get('braco_contraido'),
                 medidas.get('antebraco'), medidas.get('punho'), 
                 medidas.get('coxa') or medidas.get('coxa_proximal'),  # Aceitar ambos nomes
                 medidas.get('coxa_medial'), medidas.get('coxa_distal'), medidas.get('panturrilha'),
                 medidas.get('tornozelo'))
            )
            return cur.fetchone()['id']

def obter_avaliacoes(usuario_id, limit=10):
    """Obtém as últimas avaliações do usuário"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM avaliacoes 
                   WHERE usuario_id = %s 
                   ORDER BY data DESC 
                   LIMIT %s""",
                (usuario_id, limit)
            )
            return cur.fetchall()

def deletar_avaliacao(avaliacao_id):
    """Deleta uma avaliação pelo ID"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM avaliacoes WHERE id = %s",
                (avaliacao_id,)
            )
            return cur.rowcount > 0

def init_db():
    """Inicializa o banco de dados com as tabelas necessárias"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Ler e executar o script SQL
            with open('database.sql', 'r', encoding='utf-8') as f:
                cur.execute(f.read())
