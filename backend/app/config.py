import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def _build_postgres_url():
    """
    Constrói a URL PostgreSQL a partir das variáveis separadas do Render
    (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT) ou de DATABASE_URL.
    Retorna None se nenhuma variável de banco estiver configurada.
    """
    # Prioridade 1: DATABASE_URL já pronta (Render managed PostgreSQL)
    url = os.getenv('DATABASE_URL', '')
    if url:
        return url.replace('postgres://', 'postgresql://', 1)

    # Prioridade 2: variáveis separadas (configuração manual no Render)
    host = os.getenv('DB_HOST', '')
    name = os.getenv('DB_NAME', '')
    user = os.getenv('DB_USER', '')
    password = os.getenv('DB_PASSWORD', '')
    port = os.getenv('DB_PORT', '5432')
    if host and name and user and password:
        return f'postgresql://{user}:{password}@{host}:{port}/{name}'

    return None


class Config:
    """Configuração base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    
    # JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key')
    JWT_EXPIRATION = int(os.getenv('JWT_EXPIRATION', 86400))
    
    # IA
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///infant_id_platform.db'

class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False

    _pg_url = _build_postgres_url()

    if _pg_url:
        SQLALCHEMY_DATABASE_URI = _pg_url
        # NullPool: obrigatório com eventlet — o monkey_patch() corrompe os locks
        # internos do QueuePool, causando RuntimeError: cannot notify on un-acquired lock.
        # NullPool abre/fecha a conexão por request, sem pool, sem locks.
        from sqlalchemy.pool import NullPool as _NullPool
        SQLALCHEMY_ENGINE_OPTIONS = {
            'poolclass': _NullPool,
            'connect_args': {'connect_timeout': 10, 'sslmode': 'require'},
        }
    else:
        import tempfile as _tmp
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_tmp.gettempdir(), 'infant_id_render.db')

class TestingConfig(Config):
    """Configuração de testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
