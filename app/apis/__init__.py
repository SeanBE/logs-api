from flask import current_app, Blueprint
from flask_restplus import Api
from .namespace1 import api as ns1

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
    title='Strength Api',
    version='1.0',
    description='Description',
)

api.add_namespace(ns1)
