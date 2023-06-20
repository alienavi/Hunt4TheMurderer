from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model) :
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False, nullable=False)
    def __repr__(self) :
        return '<User %r>' % self.username