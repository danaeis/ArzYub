from datetime import datetime, timedelta
from arzyab import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Integer, String, Float


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currtype = db.Column(db.String(20), unique=True, nullable=False)
    nobitexPrice =  db.Column(db.Float)
    nobitexAmount =  db.Column(db.Float)
    wallexPrice =  db.Column(db.Float)
    wallexAmount =  db.Column(db.Float)

    def __repr__(self):
        return f"Currency('{self.nobitexPrice}', '{self.nobitexAmount}', '{self.wallexPrice}', '{self.wallexAmount}')"

