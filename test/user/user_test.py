def test_create_user_success(client):
    response = client.post(
        "/users/",
        json={"name": "Javier", "email": "javier@test.com", "password": "password123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Javier"
    assert data["email"] == "javier@test.com"
    assert "user_id" in data


def test_creat_user_duplicate_email(client):

    client.post(
        "/users/",
        json={"name": "fede", "email": "fede@mail.com", "password": "pass1234"},
    )

    response = client.post(
        "/users/",
        json={"name": "fedu", "email": "fede@mail.com", "password": "alalala123"},
    )

    assert response.status_code in (400, 409)


def test_create_user_invalid_email(client):

    response = client.post(
        "/users/",
        json={"name": "fede", "email": "fedemail.com", "password": "pass1234"},
    )

    assert response.status_code == 422
