from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    plants = db.relationship('Plant', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    nickname = db.Column(db.String(64))
    water_freq = db.Column(db.Integer)
    purchase_date = db.Column(db.Date)
    plant_img = db.Column(db.String(1000000))
    last_watered = db.Column(db.Date)
    avatar = db.Column(db.String(64))
    plant_data_id = db.Column(db.Integer, db.ForeignKey('plant__data.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Plant_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    names = db.Column(db.String(100))
    latin_name = db.Column(db.String(100))
    min_temp = db.Column(db.Integer)
    max_temp = db.Column(db.Integer)
    ideal_light = db.Column(db.String(100))
    tolerated_light = db.Column(db.String(100))
    pests = db.Column(db.String(100))
    watering = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    climate = db.Column(db.String(100))
    soil = db.Column(db.String(100))
    plants = db.relationship('Plant', backref='data', lazy='dynamic')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
