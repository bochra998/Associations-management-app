from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash

from app.models import Roles
from app.models.Users import Users
from app.schematics.User import *


class AddUser(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = UserSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            email = schema['email']
            user = Users.find_by_email(email)
            if user:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['user exist']}}
            else:
                user = Users(email=email, password=generate_password_hash(schema['password']), name=schema['name'],
                             lastname=schema['lastname'], phone=schema['phone'],
                             address=schema['address'], civilite=schema['civilite'],
                             wilaya=schema['wilaya'], avatar=schema['avatar']
                             )
                user.save()
                role = schema['role']
                user.attach_role(role=role)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class RemoveUser(Resource):
    def delete(self, user_id):
        if user_id:
            user = Users.find_by_id(id=user_id)
            if user.delete:
                return {'code': 306, 'status': 'error', 'data': {'deleted': ['user doesnt exist']}}
            else:
                if not user:
                    return {'code': 303, 'status': 'error', 'data': {'exist': ['user doesnt exist']}}
                else:
                    user.remove()
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetUser(Resource):
    def get(self, user_id):
        if user_id:
            print(user_id)
            user = Users.find_by_id(id=user_id)
            if not user:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['user doesnt exist']}}
            else:
                schema = GetUserSchema().dump(user)
                ligne = user.get_role()
                roleid = ligne.role_id
                role_name = Roles.get_by_id(rid=roleid).name
                # role = user.get_role()
                schema['role'] = role_name
                print(role_name)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


# still trying with this one
class GetAllUsers(Resource):
    def get(self):
        users = Users.find_all()
        schema = []

        if not users:
            return {'code': 303, 'status': 'error', 'data': {'exist': ['no user']}}
        else:
            for a in users:
                c = GetUserSchema().dump(a)
                # c['categorie'] = a.get_article()
                schema.append(c)

            return {'code': 300, 'status': 'success', 'data': schema}


class UpdateUser(Resource):
    def put(self, user_id):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = UpdateUserSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            user = Users.find_by_id(id=user_id)
            if not user:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['user doesnt exist']}}
            else:
                user.update(schema)
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class ActivateUser(Resource):
    def post(self, user_id):
        user = Users.find_by_id(id=user_id)
        if not user:
            return {'code': 303, 'status': 'error', 'data': {'exist': ['user doesnt exist']}}
        else:
            user.active = True
            user.save()


class GetNonActiveUsers(Resource):
    def get(self):
        users = Users.find_non_active()
        schema = []
        if not users:
            return {'code': 303, 'status': 'error', 'data': {'exist': ['no user']}}
        else:
            for a in users:
                c = nonActiveUserSchema().dump(a)
                # c['categorie'] = a.get_article()
                schema.append(c)

            return {'code': 300, 'status': 'success', 'data': schema}

class GetUserByEmail(Resource):
    def get(self, user_email):
        if user_email:
            user = Users.find_by_email(email=user_email)
            if not user:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['user doesnt exist']}}
            else:
                schema = GetUserSchema().dump(user)
                ligne = user.get_role()
                roleid = ligne.role_id
                role_name = Roles.get_by_id(rid=roleid).name
                # role = user.get_role()
                schema['role'] = role_name
                print(role_name)
                entreprise = user.get_entreprise()
                if entreprise:
                    entrepriseid = entreprise.entreprise_id
                    schema['entreprise'] = entrepriseid
                else:
                    schema['entreprise'] = None

                articles = []
                articles = user.get_articles()
                if articles:
                    number_articles = len(articles)
                    schema['number_article'] = number_articles
                else:
                    schema['number_article'] = 0

                events = []
                events = user.get_events()
                if events:
                    number_events = len(events)
                    schema['number_event'] = number_events
                else:
                    schema['number_event'] = 0

                documents = []
                documents = user.get_documents()
                if documents:
                    number_documents = len(documents)
                    schema['number_doc'] = number_documents
                else:
                    schema['number_doc'] = 0

                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}

class GetNonActiveUser(Resource):
    def get(self, user_id):
        if user_id:
            user = Users.find_non_activate_user(user=user_id)
            if not user:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['user doesnt exist']}}
            else:
                schema = GetUserSchema().dump(user)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}

class Update(Resource):
    def put(self, user_id):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = UpdateUserSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            user = Users.find_by_id(id=user_id)
            if not user:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['user doesnt exist']}}
            else:
                user.up(schema)
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}