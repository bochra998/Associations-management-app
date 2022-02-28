import marshmallow
from marshmallow import Schema, fields


class RoleSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=False)
    permission = fields.List(fields.String(), required=False)
