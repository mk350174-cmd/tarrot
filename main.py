from fastapi import FastAPI

from api.routes import health

app = FastAPI(
    title="Tarrot — The Sky-Reader",
    description="A Shamanic astrology service rooted in Turkic cosmological tradition.",
    version="0.1.0",
)

app.include_router(health.router)
