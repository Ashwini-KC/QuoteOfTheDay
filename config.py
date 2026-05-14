"""
Copywrite ASHWINI, 2026
Author: ASHWINI
CreatedDate: 14 May 2026
LastModifiedDate: 14 May 2026
"""

import os
from datetime import timedelta


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = False
    TESTING = False
    
    # Flask settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Lax"
    
    # Cache settings
    CACHE_TTL_SECONDS = 3600
    
    # Application paths
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    QUOTES_FILE = os.path.join(DATA_DIR, "quotes.json")
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    
    # Ensure logs directory exists
    os.makedirs(LOGS_DIR, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SECRET_KEY = "test-secret-key"
    SESSION_COOKIE_SECURE = False
    
    # Use in-memory test quotes file
    DATA_DIR = os.path.join(Config.BASE_DIR, "tests", "fixtures")
    QUOTES_FILE = os.path.join(DATA_DIR, "quotes.json")


def get_config():
    """Get configuration based on environment"""
    env = os.getenv("FLASK_ENV", "development")
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    return config_map.get(env, DevelopmentConfig)
