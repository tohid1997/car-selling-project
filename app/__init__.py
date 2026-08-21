from flask import Flask

from .config import Config
from .routes.auth import auth_bp
from .routes.main import main_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app