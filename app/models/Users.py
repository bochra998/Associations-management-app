from sqlalchemy.exc import IntegrityError

from app import db
from app.models.UsersDocuments import UsersDocuments
from app.models.Roles import Roles
from app.models.UserEvents import UserEvents
from app.models.UsersArticles import UsersArticles
from app.models.UsersEntreprise import UsersEntreprise
from app.models.UsersRoles import UsersRoles


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(10))
    email = db.Column(db.String(254), index=True, unique=True)
    password = db.Column(db.String(254))
    name = db.Column(db.String(254))
    lastname = db.Column(db.String(254))
    phone = db.Column(db.String(254))
    avatar = db.Column(db.String(254))
    wilaya = db.Column(db.String(254))
    civilite = db.Column(db.String(254))
    birthplace = db.Column(db.String(254))
    birthdate = db.Column(db.DATE)
    address = db.Column(db.String(256))
    socialmedia = db.Column(db.String(256))
    adhesionyear = db.Column(db.DATE)
    delete = db.Column(db.BOOLEAN, default=False)
    active = db.Column(db.BOOLEAN, default=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_onupdate=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        self.delete = True
        urole = UsersRoles.getligneone(self.id)
        urole.delete = True
        print(urole)
        db.session.commit()

    def update(self, schema):
        for key, value in schema.items():
            setattr(self, key, value)
        new = schema['role']
        role = Roles.get_by_name(new)
        urole = UsersRoles.getlignerole(role.id)
        if not urole:
            self.attach_role(new)
            db.session.commit()
        else:
            UsersRoles.update(user=self.id, role=role.id)
            db.session.commit()

    def attach_role(self, role):
        if Roles.exists(name=role):
            role = Roles.get_by_name(name=role)
            try:
                UsersRoles(user=self, roles=role).add()
                return True
            except IntegrityError:
                return False
        else:
            return False

    def get_roles(self):
        return UsersRoles.get(self)

    def get_role(self):
        return UsersRoles.getUserRole(self)

    def get_entreprise(self):
        return UsersEntreprise.getUserEntreprise(self)

    def get_articles(self):
        return UsersArticles.getAll(self.id)

    def get_events(self):
        return UserEvents.getAll(self.id)

    def get_documents(self):
        return UsersDocuments.getAll(self.id)

    def get_entreprises(self):
        return UsersEntreprise.getAll(self.id)

    def flatten(l):
        try:
            return Users.flatten(l[0]) + (Users.flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]
        except IndexError:
            return []

    def get_permissions(self):
        permissions_list = []
        urole = Users.get_role(self)
        if urole:
            role = Roles.get_by_id(urole.role_id)
            permission = role.get_role_permission()
            if permission and permission not in permissions_list:
                permissions_list.append(permission)
            unique = []
            for item in Users.flatten(permissions_list):
                if item not in unique:
                    unique.append(item)
            return unique
        else:
            return permissions_list

    # def get_permissions(cls):
    #     return cls.roles

    def up(self, schema):
        for key, value in schema.items():
            setattr(self, key, value)
        new = schema['role']
        self.attach_role(new)
        db.session.commit()

    @staticmethod
    def get_by_email(email):
        return Users.query.filter_by(email=email, delete=False).first()

    @classmethod
    def exists(cls, email):
         return bool(cls.find_by_email(email))

    @classmethod
    def seed(cls, email, uid, password):
        if not Users.exists(email=email):
            return Users(email=email, uid=uid, password=password).save()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email, delete=False).first()

    @classmethod
    def find_by_uid(cls, uid):
        return cls.query.filter_by(uid=uid, delete=False).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, delete=False).first()

    @classmethod
    def find_all(cls):
        return cls.query.filter_by(delete=False).all()

    @classmethod
    def getligneone(cls, id):
        return cls.query.filter_by(user_id=id, delete=False).first()

    @classmethod
    def find_non_active(cls):
        return cls.query.filter_by(active=False,delete=False).all()

    @classmethod
    def find_non_activate_user(cls, user):
        return cls.query.filter_by(active=False, id=user, delete=False).first()


    def __repr__(self):
        return '<Users %r>' % self.email
