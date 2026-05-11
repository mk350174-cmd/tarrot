"""
Chart endpoints — deterministic Yultuz computation through Swiss Ephemeris.

The chart is recomputed on demand from the birth profile fetched under RLS;
no chart data is persisted. The great wheel does not need a cache to turn.
"""
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import AuthContext, get_current_user
from core.supabase_client import get_user_supabase
from models.chart import NatalChart
from services.astronomy.chart import compute_natal_chart

router = APIRouter(prefix="/charts", tags=["charts"])


@router.get("/{profile_id}", response_model=NatalChart)
def get_chart_for_profile(
    profile_id: UUID,
    auth: AuthContext = Depends(get_current_user),
) -> NatalChart:
    """Weave the natal sky-map for a stored birth profile."""
    sb = get_user_supabase(auth.jwt_token)
    result = (
        sb.table("birth_profiles")
        .select("birth_datetime,latitude,longitude")
        .eq("id", str(profile_id))
        .limit(1)
        .execute()
    )
    if not result.data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Birth profile not found.")
    row = result.data[0]
    return compute_natal_chart(
        birth_dt=datetime.fromisoformat(row["birth_datetime"]),
        latitude=float(row["latitude"]),
        longitude=float(row["longitude"]),
    )
