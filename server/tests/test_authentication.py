def test_login_with_incorrect_password(app_client):
    """
    Test login with incorrect password
    Correct Credentials:
        name="foo",
        surname="bar",
        username="foobar",
        email="foo@bar.com",
        password="foobar",
    """
    response = app_client.post(
        "/login", json={"email": "foo@bar.com", "password": "bar"}
    )

    # expected response =>
    assert response.status_code == 401
    assert response.text == "Could not verify"
