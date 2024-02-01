import json
import pytest


#
# Article Tests
#
def test_get_articles(client):
    resp = client.get("/api/articles")
    assert resp.status_code == 200


@pytest.mark.skip("Requires authentication.")
def test_get_feed(client):
    resp = client.get("/api/articles/feed")
    assert resp.status_code == 200


def test_get_article(client):
    resp = client.get("/api/articles/how-to-article")
    assert resp.status_code == 200


@pytest.mark.skip("Requires authentication.")
def test_create_article(client):
    payload = {
        "article": {
            "title": "How to Article",
            "description": "A test article.",
            "body": "This is just a test!",
            "tagList": ["test", "article"],
        }
    }
    resp = client.post("/api/articles", json=json.dumps(payload))
    assert resp.status_code == 200


@pytest.mark.skip("Requires authentication.")
def test_update_article(client):
    payload = {
        "article": {
            "title": "How to Article",
            "description": "A test article.",
            "body": "This is just a test!",
            "tagList": ["test", "article"],
        }
    }
    resp = client.put("/api/articles/how-to-article", json=json.dumps(payload))
    assert resp.status_code == 200


@pytest.mark.skip("Requires authentication.")
def test_delete_article(client):
    resp = client.delete("/api/articles/how-to-article")
    assert resp.status_code == 200


#
# Article Favorties Tests
#
@pytest.mark.skip("Requires authentication.")
def test_favorite_article(client):
    resp = client.post("/api/articles/how-to-article/favorite")
    assert resp.status_code == 200


@pytest.mark.skip("Requires authentication.")
def test_unfavorite_article(client):
    resp = client.delete("/api/articles/how-to-article/favorite")
    assert resp.status_code == 200


#
# Article Comments Tests
#
def test_get_comments(client):
    resp = client.get("/api/articles/how-to-article/comments")
    assert resp.status_code == 200


@pytest.mark.skip("Requires authentication.")
def test_create_comment(client):
    data = {"comment": {"body": "What a nice article!"}}
    resp = client.post("/api/articles/how-to-article/comments", json=json.dumps(data))
    assert resp.status_code == 200


@pytest.mark.skip("Requires authentication.")
def test_delete_comment(client):
    resp = client.delete("/api/articles/how-to-article/comments/1")
    assert resp.status_code == 200


#
# Article Comments Tests
#
def test_get_tags(client):
    resp = client.get("/api/tags")
    assert resp.status_code == 200
