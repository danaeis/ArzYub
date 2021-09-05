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

class Nobitex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # currtype = db.Column(db.String(20), nullable=False)
    Pprice =  db.Column(db.Float, nullable=False)
    Pamount =  db.Column(db.Float, nullable=False)
    Sprice = db.Column(db.Float, nullable=False)
    Samount = db.Column(db.Float, nullable=False)
    curr = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Nobitex('{self.curr}', '{self.Pprice}', '{self.Pamount}', '{self.Sprice}','{self.Samount}', '{self.date_created}')"

class Wallex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # currtype = db.Column(db.String(20), nullable=False)
    Pprice =  db.Column(db.Float, nullable=False)
    Pamount =  db.Column(db.Float, nullable=False)
    Sprice = db.Column(db.Float, nullable=False)
    Samount = db.Column(db.Float, nullable=False)
    curr = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Wallex('{self.curr}', '{self.Pprice}', '{self.Pamount}', '{self.Sprice}','{self.Samount}', '{self.date_created}')"


