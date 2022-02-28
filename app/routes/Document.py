from flask import Blueprint
from flask_restful import Api
from app.controllers.Document import AddDocument, UpdateDocument, RemoveDocument, GetDocument, GetAllDocument, \
    GetDocumentByUserId

blueprint = Blueprint('document', __name__)
errors = {
    'MethodNotAllowed': {
        'status': 405,
        'message': 'bad_request',
        'some_description': 'The method is not allowed for the requested URL.'
    }
}

api = Api(blueprint)

api.add_resource(AddDocument, '/add')
api.add_resource(RemoveDocument, '/remove/<document_id>')
api.add_resource(UpdateDocument, '/update/<document_id>')
api.add_resource(GetDocument, '/get/<document_id>')
api.add_resource(GetAllDocument, '/getAll')
api.add_resource(GetDocumentByUserId, '/getdoc/<user_id>')


