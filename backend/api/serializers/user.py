from marshmallow import fields, Schema, validate


class UserSchema(Schema):
    class Meta:
        fields = ('username', 'password', 'email')

    username = fields.Str(required=True, validate=[validate.Length(max=50)])
    password = fields.Str(required=True, load_only=True)
    email = fields.Email(required=True, validate=[validate.Length(max=50)])


user_schema = UserSchema()
