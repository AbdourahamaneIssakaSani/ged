from flask import Blueprint

base_bp = Blueprint('base_bp', __name__, url_prefix='', template_folder='templates', static_folder='static')
