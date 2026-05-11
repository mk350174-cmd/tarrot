"""
Birth Profile — the ancestral record sealed by Row-Level Security.

Each profile is the private sky-map of a seeker. RLS at the PostgreSQL
layer ensures no profile is read by any spirit other than its owner.
Never bypass RLS by using the service-role key in user-facing paths.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BirthProfileCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    birth_datetime: datetime
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)


class BirthProfile(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    birth_datetime: datetime
    latitude: float
    longitude: float
    created_at: datetime
