from uuid import uuid4
from flask_uploads import UploadSet, IMAGES

from api.extensions import db

IMAGE_SET = UploadSet("images", IMAGES)
UPLOAD_PATH = '/plantc/backend/static/images/{}/{}'


class ImageModel(db.Model):
    ___tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ext_url = db.Column(db.String(50))
    plant_id = db.Column(db.Integer,
                         db.ForeignKey('plants.id'),
                         nullable=False)
    plant = db.relationship("PlantModel")

    def __init__(self, plant_id, format, ext_url=None, **kwargs):
        super().__init__(**kwargs)
        self.name = uuid4().hex + format
        self.plant_id = plant_id
        self.ext_url = ext_url

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_image(self, image):
        """Takes FileStorage and saves it to a folder"""
        folder = 'plant_{}'.format(self.plant_id)
        name = self.name
        return IMAGE_SET.save(image, folder=folder, name=name)

    def get_path(self):
        """Take image name and folder and return full path"""
        folder = 'plant_{}'.format(self.plant_id)
        name = self.name
        return UPLOAD_PATH.format(folder, name)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
