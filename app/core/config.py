from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


    # ==========================
    # APP
    # ==========================

    APP_NAME: str = "Brain Study"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True



    # ==========================
    # CORS
    # ==========================

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://brain-study.vercel.app",
    ]



    # ==========================
    # DATABASE
    # ==========================

    DATABASE_URL: str



    # ==========================
    # JWT
    # ==========================

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080



    # ==========================
    # AI ROUTER
    # ==========================

    PRIMARY_AI_PROVIDER: str = "gemini"

    FALLBACK_AI_PROVIDER: str = "groq"



    # ==========================
    # AI LIMITS
    # ==========================

    AI_MAX_INPUT_CHARS: int = 12000

    AI_MAX_OUTPUT_TOKENS: int = 4096



    # ==========================
    # GROQ
    # ==========================

    GROQ_API_KEY: str | None = None

    GROQ_MODEL: str = (
        "llama-3.3-70b-versatile"
    )



    # ==========================
    # GEMINI
    # ==========================

    GEMINI_API_KEY: str | None = None

    GEMINI_MODEL: str = (
        "gemini-2.5-flash"
    )



@lru_cache
def get_settings() -> Settings:

    return Settings()



settings = get_settings()
