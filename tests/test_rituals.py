import pytest
from fastapi.testclient import TestClient

from main import app
from services.rituals.calculator import moon_phase_ritual, turkic_animal_profile

client = TestClient(app)


@pytest.mark.parametrize(
    "lon,expected_phase",
    [
        (10.0, "Waxing Crescent"),
        (100.0, "Waxing Gibbous"),
        (200.0, "Waning Gibbous"),
        (300.0, "Waning Crescent"),
        (360.0, "Waxing Crescent"),  # normalized to 0
    ],
)
def test_moon_phase_ritual_quarters(lon: float, expected_phase: str) -> None:
    result = moon_phase_ritual(lon)
    assert result.phase == expected_phase
    assert 0 <= result.ay_longitude < 360


def test_turkic_animal_profile_canonical() -> None:
    # 2024: (2024 - 3) % 12 = 5 → Snake. Snake's element in our table is Fire.
    profile = turkic_animal_profile(2024)
    assert profile.animal == "Snake"
    assert profile.ritual_element == "Fire"


def test_rituals_endpoint_turkic_animal() -> None:
    response = client.get("/api/v1/rituals/turkic-animal/2024")
    assert response.status_code == 200
    body = response.json()
    assert body["animal"] == "Snake"
    assert body["year"] == 2024
    assert body["ritual_element"] == "Fire"
