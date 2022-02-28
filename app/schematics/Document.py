from marshmallow import Schema, fields


class DocumentSchema(Schema):
    title = fields.String(required=True)
    contenu = fields.String()
    image = fields.String()
    file = fields.String()
    categorie = fields.String()
    public = fields.Boolean()
    email = fields.String()



class UpdateDocumentSchema(Schema):
    id = fields.String()
    title = fields.String()
    contenu = fields.String()
    image = fields.String()
    file = fields.String()
    categorie = fields.String()
    public = fields.Boolean()

class GetDocumentSchema(Schema):
        id = fields.String()
        title = fields.String(required=True)
        contenu = fields.String()
        image = fields.String()
        file = fields.String()
        categorie = fields.String()
        public = fields.Boolean()
        created_on = fields.DateTime(required=True)