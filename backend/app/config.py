from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./agriflood.db"
    cache_ttl_minutes: int = 60
    open_meteo_timeout_seconds: int = 20
    gee_project_id: str = ""
    gee_enabled: bool = False
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @property
    def cors_list(self):
        return [x.strip() for x in self.cors_origins.split(',') if x.strip()]

settings = Settings()
