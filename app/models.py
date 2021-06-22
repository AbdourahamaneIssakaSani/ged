import datetime
from app import db, login_manager, bcrypt
from flask_login import UserMixin, current_user
from sqlalchemy.dialects import mysql


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column('id_user', db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(320), unique=True)
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
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    is_deleted = db.Column(db.Integer, default=int(0))
    delete_date = db.Column(db.DateTime)
    is_shared = db.Column(db.Integer, default=0)


class File(Object):
    id = db.Column('id_file', db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50))
    folder = db.Column(db.Integer, db.ForeignKey('folder.id_folder'), nullable=True)
    owner = db.Column(db.Integer, db.ForeignKey(column='user.id_user', name='fk_file_folder'))


class Folder(Object):
    id = db.Column('id_folder', db.Integer, primary_key=True, autoincrement=True)
    files = db.relationship('File')
    folders = db.relationship('Folder')
    parent_folder = db.Column(db.Integer, db.ForeignKey(column='folder.id_folder', name='fk_folder_parent'),
                              nullable=True)
    owner = db.Column(db.Integer, nullable=False)


class Message(db.Model):
    id = db.Column('id_message', db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(mysql.LONGTEXT)
    space = db.Column(db.Integer, db.ForeignKey(column='space.id_space', name='fk_msg_space'))
    sender = db.Column(db.Integer, db.ForeignKey(column='user.id_user', name='fk_msg_user'))


class SharingSpace(db.Model):
    __tablename__ = 'space'
    id = db.Column('id_space', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    admin = db.Column(db.Integer, nullable=False)
    is_archived = db.Column(db.Integer, default=0)
    members = db.relationship('Members')
    folders = db.relationship('SpaceFolders')
    files = db.relationship('SpaceFiles')
    messages = db.relationship('Message')
    archive = db.relationship('Archive')


class Archive(db.Model):
    id = db.Column('id_archive', db.Integer, primary_key=True, autoincrement=True)
    archive_date = db.Column(db.DateTime)
    space_archived = db.Column(db.Integer, db.ForeignKey(column='space.id_space', name='fk_archive_space'),
                               nullable=True)


class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(320))
    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    date_revoked = db.Column(db.DateTime)
    space = db.Column(db.Integer, db.ForeignKey(column='space.id_space', name='fk_members_space'))


class SpaceFiles(db.Model):
    __tablename__ = 'spacefiles'
    file = db.Column(db.Integer, primary_key=True, autoincrement=False)
    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    date_revoked = db.Column(db.DateTime)
    space = db.Column(db.Integer, db.ForeignKey(column='space.id_space', name='fk_files_space'))


class SpaceFolders(db.Model):
    __tablename__ = 'spacefolders'
    folder = db.Column(db.Integer, primary_key=True, autoincrement=False)
    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    date_revoked = db.Column(db.DateTime)
    space = db.Column(db.Integer, db.ForeignKey(column='space.id_space', name='fk_folders_space'))
