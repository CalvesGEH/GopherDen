from fastapi import APIRouter

from . import about

app_router = APIRouter(prefix="/app")

app_router.include_router(about.router, tags=["App: About"])