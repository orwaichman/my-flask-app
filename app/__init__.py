from flask import Flask
from flask_login import LoginManager

from config import config
from db import Session
from db.models import User

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'


@login_manager.user_loader
def load_user(user_id):
    return Session.query(User).filter_by(id=user_id).first()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        Session.remove()

    return app
