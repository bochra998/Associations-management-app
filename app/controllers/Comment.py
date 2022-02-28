from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.models import UsersComments, Users
from app.models.Comments import Comments
from app.schematics.Comment import CommentSchema, CommentArticle
from app.models.EventsComments import EventsComments
from app.models.ArticlesComments import ArticlesComments


class AddCommentEvent(Resource):
    def post(self, event_id):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = CommentSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            comment = Comments(content=schema['content'])
            comment.save()
            comment.attach_event(event=event_id)

            return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class AddCommentArticle(Resource):
    def post(self, article_id):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = CommentSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            comment = Comments(content=schema['content'])
            comment.save()
            comment.attach_article(article=article_id)
            comment.attach_user(mail=schema['email'])

            return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class RemoveCommentEvent(Resource):
    def delete(self, comment_id):
        if comment_id:
            comment = Comments.find_by_id(id=comment_id)
            if not comment:
                return {'code': 306, 'status': 'error', 'data': {'exist': ['article doesnt exist, id']}}
            else:
                if comment.delete:
                    return {'code': 303, 'status': 'error', 'data': {'deleted': ['article doesnt exist']}}
                else:
                    comment.remove_event()
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class RemoveCommentArticle(Resource):
    def delete(self, comment_id):
        if comment_id:
            comment = Comments.find_by_id(id=comment_id)
            if not comment:
                return {'code': 306, 'status': 'error', 'data': {'exist': ['article doesnt exist, id']}}
            else:
                if comment.delete:
                    return {'code': 303, 'status': 'error', 'data': {'deleted': ['article doesnt exist']}}
                else:
                    comment.remove_article()
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class UpdateComment(Resource):
    def put(self, comment_id):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = CommentSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            comment = Comments.find_by_id(id=comment_id)
            if not comment:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['article doesnt exist']}}
            else:
                comment.update(schema)
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetAllCommentEvent(Resource):
    def get(self, event_id):
        event = Comments.find_by_id(id=event_id)
        if not event:
            return {'code': 306, 'status': 'error', 'data': {'exist': ['event doesnt exist, id']}}
        else:
            if event.delete:
                return {'code': 303, 'status': 'error', 'data': {'deleted': ['event doesnt exist']}}
            else:
                comment = EventsComments.getEventsComments(event)
                com = []
                for s in comment:
                    comment = Comments.find_by_id(s.comment_id)
                    c = CommentArticle().dump(comment)
                    ligne = UsersComments.getligne(comment.id)
                    user_id = ligne.user_id
                    user = Users.find_by_id(user_id)
                    c['content'] = comment.content
                    c['email'] = user.email
                    c['avatar'] = user.avatar
                    com.append(c)
            return {'code': 300, 'status': 'success', 'data': com}


class GetAllCommentArticle(Resource):
    def get(self, article_id):
        article = Comments.find_by_id(id=article_id)
        if not article:
            return {'code': 306, 'status': 'error', 'data': {'exist': ['article doesnt exist, id']}}
        else:
            if article.delete:
                return {'code': 303, 'status': 'error', 'data': {'deleted': ['article doesnt exist']}}
            else:
                comment = ArticlesComments.getArticlesComments(article)
                com = []
                for s in comment:
                    comment = Comments.find_by_id(s.comment_id)
                    c = CommentArticle().dump(comment)
                    ligne = UsersComments.getligne(comment.id)
                    user_id = ligne.user_id
                    user = Users.find_by_id(user_id)
                    c['content'] = comment.content
                    c['email'] = user.email
                    c['avatar'] = user.avatar
                    com.append(c)
                return {'code': 300, 'status': 'success', 'data': com}
