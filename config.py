"""App configuration"""
import os
from dotenv import load_dotenv

load_dotenv()


def _fix_db_url(url: str) -> str:
    """SQLAlchemy requires postgresql://, Supabase maybe return postgres://"""
    if not url:
        raise ValueError("DATABASE_URL no está definida en las variables de entorno")
    return url.replace("postgres://", "postgresql://", 1)


class Config:
    """Base configuration"""

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = 900       # 15 min
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 days

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    # SQLAlchemy — Session pooler (IPv4, suports DDL and migrations)
    SQLALCHEMY_DATABASE_URI = _fix_db_url(os.getenv("DATABASE_URL", ""))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,    # Verify connections
        "pool_recycle": 1800,     # Reconnect every 30 minutes
        "connect_args": {
            "sslmode": "require",
            "connect_timeout": 10,
        },
    }


class DevelopmentConfig(Config):
    """Dev configuration"""
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    JWT_COOKIE_SECURE = True  # HTTPS

    # Pooler transaction
    # Migrations still uses DATABASE_URL
    SQLALCHEMY_DATABASE_URI = _fix_db_url(
        os.getenv("DATABASE_POOL_URL") or os.getenv("DATABASE_URL", "")
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 5,
        "max_overflow": 10,
        "connect_args": {
            "sslmode": "require",
            "connect_timeout": 10,
        },
    }


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


_config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config() -> Config:
    env = os.getenv("FLASK_ENV", "development")
    return _config_map.get(env, DevelopmentConfig)
