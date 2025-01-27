import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from src.logger import logger

_APP_SETTINGS: Optional["AppSettings"] = None


class AppSettings:
    """Application settings."""

    def __init__(self) -> None:
        """
        Initialise application settings and load environment settings.
        """
        _load_configs()
        self.ENV_TYPE = os.getenv("ENV_TYPE", "production")
        self.DEBUG = os.getenv("DEBUG")
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.API_VERSION = os.getenv("API_VERSION")
        self.API_V1_STR = f"/api/{self.API_VERSION}"

    DEBUG: bool = os.getenv("DEBUG", "True").lower()
    TITLE: str = "BankingApp"
    ENV_TYPE: str = "dev"

    DATABASE_URL: str = None
    API_VERSION: str = None
    API_V1_STR: str = None


def _load_configs() -> None:
    current_dir = Path(__file__).resolve().parent
    env_dir = current_dir.parents[1] / ".env"
    load_dotenv(env_dir)
    logger.info("Environment variables loaded.")


def get_app_settings() -> AppSettings:
    """
    Retrieves the singleton AppSettings instance.

    Returns:
        AppSettings: Application settings instance.
    """
    global _APP_SETTINGS

    if _APP_SETTINGS is None:
        _APP_SETTINGS = AppSettings()
        logger.info("Created and initialised new AppSettings instance.")

    return _APP_SETTINGS
