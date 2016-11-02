import os

class BaseConfig(object):

    # Flask RestPlus
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False

    # DB
    MONGO_DBNAME = 'gym'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#     if os.environ.get('DATABASE_URL') is None:
#   engine = create_engine('postgres://flaskexample:flask@localhost:5432/flaskexample', convert_unicode=True)
# else:
#   engine = create_engine(os.environ['DATABASE_URL'], convert_unicode=True)

class DevConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    RESTPLUS_ERROR_404_HELP = True

    # DB
    MONGO_HOST = 'localhost'
    SQLALCHEMY_DATABASE_URI = "postgresql:///strength"

class ProdConfig(BaseConfig):
    WTF_CSRF_ENABLED = True
    RESTPLUS_ERROR_404_HELP = False

    # DB
    MONGO_HOST = 'mongo'
    SQLALCHEMY_DATABASE_URI = "postgresql://psql/strength"
