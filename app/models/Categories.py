from app import db


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    delete = db.Column(db.BOOLEAN, default=False)

    def __repr__(self):
        return '<Categories %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def exists(cls, name):
        return bool(cls.get_by_name(name))

    @staticmethod
    def get_by_name(name):
        return Categories.query.filter_by(name=name, delete=False).first()

    @staticmethod
    def get_by_id(id):
        return Categories.query.filter_by(id=id, delete=False).first()
