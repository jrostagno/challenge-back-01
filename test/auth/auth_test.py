def test_user_login(client):

    client.post(
        "/users/",
        json={"name": "javier", "email": "javier@mail.com", "password": "pass1234"},
    )

    login_response = client.post(
        "/auth/login/", json={"email": "javier@mail.com", "password": "pass1234"}
    )

    assert login_response.status_code == 200

    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
