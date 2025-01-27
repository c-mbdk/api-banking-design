from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.api.v1.api import api_router as api_router_v1
from src.core.settings import get_app_settings
from src.db.database import get_database_client

settings = get_app_settings()


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    # Initialise db and create tables
    await get_database_client()
    yield
    # Shutdown


# Core App Instance
app = FastAPI(
    title=settings.TITLE,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.include_router(api_router_v1)
