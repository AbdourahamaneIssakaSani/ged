from flask import Blueprint, render_template

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth', template_folder='templates', static_folder='static')
