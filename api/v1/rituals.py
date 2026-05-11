"""
Ritual endpoints — ceremonial guidance derived from astronomy data.

Public: turkic-animal lookup (no auth required — it is a folk calendar).
Auth-guarded: anything tied to a stored birth profile.
"""
from datetime import datetime, timezone

from fastapi import APIRouter

from models.ritual import MoonPhaseRitual, TurkicAnimalProfile
from services.astronomy.ephemeris import get_julian_day, get_yultuz_position
from services.rituals.calculator import moon_phase_ritual, turkic_animal_profile

router = APIRouter(prefix="/rituals", tags=["rituals"])


@router.get("/turkic-animal/{year}", response_model=TurkicAnimalProfile)
def turkic_animal_for_year(year: int) -> TurkicAnimalProfile:
    """Folk-calendar lookup — open to all who would hear the great wheel."""
    return turkic_animal_profile(year)


@router.get("/moon-phase", response_model=MoonPhaseRitual)
def current_moon_phase() -> MoonPhaseRitual:
    """Read the Ay where she rides at this very moment of the sky-dance."""
    jd = get_julian_day(datetime.now(timezone.utc))
    ay = get_yultuz_position("Ay", jd)
    return moon_phase_ritual(ay.longitude)
