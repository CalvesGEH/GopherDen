from fastapi import APIRouter

from .app import app_router
from .users import user_router
from .chores import chore_router

api_router = APIRouter(prefix="/api")

api_router.include_router(app_router)
api_router.include_router(user_router)
api_router.include_router(chore_router)