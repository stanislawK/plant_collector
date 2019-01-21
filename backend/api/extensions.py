from flask_migrate import Migrate
from flask_restful import Api as FlaskApi
from flask_sqlalchemy import SQLAlchemy


"""Create the instances of the Flask extensions in the global scope"""

db = SQLAlchemy()
migrate = Migrate()
flask_api = FlaskApi()
