from marshmallow import fields, Schema


class ConfirmaionSchema(Schema):
    class Meta:
        fileds = ('id', 'user', 'expire_at', 'confirmed')
        load_only = ("user")
        dump_only = ('id', 'expire_at', 'confirmed')


conf_schema = ConfirmaionSchema()
