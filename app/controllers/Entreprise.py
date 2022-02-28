import os

from flask import request, session
# from flask_jwt_extended import current_user
from flask_restful import Resource
from marshmallow import ValidationError
# from sqlalchemy.orm import session
from sqlalchemy.sql.functions import current_user

from app.models import Users, Entreprises
from app.models.Articles import Articles
from app.models.CategoriesArticles import CategoriesArticles
from app.models.UsersEntreprise import UsersEntreprise
from app.schematics.Article import ArticleSchema, UpdateArticleSchema
from app.schematics.Entreprise import EntrepriseSchema, UpdateEntrepriseSchema, getEntrepriseSchema


class AddEntreprise(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = EntrepriseSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            name = schema['name']
            entreprise = Entreprises.find_by_name(name)
            if entreprise:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['entreprise exist']}}
            else:
                entreprise = Entreprises(name=name, address=schema['address'], logo=schema['logo'],
                                         email=schema['email'],
                                         year_creation=schema['year_creation'],
                                          fax=schema['fax']
                                         , email_user=schema['email_user'],
                                          wilaya=schema['wilaya'], website=schema['website']
                                         )
                entreprise.save()

                mail = schema['email_user']
                print(mail)
                entreprise.attach_user(mail)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class RemoveEntreprise(Resource):
    def delete(self, entreprise_id):
        if entreprise_id:
            entreprise = Entreprises.find_by_id(id=entreprise_id)
            if not entreprise:
                return {'code': 306, 'status': 'error', 'data': {'exist': ['article doesnt exist, id']}}
            else:
                if entreprise.delete:
                    return {'code': 303, 'status': 'error', 'data': {'deleted': ['article doesnt exist']}}
                else:
                    entreprise.remove()
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class UpdateEntreprise(Resource):
    def put(self, entreprise_id):
        data = request.get_json()
        print(data)
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = UpdateEntrepriseSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            print(data)
            entreprise = Entreprises.find_by_id(id=entreprise_id)
            if not entreprise:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['article doesnt exist']}}
            else:
                entreprise.update(schema)
                return {'code': 200, 'status': 'success', 'data': schema}

        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetEntreprise(Resource):
    def get(self, entreprise_id):
        if entreprise_id:
            entreprise = Entreprises.find_by_id(id=entreprise_id)
            if not entreprise:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['article doesnt exist']}}
            else:
                schema = getEntrepriseSchema().dump(entreprise)

                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetAllEntreprise(Resource):
    def get(self):
        entreprise = Entreprises.get_entreprises()
        schema = []
        for a in entreprise:
            c = getEntrepriseSchema().dump(a)
            schema.append(c)
        return {'code': 300, 'status': 'success', 'data': schema}

class GetEntrepriseByUserId(Resource):
    def get(self, user_id):
        user = Users.find_by_id(user_id)
        if user:
            schema = []
            entreprises = user.get_entreprises()
            for a in entreprises:
                entreprise = Entreprises.find_by_id(a.entreprise_id)
                c = getEntrepriseSchema().dump(entreprise)
                c['user_avatar'] = user.avatar
                c['user_nom'] = user.lastname
                c['user_prenom'] = user.name
                schema.append(c)
            return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'user dont exist'}}
