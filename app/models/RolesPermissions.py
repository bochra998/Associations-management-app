from app import db
from app.models import Roles, Permissions


class RolesPermissions(db.Model):
    __tablename__ = 'roles_permissions'
    # id = db.Column(db.Integer, primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    # delete = db.Column(db.BOOLEAN, default=False)

    permission = db.relationship(
        'Permissions',
        backref='permission'
    )
    role = db.relationship(
        'Roles',
        backref='rolesss'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update(cls, role, permission):
        ligne = cls.getoneligne(role)
        ligne.permission_id = permission
        db.session.commit()



    @classmethod
    def get(cls, user):
        role = RolesPermissions.query.filter_by(user_id=user.id).first()
        if role:
            role_name = Roles.get_by_id(rid=role.role_id)
            if role_name:
                return role_name.name
            else:
                return False
        else:
            return False
        # if role:
        #     return role.name
        # else:
        #     return False

    @classmethod
    def getRolePermission(cls, role):
        ligne = cls.query.filter_by(role_id=role.id, delete=False).first()
        if ligne:
            permission_name = Permissions.get_by_id(pid=ligne.permission_id).name
            return permission_name

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(role_id=id, delete=False).all()

    @classmethod
    def getoneligne(cls, id):
        return cls.query.filter_by(role_id=id, delete=False).first()
