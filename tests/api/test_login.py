from fastapi.testclient import TestClient
from factory.alchemy import SQLAlchemyModelFactory
from shop_list.core import security
def test_login_with_incorrect_user(client: TestClient):
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": "mdslino@gmail.com", "password": "password"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_login_with_success(client: TestClient, user_factory: SQLAlchemyModelFactory):
    user_factory.create()
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": "mdslino@gmail.com", "password": "password"},
    )
    data = response.json()
    assert response.status_code == 200
    assert all(
        key in data and data.get(key) for key in ["access_token", "token_type"]
    )

def test_test_token(client: TestClient, user_factory: SQLAlchemyModelFactory):
    user = user_factory()
    token = security.create_access_token(user.id)
    response = client.post(
        "/api/v1/login/test-token",
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200