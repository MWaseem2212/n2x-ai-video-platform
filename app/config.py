from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    GROQ_API_KEY: str
    DATABASE_URL: str
    QDRANT_URL: str = "http://localhost:6333"  

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()