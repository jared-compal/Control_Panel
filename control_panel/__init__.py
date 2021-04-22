from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from control_panel.config import Config
from flask_mongoengine import MongoEngine

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
mongo_db = MongoEngine()


def create_app():
    config_class = Config
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mongo_db.init_app(app)

    from control_panel.main.route import main
    from control_panel.auth.auth_service import auth_service
    app.register_blueprint(main)
    app.register_blueprint(auth_service)

    return app
