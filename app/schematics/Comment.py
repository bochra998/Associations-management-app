from marshmallow import Schema, fields


class CommentSchema(Schema):
    content = fields.String(required=True)
    event = fields.String(required=False)
    article = fields.String(required=False)
    email = fields.Email(required=False)

class CommentArticle(Schema):
    content = fields.String(required=True)
    email = fields.String(required=False)
    avatar = fields.String(required=False)
