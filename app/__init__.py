from flask import Flask
from flask_bootstrap import Bootstrap
from flask_assets import Environment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def manage_database(app):
    @app.before_first_request
    def initialize():
        db.init_app(app)
        db.create_all()

    ''''@app.teardown_request
    def shutdown():
        db.session.remove()'''


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    Bootstrap(app)
    manage_database(app)
    login_manager.init_app(app)
    assets = Environment()
    assets.init_app(app)
    with app.app_context():
        from app.auth.auth import auth_bp
        from app.base.base import base_bp
        from app.user.routes import user_bp
        from .assets import compile_assets
        app.register_blueprint(auth_bp)
        app.register_blueprint(base_bp)
        app.register_blueprint(user_bp)
        compile_assets(assets)

        return app
