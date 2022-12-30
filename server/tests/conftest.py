import pytest

from flask import current_app, jsonify
import mongomock
from mongoengine import connect, get_connection, disconnect
from werkzeug.security import generate_password_hash
from src.models.user_model import User


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
    return app.test_client()
