import json
import pytest


def test_create_user(client):
    payload = {
        "user": {
            "username": "mock-user",
            "email": "mock-user@realworld.io",
            "password": "password",
        }
    }
    resp = client.post("/api/users", json=json.dumps(payload))
    assert resp.status_code == 200


@pytest.mark.skip("Requires authentication.")
def test_authenticate_user(client):
    payload = {}
    resp = client.post("/api/users/login", json=json.dumps(payload))
    assert resp.status_code == 200


def test_get_current_user(client):
    resp = client.get("/api/user")
    assert resp.status_code == 200


@pytest.mark.skip("Requires authentication.")
def test_update_user(client):
    payload = {}
    resp = client.put("/api/user", json=json.dumps(payload))
    assert resp.status_code == 200
