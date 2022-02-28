from marshmallow import Schema, fields


class EventSchema(Schema):
    title = fields.String(required=True)
    price = fields.Integer(required=True)
    dateD = fields.DateTime(required=True)
    dateF = fields.DateTime(required=True)
    organiser = fields.String(required=True)
    address = fields.String(required=True)
    commune = fields.String(required=True)
    wilaya = fields.String(required=True)
    onligne = fields.Boolean(required=False)
    image = fields.String(required=True)
    categorie = fields.String(required=True)
    content = fields.String(required=False)
    email = fields.String()


class GetEventSchema(Schema):

    id = fields.String(required=True)
    title = fields.String(required=True)
    price = fields.Integer(required=True)
    dateD = fields.DateTime(required=True)
    dateF = fields.DateTime(required=True)
    organiser = fields.String(required=True)
    address = fields.String(required=True)
    commune = fields.String(required=True)
    wilaya = fields.String(required=True)
    onligne = fields.Boolean(required=False)
    image = fields.String(required=True)
    categorie = fields.String(required=True)
    content = fields.String(required=True)
    created_on = fields.DateTime(required=True)


class UpdateEventSchema(Schema):
    id = fields.String()
    title = fields.String()
    price = fields.Integer()
    dateD = fields.DateTime()
    dateF = fields.DateTime()
    organiser = fields.String()
    address = fields.String()
    commune = fields.String()
    wilaya = fields.String()
    onligne = fields.Boolean()
    image = fields.String()
    categorie = fields.String()
    content = fields.String()


class SubscribeSchema(Schema):
    email_subscriber = fields.String(required=False)

class GetSubscribe(Schema):
    email = fields.String(required=False)
    name = fields.String(required=False)
    lastname = fields.String(required=False)
    avatar = fields.String(required=False)

