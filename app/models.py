from app import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.dialects import mysql


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
    messages = db.relationship('Message')

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

    def create_sharing_space(self):
        pass

    def add_user_in_sharing_space(self):
        pass

    def view_space_activity(self):
        pass

    def validate_suppression_in_space(self):
        pass

    def archive_sharing_space(self):
        pass


class Object(db.Model):
    __abstract__ = True
    name = db.Column(db.String(256))
    path = db.Column(db.String(256))
    size = db.Column(db.Integer)
    description = db.Column(mysql.LONGTEXT)
    creation_date = db.Column(db.DateTime)


class File(Object):
    id = db.Column('id_file', db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50))
    folder = db.Column(db.Integer, db.ForeignKey('folder.id_folder'), nullable=True)
    owner = db.Column(db.Integer, db.ForeignKey(column='user.id_user', name='fk_file_folder'))


class Folder(Object):
    id = db.Column('id_folder', db.Integer, primary_key=True, autoincrement=True)
    files = db.relationship('File')
    parent_folder = db.Column(db.Integer, db.ForeignKey(column='folder.id_folder', name='fk_folder_parent'),
                              nullable=True)


class Message(db.Model):
    id = db.Column('id_message', db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(mysql.LONGTEXT)
    space = db.Column(db.Integer, db.ForeignKey(column='space.id_space', name='fk_msg_space'))
    sender = db.Column(db.Integer, db.ForeignKey(column='user.id_user', name='fk_msg_user'))


class SharingSpace(db.Model):
    __tablename__ = 'space'
    id = db.Column('id_space', db.Integer, primary_key=True, autoincrement=True)
    members = db.Column(db.JSON, default=None)
    data_shared = db.Column(db.JSON)
    files = db.Column(db.JSON)
    messages = db.relationship('Message')
    archive = db.relationship('Archive')


class Archive(db.Model):
    id = db.Column('id_archive', db.Integer, primary_key=True, autoincrement=True)
    archive_date = db.Column(db.DateTime)
    space_archived = db.Column(db.Integer, db.ForeignKey(column='space.id_space', name='fk_archive_space'),
                               nullable=True)
