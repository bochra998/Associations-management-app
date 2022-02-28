from flask import Blueprint
from flask_restful import Api

from app.controllers.User import AddUser, RemoveUser, UpdateUser, GetUser, GetNonActiveUsers, GetAllUsers, \
    GetUserByEmail, GetNonActiveUser, Update, ActivateUser

blueprint = Blueprint('user', __name__)
errors = {
    'MethodNotAllowed': {
        'status': 405,
        'message': 'bad_request',
        'some_description': 'The method is not allowed for the requested URL.'
    }
}

api = Api(blueprint)

api.add_resource(AddUser, '/add')
api.add_resource(RemoveUser, '/remove/<user_id>')
api.add_resource(UpdateUser, '/update/<user_id>')
api.add_resource(GetUser, '/get/<user_id>')
api.add_resource(GetAllUsers, '/getAll')
api.add_resource(GetNonActiveUsers, '/getNonActive')
api.add_resource(GetUserByEmail, '/getEmail/<user_email>')
api.add_resource(GetNonActiveUser, '/getnonactive/<user_id>')
api.add_resource(Update, '/up/<user_id>')
api.add_resource(ActivateUser, '/activate/<user_id>')


