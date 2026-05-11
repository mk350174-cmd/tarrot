from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Tarrot"

    # Supabase — RLS is the gatekeeper of the ancestral records
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_jwt_secret: str = ""  # for verifying user JWTs locally

    # AI
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-opus-4-7"

    # Swiss Ephemeris
    ephe_path: str = "./ephe"

    # CORS — the gate through which the steppe winds enter
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]


settings = Settings()
