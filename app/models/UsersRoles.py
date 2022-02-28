from sqlalchemy.orm import backref

from app import db


class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    user = db.relationship(
        'Users',
        backref='user'
    )
    roles = db.relationship(
        'Roles',
        backref='role'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls, user, role):
        ligne = cls.getligneone(user)
        ligne.role_id = role
        db.session.commit()

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(user_id=id, delete=False).all()

    @classmethod
    def getligneone(cls, id):
        return cls.query.filter_by(user_id=id, delete=False).first()

    @classmethod
    def getlignerole(cls, id):
        return cls.query.filter_by(role_id=id, delete=False).all()

    @classmethod
    def get(cls, user):

        roles = UsersRoles.query.filter_by(user_id=user.id, delete=False).all()
        # roles_object = []
        # if roles:
        #     for role in roles:
        #         role_name = Roles.get_by_id(rid=role.role_id)
        #         if role_name:
        #             roles_object.append(role_name)
        #
        # return roles_object
        return roles

    @classmethod
    def getUserRole(cls, user):
        if not user.delete:
            ligne = cls.query.filter_by(user_id=user.id, delete=False).first()
            return ligne
            # if ligne:
            #     # roleid = ligne.role_id
            #     role_name = Roles.get_by_id(rid=ligne.role_id).name
            #     return role_name

    # @classmethod
    # def userExist(cls,user):
    #     return bool(cls.find_by_id(user.id))
