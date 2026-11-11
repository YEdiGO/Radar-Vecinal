from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/radar_vecinal"
    secret_key: str = "cambia-esto"
    algorithm: str = "HS256"
    token_minutos: int = 60 * 8
    cors_origins: list[str] = ["http://localhost:4200"]

    max_reportes_dia: int = 10
    duracion_alerta_min: int = 30
    espera_entre_alertas_min: int = 10
    vida_media_dias: float = 15
    dias_sin_accion_critico: int = 15


settings = Settings()