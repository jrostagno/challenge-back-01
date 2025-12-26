from app.domain.notification.entities import NotificationStatus


def test_create_notification(client, auth_headers):

    response = client.post(
        "/notification/",
        headers=auth_headers,
        json={
            "title": "notificacion de prueba",
            "channel": "email",
            "content": "contenido de la notificacion",
            "target": "juan@pedro.com",
        },
    )

    assert response.status_code == 200
    notification = response.json()
    assert notification["title"] == "notificacion de prueba"
    assert notification["channel"] == "email"
    assert notification["target"] == "juan@pedro.com"


def test_create_notification_marks_sent(client, auth_headers):
    res = client.post(
        "/notification/",
        headers=auth_headers,
        json={
            "title": "test",
            "content": "msg",
            "channel": "email",
            "target": "test@mail.com",
        },
    )

    assert res.status_code == 200
    body = res.json()

    assert body["status"] == NotificationStatus.SENT.value


def test_update_notification(client, auth_headers, created_notification):
    notification_id = created_notification["notification_id"]
    response = client.put(
        f"/notification/{notification_id}",
        headers=auth_headers,
        json={
            "title": "notificacion de prueba actualizada",
            "channel": "sms",
            "content": "contenido de la notificacion actualizado",
            "target": "juan@pedro.com",
        },
    )
    assert response.status_code == 200
    notification = response.json()
    assert notification["title"] == "notificacion de prueba actualizada"


def test_delete_notification(client, auth_headers, created_notification):
    notification_id = created_notification["notification_id"]
    response = client.delete(
        f"/notification/{notification_id}",
        headers=auth_headers,
    )
    assert response.status_code == 204
    response = client.get(
        f"/notification/{notification_id}",
        headers=auth_headers,
    )

    print(response.status_code, response.json())

    assert response.status_code == 404


def test_get_notification_by_id(client, auth_headers, created_notification):
    notification_id = created_notification["notification_id"]
    response = client.get(
        f"/notification/{notification_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    notification = response.json()
    assert notification["notification_id"] == notification_id
    assert notification["title"] == "original"
    assert notification["channel"] == "email"
    assert notification["content"] == "contenido original"
    assert notification["target"] == "test@mail.com"


def test_get_all_notifications(client, auth_headers):
    response = client.get(
        "/notification/",
        headers=auth_headers,
    )
    assert response.status_code == 200
    notifications = response.json()
    assert len(notifications) == 0
