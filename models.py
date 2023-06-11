from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, generate_password_hash

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):

    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    posts = db.relationship('Feedback', cascade="delete", backref='user')

    @classmethod
    def register(cls, username, password):
        scrambled = bcrypt.generate_password_hash(password).decode("utf8")

        return scrambled
    
    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

def connect_db(app):

    db.app = app
    db.init_app(app)

class Feedback(db.Model):

    __tablename__="posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String(50), db.ForeignKey('users.username'), nullable=False)