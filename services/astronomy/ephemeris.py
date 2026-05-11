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
    "Kun": swe.SUN,              # Sun / Kun
    "Ay": swe.MOON,              # Moon / Ay
    "Arzu Tilek": swe.MERCURY,   # Mercury / Arzu Tilek
    "Altun Yultuz": swe.VENUS,   # Venus / Altun Yultuz ("golden star")
    "Mangys": swe.MARS,          # Mars / Mangys
    "Erkazar": swe.JUPITER,      # Jupiter / Erkazar
    "Zuhre": swe.SATURN,         # Saturn / Zuhre
    "Nesir": swe.URANUS,         # Uranus / Nesir
    "Poseidon": swe.NEPTUNE,     # Neptune
    "Erlik": swe.PLUTO,          # Pluto / Erlik (ruler of the underworld)
}

TURKIC_ANIMALS: list[str] = [
    "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
    "Horse", "Sheep", "Monkey", "Rooster", "Dog", "Pig",
]

ZODIAC_SIGNS: list[str] = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_ephe_initialized = False


@dataclass
class YultuzPosition:
    name: str
    longitude: float
    latitude: float
    speed: float


def init_ephe() -> None:
    """Set the ephemeris path — prepare the ancestral star charts."""
    global _ephe_initialized
    if not _ephe_initialized:
        swe.set_ephe_path(settings.ephe_path)
        _ephe_initialized = True


def get_julian_day(dt: datetime) -> float:
    """Convert a datetime to Julian Day Number (UT) for Swiss Ephemeris."""
    hour = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    return swe.julday(dt.year, dt.month, dt.day, hour)


def get_yultuz_position(yultuz_name: str, jd: float) -> YultuzPosition:
    """
    Retrieve the precise celestial position of a Yultuz (star/planet).

    Swiss Ephemeris is the sole oracle — no approximations permitted.
    """
    init_ephe()
    planet_id = YULTUZ[yultuz_name]
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    result, _ = swe.calc_ut(jd, planet_id, flags)
    return YultuzPosition(
        name=yultuz_name,
        longitude=float(result[0]),
        latitude=float(result[1]),
        speed=float(result[3]),
    )


def get_all_yultuz_positions(jd: float) -> list[YultuzPosition]:
    """Read every Yultuz across the great wheel for a given moment."""
    return [get_yultuz_position(name, jd) for name in YULTUZ]


def get_houses(
    jd: float, latitude: float, longitude: float, system: bytes = b"P"
) -> tuple[list[float], float, float]:
    """
    Compute the twelve houses, Ascendant, and Midheaven.

    Default house system is Placidus (b"P"). Returns:
      (cusps[1..12], ascendant, midheaven)
    """
    init_ephe()
    cusps, ascmc = swe.houses(jd, latitude, longitude, system)
    return list(cusps[:12]), float(ascmc[0]), float(ascmc[1])


def longitude_to_sign(longitude: float) -> tuple[str, float]:
    """Return (sign_name, degree_within_sign) for an ecliptic longitude."""
    lon = longitude % 360
    idx = int(lon // 30)
    return ZODIAC_SIGNS[idx], lon - idx * 30


def turkic_animal_index(year: int) -> int:
    """Return the Turkic 12-animal cycle index (0–11) for a given year."""
    return (year - 3) % 12


def get_turkic_animal(year: int) -> str:
    """Return the Turkic animal name for a given birth year."""
    return TURKIC_ANIMALS[turkic_animal_index(year)]
