from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from flask_restful import Resource
from marshmallow import ValidationError
from passlib.hash import pbkdf2_sha256

from api.models.user import UserModel
from api.models.confirmation import ConfirmationModel
from api.serializers.user import user_schema


import pdb

"""Messages"""
CREATED_SUCCESFULLY = "Confirmation email was sent"
USER_ALREADY_EXIST = "User with that {} already exist"
FAILED_TO_CREATE = "Error when trying to register new user"
NOT_CONFIRMED = "Registration wasn't comifired"
INVALID_CREDENTIALS = "Invalid credentials"


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
