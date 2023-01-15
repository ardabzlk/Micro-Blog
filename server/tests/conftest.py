"""
“Conftest” file includes some initialization processes. Those processes grouped into fixtures.
Within a Flask application, main fixture to be created is a flask application.
"""

import pytest

from flask import current_app, jsonify
from mongoengine import connect, get_connection, disconnect
from werkzeug.security import generate_password_hash
from src.models.user_model import User

# scope="module" means that the fixture will be executed only once per test module
# scope="function" means that the fixture will be executed once per test function
# scope="session" means that the fixture will be executed once per test session
# scope="class" means that the fixture will be executed once per test class
# scope="package" means that the fixture will be executed once per test package
# default scope is "function"
# https://docs.pytest.org/en/latest/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session


@pytest.fixture(scope="module")
def message():
    return "Hello World"

# fixture to create a flask application
# and set the environment variable to point to the config file
# the fixture will be executed once per test module
@pytest.fixture
def mock_config(tmp_path, monkeypatch):
    """Mock config file for testing"""
    # create a temporary config file
    # and write some config data to it
    # the config file will be deleted after the test is finished
    config = tmp_path / "config.json"
    config.write_text(
        """
        {
            "APP_NAME": "micro-blog-app",
            "DEBUG": true,
            "TESTING": true,
            "SECRET_KEY": "micro-blog-playground",
            "DB_NAME": "micro-blog",
            "WTF_CSRF_ENABLED": false,

            "MONGODB_SETTINGS": {
                "db": "micro-blog",
                "host": "mongomock://localhost",
                "uuidRepresentation":"standard"
            }
        }
        """
    )

    # set the environment variable to point to the config file
    monkeypatch.setenv("CONFIG_PATH", str(config))


@pytest.fixture
# pass the mock_config fixture as an argument to the app_client fixture
def app_client(mock_config):
    from app import app, db
    # create the tables in the database
    user = User(
        name="foo",
        surname="bar",
        username="foobar",
        email="foo@bar.com",
        # generation hash password for user as in the register route
        password=generate_password_hash(
            "foobar", method='sha256'),
    )
    user.save()
    # yield can be used to return a value from a fixture here
    # and the code after the yield will be executed after the test is finished
    return app.test_client()
