from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "fincrypt.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "This is some secret data"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fincrypt.db"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Cards

    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app


def create_db(app):
    if path.exists("fincrypt/" + DB_NAME):
        db.create_all(app=app)
