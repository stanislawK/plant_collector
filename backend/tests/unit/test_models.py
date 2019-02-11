import pytest

from api.models.plant import PlantModel
from api.models.user import UserModel


def test_user_model(new_user):
    """
    GIVEN a User Model
    WHEN a new User is created
    THEN check user data
    """
    new_user = UserModel(username=new_user['username'],
                         password=new_user['password'],
                         email=new_user['email'])

    assert new_user.username == 'TestUser'
    assert new_user.password == 'testPass1!'
    assert new_user.email == "test@test.com"


def test_plant_model(new_plant):
    """
    GIVEN a Plant Model
    WHEN a new Plant is created
    THEN check plant data
    """
    plant = PlantModel(name=new_plant["name"],
                       latin=new_plant["latin"],
                       difficulty=new_plant["difficulty"])

    assert plant.name == "Monstera"
    assert plant.latin == "Monstera Adans."
    assert plant.difficulty == 5
