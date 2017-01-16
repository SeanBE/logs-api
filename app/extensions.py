from raven.contrib.flask import Sentry
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

db = SQLAlchemy()

user_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')

sentry = Sentry()
