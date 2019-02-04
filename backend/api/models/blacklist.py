from api.extensions import db


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    @classmethod
    def is_jti_blacklisted(cls, jti):
        revoked = cls.query.filter_by(jti=jti).first()
        return bool(revoked)

    def add(self):
        db.session.add(self)
        db.session.commit()
