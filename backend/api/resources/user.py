from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_refresh_token_required,
    jwt_required,
)
from flask_restful import Resource
from marshmallow import ValidationError
from passlib.hash import pbkdf2_sha256

from api.models.blacklist import RevokedTokenModel
from api.models.confirmation import ConfirmationModel
from api.models.user import UserModel
from api.serializers.user import user_schema


import pdb

"""Messages"""
CREATED_SUCCESFULLY = "Confirmation email was sent"
USER_ALREADY_EXIST = "User with that {} already exist"
FAILED_TO_CREATE = "Error when trying to register new user"
NOT_CONFIRMED = "Registration wasn't comifired"
INVALID_CREDENTIALS = "Invalid credentials"
REVOKE_ACCESS = "Access token has been revoked."
REVOKE_REFRESH = "Refresh token has been revoked."


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        user = user_schema.dump(UserModel.find_by_id(user_id))
        return {"user": user}, 200


class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            return {"message": err.messages}, 400

        hashed = pbkdf2_sha256.hash(user_data['password'])
        new_user = UserModel(username=user_data['username'],
                             password=hashed,
                             email=user_data['email'])

        if UserModel.find_by_username(new_user.username):
            return {"message": USER_ALREADY_EXIST.format('username')}, 400
        if UserModel.find_by_email(new_user.email):
            return {"message": USER_ALREADY_EXIST.format('email')}, 400

        new_user.save_to_db()
        confirmation = ConfirmationModel(new_user.id)
        confirmation.save_to_db()
        new_user.send_confirmation_email()
        return {"message": CREATED_SUCCESFULLY}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        try:
            user_data = user_schema.load(request.get_json(),
                                         partial=('email',))
        except ValidationError as err:
            return {"message": err.messages}, 400
        username = user_data["username"]
        password = user_data["password"]
        user = UserModel.find_by_username(username)
        if user and pbkdf2_sha256.verify(password, user.password):
            conf = user.most_recent_confirmation
            if conf and conf.confirmed:
                token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": token,
                        "refresh_token": refresh_token}, 200
            return {"message": NOT_CONFIRMED}, 400
        return {"message": INVALID_CREDENTIALS}, 401


class UserLogoutAccess(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return {"message": REVOKE_ACCESS}, 200


class UserLogoutRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return {"message": REVOKE_REFRESH}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
