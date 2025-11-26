from pydantic_settings import BaseSettings
from decimal import Decimal


class Settings(BaseSettings):
    EBAY_FEE_PERCENT: Decimal = Decimal("0.13")
    HANDLING_COST: Decimal = Decimal("2.00")
    GOOGLE_API_KEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()