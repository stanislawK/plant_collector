from flask import Flask
from flask_cors import CORS
from flask_uploads import configure_uploads, patch_request_class

from api.extensions import db, jwt, flask_api, mail, migrate
from api.models.blacklist import RevokedTokenModel
from api.models.image import IMAGE_SET
from api.resources.confirmation import Confirmation
from api.resources.description import Description
from api.resources.image import ImageUpload, Image
from api.resources.plant import Plant, Plants
from api.resources.user import (
    TokenRefresh,
    User,
    UserLogin,
    UserLogoutAccess,
    UserLogoutRefresh,
    UserRegister,
)


def create_app(test_config=None):
    """Application factory function"""
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object('api.config.DevelopmentConfig')
    else:
        app.config.update(test_config)

    initialize_extensions(app)
    CORS(app)
    patch_request_class(app, 10 * 1024 * 1024)
    configure_uploads(app, IMAGE_SET)

    return app


def initialize_extensions(app):
    """Helper functions"""
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    migrate.init_app(app, db, directory='api/migrations')
    jwt.init_app(app)
    mail.init_app(app)
    flask_api.init_app(app)


"""Adding Resources"""
flask_api.add_resource(UserRegister, "/register")
flask_api.add_resource(Confirmation, "/confirmation/<string:confirmation_id>")
flask_api.add_resource(UserLogin, "/login")
flask_api.add_resource(UserLogoutAccess, "/logout/access")
flask_api.add_resource(UserLogoutRefresh, "/logout/refresh")
flask_api.add_resource(User, "/user")
flask_api.add_resource(TokenRefresh, "/refresh")
flask_api.add_resource(Plant, "/plant", "/plant/<int:plant_id>")
flask_api.add_resource(Plants, "/plants")
flask_api.add_resource(Description, "/plant/<int:plant_id>/description",
                       "/plant/<int:plant_id>/description/<int:desc_id>")
flask_api.add_resource(ImageUpload, "/plant/<int:plant_id>/upload/image")
flask_api.add_resource(Image, "/plant/<int:plant_id>/image")


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """Checking if a token is blacklisted"""
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)
