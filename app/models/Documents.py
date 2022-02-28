from pymysql import IntegrityError

from app import db
from app.models import Users
from app.models.Categories import Categories
from app.models.CategoriesDocuments import CategoriesDocuments
from app.models.UsersDocuments import UsersDocuments
from app.models.UsersArticles import UsersArticles


class Documents(db.Model):
    tablename = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    contenu = db.Column(db.String(255))
    image = db.Column(db.String(255))
    file = db.Column(db.String(255))
    public = db.Column(db.Boolean)
    email = db.Column(db.String(255))

    delete = db.Column(db.Boolean, default=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<Documents %r>' % self.title

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        self.delete = True
        cdocument = CategoriesDocuments.getligne(self.id)
        cdocument.delete = True
        print(cdocument)
        db.session.commit()

    def update(self, schema):
        for key, value in schema.items():
            setattr(self, key, value)
            new = schema['categorie']
            cat = Categories.get_by_name(new)
            CategoriesDocuments.update(document=self.id, category=cat.id)
        db.session.commit()

    def get_document(self):
        return CategoriesDocuments.getDocumentCategory(self)

    def attach_categorie(self, categorie):
        if Categories.exists(categorie):
            cat = Categories.get_by_name(name=categorie)
            try:
                CategoriesDocuments(document=self, category=cat).add()
                return True
            except IntegrityError:
                return False
        else:
            return False

    def attach_user(self, mail):
        if Users.exists(email=mail):
            user = Users.get_by_email(email=mail)
            try:
                UsersDocuments(user=user, documents=self).add()
                return True
            except IntegrityError:
                return False
        else:
            return False

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title, delete=False).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, delete=False).first()

    @classmethod
    def get_documents(cls):
        return cls.query.filter_by(delete=False).all()

