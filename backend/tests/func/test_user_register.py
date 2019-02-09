import pytest


def test_register_valid_user(client, new_user):
    """
    GIVEN test client and valid user data
    WHEN post request sent to register endpoint
    THEN check status 201 and response message
    """
    rv = client.post('/register', json=new_user)
    response = rv.get_json()
    assert rv.status == '201 CREATED'
    assert response['message'] == 'Confirmation email was sent'


def test_register__user_two_times(client, new_user):
    """
    GIVEN test client and valid user data
    WHEN post request sent to register endpoint two times with these same user
    THEN check status 400 and error message
    """
    rv = client.post('/register', json=new_user)
    response = rv.get_json()
    assert rv.status == '201 CREATED'

    rv = client.post('/register', json=new_user)
    response = rv.get_json()
    assert rv.status == '400 BAD REQUEST'
    assert response['message'] == 'User with that username already exist'


def test_register_with_invalid_email(client, new_user):
    """
    GIVEN test client and user with invalid email, and without
    WHEN post request sent to register endpoint
    THEN check status and response
    """
    new_user['email'] = 'wrong_email'
    rv = client.post('/register', json=new_user)
    response = rv.get_json()['message']['email'][0]
    assert rv.status == '400 BAD REQUEST'
    assert response == 'Not a valid email address.'

    del new_user['email']
    rv = client.post('/register', json=new_user)
    response = rv.get_json()['message']['email'][0]
    assert rv.status == '400 BAD REQUEST'
    assert response == 'Missing data for required field.'


def test_register_with_weak_password(client, new_user):
    """
    GIVEN test client and user with weak password
    WHEN post request sent to register endpoint
    THEN check status and response
    """
    new_user['password'] = 'weak_password'
    rv = client.post('/register', json=new_user)
    res = rv.get_json()['message']['password'][0]
    assert rv.status == '400 BAD REQUEST'
    assert res == 'Uppercase, lowercase, digit and special symbol required'
