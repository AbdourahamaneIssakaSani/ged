from app import db, login_manager, bcrypt
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
    files = db.relationship('File')

    def __init__(self, f_name, l_name, email, pwd):
        self.first_name = f_name
        self.last_name = l_name
        self.email = email
        self.password = pwd

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_pwd):
        self.password_hash = bcrypt.generate_password_hash(plain_text_pwd)

    def verify_password(self, provided_password):
        return bcrypt.check_password_hash(self.password_hash, provided_password)


class File(db.Model):
    id = db.Column('id_file', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    data = db.Column(db.String(256))
    size = db.Column(db.Integer)
    description = db.Column(db.TEXT)
    date_creation = db.Column(db.DateTime)
    owner = db.Column(db.Integer, db.ForeignKey('user.id_user'))


''''class Account(db.Model):
    id = db.Column('id_account', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(255))
'''
