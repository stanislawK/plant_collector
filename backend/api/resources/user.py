from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidatronError

from api.models.user import UserModel
from api.serializers.user import user_schema

"""Messages"""
CREATED_SUCCESFULLY = "User created successfully"
USER_ALREADY_EXIST = "User with that {} already exist"
FAILED_TO_CREATE = "Error when trying to register new user"


class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            user_data = user_schema.load(request.get_json())
        except ValidatronError as err:
            return jsonify(err.messages), 400

        new_user = UserModel(username=user_data['username'],
                             password=user_data['password'],
                             email=user_data['email'])

        if UserModel.find_by_username(new_user.username):
            return {"message": USER_ALREADY_EXIST.format('username')}, 400
        if UserModel.find_by_email(new_user.email):
            return {"message": USER_ALREADY_EXIST.format('email')}, 400

        new_user.save_to_db()
        return {"message": CREATED_SUCCESFULLY}, 201
