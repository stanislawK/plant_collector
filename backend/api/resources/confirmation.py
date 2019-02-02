from time import time

from flask_restful import Resource

from api.models.confirmation import ConfirmationModel
from api.models.user import UserModel
from api.serializers.confirmation import conf_schema


NOT_FOUND = "Confirmation reference not found."
EXPIRED = "Confirmation link has expired"
ALREADY_CONFIRMED = "Registration has already been confirmed"
SUCCESFULLY_CONFIRMED = "Registration successfully confirmed"


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": NOT_FOUND}, 404

        if confirmation.expired():
            return {"message": EXPIRED}, 400

        if confirmation.confirmed:
            return {"message": ALREADY_CONFIRMED}

        confirmation.confirmed = True
        confirmation.save_to_db()

        return {"message": SUCCESFULLY_CONFIRMED}, 200
