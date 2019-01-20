from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

"""Create the instances of the Flask extensions in the global scope"""

db = SQLAlchemy()
migrate = Migrate()


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
