from __future__ import annotations

from fastapi.testclient import TestClient

from app import main as main_module


class DummyManager:
    def __init__(self) -> None:
        self.closed = False

    async def close(self) -> None:
        self.closed = True


def test_lifespan_creates_and_closes_managers(monkeypatch):
    google_manager = DummyManager()
    bing_manager = DummyManager()

    monkeypatch.setattr(main_module, "build_google_manager", lambda settings: google_manager)
    monkeypatch.setattr(main_module, "build_bing_manager", lambda settings: bing_manager)

    with TestClient(main_module.app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert main_module.app.state.google_manager is google_manager
        assert main_module.app.state.bing_manager is bing_manager
        assert google_manager.closed is False
        assert bing_manager.closed is False

    assert google_manager.closed is True
    assert bing_manager.closed is True
