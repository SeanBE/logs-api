import os

class BaseConfig(object):

    SERVER_NAME = os.environ['SERVER_NAME']

    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False

    MONGO_DBNAME = 'gym'
    # MONGO_PASSWORD = 'strength'
    # MONGO_USERNAME = 'jdoe'
class DevConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
