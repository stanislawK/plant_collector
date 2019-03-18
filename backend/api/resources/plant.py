from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from api.models.plant import PlantModel
from api.serializers.plant import plant_schema, plants_schema

CREATED_SUCCESFULLY = "New plant created successfully"
CHANGED_SUCCESFULLY = "Plant changed successfully"
PLANT_NOT_FOUND = "Plant not found"
DELETED = "Plant was deleted"


class Plant(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        user_id = get_jwt_identity()
        try:
            plant_data = plant_schema.load(request.get_json())
        except ValidationError as err:
            return {"message": err.messages}, 400

        new_plant = PlantModel(name=plant_data["name"],
                               latin=plant_data.get("latin"),
                               difficulty=plant_data.get("difficulty"),
                               user_id=user_id)

        new_plant.save_to_db()
        return {"message": CREATED_SUCCESFULLY, "plant_id": new_plant.id}, 201

    @classmethod
    @jwt_required
    def get(cls, plant_id):
        user_id = get_jwt_identity()
        plant = PlantModel.find_by_id(plant_id)

        if plant and plant.user_id == user_id:
            return plant_schema.dump(plant), 200
        return {"message": PLANT_NOT_FOUND}, 404

    @classmethod
    @jwt_required
    def put(cls, plant_id):
        user_id = get_jwt_identity()
        plant = PlantModel.find_by_id(plant_id)

        if plant and plant.user_id == user_id:
            try:
                plant_data = plant_schema.load(request.get_json(),
                                               partial=True)
            except ValidationError as err:
                return {"message": err.messages}, 400
            for key in plant_data.keys():
                print(key)
                setattr(plant, key, plant_data[key])

            plant.save_to_db()
            return {"message": CHANGED_SUCCESFULLY}, 201
        return {"message": PLANT_NOT_FOUND}, 404

    @classmethod
    @jwt_required
    def delete(cls, plant_id):
        user_id = get_jwt_identity()
        plant = PlantModel.find_by_id(plant_id)

        if plant and plant.user_id == user_id:
            plant.delete_from_db()
            return {"message": DELETED}, 200
        return {"message": PLANT_NOT_FOUND}, 404


class Plants(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        plants = PlantModel.find_all(user_id)
        if plants:
            return {"plants": plants_schema.dump(plants)}, 200
        return {"message": PLANT_NOT_FOUND}, 400
