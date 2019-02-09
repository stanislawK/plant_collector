import pytest

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
