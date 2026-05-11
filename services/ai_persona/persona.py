"""
The Shaman's Voice — AI-driven interpretive layer for astrological readings.

This service weaves pre-computed Yultuz data (from services/astronomy)
into narrative wisdom using Turkic and Shamanic metaphor.

IMPORTANT: This layer must never perform astronomical calculations.
All numerical chart data must originate from services/astronomy.
"""
import anthropic

from core.config import settings
from models.chart import NatalChart

_SYSTEM_PROMPT = """You are Korkut Ata, the ancestral sky-reader of the Turkic steppe.

You interpret celestial charts using Shamanic and Turkic metaphors. You speak of
Yultuz (stars/planets) by their Turkic names — Kun (Sun), Ay (Moon),
Arzu Tilek (Mercury), Altun Yultuz (Venus), Mangys (Mars), Erkazar (Jupiter),
Zuhre (Saturn), Nesir (Uranus), Erlik (Pluto). You weave imagery of the
great wheel, the ancestral path, the steppe wind, fire spirits, and the
twelve-animal cycle.

CRITICAL: Never calculate or estimate positions, angles, or houses yourself.
All numerical chart data is provided to you below. Read it, do not compute it.
""".strip()


def _format_chart_for_prompt(chart: NatalChart) -> str:
    lines: list[str] = []
    lines.append("=== YULTUZ POSITIONS ===")
    for p in chart.yultuz_positions:
        lines.append(
            f"{p.name}: {p.degree_in_sign:.2f}° {p.sign} "
            f"(lon {p.longitude:.2f}°, speed {p.speed:+.3f})"
        )
    lines.append("")
    lines.append(f"Ascendant: {chart.ascendant:.2f}°")
    lines.append(f"Midheaven: {chart.midheaven:.2f}°")
    lines.append("")
    lines.append("=== HOUSE CUSPS ===")
    for h in chart.house_cusps:
        lines.append(f"House {h.house}: {h.longitude:.2f}° ({h.sign})")
    lines.append("")
    lines.append("=== ASPECTS ===")
    if chart.aspects:
        for a in chart.aspects:
            lines.append(
                f"{a.yultuz_a} {a.aspect_name} {a.yultuz_b} "
                f"(angle {a.angle:.2f}°, orb {a.orb:.2f}°)"
            )
    else:
        lines.append("(none within orb)")
    lines.append("")
    lines.append(
        f"Turkic animal of birth year: {chart.turkic_animal} "
        f"(index {chart.turkic_animal_index})"
    )
    return "\n".join(lines)


def _build_user_prompt(chart: NatalChart, focus: str | None) -> str:
    focus_line = (
        f"\nFocus the reading on the theme: **{focus}**.\n" if focus else ""
    )
    return (
        "Interpret the following sky-map for the seeker. "
        "Use Turkic Shamanic metaphors throughout. "
        "Reference at least the Kun, the Ay, the Ascendant, and the seeker's "
        "Turkic animal. Speak as Korkut Ata would — warm, mythic, grounded."
        f"{focus_line}\n\n"
        f"{_format_chart_for_prompt(chart)}"
    )


async def generate_reading(chart: NatalChart, focus: str | None = None) -> str:
    """
    Generate a Shamanic reading from pre-computed chart data.

    The LLM interprets; Swiss Ephemeris computes. Never conflate these roles.
    """
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    message = await client.messages.create(
        model=settings.anthropic_model,
        max_tokens=1500,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _build_user_prompt(chart, focus)}],
    )
    parts: list[str] = []
    for block in message.content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    return "\n".join(parts)
