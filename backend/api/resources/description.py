from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from api.models.description import DescriptionModel
from api.models.plant import PlantModel
from api.resources.plant import PLANT_NOT_FOUND
from api.serializers.description import desc_schema

CREATED_SUCCESFULLY = "New description created successfully"
DESC_CHANGED = "Description changed successfully"
DESC_DELETED = "Description deleted successfully"
DESC_NOT_FOUND = "Description was not found"


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
            return {"message": CREATED_SUCCESFULLY,
                    "desc_id": new_desc.id}, 201
        return {"message": PLANT_NOT_FOUND}, 404

    @classmethod
    @jwt_required
    def put(cls, plant_id, desc_id):
        user_id = get_jwt_identity()
        desc = DescriptionModel.find_by_id(desc_id)
        plant = PlantModel.find_by_id(plant_id)

        if desc and plant.user_id == user_id and desc.plant_id == plant_id:
            try:
                desc_data = desc_schema.load(request.get_json())
            except ValidationError as err:
                return {"message": err.messages}, 400

            desc.source = desc_data.get('source')
            desc.content = desc_data['content']

            desc.save_to_db()
            return {"message": DESC_CHANGED}, 200
        return {"message": DESC_NOT_FOUND}, 404

    @classmethod
    @jwt_required
    def delete(cls, plant_id, desc_id):
        user_id = get_jwt_identity()
        desc = DescriptionModel.find_by_id(desc_id)
        plant = PlantModel.find_by_id(plant_id)

        if desc and plant.user_id == user_id and desc.plant_id == plant_id:
            desc.delete_from_db()
            return {"message": DESC_DELETED}, 200
        return {"message": DESC_NOT_FOUND}, 404
