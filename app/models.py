from app import db
from app import bcrypt


class User(db.Model):
    id = db.Column('id_user', db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(255))

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
        self.password_hash = bcrypt.generate_password_hash(plain_text_pwd).decode('utf-8')

    def email_is_unique(self, email):
        user = User.query.filter_by(email=email).first()
        print(email, user)
        if user:
            return False
        return True


''''class Account(db.Model):
    id = db.Column('id_account', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(255))
'''
