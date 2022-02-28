import datetime
from json import dumps

from flask import request, session
from flask_restful import Resource
from flask_restful.representations import json
from marshmallow import ValidationError
from pymysql import IntegrityError

from app.models import Events, Users
from app.models.SubscribedEvent import SubscribedEvent
from app.models.UserEvents import UserEvents
from app.schematics.Event import EventSchema, GetEventSchema, UpdateEventSchema, SubscribeSchema, GetSubscribe


class AddEvent(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = EventSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            title = schema['title']
            event = Events.find_by_title(title)
            if event:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['Event exist']}}
            else:
                dated = schema['dateD']
                d = dumps(dated, default=str)
                # f = schema['dateF']
                event = Events(title=title, organiser=schema['organiser'], image=schema['image'], price=schema['price'],
                               dateD=schema['dateD'], dateF=schema['dateF'], address=schema['address'],
                               commune=schema['commune'], wilaya=schema['wilaya'], onligne=schema['onligne'],
                               content=schema['content'], email=schema['email'])
                event.save()
                cat = schema['categorie']

                event.attach_categorie(categorie=cat)
                mail = schema['email']
                print(mail)
                event.attach_user(mail)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class RemoveEvent(Resource):
    def delete(self, event_id):
        if event_id:
            event = Events.find_by_id(id=event_id)
            if not event:
                return {'code': 306, 'status': 'error', 'data': {'exist': ['event doesnt exist, id']}}
            else:
                if event.delete:
                    return {'code': 303, 'status': 'error', 'data': {'deleted': ['event doesnt exist']}}
                else:
                    event.remove()
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class UpdateEvent(Resource):
    def put(self, event_id):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = UpdateEventSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            event = Events.find_by_id(id=event_id)
            if not event:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['event doesnt exist']}}
            else:
                event.update(schema)
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetEvent(Resource):
    def get(self, event_id):
        if event_id:
            event = Events.find_by_id(id=event_id)
            if not event:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['event doesnt exist']}}
            else:
                schema = GetEventSchema().dump(event)
                category = event.get_event()
                schema['categorie'] = category
                print(category)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class SubscribeEvent(Resource):
    def post(self, event_id):
        if event_id:
            event = Events.find_by_id(id=event_id)
            data = request.get_json()

            if not event:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['event doesnt exist']}}
            else:
                schema = SubscribeSchema().load(data)
                mail = schema['email_subscriber']
                event.subscribe_user(mail)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetSubscribed(Resource):
    def get(self, event_id):
        if event_id:
            event = Events.find_by_id(id=event_id)
            if not event:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['event doesnt exist']}}

            else:
                subscribes = SubscribedEvent.find_subscribed(event_id)
                sub = []
                for s in subscribes:
                    user = Users.find_by_id(s.user_id)
                    c = GetSubscribe().dump(user)
                    c['email'] = user.email
                    c['name'] = user.name
                    c['lastname'] = user.lastname
                    c['avatar'] = user.avatar
                    sub.append(c)
                    # subuser = [subscribes.user_id]
                return {'code': 300, 'status': 'success', 'data': sub}

        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetAllEvent(Resource):
    def get(self):
        event = Events.get_events()
        schema = []
        for a in event:
            e = GetEventSchema().dump(a)
            e['categorie'] = a.get_event()
            schema.append(e)
        return {'code': 300, 'status': 'success', 'data': schema}

class GetRecentEvent(Resource):
    def get(self):
        event = Events.get_recent_events()
        schema = []
        for a in event:
            e = GetEventSchema().dump(a)
            e['categorie'] = a.get_event()
            schema.append(e)
        return {'code': 300, 'status': 'success', 'data': schema}

class GetEventByUserId(Resource):
    def get(self, user_id):
        user = Users.find_by_id(user_id)
        if user:
            schema = []
            events = user.get_events()
            for a in events:
                event = Events.find_by_id(a.events_id)
                c = GetEventSchema().dump(event)
                c['categorie'] = event.get_event()
                schema.append(c)
            return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'user dont exist'}}
