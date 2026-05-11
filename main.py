from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import birth_profiles, charts, health, readings, rituals
from core.config import settings

app = FastAPI(
    title="Tarrot — The Sky-Reader",
    description="A Shamanic astrology service rooted in Turkic cosmological tradition.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_API_PREFIX = "/api/v1"
app.include_router(health.router, prefix=_API_PREFIX)
app.include_router(birth_profiles.router, prefix=_API_PREFIX)
app.include_router(charts.router, prefix=_API_PREFIX)
app.include_router(readings.router, prefix=_API_PREFIX)
app.include_router(rituals.router, prefix=_API_PREFIX)
