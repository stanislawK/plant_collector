from api.extensions import db
from api.models.description import DescriptionModel
from api.models.images import ImageModel


class PlantModel(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    latin = db.Column(db.String(50))
    difficulty = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    descriptions = db.relationship(
        "DescriptionModel", lazy=True, cascade="all, delete-orphan"
    )
    images = db.relationship(
        "ImageModel", lazy=True, cascade="all, delete-orphan"
    )

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
