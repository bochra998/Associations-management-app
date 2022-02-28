
from flask import request, session, jsonify
from flask_restful import Resource
from marshmallow import ValidationError

from app.models import Users
from app.models.Articles import Articles
from app.schematics.Article import ArticleSchema, UpdateArticleSchema, GetArticleSchema


class AddArticle(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = ArticleSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            title = schema['title']
            article = Articles.find_by_title(title)
            if article:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['article exist']}}
            else:
                article = Articles(title=title, author=schema['author'], image=schema['image'],contenu=schema['contenu'], email=schema['email'] )
                article.save()
                cat = schema['categorie']
                article.attach_categorie(categorie=cat)
                mail = schema['email']
                print(mail)
                article.attach_user(mail)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class RemoveArticle(Resource):
    def delete(self, article_id):
        if article_id:
            article = Articles.find_by_id(id=article_id)
            if not article:
                return {'code': 306, 'status': 'error', 'data': {'exist': ['article doesnt exist, id']}}
            else:
                if article.delete:
                    return {'code': 303, 'status': 'error', 'data': {'deleted': ['article doesnt exist']}}
                else:
                    article.remove()
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class UpdateArticle(Resource):
    def put(self, article_id):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        try:
            schema = UpdateArticleSchema().load(data)
        except ValidationError as err:
            return {'code': 304, 'status': 'error', 'data': err.messages}
        if data:
            article = Articles.find_by_id(id=article_id)
            if not article:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['article doesnt exist']}}
            else:
                article.update(schema)
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetArticle(Resource):
    def get(self, article_id):
        if article_id:
            article = Articles.find_by_id(id=article_id)
            if not article:
                return {'code': 303, 'status': 'error', 'data': {'exist': ['article doesnt exist']}}
            else:
                schema = GetArticleSchema().dump(article)
                category = article.get_article()
                schema['categorie'] = category
                print(category)
                return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'registration': ['Something is wrong.']}}


class GetAllArticle(Resource):
    def get(self):
        articles = Articles.get_articles()
        schema = []
        for a in articles:
            c = GetArticleSchema().dump(a)
            c['categorie'] = a.get_article()
            schema.append(c)

        return {'code': 300, 'status': 'success', 'data': schema}

class GetRecentArticle(Resource):
    def get(self):
        articles = Articles.get_recent_articles()
        schema = []
        for a in articles:
            c = GetArticleSchema().dump(a)
            c['categorie'] = a.get_article()
            schema.append(c)
        return {'code': 300, 'status': 'success', 'data': schema}

class printsession(Resource):
    def get(self):
        print(session['email'])
        return jsonify(session['email'])

class GetArticlesByUserId(Resource):
    def get(self, user_id):
        user = Users.find_by_id(user_id)
        if user:
            schema = []
            articles = user.get_articles()
            for a in articles:
                article = Articles.find_by_id(a.article_id)
                c = GetArticleSchema().dump(article)
                c['categorie'] = article.get_article()
                schema.append(c)
            return {'code': 300, 'status': 'success', 'data': schema}
        else:
            return {'code': 305, 'status': 'error', 'data': {'user dont exist'}}
