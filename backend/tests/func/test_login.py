import pytest


from api.models.confirmation import ConfirmationModel


def test_login_with_valid_user(client, new_user, registred_user):
    """
    GIVEN registred user and app instnce
    WHEN login with valid user data
    THEN check if jwt and refresh token are in response
    """
    rv = client.post('/login', json={
                                    'username': new_user['username'],
                                    'password': new_user['password']
                                    })
    response = rv.get_json()
    assert rv.status == '200 OK'
    assert response['access_token']
    assert response['refresh_token']


def test_login_with_invalid_password(client, new_user, registred_user):
    """
    GIVEN registred user and app instnce
    WHEN trying to login with wrong password
    THEN check if proper error was raised with 401 status code
    """
    rv = client.post('/login', json={'username': new_user['username'],
                                     'password': 'WrongPassword1!'
                                     })
    response = rv.get_json()
    assert rv.status == '401 UNAUTHORIZED'
    assert response['message'] == 'Invalid credentials'


def test_login_unregistered_user(client, new_user):
    """
    GIVEN user data and app instnce
    WHEN trying to login unregistered user
    THEN check if proper error was raised with 401 status code
    """
    rv = client.post('/login', json={
                                    'username': new_user['username'],
                                    'password': new_user['password']
                                    })
    response = rv.get_json()
    assert rv.status == '401 UNAUTHORIZED'
    assert response['message'] == 'Invalid credentials'


def test_login_unconfirmed_user(client, new_user):
    """
    GIVEN registered but unconfirmed user and app instnce
    WHEN trying to login unconfirmed user
    THEN check if proper error was raised with 400 status code
    """
    register = client.post('/register', json=new_user)
    rv = client.post('/login', json={
                                    'username': new_user['username'],
                                    'password': new_user['password']
                                    })
    response = rv.get_json()
    assert rv.status == '400 BAD REQUEST'
    assert response['message'] == "Registration wasn't comifired"
