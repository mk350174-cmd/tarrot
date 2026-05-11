"""
Chart computation smoke test — verifies the loom returns a fully-formed
NatalChart with all Yultuz present and Turkic animal derived from the
year via the canonical (Y-3) mod 12 formula.

This test requires Swiss Ephemeris built-in (Moshier fallback) data —
no external ephe files are needed for basic precision.
"""
from datetime import datetime

import pytest

pytest.importorskip("swisseph")

from services.astronomy.chart import compute_natal_chart  # noqa: E402
from services.astronomy.ephemeris import YULTUZ  # noqa: E402


def test_compute_natal_chart_returns_all_yultuz() -> None:
    chart = compute_natal_chart(
        birth_dt=datetime(1990, 6, 15, 12, 0, 0),
        latitude=41.0082,   # Istanbul
        longitude=28.9784,
    )
    assert {p.name for p in chart.yultuz_positions} == set(YULTUZ.keys())
    assert len(chart.house_cusps) == 12
    assert chart.turkic_animal == "Sheep"  # (1990 - 3) % 12 = 7 → Sheep
    for p in chart.yultuz_positions:
        assert 0 <= p.longitude < 360
        assert p.sign in {
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
        }
