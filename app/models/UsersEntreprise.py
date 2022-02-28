from app import db
from app.models.Roles import Roles


class UsersEntreprise(db.Model):
    __tablename__ = 'users_entreprises'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprises.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    user = db.relationship(
        'Users',
        backref='u'
    )
    entreprises = db.relationship(
        'Entreprises',
        backref='entreprise'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(entreprise_id=id, delete=False).first()

    @classmethod
    def getUserEntreprise(cls, user):
        if not user.delete:
            ligne = cls.query.filter_by(user_id=user.id, delete=False).first()
            return ligne
    @classmethod
    def getAll(cls, id):
        return cls.query.filter_by(user_id=id, delete=False).all()
