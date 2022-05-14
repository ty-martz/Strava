from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime())
    activity = db.Column(db.String(10000))
    upd_date = db.Column(db.DateTime(), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_sec = db.Column(db.Float)
    dist_km = db.Column(db.Float)
    max_heart_rate = db.Column(db.Integer)
    max_speed = db.Column(db.Float)
    average_speed = db.Column(db.Float)
    elevation_gain = db.Column(db.Float)
    average_heart_rate = db.Column(db.Integer)
    calories = db.Column(db.Integer)
    hour_of_day = db.Column(db.Integer)
    month_of_year = db.Column(db.Integer)
    distance_miles = db.Column(db.Float)
    time_minutes = db.Column(db.Float)
    max_speed_mph = db.Column(db.Float)
    average_speed_mph = db.Column(db.Float)
    elevation_gain_ft = db.Column(db.Float)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Activities')

