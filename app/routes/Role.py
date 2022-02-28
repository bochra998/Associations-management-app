from flask import Blueprint
from flask_restful import Api
from app.controllers.Role import AddRole, UpdateRole, GetRole, RemoveRole, GetAllRole
blueprint = Blueprint('role', __name__)
errors = {
    'MethodNotAllowed': {
        'status': 405,
        'message': 'bad_request',
        'some_description': 'The method is not allowed for the requested URL.'
    }
}

api = Api(blueprint)

api.add_resource(AddRole, '/add')
api.add_resource(RemoveRole, '/remove/<role_id>')
api.add_resource(UpdateRole, '/update/<role_id>')
api.add_resource(GetRole, '/get/<role_id>')
api.add_resource(GetAllRole, '/getAll')
