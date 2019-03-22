from marshmallow import fields, Schema, validate


class DescriptionSchema(Schema):
    class Meta:
        fields = ('plant', 'content', 'source', 'id')
        load_only = ('plant',)
        dump_only = ('id', )

    id = fields.Int()
    content = fields.Str(required=True, validete=[validate.Length(max=2000)])
    source = fields.Str(validate=[validate.Length(max=50)])


desc_schema = DescriptionSchema()
