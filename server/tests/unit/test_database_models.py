import pytest
from ..database.models import User
import mongoengine.errors
from werkzeug.security import generate_password_hash


def test_user_model_with_missing_password():
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


@pytest.mark.parametrize("_password", [
    "123",
    "1234567",
    "asxc21",
    "agssdd"])
def test_user_model_with_wrong_password(_password):
    """
    Test user model with wrong password
    GIVEN: a user model with wrong password
    WHEN: user model is validated
    THEN: it should raise ValidationError
    """
    # given

    respresentative_data = {
        "name": "John",
        "surname": "Doe",
        "username": "johndoe",
        "email": "foo@sixfab.com",
        "password":  "123"
    }

    user = User(
        name="John",
        surname="Doe",
        username="johndoe",
        email="foo@sixfab.com",
        password=_password
    )
    assert respresentative_data["name"] == user.name
    assert respresentative_data["surname"] == user.surname
    assert respresentative_data["username"] == user.username
    assert respresentative_data["email"] == user.email
    # password should be hashed
    # so it should not be equal to the given password
    assert respresentative_data["password"] != user.password
