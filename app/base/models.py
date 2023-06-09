from app import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))