from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

import pytest


def test_logout_user_with_valid_access_token(client, access_token):
    """
    GIVEN logged in user and app instance
    WHEN trying to logout with access token
    THEN check 200 status code and response
    """
    rv_logout = client.post('/logout/access',
                            headers={'Authorization': 'Bearer {}'
                                     .format(access_token)})
    response = rv_logout.get_json()
    assert rv_logout.status == '200 OK'
    assert response['message'] == 'Access token has been revoked.'


def test_logout_user_with_valid_refresh_tkn(client, registred_user, new_user):
    """
    GIVEN logged in user and app instance
    WHEN trying to logout with refresh token
    THEN check 200 status code and response
    """
    rv = client.post('/login', json={'username': new_user['username'],
                                     'password': new_user['password']})
    refresh_token = rv.get_json()['refresh_token']
    rv_logout = client.post('/logout/refresh',
                            headers={'Authorization': 'Bearer {}'
                                     .format(refresh_token)})
    response = rv_logout.get_json()
    assert rv_logout.status == '200 OK'
    assert response['message'] == 'Refresh token has been revoked.'


def test_logout_user_with_valid_tokens(client, registred_user, new_user):
    """
    GIVEN logged in user and app instance
    WHEN trying to logout access and then refresh token
    THEN check 200 status code and response
    """
    rv = client.post('/login', json={'username': new_user['username'],
                                     'password': new_user['password']})
    access_token = rv.get_json()['access_token']
    refresh_token = rv.get_json()['refresh_token']
    rv_access = client.post('/logout/access',
                            headers={'Authorization': 'Bearer {}'
                                     .format(access_token)})
    resp_access = rv_access.get_json()
    assert rv_access.status == '200 OK'
    assert resp_access['message'] == 'Access token has been revoked.'

    rv_refresh = client.post('/logout/refresh',
                             headers={'Authorization': 'Bearer {}'
                                      .format(refresh_token)})
    resp_refresh = rv_refresh.get_json()
    assert rv_refresh.status == '200 OK'
    assert resp_refresh['message'] == 'Refresh token has been revoked.'


def test_logout_user_without_token(client, access_token):
    """
    GIVEN logged in user and app instance
    WHEN trying to logout users withot token in header
    THEN check 401 status code, and error message
    """
    rv_logout = client.post('/logout/access')
    resp = rv_logout.get_json()
    assert rv_logout.status == '401 UNAUTHORIZED'
    assert resp['msg'] == 'Missing Authorization Header'


def test_logout_user_with_invalid_token(client, registred_user, new_user, jwt):
    """
    GIVEN logged in user and app instance
    WHEN trying to logout with invalid access token
    THEN check 401 status code and error message
    """
    rv = client.post('/login', json={'username': new_user['username'],
                                     'password': new_user['password']})
    rv_logout = client.post('/logout/access',
                            headers={'Authorization': 'Bearer {}'
                                     .format(jwt)})
    response = rv_logout.get_json()
    assert rv_logout.status == '422 UNPROCESSABLE ENTITY'
    assert response['msg'] == 'Signature verification failed'


def test_logout_user_with_expired_token(expired_client,
                                        access_token):
    """
    GIVEN logged in user and app instance
    WHEN trying to logout with expired access token
    THEN check 401 status code and error message
    """
    rv_logout = expired_client.post('/logout/access',
                                    headers={'Authorization': 'Bearer {}'
                                             .format(access_token)})
    response = rv_logout.get_json()
    assert rv_logout.status == '401 UNAUTHORIZED'
    assert response['msg'] == 'Token has expired'
