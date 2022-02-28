from app import db
from app.models.Roles import Roles


class UsersDocuments(db.Model):
    __tablename__ = 'users_documents'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    user = db.relationship(
        'Users',
        backref='usersssssss'
    )
    documents = db.relationship(
        'Documents',
        backref='doc'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(document_id=id, delete=False).first()

    @classmethod
    def getAll(cls, id):
        return cls.query.filter_by(user_id=id, delete=False).all()

