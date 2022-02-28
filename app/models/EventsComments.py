from app import db

# from app.models import Articles
# from app.models.Comments import Comments


class EventsComments(db.Model):
    __tablename__ = 'events_comments'
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    event = db.relationship(
        'Events',
        backref='ev'
    )
    comment = db.relationship(
        'Comments',
        backref='commentss'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls, event, comment):
        ligne = cls.getligne(event)
        ligne.comment_id = comment
        db.session.commit()

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(comment_id=id, delete=False).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, delete=False).first()

    @classmethod
    def getEventsComments(cls, event):
        return cls.query.filter_by(event_id=event.id, delete=False).all()

