"""
Sky-Map Schemas — Pydantic models describing the computed celestial chart.

These shapes carry deterministic data from services/astronomy down to
the ai_persona and rituals services. The numbers within originate ONLY
from Swiss Ephemeris.
"""
from pydantic import BaseModel


class YultuzPositionDTO(BaseModel):
    name: str  # e.g. "Kun", "Ay", "Arzu Tilek", "Altun Yultuz"
    longitude: float
    latitude: float
    speed: float
    sign: str  # zodiac sign name
    degree_in_sign: float


class HouseCuspDTO(BaseModel):
    house: int  # 1..12
    longitude: float
    sign: str


class AspectDTO(BaseModel):
    yultuz_a: str
    yultuz_b: str
    angle: float
    aspect_name: str  # conjunction, opposition, trine, square, sextile
    orb: float


class NatalChart(BaseModel):
    """The seeker's complete sky-map at the moment of first breath."""

    yultuz_positions: list[YultuzPositionDTO]
    house_cusps: list[HouseCuspDTO]
    aspects: list[AspectDTO]
    ascendant: float
    midheaven: float
    turkic_animal: str
    turkic_animal_index: int
