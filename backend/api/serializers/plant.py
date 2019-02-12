from marshmallow import fields, Schema, validate


class PlantSchema(Schema):
    class Meta:
        fields = ('name', 'latin', 'user', 'difficulty')
        load_only = ('user',)

    name = fields.Str(required=True, validate=[validate.Length(max=50)])
    latin = fields.Str(validate=[validate.Length(max=50)])
    difficulty = fields.Int(validate=[validate.Range(min=0, max=10)])


plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)
