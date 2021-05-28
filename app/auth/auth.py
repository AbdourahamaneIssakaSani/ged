import binascii
import hashlib
import os

from flask import render_template, redirect, url_for, flash
from app.auth import auth_bp
from .forms import LoginForm, CreateAccountForm
from .. import db
from ..models import User


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    password_hash = hashlib.pbkdf2_hmac(
        'sha512',
        password.encode('utf-8'),
        salt,
        100000
    )
    password_hash = binascii.hexlify(password_hash)
    return (salt + password_hash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    password_hash = hashlib.pbkdf2_hmac(
        'sha512',
        provided_password.encode('utf-8'),
        salt.encode('ascii'),
        100000
    )
    password_hash = binascii.hexlify(password_hash).decode('ascii')
    return password_hash == stored_password


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data)
        if user and verify_password(user.password_hash, login_form.password):
            redirect('welcome.html')
    return render_template('login.html', title='Se connecter', login_form=login_form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = CreateAccountForm()
    print(4)
    if register_form.is_submitted():
        print(4)
        if User.email_is_unique(email=register_form.email.data):
            new_user = User(
                f_name=register_form.first_name.data,
                l_name=register_form.last_name.data,
                email=register_form.email.data,
                pwd=register_form.password.data
            )
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('aut_bp.login'))
        else:
            flash('Cette adresse email existe déjà !')
    # if register_form.errors !={}:

    return render_template('register.html', title='Créer un compte', register_form=register_form)
