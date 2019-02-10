from api.extensions import db


class DescriptionModel(db.Model):
    __tablename__ = 'descriptions'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(50))
    plant_id = db.Column(db.Integer,
                         db.ForeignKey('plants.id'),
                         nullable=False)
    plant = db.relationship("PlantModel")

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
