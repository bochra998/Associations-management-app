from marshmallow import Schema, fields, validate


# class UserSchema(Schema):
#     class Meta:
#         fields = (
#             'uid', 'uname', 'domain', 'package', 'mysql_host', 'mysql_username', 'mysql_password', 'mysql_database',
#             'server_id', 'updated_on', 'created_on')
#         ordered = True
#
#     uid = fields.String()
#     uname = fields.String()
#     domain = fields.String()
#     # package = fields.Nested(PackageSchema)
#     mysql_host = fields.String()
#     mysql_username = fields.String()
#     mysql_password = fields.String()
#     mysql_database = fields.String()
#     server_id = fields.Int()
#     created_on = fields.DateTime()
#     updated_on = fields.DateTime()
#

class UserSchema(Schema):
    lastname = fields.String(required=True)
    name = fields.String(required=True)
    address = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.String(required=True)
    civilite = fields.String(required=False)
    wilaya = fields.String(required=False)
    avatar = fields.String(required=False)




class GetUserSchema(Schema):
    id = fields.String()
    lastname = fields.String(required=True)
    name = fields.String(required=True)
    address = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.Email(required=True)
    avatar = fields.String()
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.String()
    active = fields.Boolean()
    entreprise = fields.String(required=False)
    number_article = fields.Integer(required=False)
    number_event = fields.Integer(required=False)
    number_doc = fields.Integer(required=False)


class UpdateUserSchema(Schema):
    id = fields.String()
    lastname = fields.String()
    name = fields.String()
    address = fields.String()
    phone = fields.String()
    email = fields.Email()
    avatar = fields.String()
    role = fields.String()

class nonActiveUserSchema(Schema):
    id = fields.String()
    lastname = fields.String()
    name = fields.String()
    address = fields.String()
    phone = fields.String()
    email = fields.Email()
    avatar = fields.String()
    created_on = fields.DateTime()
    active = fields.String()

#
# class AddUserSchema(Schema):
#     email = fields.Email(required=True)
#     api_pwd = fields.Str(required=True)
#     username = fields.Str(required=True, validate=validate.Regexp('^[A-Za-z0-9_-]*$',
#                                                                   error='Invalid username format.'))
#     domain = fields.Str(required=True, validate=validate.Regexp('^[A-Za-z0-9_-]*$',
#                                                                 error='Invalid domain format.'))
#     package = fields.Int(required=False)
#
#
# class ReAddSubsSchema(Schema):
#     domains = fields.List(fields.String(), required=True)
#
#
# class ChangeDomainSchema(Schema):
#     domain = fields.Str(required=True, validate=validate.Regexp('^[A-Za-z0-9_-]*$',
#
#                                                                 error='Invalid domain format.'))


class ChangePackageSchema(Schema):
    package = fields.Str(required=True)


class ChangeApiConfSchema(Schema):
    email = fields.Email(required=True)
    api_pwd = fields.Str(required=True)
