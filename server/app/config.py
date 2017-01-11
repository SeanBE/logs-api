import os


class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'lwj2s1(f$7*)xx)e81203*21xa(hctg4ghlm0g*a98q1rfm*(!')


class DevConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://sean:tracker@localhost/strength'


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    # TODO move to /tmp/
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


class ProdConfig(BaseConfig):
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
