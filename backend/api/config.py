import logging
import os
from os import urandom


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    """set jwt secret key"""
    JWT_SECRET_KEY = None
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    """flask_mail configuration required in production env"""
    MAIL_SERVER = None
    MAIL_PORT = None
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_USE_TLS = None
    MAIL_USE_SSL = None
    MAIL_ASCII_ATTACHMENTS = None

    """set maximum image size"""
    MAX_CONTENT_LENGTH = None

    """set directory for images"""
    UPLOADED_IMAGES_DEST = None


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    logging.basicConfig(level=logging.DEBUG)

    """db config"""
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://{username}:{password}@{hostname}:{port}/{databasename}"
        .format(
            username=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            hostname=os.environ.get('DB_HOST'),
            port=5432,
            databasename=os.environ.get('DB_NAME'),
        ))
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    """jwt config"""
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = 900

    """set maximum image size"""
    MAX_CONTENT_LENGTH = None

    """set directory for images"""
    UPLOADED_IMAGES_DEST = os.path.join("static", "images")


class TestConfig(Config):
    TESTING = True
