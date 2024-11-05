import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Mysecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking modifications for performance
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'

class DevelopmentConfig(Config):
    """Development configuration class."""
    DEBUG = True  # Enable debug mode for development
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///dev.db'

class TestingConfig(Config):
    """Testing configuration class."""
    TESTING = True  # Enable testing mode
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///test.db'

class ProductionConfig(Config):
    """Production configuration class."""
    DEBUG = False  # Disable debug mode in production
    DATABASE_URL = os.environ.get('DATABASE_URL')  # Should be set in environment variables