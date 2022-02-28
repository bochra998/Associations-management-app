import json

from flask_jwt_extended import create_access_token
from marshmallow import Schema, fields, validate, validates_schema, ValidationError
import datetime


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class RegisterSchema(Schema):
    name = fields.String(required=True)
    lastname = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    confirmpass = fields.Str(required=True, validate=validate.Length(min=6))
    phone = fields.String(required=True)
    civilite = fields.String(required=True)
    wilaya = fields.String(required=True)

    @validates_schema
    def confirm_pass(self, data, **kwargs):
        if data["password"] != data["confirmpass"]:
            raise ValidationError("pass are not the same ", "confirmpass")


class LoginResponseSchema(Schema):
    # class Meta:
        # fields = ('uid', 'fullname', 'email', 'phone', 'token', 'permissions', 'avatar')
        # ordered = True

    uid = fields.String()
    id = fields.String()
    fullname = fields.Method('getFullname')
    email = fields.Email()
    phone = fields.String()
    token = fields.Method('getToken')
    permissions = fields.Method('getPermissions')
    avatar = fields.String()
    role = fields.String()
    active = fields.Boolean()

    @classmethod
    def getFullname(cls, obj):
        if obj.name and obj.lastname:
            return '{0} {1}'.format(obj.name, obj.lastname)

    @classmethod
    def getPermissions(cls, obj):
        return obj.find_by_uid(obj.uid).get_permissions()

    @classmethod
    def getToken(cls, obj):
        return create_access_token(identity=obj.email, expires_delta=datetime.timedelta(days=365))
