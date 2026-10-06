from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Tooly"
    database_url: str = "sqlite:///./tooly.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TOOLY_",
        extra="ignore",
    )


settings = Settings()
