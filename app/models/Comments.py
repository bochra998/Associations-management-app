from sqlalchemy.exc import IntegrityError

from app import db

from app.models import Articles, Users
from app.models.ArticlesComments import ArticlesComments
from app.models.EventsComments import EventsComments
from app.models.Events import Events
from app.models.UsersComments import UsersComments


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))

    delete = db.Column(db.BOOLEAN, default=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<Articles %r>' % self.auteur

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove_event(self):
        self.delete = True
        ev = EventsComments.getligne(self.id)
        ev.delete = True
        db.session.commit()

    def remove_article(self):
        ar = ArticlesComments.getligne(self.id)
        self.delete = True
        ar.delete = True
        db.session.commit()

    def update(self, schema):
        for key, value in schema.items():
            setattr(self, key, value)
        db.session.commit()

    def attach_article(self, article):
        if Articles.exists(article):
            art = Articles.find_by_id(id=article)
            try:
                ArticlesComments(article=art, comment=self).add()
                return True
            except IntegrityError:
                return False
        else:
            return False

    def attach_event(self, event):
        if Events.exists(event):
            ev = Events.find_by_id(id=event)
            try:
                EventsComments(event=ev, comment=self).add()
                return True
            except IntegrityError:
                return False
        else:
            print(event)
            return False

    def attach_user(self, mail):
        if Users.exists(email=mail):
            user = Users.get_by_email(email=mail)
            try:
                UsersComments(user=user, comments=self).add()
                return True
            except IntegrityError:
                return False
        else:
            return False

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, delete=False).first()
