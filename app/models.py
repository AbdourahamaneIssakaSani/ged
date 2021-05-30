from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column('id_user', db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(256))

    def __init__(self, f_name, l_name, email, pwd):
        self.first_name = f_name
        self.last_name = l_name
        self.email = email
        self.password_hash = pwd

    """"@property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_pwd):
        self.password_hash = bcrypt.generate_password_hash(plain_text_pwd).decode('utf-8')

    @property
    def verify_password(self, provided_password):
        return check_password_hash(self.password, provided_password)"""


''''class Account(db.Model):
    id = db.Column('id_account', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(255))
'''
