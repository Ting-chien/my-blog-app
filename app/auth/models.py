from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

from .. import db, login_manager


class Permission:
    """
    以二的次方作為權限值，可以幫助我們為每一種權限組合
    建立不重複的值，以便賦予角色的 permission。

    Ex: FOLLOW + COMMENT = 3
    """
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True) # 方便指定預設使用者權限的欄位
    permissions = db.Column(db.Integer, default=0)
    users = db.relationship('User', backref='role', lazy='dynamic')

    # def __init__(self, **kwargs):
    #     super(Role, self).__init__(**kwargs)
    #     if self.permissions is None:
    #         self.permissions = 0

    @staticmethod
    def insert_roles():
        """
        透過此靜態函數，可以在建立新環境時，快速建立起基本的角色配置，並且
        因為函數在建立角色時會去檢查是否已存在，因此日後角色有調整、擴充時
        也可以重複利用此函數來執行。
        """
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User' # 新用戶的預設角色為 User
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        """
        權限比對的關鍵函數，透過 AND(&&) 函數來檢查是否有
        某動作的權限。
        
        EX: 
            permission=FOLLOW+COMMENT => 3 (0011)
            perm=COMMENT => 2 (0010)
        
            0011 & 0010 = 0010 => 權限通過
        """
        return self.permissions & perm == perm

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

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # 讓一開始建立用戶時檢查email是否為admin帳戶，若是則給予 admin 權限，
        # 若不是則給予預設權限。
        if self.role is None:
            if self.email == current_app.config['ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

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
            data = s.loads(token, max_age=expiration)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self, perm):
        """
        方便使用者比對權限的函數
        """
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        """
        方便使用者檢查是否為 admin 的函數
        """
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return '<User %r>' % self.username
    

class AnonymousUser(AnonymousUserMixin):
    """
    為了方便建立一個 AnonymousUser 類別，來實作 flask-login
    裡的 anonymous_user 變數設定
    """
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

    
# call this function when login with a authorozed user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))