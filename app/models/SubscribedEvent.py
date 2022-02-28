from app import db
from app.models.Roles import Roles


class SubscribedEvent(db.Model):
    __tablename__ = 'subscribed_events'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    user = db.relationship(
        'Users',
        backref='use'
    )
    events = db.relationship(
        'Events',
        backref='events'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_subscribed(cls, id):
        return cls.query.filter_by(event_id=id, delete=False).all()
