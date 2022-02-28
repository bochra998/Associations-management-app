from flask import Blueprint
from flask_restful import Api
from app.controllers.Article import AddArticle, RemoveArticle, UpdateArticle, GetArticle, GetAllArticle, printsession, \
    GetRecentArticle, GetArticlesByUserId

blueprint = Blueprint('article', __name__)
errors = {
    'MethodNotAllowed': {
        'status': 405,
        'message': 'bad_request',
        'some_description': 'The method is not allowed for the requested URL.'
    }
}

api = Api(blueprint)

api.add_resource(AddArticle, '/add')
api.add_resource(RemoveArticle, '/remove/<article_id>')
api.add_resource(UpdateArticle, '/update/<article_id>')
api.add_resource(GetArticle, '/get/<article_id>')
api.add_resource(GetAllArticle, '/get')
api.add_resource(GetRecentArticle, '/getRecent')
api.add_resource(GetArticlesByUserId, '/getarticle/<user_id>')




