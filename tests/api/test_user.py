from unittest.mock import patch

from factory.alchemy import SQLAlchemyModelFactory
from fastapi.testclient import TestClient
from shop_list.core import security


def test_user_creation(client: TestClient):
    user_data = {
        "email": "mdslino@gmail.com",
        "first_name": "Marcelo",
        "last_name": "Lino",
        "password": "password",
        "verify_password": "password",
    }
    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == 200


def test_user_creation_with_registrations_closed(client: TestClient):
    user_data = {
        "email": "mdslino@gmail.com",
        "first_name": "Marcelo",
        "last_name": "Lino",
        "password": "password",
        "verify_password": "password",
    }
    with patch(
        "shop_list.api.api_v1.endpoints.users.settings"
    ) as settings_mock:
        settings_mock.USERS_OPEN_REGISTRATION = False
        response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 403


def test_user_creation_with_user_already_registred(
    client: TestClient, user_factory: SQLAlchemyModelFactory
):
    user_factory.create()
    user_data = {
        "email": "mdslino@gmail.com",
        "first_name": "Marcelo",
        "last_name": "Lino",
        "password": "password",
        "verify_password": "password",
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400


def test_get_user_me(client: TestClient, user_factory: SQLAlchemyModelFactory):
    user = user_factory()
    token = security.create_access_token(user.id)
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "mdslino@gmail.com"


def test_update_user(client: TestClient, user_factory: SQLAlchemyModelFactory):
    user = user_factory()
    token = security.create_access_token(user.id)
    response = client.patch(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "new_email@gmail.com", "password": "new_password"},
    )
    response.status_code == 200
