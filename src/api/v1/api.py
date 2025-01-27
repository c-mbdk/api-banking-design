from fastapi import APIRouter

from src.api.v1.routers import (
    account,
    customer
)
from src.core.settings import get_app_settings

settings = get_app_settings()


api_router = APIRouter(prefix=settings.API_V1_STR)
api_router.include_router(customer.router)
api_router.include_router(account.router)
