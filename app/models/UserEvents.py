from app import db
from app.models.Roles import Roles


class UserEvents(db.Model):
    __tablename__ = 'users_events'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    user = db.relationship(
        'Users',
        backref='userss'
    )
    events = db.relationship(
        'Events',
        backref='eventt'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(events_id=id, delete=False).first()

    @classmethod
    def getAll(cls, id):
        return cls.query.filter_by(user_id=id, delete=False).all()



