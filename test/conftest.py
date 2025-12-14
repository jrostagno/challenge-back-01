import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.infraestructure.db.base import Base
from app.infraestructure.db.session import get_session
from app.main import app

load_dotenv(".env.test", override=False)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está seteada.")

engine = create_engine(DATABASE_URL)


TestingSessionLocal = sessionmaker[Session](
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Fixture : Create all tables in the database for testing
@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Fixture : Get a test database session with rollback for each test
@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session
    session.close()
    if transaction.is_active:
        transaction.rollback()
    connection.close()


@pytest.fixture()
def user_credentials():
    """
    Fixture: Return a dictionary with the user credentials
    """
    return {"name": "Javier", "email": "javier@mail.com", "password": "pass1234"}


@pytest.fixture()
def auth_headers(client, user_credentials):

    res_user = client.post("/users/", json=user_credentials)

    assert res_user.status_code == 200

    res_login = client.post(
        "/auth/login",
        json={
            "email": user_credentials["email"],
            "password": user_credentials["password"],
        },
    )
    assert res_login.status_code == 200
    data = res_login.json()
    access_token = data["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def created_notification(client, auth_headers):
    res = client.post(
        "/notification/",
        headers=auth_headers,
        json={
            "title": "original",
            "channel": "email",
            "content": "contenido original",
            "target": "test@mail.com",
        },
    )
    assert res.status_code == 200
    return res.json()


# Fixture: Override get_db from fastapi


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_db

    with TestClient(app) as client:
        yield client
