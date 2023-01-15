"""
Correct Credentials:
    name="foo",
    surname="bar",
    username="foobar",
    email="foo@bar.com",
    password="foobar",
"""


def test_login_with_incorrect_password(app_client):
    # Test login with incorrect password screnario
    response = app_client.post(
        "/login", json={"email": "foo@bar.com", "password": "bar"}
    )

    # expected response =>
    assert response.status_code == 401
    assert response.text == "Could not verify"

# ------------------------------------------------------------


def test_login_with_correct_password(app_client):
    # Test login with correct password screnario
    response = app_client.post(
        "/login", json={"email": "foo@bar.com", "password": "foobar"}
    )
    # expected response =>
    assert response.status_code == 200


# ------------------------------------------------------------

def test_login_with_incorrect_email(app_client):
    # Test login with incorrect email screnario
    response = app_client.post(
        "/login", json={"email": "no@bar.com", "password": "foobar"}
    )

    # expected response =>
    assert response.status_code == 404
    assert response.text == "No such user"

# ------------------------------------------------------------


def test_login_with_empty_email(app_client):
    # Test login with empty email screnario
    response = app_client.post(
        "/login", json={"email": "", "password": "foobar"}
    )

    # expected response =>
    assert response.status_code == 200
    assert response.text == "empty field"


def test_list_blog_posts_without_token(app_client):
    # Test list blog posts without token screnario
    response = app_client.get("/blog_posts")

    # expected response =>
    assert response.status_code == 401
    assert response.text == '{\n  "message": "Token is missing"\n}\n'


def test_list_blog_posts_with_token(app_client):
    # Test list blog posts with token screnario
    token_request = app_client.post(
        "/login", json={"email": "foo@bar.com", "password": "foobar"}
    )
    token = token_request.json["token"]

    response = app_client.get(
        "/blog_posts", headers={"Authorization": "Bearer " + token})

    # expected response =>
    assert response.status_code == 200


# Path: server\tests\test_authentication.py
# Compare this snippet from server\src\routes\auth\login_register_routes.py:
