from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from marshmallow import ValidationError

from api.helpers.image import get_extension
from api.models.image import ImageModel
from api.models.plant import PlantModel
from api.serializers.image import img_schema
from api.resources.plant import PLANT_NOT_FOUND


IMAGE_UPLOADED = "Image was successfully uploaded"
ILLEGAL_EXT = "This file is not allowed"


class ImageUpload(Resource):
    @classmethod
    @jwt_required
    def post(cls, plant_id):
        user_id = get_jwt_identity()
        plant = PlantModel.find_by_id(plant_id)

        if plant and plant.user_id == user_id:
            try:
                img_data = img_schema.load(request.files)
            except ValidationError as err:
                return {"message": err.messages}, 400

            format = get_extension(img_data["image"])
            new_img = ImageModel(plant_id=plant_id, format=format)
            new_img.save_to_db()
            try:
                new_img.save_image(img_data["image"])
                return {"message": IMAGE_UPLOADED}, 201
            except UploadNotAllowed:
                return {"message": ILLEGAL_EXT + format + new_img.name}, 400
        return {"message": PLANT_NOT_FOUND}, 404
