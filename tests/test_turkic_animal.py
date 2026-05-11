"""Canonical formula: C = (Y - 3) mod 12; animal order begins at Rat."""
import pytest

from services.astronomy.ephemeris import (
    TURKIC_ANIMALS,
    get_turkic_animal,
    turkic_animal_index,
)


@pytest.mark.parametrize(
    "year,expected",
    [
        (1923, "Rat"),
        (1924, "Ox"),
        (1925, "Tiger"),
        (1990, "Sheep"),
        (2024, "Snake"),
        (2025, "Horse"),
    ],
)
def test_get_turkic_animal(year: int, expected: str) -> None:
    assert get_turkic_animal(year) == expected


def test_turkic_animal_index_within_bounds() -> None:
    for year in range(1900, 2100):
        idx = turkic_animal_index(year)
        assert 0 <= idx < 12
        assert TURKIC_ANIMALS[idx] == get_turkic_animal(year)
