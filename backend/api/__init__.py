from flask import Flask

from api.extensions import db, flask_api, migrate
from api.resources.user import UserRegister



"""Application factory function"""

def create_app():
    app = Flask(__name__)
    app.config.from_object('api.config.DevelopmentConfig')

    initialize_extensions(app)
    return app


"""Helper functions"""

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    migrate.init_app(app, db, directory='api/migrations')
    flask_api.init_app(app)

"""Adding Resources"""
flask_api.add_resource(UserRegister, "/register")
