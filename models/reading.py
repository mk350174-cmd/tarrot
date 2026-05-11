"""
Reading Schemas — the woven narrative returned by the steppe oracle.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReadingRequest(BaseModel):
    birth_profile_id: UUID
    focus: str | None = None  # optional thematic focus: "love", "path", "ancestors"


class Reading(BaseModel):
    birth_profile_id: UUID
    narrative: str
    generated_at: datetime
    model: str
