"""
The Ceremonial Compass — ritual timing derived from pre-computed Yultuz positions.

This service never calls Swiss Ephemeris directly. All astronomical data
must be passed in from services/astronomy/ephemeris.py. The steppe oracle
reads the sky; this module reads the oracle.
"""
from models.ritual import MoonPhaseRitual, TurkicAnimalProfile
from services.astronomy.ephemeris import get_turkic_animal, turkic_animal_index

_ANIMAL_ELEMENTS: dict[str, str] = {
    "Rat": "Water", "Ox": "Earth", "Tiger": "Wood", "Rabbit": "Wood",
    "Dragon": "Earth", "Snake": "Fire", "Horse": "Fire", "Sheep": "Earth",
    "Monkey": "Metal", "Rooster": "Metal", "Dog": "Earth", "Pig": "Water",
}


def moon_phase_ritual(ay_longitude: float) -> MoonPhaseRitual:
    """
    Derive the ritual significance of the Ay (Moon) from its ecliptic longitude.

    Phases are divided into four sacred quarters of the great wheel.
    NOTE: caller must pass an ay_longitude that originated from Swiss Ephemeris.
    """
    lon = ay_longitude % 360
    if lon < 90:
        phase = "Waxing Crescent"
        guidance = "Set ancestral intentions; the steppe wind carries new seeds."
    elif lon < 180:
        phase = "Waxing Gibbous"
        guidance = "The fire of growth burns bright — tend it with patient hands."
    elif lon < 270:
        phase = "Waning Gibbous"
        guidance = "Release what no longer serves the spirit walk."
    else:
        phase = "Waning Crescent"
        guidance = "Rest and commune with the ancestor spirits."
    return MoonPhaseRitual(ay_longitude=lon, phase=phase, guidance=guidance)


def turkic_animal_profile(year: int) -> TurkicAnimalProfile:
    """
    Return the ritual profile for a birth year via the Turkic 12-animal cycle.

    The animal index follows the canonical formula C = (Y - 3) mod 12,
    sourced exclusively from services/astronomy/ephemeris.
    """
    animal = get_turkic_animal(year)
    return TurkicAnimalProfile(
        year=year,
        animal=animal,
        animal_index=turkic_animal_index(year),
        ritual_element=_ANIMAL_ELEMENTS.get(animal, "Unknown"),
    )
