"""
Módulo de conexão com banco de dados PostgreSQL
"""
import os
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

def init_db():
    """Inicializa o banco de dados com as tabelas necessárias"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Ler e executar o script SQL
            with open('database.sql', 'r', encoding='utf-8') as f:
                cur.execute(f.read())
