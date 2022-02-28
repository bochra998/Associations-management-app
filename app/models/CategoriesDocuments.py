from app import db
from app.models.Categories import Categories


class CategoriesDocuments(db.Model):
    __tablename__ = 'categories_documents'
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    document = db.relationship(
        'Documents',
        backref='document'
    )
    category = db.relationship(
        'Categories',
        backref='categori'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls, document, category):
        ligne = cls.getligne(document)
        ligne.category_id = category
        db.session.commit()

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(document_id=id, delete=False).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, delete=False).first()

    @classmethod
    def getDocumentCategory(cls, document):
        ligne = cls.query.filter_by(document_id=document.id, delete=False).first()
        if ligne:
            category_name = Categories.get_by_id(id=ligne.category_id).name
            return category_name
