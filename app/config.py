import os

class BaseConfig(object):

    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False

    MONGO_DBNAME = 'gym'
    MONGO_HOST = 'db'

class DevConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
