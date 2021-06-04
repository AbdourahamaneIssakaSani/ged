from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user

from app.auth import auth_bp
from .forms import LoginForm, RegisterForm
from .utils import email_is_unique
from .. import db
from ..models import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    login_error_message = None
    if login_form.validate_on_submit():
        """validate_on_submit will check if it is a POST request and if it is valid"""
        auth_ok = False
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None:
            auth_ok = user.verify_password(login_form.password.data)
        if auth_ok:
            login_user(user, remember=login_form.remember_me)
            return redirect(url_for('user_bp.dashboard'))
        else:
            login_error_message = 'Échec de connexion : vérifiez votre email ou mot de passe'
            return render_template('login.html', title='Se connecter', login_form=login_form,
                                   login_error_message=login_error_message)
    else:
        return render_template('login.html', title='Se connecter', login_form=login_form,
                               login_error_message=login_error_message)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        if email_is_unique(email=register_form.email.data):
            new_user = User(
                f_name=register_form.first_name.data,
                l_name=register_form.last_name.data,
                email=register_form.email.data,
                pwd=register_form.password_confirm.data
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth_bp.login'))
        else:
            flash('Cette adresse email existe déjà !', category='warning')
    else:
        return render_template('register.html', title='Créer un compte', register_form=register_form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
