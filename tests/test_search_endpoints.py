from __future__ import annotations


def test_google_search_one_stubbed(client):
    response = client.post("/google/search-one", json={"query": "test"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["has_more"] is False
    assert payload["results"]["organic"][0]["url"] == "https://example.com"


def test_google_search_many_stubbed(client):
    response = client.post("/google/search-many", json={"query": "test", "starts": [0, 10]})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["pages"]) == 1
    page = payload["pages"][0]
    assert page["results"]["organic"][0]["url"] == "https://example.com"


def test_google_search_top_stubbed(client):
    response = client.post("/google/search-top", json={"query": "test", "limit": 1})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["pages"]) == 1
    page = payload["pages"][0]
    assert page["results"]["organic"][0]["title"] == "Example"


def test_bing_search_one_stubbed(client):
    response = client.post("/bing/search-one", json={"query": "test"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["has_more"] is False
    assert payload["results"]["organic"][0]["title"] == "Example"


def test_bing_search_many_stubbed(client):
    response = client.post("/bing/search-many", json={"query": "test", "starts": [0, 10]})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["pages"]) == 1
    page = payload["pages"][0]
    assert page["results"]["organic"][0]["url"] == "https://example.com"


def test_bing_search_top_stubbed(client):
    response = client.post("/bing/search-top", json={"query": "test", "limit": 1})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["pages"]) == 1
    page = payload["pages"][0]
    assert page["results"]["organic"][0]["title"] == "Example"
