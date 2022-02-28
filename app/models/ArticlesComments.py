from app import db

# from app.models import Articles
# from app.models.Comments import Comments


class ArticlesComments(db.Model):
    __tablename__ = 'articles_comments'
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    article = db.relationship(
        'Articles',
        backref='ar'
    )
    comment = db.relationship(
        'Comments',
        backref='comments'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls, article, comment):
        ligne = cls.getligne(article)
        ligne.comment_id = comment
        db.session.commit()

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(comment_id=id, delete=False).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, delete=False).first()

    @classmethod
    def getArticlesComments(cls, article):
        return cls.query.filter_by(article_id=article.id, delete=False).all()


