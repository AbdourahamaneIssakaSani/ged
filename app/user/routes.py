from flask import render_template
from flask_login import login_required

from app.user import user_bp


@user_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', title='Tableau de bord')
