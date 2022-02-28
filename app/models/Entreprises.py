from app import db
from app.models import Users
from app.models.UsersEntreprise import UsersEntreprise
from sqlalchemy.exc import IntegrityError


class Entreprises(db.Model):
    tablename = 'entreprises'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    email = db.Column(db.String(255))
    raison_sociale = db.Column(db.String(255))
    forme_juridique = db.Column(db.String(255))
    quality = db.Column(db.String(255))
    secteur_activity = db.Column(db.String(255))
    contact = db.Column(db.String(255))
    fax = db.Column(db.String(255))
    address = db.Column(db.String(255))
    commune = db.Column(db.String(255))
    wilaya = db.Column(db.String(255))
    nb_employes = db.Column(db.INT)
    chiffre_affaires = db.Column(db.FLOAT)
    capitale = db.Column(db.FLOAT)
    year_creation = db.Column(db.DateTime)
    facebook = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    website = db.Column(db.String(255))
    produits_service = db.Column(db.String(255))
    presentation = db.Column(db.String(255))
    confirmation = db.Column(db.BOOLEAN)
    file = db.Column(db.String(255))
    Description = db.Column(db.String(255))
    delete = db.Column(db.Boolean, default=False)
    email_user = db.Column(db.String(255))

    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def repr(self):
        return '<Category %r>' % self.name

    @classmethod
    def exists(cls, id):
        return bool(cls.find_by_id(id))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        self.delete = True
        u = UsersEntreprise.getligne(self.id)
        u.delete = True
        db.session.commit()

    def update(self, schema):
        for key, value in schema.items():
            setattr(self, key, value)
        db.session.commit()

    def attach_user(self, mail):
        if Users.exists(email=mail):
            user = Users.get_by_email(email=mail)
            try:
                UsersEntreprise(user=user, entreprises=self).add()
                return True
            except IntegrityError:
                return False
        else:
            return False


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name, delete=False).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, delete=False).first()

    @classmethod
    def get_entreprises(cls):
        return cls.query.filter_by(delete=False).all()