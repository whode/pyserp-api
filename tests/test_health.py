from __future__ import annotations


def test_health_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_ok(client, monkeypatch):
    monkeypatch.setenv("PYSERP_ENV", "test")
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "pyserp-api"
    assert data["env"] == "test"
    assert "pyserp_version" in data
