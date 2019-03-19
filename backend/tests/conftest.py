import os
import tempfile

import pytest

from api import create_app
from api.extensions import db
from api.models.confirmation import ConfirmationModel


@pytest.fixture
def app():
    """Create and configure a new app instance for tests."""
    # create a temp file to isolate the db for each test
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'DATABASE': db_path,
        'SQLALCHEMY_DATABASE_URI': "sqlite://",
        'JWT_SECRET_KEY': 'TestJWTKey',
        'UPLOADED_IMAGES_DEST': 'Secret'
    })

    # create the db and load test data
    with app.app_context():
        db.init_app(app)
        db.create_all()

    yield app

    # close and remove the temporary db
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def expired_client(app):
    """A test client for the app."""
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = -1
    return app.test_client()


@pytest.fixture
def _db():
    """Create and configure a new db instance for pytest-flask-sqlalchemy"""
    # create a temp file to isolate the db for each test
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'DATABASE': db_path,
        'SQLALCHEMY_DATABASE_URI': "sqlite://",
        'UPLOADED_IMAGES_DEST': 'Secret'
    })

    # create the db and load test data
    with app.app_context():
        db.init_app(app)
        db.create_all()

        yield db

    # close and remove the temporary db
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def new_user():
    user = {'username': "TestUser",
            'password': "testPass1!",
            'email': "test@test.com"}
    return user


@pytest.fixture
def registred_user(new_user, client, app, _db):
    rv = client.post('/register', json=new_user)
    with app.app_context():
        db = _db
        confirmations = db.session.query(ConfirmationModel).all()
        conf_id = confirmations[0].id
        rv2 = client.get("/confirmation/{}".format(conf_id))


@pytest.fixture
def access_token(client, new_user, registred_user):
    rv = client.post('/login', json={'username': new_user['username'],
                                     'password': new_user['password']})
    access_token = rv.get_json()['access_token']
    return access_token


@pytest.fixture
def jwt():
    jwt = ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDk0NzQzMjksImZyZ'
           'XNoIjp0cnVlLCJ0eXBlIjoiYWNjZXNzIiwianRpIjoiMjE3NWI2ZjgtY2Y0Zi00Njd'
           'kLTg5NTQtZmY5ZjcxMDM2NmFmIiwibmJmIjoxNTQ5NDc0Mjk5LCJpZGVudGl0eSI6N'
           'SwiaWF0IjoxNTQ5NDc0Mjk5fQ.IcoarNxOYrS-EAbAAPc_ZgbzGK8n_hXDCb_tkEhn'
           'Y9c')
    return jwt


@pytest.fixture
def new_plant():
    plant = {"name": "Monstera",
             "latin": "Monstera Adans.",
             "difficulty": 5}
    return plant


@pytest.fixture
def new_desc():
    description = {"content": "Description content",
                   "source": "wikipedia"}
    return description
