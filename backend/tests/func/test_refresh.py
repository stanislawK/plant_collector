import pytest


def test_refreshing_new_token(client, new_user, registred_user):
    """
    GIVEN logged in user with fresh token and app instance
    WHEN refreshing access token
    THEN new access_token should be returned
    """
    rv = client.post('/login', json={'username': new_user['username'],
                                     'password': new_user['password']})
    refresh_token = rv.get_json()['refresh_token']
    rv_refresh = client.post('/refresh',
                             headers={'Authorization': 'Bearer {}'
                                      .format(refresh_token)})
    response = rv_refresh.get_json()
    assert rv_refresh.status == '200 OK'
    assert response['access_token']


def test_refreshing_expired_token(expired_client, new_user, registred_user):
    """
    GIVEN logged in user with expired token and app instance
    WHEN refreshing access token
    THEN new access_token should be returned
    """
    rv = expired_client.post('/login',
                             json={'username': new_user['username'],
                                   'password': new_user['password']})
    refresh_token = rv.get_json()['refresh_token']
    rv_refresh = expired_client.post('/refresh',
                                     headers={'Authorization': 'Bearer {}'
                                              .format(refresh_token)})
    response = rv_refresh.get_json()
    assert rv_refresh.status == '200 OK'
    assert response['access_token']


def test_refreshing_without_refresh_token(client, new_user, registred_user):
    """
    GIVEN logged in user with fresh token and app instance
    WHEN trying to refresh without valid refresh token
    THEN check 401 status code and error message
    """
    rv = client.post('/login', json={'username': new_user['username'],
                                     'password': new_user['password']})
    rv_refresh = client.post('/refresh')
    response = rv_refresh.get_json()
    assert rv_refresh.status == '401 UNAUTHORIZED'
    assert response['msg'] == 'Missing Authorization Header'


def test_refreshing_with_access_token(client, new_user, registred_user):
    """
    GIVEN logged in user with fresh token and app instance
    WHEN trying to refresh with access token
    THEN check 401 status code and error message
    """
    rv = client.post('/login', json={'username': new_user['username'],
                                     'password': new_user['password']})
    access_token = rv.get_json()['access_token']
    rv_refresh = client.post('/refresh',
                             headers={'Authorization': 'Bearer {}'
                                      .format(access_token)})
    response = rv_refresh.get_json()
    assert rv_refresh.status == '422 UNPROCESSABLE ENTITY'
    assert response['msg'] == 'Only refresh tokens are allowed'
