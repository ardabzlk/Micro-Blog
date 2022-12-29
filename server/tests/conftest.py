import pytest

from flask import current_app
import mongomock
from mongoengine import connect, get_connection, disconnect

from src.models.user_model import User


@pytest.fixture
def mock_config(tmp_path, monkeypatch):
    """Mock config file for testing"""

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
def app_client(mock_config, monkeypatch):
    from app import app, db

    user = User(
        name="foo",
        surname="bar",
        username="foobar",
        email="foo@bar.com",
        password="foobar",
    )
    user.save()

    return app.test_client()
