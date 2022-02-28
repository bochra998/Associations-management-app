from app import db

# from app.models import Articles
from app.models.Categories import Categories


class CategoriesArticles(db.Model):
    __tablename__ = 'categories_articles'
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    article = db.relationship(
        'Articles',
        backref='article'
    )
    category = db.relationship(
        'Categories',
        backref='category'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls, article, category):
        ligne = cls.getligne(article)
        ligne.category_id = category
        db.session.commit()

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(article_id=id, delete=False).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, delete=False).first()

    @classmethod
    def getArticleCategory(cls, article):
        ligne = cls.query.filter_by(article_id=article.id, delete=False).first()
        if ligne:
            category_name = Categories.get_by_id(id=ligne.category_id).name
            return category_name
