from marshmallow import Schema, fields


class ArticleSchema(Schema):

    title = fields.String(required=True)
    author = fields.String(required=True)
    image = fields.String(required=True)
    categorie = fields.String(required=True)
    contenu = fields.String(required=True)
    email = fields.String(required=True)




class GetArticleSchema(Schema):

    id = fields.String(required=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    image = fields.String(required=True)
    categorie = fields.String(required=True)
    contenu = fields.String(required=True)
    created_on = fields.DateTime(required=True)


class UpdateArticleSchema(Schema):
    id = fields.String()
    title = fields.String()
    author = fields.String()
    image = fields.String()
    categorie = fields.String(required=False)
    contenu = fields.String()


