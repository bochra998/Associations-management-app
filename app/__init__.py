from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app.config.config import app_config

# from celery import Celery

# celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

from app.routes import User, auth, article, event, document, comment, entreprise, role
from app.models import *


# from app.controllers import *


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # api = Api(app=api_blueprint)
    app.config.from_object(app_config['development'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # celery.conf.update(app.config)
    db.init_app(app)
    jwt.init_app(app)
    from app.decorators import Jwt
    ma.init_app(app)

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(User.blueprint, url_prefix='/user')
    app.register_blueprint(article, url_prefix='/article')
    app.register_blueprint(event, url_prefix='/event')
    app.register_blueprint(document, url_prefix='/document')
    app.register_blueprint(comment, url_prefix='/comment')
    app.register_blueprint(entreprise, url_prefix='/entreprise')
    app.register_blueprint(role, url_prefix='/role')

    # app.register_blueprint(sites, url_prefix='/sites')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    return app
