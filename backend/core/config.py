from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FarmSyn ERP"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///backend/farm.db"

    # Security
    SECRET_KEY: str = "CHANGE_THIS_TO_A_STRONG_SECRET"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()

