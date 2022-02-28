from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from app import db

from app.models import Users
from app.models.Categories import Categories
from app.models.CategoriesArticles import CategoriesArticles
from app.models.UsersArticles import UsersArticles


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    image = db.Column(db.String(255))
    contenu = db.Column(db.Text)
    email = db.Column(db.String(255))

    delete = db.Column(db.BOOLEAN, default=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<Articles %r>' % self.auteur

    @classmethod
    def exists(cls, id):
        return bool(cls.find_by_id(id))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        self.delete = True
        carticle = CategoriesArticles.getligne(self.id)
        carticle.delete = True
        u = UsersArticles.getligne(self.id)
        u.delete = True
        print(carticle)
        db.session.commit()

    def update(self, schema):
        for key, value in schema.items():
            setattr(self, key, value)
            new = schema['categorie']
            cat = Categories.get_by_name(new)
            CategoriesArticles.update(article=self.id, category=cat.id)
        db.session.commit()

    def attach_categorie(self, categorie):
        if Categories.exists(categorie):
            cat = Categories.get_by_name(name=categorie)
            try:
                CategoriesArticles(article=self, category=cat).add()
                return True
            except IntegrityError:
                return False
        else:
            return False

    def attach_user(self, mail):
        if Users.exists(email=mail):
            user = Users.get_by_email(email=mail)
            try:
                UsersArticles(user=user, articles=self).add()
                return True
            except IntegrityError:
                return False
        else:
            return False

    def get_article(self):
        return CategoriesArticles.getArticleCategory(self)

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title, delete=False).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, delete=False).first()

    @classmethod
    def find(cls):
        return cls.query.filter_by(delete=False).all()

    @classmethod
    def get_articles(cls):
        return cls.query.filter_by(delete=False).all()

    @classmethod
    def get_recent_articles(cls):
        return cls.query.filter_by(delete=False).order_by(desc('id')).limit(3)

    # @staticmethod
    # def get_by_name(name):
    #     return Categories.query.filter_by(name=name, delete=False).first()

