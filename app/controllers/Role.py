
from flask import request, session
from flask_restful import Resource
from marshmallow import ValidationError

from app.models.Users import Users
from app.models.Roles import Roles
from app.schematics.Role import RoleSchema


class AddRole(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = RoleSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            name = schema['name']
            role = Roles.get_by_name(name)
            if role:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['role exist']}}
            else:
                role = Roles(name=name)
                role.save()
                permissions = schema['permission']
                for p in permissions:
                    role.attach_permission(perm_name=p)
                mail = schema['name']
                user = Users.find_by_email(mail)
                print(mail)
                role.attach_user(user)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'add': ['Something is wrong.']}}


class RemoveRole(Resource):
    def delete(self, role_id):
        if role_id:
            role = Roles.get_by_id(rid=role_id)
            if not role:
                return {'code': 306, 'status': 'error', 'data': {'exist': ['role doesnt exist, id']}}
            else:
                if role.delete:
                    return {'code': 303, 'status': 'error', 'data': {'deleted': ['role doesnt exist']}}
                else:
                    role.remove()
        else:
            return {'code': 305, 'status': 'error', 'data': {'role': ['Something is wrong.']}}


class UpdateRole(Resource):
    def put(self, role_id):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = RoleSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            role = Roles.get_by_id(rid=role_id)
            if not role:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['article doesnt exist']}}
            else:
                per = schema['permission']
                print(per)
                role.update(schema)
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetRole(Resource):
    def get(self, role_id):
        if role_id:
            role = Roles.get_by_id(rid=role_id)
            if not role:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['article doesnt exist']}}
            else:
                schema = RoleSchema().dump(role)
                permission = role.get_role_permission()
                schema['permissopn'] = permission
                # print(category)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetAllRole(Resource):
    def get(self):
        role = Roles.get_roles()
        schema = []
        for a in role:
            c = RoleSchema().dump(a)
            c['permission'] = a.get_role_permission()
            schema.append(c)
        return {'code': 300, 'status': 'success', 'data': schema}
