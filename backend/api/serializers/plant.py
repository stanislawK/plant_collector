from marshmallow import fields, Schema, validate

from api.serializers.description import DescriptionSchema
from api.serializers.image import ImageModelSchema


class PlantSchema(Schema):
    class Meta:
        fields = ('name',
                  'latin',
                  'user',
                  'difficulty',
                  'descriptions',
                  'images',
                  'id')
        load_only = ('user',)
        dump_only = ('descriptions', 'id', 'images')

    id = fields.Int()
    name = fields.Str(required=True, validate=[validate.Length(max=50)])
    latin = fields.Str(validate=[validate.Length(max=50)])
    difficulty = fields.Int(validate=[validate.Range(min=0, max=10)])
    descriptions = fields.Nested(DescriptionSchema, many=True)
    images = fields.Nested(ImageModelSchema, many=True)


plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)
