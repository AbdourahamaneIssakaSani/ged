from flask import Flask
from flask_bootstrap import Bootstrap
from flask_assets import Environment


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    Bootstrap(app)
    assets = Environment()
    assets.init_app(app)
    with app.app_context():
        from app.auth.auth import auth_bp
        from app.base.base import base_bp
        from .assets import compile_assets
        app.register_blueprint(auth_bp)
        app.register_blueprint(base_bp)
        compile_assets(assets)

        return app
