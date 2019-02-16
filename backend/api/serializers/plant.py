from marshmallow import fields, Schema, validate

from api.serializers.description import DescriptionSchema


class PlantSchema(Schema):
    class Meta:
        fields = ('name', 'latin', 'user', 'difficulty', 'descriptions')
        load_only = ('user',)
        dump_only = ('descriptions',)

    name = fields.Str(required=True, validate=[validate.Length(max=50)])
    latin = fields.Str(validate=[validate.Length(max=50)])
    difficulty = fields.Int(validate=[validate.Range(min=0, max=10)])
    descriptions = fields.Nested(DescriptionSchema, many=True)


plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)
