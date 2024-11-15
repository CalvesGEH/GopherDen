from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from backend.utils.logger import get_logger

from backend.schema import schema

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan_fn(_: FastAPI) -> AsyncGenerator[None, None]:
    """
    lifespan_fn controls the startup and shutdown of the FastAPI Application.
    This function is called when the FastAPI application starts and stops.

    See FastAPI documentation for more information:
      - https://fastapi.tiangolo.com/advanced/events/
    """
    logger.info("start: database initialization")
    import backend.db.init_db as init_db
    init_db.main()
    logger.info("end: database initialization")

    # logger.info("------APP SETTINGS------")
    # logger.info(
    #     settings.model_dump_json(
    #         indent=4,
    #         exclude={
    #             "SECRET",
    #             "SFTP_PASSWORD",
    #             "SFTP_USERNAME",
    #             "DB_URL",  # replace by DB_URL_PUBLIC for logs
    #             "DB_PROVIDER",
    #             "SMTP_USER",
    #             "SMTP_PASSWORD",
    #         },
    #     )
    # )

    yield

app = FastAPI(
    title="GopherDen",
    description="A simple web app to manage your household chores.",
    version="0.0.1b",
    lifespan=lifespan_fn,
)

# fix routes that would get their tags duplicated by use of @controller,
# leading to duplicate definitions in the openapi spec
for route in app.routes:
    logger.debug("Checking route: %s", route)
    if isinstance(route, APIRoute):
        route.tags = list(set(route.tags))

@app.get("/")
def homepage():
    return {"message": "Welcome to the homepage!!"}

def main():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=7877,
        log_level="debug",
        reload=True,
        reload_dirs=['./backend'],
        reload_excludes='*.log',
    )


if __name__ == "__main__":
    main()