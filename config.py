import os

PROJECT_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DB_PATH = os.path.join(PROJECT_ROOT_DIR, 'site.db')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{PROJECT_DB_PATH}'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
