"""
The Ceremonial Compass — ritual timing derived from pre-computed Yultuz positions.

This service never calls Swiss Ephemeris directly. All astronomical data
must be passed in from services/astronomy/ephemeris.py. The steppe oracle
reads the sky; this module reads the oracle.
"""
from dataclasses import dataclass
from datetime import datetime

from services.astronomy.ephemeris import YultuzPosition, get_turkic_animal


@dataclass
class RitualWindow:
    name: str
    description: str
    start: datetime
    end: datetime
    auspicious: bool


def get_moon_phase_ritual(ay_longitude: float) -> str:
    """
    Derive the ritual significance of the Ay (Moon) from its ecliptic longitude.

    Phases are divided into four sacred quarters of the great wheel.
    """
    phase = ay_longitude % 360
    if phase < 90:
        return "Waxing Crescent — time for setting ancestral intentions"
    elif phase < 180:
        return "Waxing Gibbous — the fire of growth burns bright on the steppe"
    elif phase < 270:
        return "Waning Gibbous — release what no longer serves the spirit walk"
    else:
        return "Waning Crescent — rest and commune with the ancestor spirits"


def assess_yultuz_harmony(positions: list[YultuzPosition]) -> dict[str, object]:
    """
    Assess the ceremonial harmony of the sky from a list of Yultuz positions.

    Returns a summary of dominant energies for ritual planning.
    All position data must originate from services/astronomy/ephemeris.
    """
    dominant = max(positions, key=lambda p: abs(p.speed))
    return {
        "dominant_yultuz": dominant.name,
        "longitude": dominant.longitude,
        "ceremony_note": f"{dominant.name} leads the sky-dance — align rituals to its path.",
    }


def birth_year_ritual_profile(birth_year: int) -> dict[str, object]:
    """
    Return the ritual profile for a birth year based on the Turkic animal cycle.

    The animal is derived via C = (Y-3) mod 12 (canonical formula from ephemeris).
    """
    animal = get_turkic_animal(birth_year)
    return {
        "turkic_animal": animal,
        "birth_year": birth_year,
        "ritual_element": _animal_element(animal),
    }


_ANIMAL_ELEMENTS: dict[str, str] = {
    "Rat": "Water", "Ox": "Earth", "Tiger": "Wood", "Rabbit": "Wood",
    "Dragon": "Earth", "Snake": "Fire", "Horse": "Fire", "Sheep": "Earth",
    "Monkey": "Metal", "Rooster": "Metal", "Dog": "Earth", "Pig": "Water",
}


def _animal_element(animal: str) -> str:
    return _ANIMAL_ELEMENTS.get(animal, "Unknown")
