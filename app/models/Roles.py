from sqlalchemy.exc import IntegrityError

from app import db
from app.models.UsersRoles import UsersRoles
from app.models.Permissions import Permissions
from app.models.RolesPermissions import RolesPermissions


class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    delete = db.Column(db.BOOLEAN, default=False)

    def attach_permission(self, perm_name):
        if Permissions.exists(perm_name=perm_name):
            permission = Permissions.get_by_perm_name(perm_name=perm_name)
            try:
                RolesPermissions(role=self, permission=permission).add()
                return True
            except IntegrityError:
                return False

    def get_role_permission(self):
        permissions_array = []
        perms = RolesPermissions.query.filter_by(role_id=self.id).all()
        for perm in perms:
            permission = Permissions.get_by_id(pid=perm.permission_id).perm_name
            if permission and permission not in permissions_array:
                permissions_array.append(permission)
        return permissions_array

    def attach_user(self, user):
        UsersRoles(user=user, roles=self).add()
        return True

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        self.delete = True
        p = RolesPermissions.getligne(self.id)
        for per in p:
            per.delete = True
        u = UsersRoles.getlignerole(self.id)
        for user in u:
            user.delete = True
        db.session.commit()

    @classmethod
    def exists(cls, name):
        return bool(cls.get_by_name(name))

    @classmethod
    def add(cls, name):
        if not Roles().exists(name=name):
            return Roles(name=name).save()

    def update(self, schema):
        new = schema['permission']
        ligne = RolesPermissions.getligne(self.id)
        for l in ligne:
            l.remove()
        for p in new:
            per = Permissions.get_by_perm_name(p)
            RolesPermissions(permission=per, role=self).add()
            print(per.id)
        self.name = schema['name']

        # for key, value in schema.items():
        #     setattr(self, key, value)

        db.session.commit()

    def get_role(self):
        return RolesPermissions.getDocumentCategory(self)

    @classmethod
    def get_roles(cls):
        return cls.query.filter_by(delete=False).all()

    @staticmethod
    def get_by_name(name):
        return Roles.query.filter_by(name=name, delete=False).first()

    @classmethod
    def get_by_id(cls, rid):
        return cls.query.filter_by(id=rid, delete=False).first()

    def __repr__(self):
        return '<Roles %r>' % self.name
