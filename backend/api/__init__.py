from flask import Flask
from flask_cors import CORS

from api.extensions import db, flask_api, mail, migrate
from api.resources.user import UserRegister
from api.resources.confirmation import Confirmation


def create_app(test_config=None):
    """Application factory function"""
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object('api.config.DevelopmentConfig')
    else:
        app.config.update(test_config)

    initialize_extensions(app)
    CORS(app)

    return app


def initialize_extensions(app):
    """Helper functions"""
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    migrate.init_app(app, db, directory='api/migrations')
    mail.init_app(app)
    flask_api.init_app(app)


"""Adding Resources"""
flask_api.add_resource(UserRegister, "/register")
flask_api.add_resource(Confirmation, "/confirmation/<string:confirmation_id>")
