from app.config import Settings
from app.main import create_app


def test_settings_do_not_expose_secret_values(monkeypatch):
    monkeypatch.setenv("LINE_CHANNEL_ACCESS_TOKEN", "not-for-output")

    settings = Settings.from_environment()

    assert settings.integration_status("line") == "configured"
    assert "not-for-output" not in repr(settings)


def test_health_endpoint_reports_the_official_brand():
    from fastapi.testclient import TestClient

    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "brand": "U.Perfect"}
