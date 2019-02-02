import pytest


from api.extensions import mail
from api.models.user import UserModel
from api.models.confirmation import ConfirmationModel


def test_receive_confirmation_mail(client, new_user):
    """
    GIVEN an application instance, valid user, and mocked email outbox
    WHEN sending valid user data to register endpoint
    THEN check if message with acivation link was sent
    """
    with mail.record_messages() as outbox:
        rv = client.post('/register', json=new_user)
        assert rv.status == '201 CREATED'
        response = rv.get_json()
        assert response['message'] == 'Confirmation email was sent'

        assert len(outbox) == 1
        assert outbox[0].recipients[0] == new_user['email']
        assert '/confirmation/' in outbox[0].body


def test_confirmation_data_from_db(client, new_user, app, _db):
    """
    GIVEN an application instance, valid user, and mocked db
    WHEN sending valid user data to register endpoint
    THEN check cofirmation data
    """
    rv = client.post('/register', json=new_user)
    with app.app_context():
        db = _db
        users = db.session.query(UserModel).all()
        confirmations = db.session.query(ConfirmationModel).all()
        assert len(users) == 1
        assert len(confirmations) == 1
        assert users[0].username == "TestUser"
        assert users[0].id == confirmations[0].user_id
        assert not confirmations[0].confirmed


def test_confirmation_data_when_confirmed_correct(client, new_user, app, _db):
    """
    GIVEN an application instance, valid user, and mocked db
    WHEN sending valid user data to register endpoint, and cofirmed
    THEN check cofirmation data
    """
    rv = client.post('/register', json=new_user)
    with app.app_context():
        db = _db
        confirmations = db.session.query(ConfirmationModel).all()
        conf_id = confirmations[0].id
        rv2 = client.get("/confirmation/{}".format(conf_id))
        assert rv2.status == '200 OK'
        response = rv2.get_json()
        assert response['message'] == "Registration successfully confirmed"
        assert confirmations[0].confirmed


def test_confirmation_with_invalid_id(client):
    """
    GIVEN an application instance
    WHEN trying to confirm registration with invalid id
    THEN check if proper error raised
    """
    rv = client.get("/confirmation/invalid_id")
    assert rv.status == '404 NOT FOUND'
    response = rv.get_json()
    assert response['message'] == "Confirmation reference not found."


def test_confirmation_with_expired_id(client, new_user, app, _db):
    """
    GIVEN an application instance, valid user, and mocked db
    WHEN trying to confirm with expired id
    THEN check if proper error raised
    """
    rv = client.post('/register', json=new_user)
    with app.app_context():
        db = _db
        confirmations = db.session.query(ConfirmationModel).all()
        conf_id = confirmations[0].id
        assert not confirmations[0].expired()
        confirmations[0].force_to_expire()
        assert confirmations[0].expired()
        rv2 = client.get("/confirmation/{}".format(conf_id))
        assert rv2.status == '400 BAD REQUEST'
        response = rv2.get_json()
        assert response['message'] == "Confirmation link has expired"
        assert not confirmations[0].confirmed


def test_confirmation_when_already_confirmed(client, new_user, app, _db):
    """
    GIVEN an application instance, valid user, and mocked db
    WHEN sending valid user data to register endpoint, and cofirmed twice
    THEN check if proper error rised
    """
    rv = client.post('/register', json=new_user)
    with app.app_context():
        db = _db
        confirmations = db.session.query(ConfirmationModel).all()
        conf_id = confirmations[0].id
        rv2 = client.get("/confirmation/{}".format(conf_id))
        rv3 = client.get("/confirmation/{}".format(conf_id))
        assert rv3.status == '400 BAD REQUEST'
        response = rv3.get_json()
        assert response["message"] == "Registration has already been confirmed"
