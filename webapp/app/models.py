from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt
from app import app

# Storing User Data
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(64))
    ratings = db.relationship("Ratings", backref="rater", lazy="dynamic")

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

# Load in users
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Storing User Ratings
class Ratings(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('animes.id'))
    #anime_name = db.Column(db.String(256), db.ForeignKey('animes.name'))
    user_rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return '<User Ratings>'


# Storing Anime Data
class Animes(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String)
    genre = db.Column(db.String)
    type = db.Column(db.String)
    episodes = db.Column(db.String)
    avg_rating = db.Column(db.Float)
    members = db.Column(db.Integer)
    ratings = db.relationship('Ratings', backref='anime_info', lazy='dynamic')

    def __repr__(self):
        return '<Animes>'

