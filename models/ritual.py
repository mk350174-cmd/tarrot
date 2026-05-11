"""
Ritual Schemas — ceremonial guidance derived from the great wheel.
"""
from pydantic import BaseModel


class TurkicAnimalProfile(BaseModel):
    year: int
    animal: str
    animal_index: int
    ritual_element: str


class MoonPhaseRitual(BaseModel):
    ay_longitude: float
    phase: str
    guidance: str
