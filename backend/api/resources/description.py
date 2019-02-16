from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from api.models.description import DescriptionModel
from api.models.plant import PlantModel
from api.resources.plant import PLANT_NOT_FOUND
from api.serializers.description import desc_schema

CREATED_SUCCESFULLY = "New description created successfully"


class Description(Resource):
    @classmethod
    @jwt_required
    def post(cls, plant_id):
        user_id = get_jwt_identity()
        plant = PlantModel.find_by_id(plant_id)

        if plant and plant.user_id == user_id:
            try:
                desc_data = desc_schema.load(request.get_json())
            except ValidationError as err:
                return {"message": err.messages}, 400

            new_desc = DescriptionModel(content=desc_data["content"],
                                        source=desc_data.get('source'),
                                        plant_id=plant_id)

            new_desc.save_to_db()
            return {"message": CREATED_SUCCESFULLY}, 201
        return {"message": PLANT_NOT_FOUND}, 404
