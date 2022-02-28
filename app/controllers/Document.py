from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.models import Users
from app.models.Documents import Documents
from app.schematics.Document import DocumentSchema, GetDocumentSchema, UpdateDocumentSchema


class AddDocument(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = DocumentSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            title = schema['title']
            document = Documents.find_by_title(title)
            if document:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['Document exist']}}
            else:
                document = Documents(title=title, contenu=schema['contenu'], image=schema['image'], file=schema['file'],
                                     public=schema['public'])
                document.save()
                cat = schema['categorie']
                document.attach_categorie(categorie=cat)
                mail = schema['email']
                print(mail)
                document.attach_user(mail)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class RemoveDocument(Resource):
    def delete(self, document_id):
        if document_id:
            document = Documents.find_by_id(id=document_id)
            if not document:
                return {'code': 306, 'status': 'error', 'data': {'exist': ['document doesnt exist, id']}}
            else:
                if document.delete:
                    return {'code': 303, 'status': 'error', 'data': {'deleted': ['document doesnt exist']}}
                else:
                    document.remove()
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class UpdateDocument(Resource):
    def put(self, document_id):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = UpdateDocumentSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            document = Documents.find_by_id(id=document_id)
            if not document:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['document doesnt exist']}}
            else:
                document.update(schema)
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetDocument(Resource):
    def get(self, document_id):
        if document_id:
            document = Documents.find_by_id(id=document_id)
            if not document:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['document doesnt exist']}}
            else:
                schema = GetDocumentSchema().dump(document)
                category = document.get_document()
                schema['categorie'] = category
                print(category)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetAllDocument(Resource):
    def get(self):
        document = Documents.get_documents()
        schema = []
        for a in document:
            d = GetDocumentSchema().dump(a)
            d['categorie'] = a.get_document()
            schema.append(d)
        return {'code': 300, 'status': 'success', 'data': schema}

class GetDocumentByUserId(Resource):
    def get(self, user_id):
        user = Users.find_by_id(user_id)
        if user:
            schema = []
            documents = user.get_documents()
            for a in documents:
                document = Documents.find_by_id(a.document_id)
                c = GetDocumentSchema().dump(document)
                c['categorie'] = document.get_document()
                schema.append(c)
            return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'user dont exist'}}

