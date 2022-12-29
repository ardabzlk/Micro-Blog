import pytest
from .database.models import User
import mongoengine.errors


def test_user_model_with_missing_params():
    """
    Test user model with missing params
    """
    user = User(
        name="John",
        surname="Doe",
        username="johndoe",
        email="foo@sixfab.com",
    )

    with pytest.raises(mongoengine.errors.ValidationError) as e:
        user.validate()

    assert "Field is required: ['password']" in str(e.value)
