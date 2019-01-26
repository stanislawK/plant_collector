import os
import tempfile

import pytest

from api import create_app
from api.extensions import db


@pytest.fixture
def app():
    """Create and configure a new app instance for tests."""
    # create a temp file to isolate the db for each test
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'DATABASE': db_path,
        'SQLALCHEMY_DATABASE_URI': "sqlite://"
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
def _db():
    """Create and configure a new db instance for pytest-flask-sqlalchemy"""
    # create a temp file to isolate the db for each test
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'DATABASE': db_path,
        'SQLALCHEMY_DATABASE_URI': "sqlite://"
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
            'password': "testPass",
            'email': "test@test.com"}
    return user
