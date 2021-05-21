from flask import render_template
from app.auth import auth_bp
from .forms import LoginForm, CreateAccountForm


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    return render_template('login.html', form=login_form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = CreateAccountForm()
    return render_template('register.html', form=reg_form)
