import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

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
    # SQLite para desenvolvimento rápido (sem falhas de conexão PostgreSQL)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///infant_id_platform.db'

class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    # SQLite por padrão no Render — evita timeout de conexão PostgreSQL no startup (502)
    # Para usar PostgreSQL: configure DATABASE_URL E defina USE_POSTGRES=true nas env vars do Render
    _db_url = os.getenv('DATABASE_URL', '')
    _use_pg = os.getenv('USE_POSTGRES', 'false').lower() == 'true'
    if _db_url and _use_pg:
        SQLALCHEMY_DATABASE_URI = _db_url.replace('postgres://', 'postgresql://', 1)
        # Timeout curto para não travar o startup caso o banco esteja indisponível
        SQLALCHEMY_ENGINE_OPTIONS = {'connect_args': {'connect_timeout': 5}, 'pool_pre_ping': True}
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
