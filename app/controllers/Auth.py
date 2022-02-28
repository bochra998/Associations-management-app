from flask import request, session
from flask_jwt_extended import  get_jwt_identity, jwt_required
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from app.decorators.Auth import check_permissions
from app.models import Roles
from app.models.Users import Users
from app.schematics.Auth import LoginSchema, LoginResponseSchema, RegisterSchema

db = SQLAlchemy()


class Login(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        try:
            schema = LoginSchema().load(data)
        except ValidationError as err:
            return False
        if data:
            email = schema['email']
            password = schema['password']
            print(email)

            user = Users.find_by_email(email)
            if not user or not check_password_hash(user.password, password):
                return False
            schema = LoginResponseSchema().dump(user)
            print(schema)
            ligne = user.get_role()
            if ligne:
                roleid = ligne.role_id
                role_name = Roles.get_by_id(rid=roleid).name
                # role = user.get_role()
                schema['role'] = role_name
                print(role_name)
            else:
                schema['role'] = None
            # session['email'] = email
            # print(session['email'])
            return schema
        else:
            return False

class Check(Resource):
    @jwt_required()
    # @check_permissions(['can_do', 'IsUser'])
    def get(self):
        current_user = get_jwt_identity()
        user = Users.find_by_email(email=current_user)
        schema = LoginResponseSchema().dump(user)
        return {'code': 300, 'status': 'success', 'data': schema}


class Register(Resource):
    def post(self):
        data = request.get_json()
        try:
            schema = RegisterSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            email = schema['email']
            user = Users.find_by_email(email)
            if user:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['user exist']}}
            else:
                Users(email=email, password=generate_password_hash(schema['password']), name=schema['name'],
                      lastname=schema['lastname'], phone=schema['phone'], civilite=schema['civilite'],
                      wilaya=schema['wilaya'], ).save()
                return True
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class Addsession(Resource):
        def post (self, email):
            session['email'] = email
            print(session['email'])