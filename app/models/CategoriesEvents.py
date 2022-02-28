from app import db
from app.models.Categories import Categories


class CategoriesEvents(db.Model):
    __tablename__ = 'categories_events'
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    delete = db.Column(db.BOOLEAN, default=False)

    event = db.relationship(
        'Events',
        backref='event'
    )
    category = db.relationship(
        'Categories',
        backref='categoryy'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls, event, category):
        ligne = cls.getligne(event)
        ligne.category_id = category
        db.session.commit()

    @classmethod
    def getligne(cls, id):
        return cls.query.filter_by(event_id=id, delete=False).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, delete=False).first()

    @classmethod
    def getEventCategory(cls, event):
        ligne = cls.query.filter_by(event_id=event.id, delete=False).first()
        if ligne:
            category_name = Categories.get_by_id(id=ligne.category_id).name
            return category_name
