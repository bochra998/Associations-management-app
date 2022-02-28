from flask import Blueprint
from flask_restful import Api

# from app.controllers import *
from app.controllers.Auth import Register, Login,Addsession , Check


blueprint = Blueprint('auth', __name__)
errors = {
    'MethodNotAllowed': {
        'status': 405,
        'message': 'bad_request',
        'some_description': 'The method is not allowed for the requested URL.'
    }
}

api = Api(blueprint)

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Check, '/check')
api.add_resource(Addsession, '/add/<email>')
