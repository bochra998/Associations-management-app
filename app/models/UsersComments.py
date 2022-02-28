from app import db
from app.models.Roles import Roles

class UsersComments(db.Model):
    __tablename__ = 'users_comments'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    user = db.relationship(
        'Users',
        backref='uuuuuusers'
    )
    comments = db.relationship(
        'Comments',
        backref='commmentsss'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(comment_id=id, delete=False).first()

    @classmethod
    def getAll(cls, id):
        return cls.query.filter_by(user_id=id, delete=False).all()

