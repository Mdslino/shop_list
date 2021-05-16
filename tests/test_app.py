from fastapi import FastAPI
from shop_list.main import create_app
from shop_list.core.config import settings
from fastapi.testclient import TestClient


def test_app_creation():
    app = create_app()
    assert app.title == settings.PROJECT_NAME
    assert app.openapi_url == f"{settings.API_V1_STR}/openapi.json"
    assert isinstance(app, FastAPI)


def test_app_healthcheck(client: TestClient):
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
