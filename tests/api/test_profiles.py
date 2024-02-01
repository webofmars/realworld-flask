def test_get_profile(client):
    usr = "mock-user"
    resp = client.get(f"/api/profiles/{usr}")
    assert resp.status_code == 200


def test_follow_profile(client):
    usr = "mock-user"
    resp = client.post(f"/api/profiles/{usr}/follow")
    assert resp.status_code == 200


def test_unfollow_profile(client):
    usr = "mock-user"
    resp = client.delete(f"/api/profiles/{usr}/follow")
    assert resp.status_code == 200
