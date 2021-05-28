from flask import Blueprint, render_template

from app.auth.forms import CreateAccountForm, LoginForm

base_bp = Blueprint('base_bp', __name__, template_folder='templates', static_folder='static')


@base_bp.route('/', methods=['GET', 'POST'])
def base():
    register_form = CreateAccountForm()
    login_form = LoginForm()
    return render_template('welcome.html', title='Welcome', register_form=register_form, login_form=login_form)
