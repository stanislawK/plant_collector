from marshmallow import fields, Schema, validate, pre_dump

from api.models.user import UserModel

STRENGTH_ERROR = "Uppercase, lowercase, digit and special symbol required"

class UserSchema(Schema):
    class Meta:
        fields = ('username', 'password', 'email')

    strength = ("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])"
                "(?=.*[!@#$%^&*()\-_+<,>.?/~`]).{8,}$")
    username = fields.Str(required=True, validate=[validate.Length(max=50)])
    password = fields.Str(required=True,
                          validate=[validate.Regexp(strength,
                                    error=STRENGTH_ERROR)],
                          load_only=True)
    email = fields.Email(required=True, validate=[validate.Length(max=50)])

    @pre_dump
    def _pre_dump(self, user: UserModel):
        user.confirmation = [user.most_recent_confirmation]
        return user


user_schema = UserSchema()
