"""
Reading endpoints — the Shaman's Voice speaks over the deterministic chart.

The chart is computed via Swiss Ephemeris (services/astronomy.chart) and
handed to services/ai_persona for narrative weaving. The LLM never sees
raw birth coordinates without the chart layer between.
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import AuthContext, get_current_user
from core.config import settings
from core.supabase_client import get_user_supabase
from models.reading import Reading, ReadingRequest
from services.ai_persona.persona import generate_reading
from services.astronomy.chart import compute_natal_chart

router = APIRouter(prefix="/readings", tags=["readings"])


@router.post("", response_model=Reading)
async def create_reading(
    payload: ReadingRequest,
    auth: AuthContext = Depends(get_current_user),
) -> Reading:
    """Compute the chart, then let Korkut Ata speak."""
    sb = get_user_supabase(auth.jwt_token)
    result = (
        sb.table("birth_profiles")
        .select("birth_datetime,latitude,longitude")
        .eq("id", str(payload.birth_profile_id))
        .limit(1)
        .execute()
    )
    if not result.data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Birth profile not found.")

    row = result.data[0]
    chart = compute_natal_chart(
        birth_dt=datetime.fromisoformat(row["birth_datetime"]),
        latitude=float(row["latitude"]),
        longitude=float(row["longitude"]),
    )
    narrative = await generate_reading(chart, focus=payload.focus)
    return Reading(
        birth_profile_id=payload.birth_profile_id,
        narrative=narrative,
        generated_at=datetime.now(timezone.utc),
        model=settings.anthropic_model,
    )
