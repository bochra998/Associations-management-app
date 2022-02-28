from flask import Blueprint
from flask_restful import Api
from app.controllers.Entreprise import AddEntreprise, RemoveEntreprise, GetEntreprise, GetAllEntreprise, \
    UpdateEntreprise, GetEntrepriseByUserId

blueprint = Blueprint('entreprise', __name__)
errors = {
    'MethodNotAllowed': {
        'status': 405,
        'message': 'bad_request',
        'some_description': 'The method is not allowed for the requested URL.'
    }
}

api = Api(blueprint)

api.add_resource(AddEntreprise, '/add')
api.add_resource(RemoveEntreprise, '/remove/<entreprise_id>')
api.add_resource(UpdateEntreprise, '/update/<entreprise_id>')
api.add_resource(GetEntreprise, '/get/<entreprise_id>')
api.add_resource(GetAllEntreprise, '/getAll')
api.add_resource(GetEntrepriseByUserId, '/getentreprise/<user_id>')


