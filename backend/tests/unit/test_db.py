import pytest

from api.models.plant import PlantModel
from api.models.user import UserModel
from api.models.description import DescriptionModel


def test_add_new_user_to_db(db_session, new_user):
    """
    GIVEN mocked db session, and user instance
    WHEN a new user added to db
    THEN check the user data from db
    """
    assert len(db_session.query(UserModel).all()) == 0

    new_user = UserModel(username=new_user['username'],
                         password=new_user['password'],
                         email=new_user['email'])

    db_session.add(new_user)

    user = db_session.query(UserModel).filter_by(username="TestUser").first()
    assert user.password == "testPass1!"
    assert user.email == "test@test.com"


def test_add_new_plant_to_db(db_session, new_plant):
    """
    GIVEN mocked db session, and plant instance
    WHEN a new plant added to db
    THEN check the plant data from db
    """
    assert len(db_session.query(PlantModel).all()) == 0

    new_plant = PlantModel(name=new_plant["name"],
                           latin=new_plant["latin"],
                           difficulty=new_plant["difficulty"],
                           user_id=1)

    db_session.add(new_plant)
    plant = db_session.query(PlantModel).filter_by(name="Monstera").first()
    assert plant.latin == "Monstera Adans."
    assert plant.difficulty == 5
    assert plant.user_id == 1


def test_add_new_desc_to_db(db_session, new_desc):
    """
    GIVEN mocked db session, and plant description
    WHEN a new description added to db
    THEN check the description data from db
    """
    assert len(db_session.query(DescriptionModel).all()) == 0

    new_desc = DescriptionModel(content=new_desc["content"],
                                source=new_desc["source"],
                                plant_id=1)

    db_session.add(new_desc)
    desc = db_session.query(DescriptionModel).filter_by(plant_id=1).first()
    assert desc.content == 'Description content'
    assert desc.source == 'wikipedia'
    assert desc.plant_id == 1
