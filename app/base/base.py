from flask import Blueprint, render_template

base_bp = Blueprint('base_bp', __name__, template_folder='templates', static_folder='static')


@base_bp.route('/', methods=['GET', 'POST'])
def base():
    return render_template('layout.html')
