from app import db
from app.models.Roles import Roles


class UsersArticles(db.Model):
    __tablename__ = 'users_articles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    user = db.relationship(
        'Users',
        backref='users'
    )
    articles = db.relationship(
        'Articles',
        backref='articles'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(article_id=id, delete=False).first()

    @classmethod
    def getAll(cls, id):
        return cls.query.filter_by(user_id=id, delete=False).all()
