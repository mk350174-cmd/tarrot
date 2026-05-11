"""Auth-guarded endpoints must reject unauthenticated callers."""
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_birth_profiles_requires_auth() -> None:
    response = client.get("/api/v1/birth-profiles")
    assert response.status_code in (401, 403)


def test_readings_requires_auth() -> None:
    response = client.post(
        "/api/v1/readings",
        json={"birth_profile_id": "00000000-0000-0000-0000-000000000000"},
    )
    assert response.status_code in (401, 403)
