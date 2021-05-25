from flask import Blueprint, render_template

from app.auth.forms import LoginForm

base_bp = Blueprint('base_bp', __name__, template_folder='templates', static_folder='static')


@base_bp.route('/', methods=['GET', 'POST'])
def base():
    login_form = LoginForm()
    return render_template('welcome.html', title='Welcome', form=login_form)
