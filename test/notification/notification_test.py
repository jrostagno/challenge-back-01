from app.api.notification.notification_controller import get_notification_sender
from app.domain.notification.entities import NotificationStatus
from test.conftest import ErrorSender, SpySender


def test_create_notification_happy_path(client, auth_headers):
    res = client.post(
        "/notification/",
        headers=auth_headers,
        json={
            "title": "notificacion de prueba",
            "channel": "email",
            "content": "contenido de la notificacion",
            "target": "juan@pedro.com",
        },
    )

    # 👇 si falla, te muestra el json de error
    assert res.status_code == 200, res.json()

    notification = res.json()
    assert notification["title"] == "notificacion de prueba"
    assert notification["channel"] == "email"
    assert notification["target"] == "juan@pedro.com"
    # 👇 y acá validás el efecto de la “API externa”
    assert notification["status"] == NotificationStatus.SENT.value


def test_notification_marked_error_when_sender_fails(client, auth_headers):
    client.app.dependency_overrides[get_notification_sender] = lambda: ErrorSender()

    res = client.post(
        "/notification/",
        headers=auth_headers,
        json={
            "title": "test",
            "content": "mensaje válido",
            "channel": "email",
            "target": "test@mail.com",
        },
    )

    assert res.status_code == 200, res.json()
    body = res.json()
    assert body["status"] == NotificationStatus.ERROR.value
    assert body["error_message"] == "delivery failed"


def test_sender_is_called_with_correct_data(client, auth_headers):
    spy = SpySender()
    client.app.dependency_overrides[get_notification_sender] = lambda: spy

    res = client.post(
        "/notification/",
        headers=auth_headers,
        json={
            "title": "titulo",
            "content": "mensaje válido",
            "channel": "email",
            "target": "test@mail.com",
        },
    )

    assert res.status_code == 200, res.json()
    assert spy.called is True
    assert spy.last_notification is not None
    assert spy.last_notification.title == "titulo"
    assert spy.last_notification.channel == "email"
    assert spy.last_notification.target == "test@mail.com"


def test_sms_content_is_truncated_before_sending(client, auth_headers):
    spy = SpySender()
    client.app.dependency_overrides[get_notification_sender] = lambda: spy

    long_text = "x" * 500

    res = client.post(
        "/notification/",
        headers=auth_headers,
        json={
            "title": "titulo",
            "content": long_text,
            "channel": "sms",
            "target": "+5491112345678",
        },
    )

    assert res.status_code == 200, res.json()
    assert spy.called is True
    assert spy.last_notification is not None
    assert len(spy.last_notification.content) <= 160


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
