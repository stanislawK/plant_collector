import pytest

from api.models.user import UserModel


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
