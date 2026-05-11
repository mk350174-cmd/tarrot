"""
The Shaman's Voice — AI-driven interpretive layer for astrological readings.

This service weaves pre-computed Yultuz data (from services/astronomy)
into narrative wisdom using Turkic and Shamanic metaphor.

IMPORTANT: This layer must never perform astronomical calculations.
All numerical chart data must originate from services/astronomy/ephemeris.
"""
import anthropic

from core.config import settings


def _build_reading_prompt(chart_data: dict[str, object]) -> str:
    """Construct the shamanic reading prompt from pre-computed chart data."""
    return (
        "You are Korkut Ata, the ancestral sky-reader of the Turkic steppe.\n"
        "Interpret the following celestial chart using Shamanic and Turkic metaphors.\n"
        "Never calculate positions yourself — they are provided below.\n\n"
        f"Chart Data:\n{chart_data}\n\n"
        "Reference Yultuz (stars/planets) by their Turkic names, the 12-animal cycle, "
        "and the wisdom of the ancestral path."
    )


async def generate_reading(chart_data: dict[str, object]) -> str:
    """
    Generate a shamanic astrological reading from pre-computed chart data.

    The LLM interprets; Swiss Ephemeris computes. Never conflate these roles.
    """
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    message = await client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        messages=[{"role": "user", "content": _build_reading_prompt(chart_data)}],
    )
    return str(message.content[0].text)  # type: ignore[union-attr]
