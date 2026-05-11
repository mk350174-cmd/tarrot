"""
The Sky-Reader's Loom — weaves a complete natal chart from Yultuz positions,
house cusps, and aspect geometry.

Every value here is computed by Swiss Ephemeris through services/astronomy/ephemeris.
The LLM never reaches into this loom — it only reads the finished cloth.
"""
from datetime import datetime

from models.chart import AspectDTO, HouseCuspDTO, NatalChart, YultuzPositionDTO
from services.astronomy.ephemeris import (
    YULTUZ,
    get_all_yultuz_positions,
    get_houses,
    get_julian_day,
    get_turkic_animal,
    longitude_to_sign,
    turkic_animal_index,
)

# Aspect angles and their tolerable orbs (degrees)
_ASPECTS: list[tuple[str, float, float]] = [
    ("conjunction", 0.0, 8.0),
    ("opposition", 180.0, 8.0),
    ("trine", 120.0, 6.0),
    ("square", 90.0, 6.0),
    ("sextile", 60.0, 4.0),
]


def _angular_separation(a: float, b: float) -> float:
    """Smallest angular distance between two ecliptic longitudes (0..180)."""
    diff = abs((a - b) % 360)
    return diff if diff <= 180 else 360 - diff


def _detect_aspect(lon_a: float, lon_b: float) -> tuple[str, float, float] | None:
    sep = _angular_separation(lon_a, lon_b)
    for name, angle, orb in _ASPECTS:
        delta = abs(sep - angle)
        if delta <= orb:
            return name, sep, delta
    return None


def compute_natal_chart(
    birth_dt: datetime, latitude: float, longitude: float
) -> NatalChart:
    """
    Weave the complete sky-map for the moment of first breath.

    All numbers herein flow from Swiss Ephemeris — never from the LLM.
    """
    jd = get_julian_day(birth_dt)

    raw_positions = get_all_yultuz_positions(jd)
    positions_dto: list[YultuzPositionDTO] = []
    for p in raw_positions:
        sign, deg = longitude_to_sign(p.longitude)
        positions_dto.append(
            YultuzPositionDTO(
                name=p.name,
                longitude=p.longitude,
                latitude=p.latitude,
                speed=p.speed,
                sign=sign,
                degree_in_sign=deg,
            )
        )

    cusps, ascendant, midheaven = get_houses(jd, latitude, longitude)
    house_cusps_dto = [
        HouseCuspDTO(house=i + 1, longitude=lon, sign=longitude_to_sign(lon)[0])
        for i, lon in enumerate(cusps)
    ]

    aspects_dto: list[AspectDTO] = []
    names = list(YULTUZ.keys())
    for i, a_name in enumerate(names):
        for b_name in names[i + 1 :]:
            a = next(p for p in raw_positions if p.name == a_name)
            b = next(p for p in raw_positions if p.name == b_name)
            hit = _detect_aspect(a.longitude, b.longitude)
            if hit is not None:
                aspect_name, sep, orb = hit
                aspects_dto.append(
                    AspectDTO(
                        yultuz_a=a_name,
                        yultuz_b=b_name,
                        angle=sep,
                        aspect_name=aspect_name,
                        orb=orb,
                    )
                )

    year = birth_dt.year
    return NatalChart(
        yultuz_positions=positions_dto,
        house_cusps=house_cusps_dto,
        aspects=aspects_dto,
        ascendant=ascendant,
        midheaven=midheaven,
        turkic_animal=get_turkic_animal(year),
        turkic_animal_index=turkic_animal_index(year),
    )
