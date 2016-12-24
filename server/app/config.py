import os


class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


class ProdConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_ENABLED = True

    DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    DB_USERNAME = os.environ.get('POSTGRES_USER', 'sean')
    DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'tracker')
    DB_NAME = os.environ.get('POSTGRES_DB', 'strength')

    SQLALCHEMY_DATABASE_URI = ('postgresql://%s:%s@%s/%s'
                               .format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME))


config = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig
}
