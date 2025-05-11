from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model) :
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    completed_rooms = db.relationship('RoomCompletion', backref='user', lazy=True)
    clues = db.relationship('Clue', backref='user', lazy=True)
    def __repr__(self) :
        return '<User %r>' % self.username

class RoomCompletion(db.Model):
    __tablename__ = 'room_completion'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_name = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<RoomCompletion {self.room_name} for User {self.user_id}>'

class Clue(db.Model):
    __tablename__ = 'clue'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_name = db.Column(db.String(50), nullable=False)
    clue_text = db.Column(db.Text, nullable=False)
    discovered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Clue {self.room_name}>'