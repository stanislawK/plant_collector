import pytest


from api.extensions import mail


def test_receive_confirmation_mail(client, new_user):
    """
    GIVEN an application instance, valid user and mocked email outbox
    WHEN sending valid user data to register endpoint
    THEN check if message with acivation link was sent
    """
    rv = client.post('/register', json=new_user)
    assert rv.status == '201 CREATED'
    assert response['message'] == 'Confirmation email was sent'

    with mail.record_messages() as outbox:
        assert len(outbox) == 1
