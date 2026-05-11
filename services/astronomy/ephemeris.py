"""
The Oracle's Lens — deterministic astronomical calculations via Swiss Ephemeris.

All Yultuz (star/planet) positions, house cusps, and aspect calculations
must flow through this module. The LLM must never estimate or compute
astronomical values; the great wheel does not guess.
"""
from dataclasses import dataclass
from datetime import datetime

import swisseph as swe

from core.config import settings

YULTUZ: dict[str, int] = {
    "Kun": swe.SUN,          # Sun / Kun
    "Ay": swe.MOON,           # Moon / Ay
    "Arzu Tilek": swe.MERCURY, # Mercury / Arzu Tilek
    "Shulpan": swe.VENUS,     # Venus / Shulpan
    "Mangys": swe.MARS,       # Mars / Mangys
    "Erkazar": swe.JUPITER,   # Jupiter / Erkazar
    "Zuhre": swe.SATURN,      # Saturn / Zuhre
    "Nesir": swe.URANUS,      # Uranus / Nesir
    "Poseidon": swe.NEPTUNE,  # Neptune
    "Erlik": swe.PLUTO,       # Pluto / Erlik (ruler of the underworld)
}

TURKIC_ANIMALS: list[str] = [
    "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
    "Horse", "Sheep", "Monkey", "Rooster", "Dog", "Pig",
]


@dataclass
class YultuzPosition:
    name: str
    longitude: float
    latitude: float
    speed: float


def init_ephe() -> None:
    """Set the ephemeris path — prepare the ancestral star charts."""
    swe.set_ephe_path(settings.ephe_path)


def get_julian_day(dt: datetime) -> float:
    """Convert a datetime to Julian Day Number for Swiss Ephemeris."""
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)


def get_yultuz_position(yultuz_name: str, jd: float) -> YultuzPosition:
    """
    Retrieve the precise celestial position of a Yultuz (star/planet).

    Swiss Ephemeris is the sole oracle — no approximations permitted.
    """
    planet_id = YULTUZ[yultuz_name]
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    result, _ = swe.calc_ut(jd, planet_id, flags)
    return YultuzPosition(
        name=yultuz_name,
        longitude=result[0],
        latitude=result[1],
        speed=result[3],
    )


def turkic_animal_index(year: int) -> int:
    """Return the Turkic 12-animal cycle index (0–11) for a given year."""
    return (year - 3) % 12


def get_turkic_animal(year: int) -> str:
    """Return the Turkic animal name for a given birth year."""
    return TURKIC_ANIMALS[turkic_animal_index(year)]
