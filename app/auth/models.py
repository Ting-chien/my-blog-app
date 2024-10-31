from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

from .. import db, login_manager


class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_confirmation_token(self):
        """
        透過 itsdangeorous 套件的 URLSafeTimedSerializer 函數
        來生成一個具有時效性的 token，提供用戶驗證。
        """
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({"confirm": self.id})
    
    def confirm(self, token, expiration=3600):
        """
        用戶點擊確認連結後，會回透驗證此 token 是否正確。

        :param token: User confirm token
        :param expiration: Confim time limitation
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'), max_age=expiration)
        except:
            return False
        print(data.get("confirm"))
        if data.get('confirm') != self.id:
            print("Not confirmed")
            return False
        print("Confirmed")
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username
    
# call this function when login with a authorozed user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))