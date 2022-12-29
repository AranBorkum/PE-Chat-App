from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.user import User

DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres"


def create_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config["SECRET_KEY"] = "secret_key"

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        with Session(create_engine(DB_URI)) as sql_session:
            return sql_session.query(User).filter(User.id == user_id).first()

    with app.app_context():
        from .views import view

        app.register_blueprint(view, url_prefix="/")

        return app