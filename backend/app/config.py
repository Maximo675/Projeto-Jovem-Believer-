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
    # Render.com retorna URLs com prefixo "postgres://" -- SQLAlchemy exige "postgresql://"
    _db_url = os.getenv('DATABASE_URL', '')
    if _db_url:
        SQLALCHEMY_DATABASE_URI = _db_url.replace('postgres://', 'postgresql://', 1)
    else:
        # Fallback SQLite quando DATABASE_URL não está configurado no Render
        # Isso evita crash 502 no startup — banco PostgreSQL pode ser adicionado depois
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
