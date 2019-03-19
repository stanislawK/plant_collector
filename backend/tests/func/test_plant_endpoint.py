import pytest


def test_add_new_plant(client, access_token, new_plant):
    """
    GIVEN logged in user, plant data, and app instance
    WHEN trying to add new plant with valida data
    THEN check 201 status code and response
    """
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
                                    access_token,
                                    new_plant):
    """
    GIVEN logged in user, plant data, and app instance
    WHEN trying to add new plant without required field
    THEN check if 400 status code and proper error raised
    """
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


def test_get_plant(client, access_token, new_plant):
    """
    GIVEN logged in user, plant data and app instance
    WHEN trying to get previously added plant
    THEN check 200 status code, and plant data
    """
    rv = client.post('/plant',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_plant)

    rv = client.get('/plant/1',
                    headers={'Authorization': 'Bearer {}'
                             .format(access_token)})
    res = rv.get_json()

    assert rv.status == '200 OK'
    assert res["name"] == "Monstera"
    assert res['latin'] == "Monstera Adans."


def test_get_plants(client, access_token, new_plant):
    """
    GIVEN logged in user, plant data and app instance
    WHEN trying to get added plants
    THEN check 200 status code, and plants data
    """
    rv = client.post('/plant',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_plant)
    rv = client.post('/plant',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_plant)

    rv = client.get('/plants',
                    headers={'Authorization': 'Bearer {}'
                             .format(access_token)})
    res = rv.get_json()['plants']

    assert rv.status == '200 OK'
    assert len(res) == 2
    assert res[0]["name"] == "Monstera"
    assert res[1]['latin'] == "Monstera Adans."


def test_edit_plant_data(client, access_token, new_plant):
    """
    GIVEN logged in user, plant data and app instance
    WHEN trying to edit plant with valida data
    THEN check 201 status code, response, and edited plant data
    """
    rv = client.post('/plant',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_plant)

    edited = {"name": "Monstera2",
              "latin": "Monstera Adans2."}
    rv = client.put('/plant/1',
                    headers={'Authorization': 'Bearer {}'
                             .format(access_token)},
                    json=edited)
    res = rv.get_json()

    assert rv.status == "201 CREATED"
    assert res["message"] == "Plant changed successfully"

    # Check if plant data was changed correctly
    rv = client.get('/plant/1',
                    headers={'Authorization': 'Bearer {}'
                             .format(access_token)})
    res = rv.get_json()

    assert res["name"] == "Monstera2"
    assert res["latin"] == "Monstera Adans2."


def test_delete_plant(client, access_token, new_plant):
    """
    GIVEN logged in user, plant data and app instance
    WHEN trying to delete
    THEN check 200 status code and response
    """
    rv = client.post('/plant',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_plant)

    rv = client.delete('/plant/1',
                       headers={'Authorization': 'Bearer {}'
                                .format(access_token)})

    res = rv.get_json()

    assert rv.status == '200 OK'
    assert res['message'] == "Plant was deleted"


def test_delete_plant_with_invalid_token(client, access_token, new_plant, jwt):
    """
    GIVEN logged in user, plant data and app instance
    WHEN trying to delete plant without and with invalid token
    THEN check if 401 status code and proper error raised
    """
    rv = client.post('/plant',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_plant)

    rv = client.delete('/plant/1',
                       headers={'Authorization': 'Bearer {}'
                                .format(jwt)})
    res = rv.get_json()

    assert rv.status == '422 UNPROCESSABLE ENTITY'
    assert res['msg'] == "Signature verification failed"

    rv = client.delete('/plant/1')
    res = rv.get_json()

    assert rv.status == '401 UNAUTHORIZED'
    assert res['msg'] == 'Missing Authorization Header'
