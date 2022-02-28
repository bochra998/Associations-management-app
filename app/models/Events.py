from pymysql import IntegrityError
from sqlalchemy import desc

from app import db
from app.models.Categories import Categories
from app.models.CategoriesEvents import CategoriesEvents
from app.models import Users
from app.models.SubscribedEvent import SubscribedEvent
from app.models.UserEvents import UserEvents


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    price = db.Column(db.Integer)
    dateD = db.Column(db.DateTime)
    dateF = db.Column(db.DateTime)
    address = db.Column(db.String(255))
    commune = db.Column(db.String(255))
    wilaya = db.Column(db.String(255))
    onligne = db.Column(db.BOOLEAN(255))
    organiser = db.Column(db.String(255))
    image = db.Column(db.String(255))
    content = db.Column(db.String(255))
    email = db.Column(db.String(255))

    delete = db.Column(db.BOOLEAN, default=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<Events %r>' % self.title

    @classmethod
    def exists(cls, id):
        return bool(cls.find_by_id(id))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        self.delete = True
        u = UserEvents.getligne(self.id)
        u.delete = True
        cevent = CategoriesEvents.getligne(self.id)
        cevent.delete = True
        print(cevent)
        db.session.commit()

    def update(self, schema):
        for key, value in schema.items():
            setattr(self, key, value)
            new = schema['categorie']
            cat = Categories.get_by_name(new)
            CategoriesEvents.update(event=self.id, category=cat.id)
        db.session.commit()

    def get_event(self):
        return CategoriesEvents.getEventCategory(self)

    def attach_categorie(self, categorie):
        if Categories.exists(categorie):
            cat = Categories.get_by_name(name=categorie)
            try:
                CategoriesEvents(event=self, category=cat).add()
                return True
            except IntegrityError:
                return False
        else:
            return False

    def attach_user(self, mail):
        if Users.exists(email=mail):
            user = Users.get_by_email(email=mail)
            try:
                UserEvents(user=user, events=self).add()
                return True
            except IntegrityError:
                return False
        else:
            return False

    def subscribe_user(self, mail):
        if Users.exists(email=mail):
            user = Users.get_by_email(email=mail)
            try:
                SubscribedEvent(user=user, events=self).add()
                return True
            except IntegrityError:
                return False
        else:
            return False

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title, delete=False).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, delete=False).first()

    @staticmethod
    def get_by_name(name):
        return Categories.query.filter_by(name=name, delete=False).first()

    @classmethod
    def get_events(cls):
        return cls.query.filter_by(delete=False).all()

    @classmethod
    def get_recent_events(cls):
        return cls.query.filter_by(delete=False).order_by(desc('id')).limit(3)

