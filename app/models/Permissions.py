from app import db


class Permissions(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    perm_name = db.Column(db.String(255), unique=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def exists(cls, perm_name):
        return bool(cls.get_by_perm_name(perm_name))

    @classmethod
    def add(cls, name, perm_name):
        if not Permissions().exists(perm_name=perm_name):
            return Permissions(name=name, perm_name=perm_name).save()

    @staticmethod
    def get_by_perm_name(perm_name):
        return Permissions.query.filter_by(perm_name=perm_name).first()

    @classmethod
    def get_by_id(cls, pid):
        return cls.query.filter_by(id=pid).first()

    @classmethod
    def get_all_permission(cls):
        permissions_array = []
        perms = Permissions.query.all()
        for perm in perms:
            permission = perm.perm_name
            if permission and permission not in permissions_array:
                permissions_array.append(permission)
        return permissions_array

    def __repr__(self):
        return '<Permissions %r>' % self.name
