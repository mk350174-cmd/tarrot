"""
Birth Profile — the ancestral record sealed by Row-Level Security.

Each profile is the private sky-map of a seeker. RLS at the PostgreSQL
layer ensures no profile is read by any spirit other than its owner.
Do not bypass RLS by using the service-role key in user-facing code paths.
"""
import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID

from core.database import Base


class BirthProfileORM(Base):
    """ORM model. Row-Level Security is enforced at the PostgreSQL level."""

    __tablename__ = "birth_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    birth_datetime = Column(DateTime(timezone=True), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class BirthProfileCreate(BaseModel):
    name: str
    birth_datetime: datetime
    latitude: float
    longitude: float


class BirthProfileResponse(BaseModel):
    id: str
    name: str
    birth_datetime: datetime
    latitude: float
    longitude: float
    created_at: datetime

    model_config = {"from_attributes": True}
