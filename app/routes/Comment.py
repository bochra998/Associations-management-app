from flask import Blueprint
from flask_restful import Api
from app.controllers.Comment import AddCommentArticle, AddCommentEvent, GetAllCommentArticle, GetAllCommentEvent,\
    UpdateComment, RemoveCommentArticle, RemoveCommentEvent

blueprint = Blueprint('comment', __name__)
errors = {
    'MethodNotAllowed': {
        'status': 405,
        'message': 'bad_request',
        'some_description': 'The method is not allowed for the requested URL.'
    }
}

api = Api(blueprint)

api.add_resource(AddCommentArticle, '/addart/<article_id>')
api.add_resource(AddCommentEvent, '/addev/<event_id>')
api.add_resource(GetAllCommentArticle, '/getart/<article_id>')
api.add_resource(GetAllCommentEvent, '/getev/<event_id>')
api.add_resource(UpdateComment, '/update/<comment_id>')
api.add_resource(RemoveCommentArticle, '/removeart/<comment_id>')
api.add_resource(RemoveCommentEvent, '/removeev/<comment_id>')
