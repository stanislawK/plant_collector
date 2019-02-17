import pytest


def test_add_new_description(client, access_token, new_plant, new_desc):
    """
    GIVEN logged in user, plant, description data and app instance
    WHEN trying add new valid description
    THEN check 200 status code and response
    """
    rv = client.post('/plant',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_plant)
    rv = client.post('/plant/1/description',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_desc)
    response = rv.get_json()

    assert rv.status == '201 CREATED'
    assert response["message"] == "New description created successfully"


def test_add_new_description_without_content(client,
                                             access_token,
                                             new_plant,
                                             new_desc):
    """
    GIVEN logged in user, plant, description without content and app instance
    WHEN trying add invalid description
    THEN check 400 status code and error message
    """
    rv = client.post('/plant',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_plant)
    del new_desc['content']
    rv = client.post('/plant/1/description',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_desc)
    response = rv.get_json()
    error = response["message"]['content'][0]
    assert rv.status == '400 BAD REQUEST'
    assert error == "Missing data for required field."


def test_add_new_description_without_token(client,
                                           access_token,
                                           new_plant,
                                           new_desc):
    """
    GIVEN logged in user, plant, description and app instance
    WHEN trying to add description without token
    THEN check 401 status code and error message
    """
    rv = client.post('/plant',
                     headers={'Authorization': 'Bearer {}'
                              .format(access_token)},
                     json=new_plant)
    rv = client.post('/plant/1/description', json=new_desc)
    response = rv.get_json()
    assert rv.status == '401 UNAUTHORIZED'
    assert response['msg'] == 'Missing Authorization Header'
