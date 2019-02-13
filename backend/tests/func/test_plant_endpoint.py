import pytest


def test_add_new_plant(client, registred_user, new_user, new_plant):
    """
    GIVEN logged in user, plant data, and app instance
    WHEN trying to add new plant with valida data
    THEN check 200 status code and response
    """
    rv = client.post('/login', json={'username': new_user['username'],
                                     'password': new_user['password']})
    access_token = rv.get_json()['access_token']
    rv = client.post('/plant',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_plant)
    response = rv.get_json()

    assert rv.status == '201 CREATED'
    assert response['message'] == 'New plant created successfully'

    """WHEN Trying to add plant without non required data"""
    del new_plant['latin']
    del new_plant['difficulty']
    rv2 = client.post('/plant',
                      headers={'Authorization': 'Bearer {}'
                               .format(access_token)},
                      json=new_plant)
    response2 = rv2.get_json()

    assert rv2.status == '201 CREATED'


def test_add_new_plant_without_name(client,
                                    registred_user,
                                    new_user,
                                    new_plant):
    """
    GIVEN logged in user, plant data, and app instance
    WHEN trying to add new plant without required field
    THEN check if 400 status code and proper error raised
    """
    rv = client.post('/login', json={'username': new_user['username'],
                                     'password': new_user['password']})
    access_token = rv.get_json()['access_token']
    del new_plant['name']
    rv = client.post('/plant',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_plant)
    res = rv.get_json()

    assert rv.status == '400 BAD REQUEST'
    assert res['message']['name'][0] == 'Missing data for required field.'


def test_add_new_plant_without_jwt(client, new_plant):
    """
    GIVEN plant data, and app instance
    WHEN trying to add new plant without jwt
    THEN check if 401 status code and proper error raised
    """
    rv = client.post('/plant', json=new_plant)
    res = rv.get_json()

    assert rv.status == '401 UNAUTHORIZED'
    assert res['msg'] == 'Missing Authorization Header'
