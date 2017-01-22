import os


class BaseConfig(object):
    ERROR_404_HELP = False
    TRAP_HTTP_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get(
        'SECRET_KEY', 'lwj2s1(f$7*)xx)e81203*21xa(hctg4ghlm0g*a98q1rfm*(!')


class DevConfig(BaseConfig):
    ENV = 'development'
    DEBUG = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://sean:tracker@localhost/strength'


class TestConfig(BaseConfig):
    ENV = 'testing'
    TESTING = True
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'
    DB_PATH = "/tmp/test.db"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DB_PATH


class ProdConfig(BaseConfig):
    ENV = 'production'
    WTF_CSRF_ENABLED = True

    DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    DB_USER = os.environ.get('POSTGRES_USER', 'sean')
    DB_PW = os.environ.get('POSTGRES_PASSWORD', 'tracker')
    DB_NAME = os.environ.get('POSTGRES_DB', 'strength')

    SQLALCHEMY_DATABASE_URI = ('postgresql://{}:{}@{}/{}'
                               .format(DB_USER, DB_PW, DB_HOST, DB_NAME))


config = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig
}
