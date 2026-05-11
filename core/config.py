from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Tarrot"
    supabase_url: str = ""
    supabase_key: str = ""
    database_url: str = ""
    anthropic_api_key: str = ""
    ephe_path: str = "./ephe"  # Swiss Ephemeris data directory


settings = Settings()
