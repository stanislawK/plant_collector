from setuptools import find_packages, setup

setup(
    name='plant-collector',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask==1.0.2',
        'Flask-SQLAlchemy==2.3.1',
        'Flask-Migrate==2.3.0',
        'psycopg2==2.7.6',
        'Flask-Mail==0.9.1',
        'marshmallow==3.0.0rc1',
        'flask-restful==0.3.7',
        'flask-cors==3.0.7',
        'pytest==4.2.0',
        'pytest-flask-sqlalchemy==1.0.0',
        'passlib==1.7.1',
        'flask-jwt-extended==3.17.0',
        'flask-uploads==0.2.1'
    ],
)
