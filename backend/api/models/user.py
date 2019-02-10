from flask import request, url_for
from flask_mail import Message

from api.extensions import db, mail
from api.models.confirmation import ConfirmationModel
from api.models.plant import PlantModel


SUBJECT = "Potwierdzenie rejestracji w plant_collector"
BODY = "Wejdź w poniższy link aby potwierdzić rejestrację {}"


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    plants = db.relationship(
        "PlantModel", lazy=True, cascade="all, delete-orphan"
    )

    @property
    def most_recent_confirmation(self):
        expire_desc = db.desc(ConfirmationModel.expire_at)
        return self.confirmation.order_by(expire_desc).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for(
            'confirmation', confirmation_id=self.most_recent_confirmation.id
        )
        msg = Message(
            subject=SUBJECT,
            sender=("plant", "plant@test.com"),
            recipients=[self.email]
        )
        msg.body = BODY.format(link)

        with mail.record_messages() as outbox:
            mail.send(msg)
        print(outbox[0], flush=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
