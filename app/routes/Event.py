from flask import Blueprint
from flask_restful import Api
from app.controllers.Event import AddEvent, UpdateEvent, RemoveEvent, GetEvent, SubscribeEvent, GetSubscribed, \
    GetAllEvent, GetRecentEvent, GetEventByUserId

blueprint = Blueprint('event', __name__)
errors = {
    'MethodNotAllowed': {
        'status': 405,
        'message': 'bad_request',
        'some_description': 'The method is not allowed for the requested URL.'
    }
}

api = Api(blueprint)

api.add_resource(AddEvent, '/add')
api.add_resource(RemoveEvent, '/remove/<event_id>')
api.add_resource(UpdateEvent, '/update/<event_id>')
api.add_resource(GetEvent, '/get/<event_id>')
api.add_resource(GetRecentEvent, '/getRecent')
api.add_resource(SubscribeEvent, '/sub/<event_id>')
api.add_resource(GetSubscribed, '/getsub/<event_id>')
api.add_resource(GetAllEvent, '/get')
api.add_resource(GetEventByUserId, '/getevent/<user_id>')


