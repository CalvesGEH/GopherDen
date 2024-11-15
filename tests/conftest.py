import contextlib
from collections.abc import Generator

from pytest import MonkeyPatch, fixture

mp = MonkeyPatch()
mp.setenv("PRODUCTION", "True")
mp.setenv("TESTING", "True")
mp.setenv("ALLOW_SIGNUP", "True")
from pathlib import Path

from fastapi.testclient import TestClient

from schema import schema

from main import app
from core import config
from db.db_setup import SessionLocal, generate_session
from db.init_db import main
from tests.fixtures import *

main()


def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@fixture(scope="session")
def api_client():
    app.dependency_overrides[generate_session] = override_get_db

    yield TestClient(app)

    with contextlib.suppress(Exception):
        settings = config.get_app_settings()
        settings.DB_PROVIDER.db_path.unlink()  # Handle SQLite Provider


@fixture(scope="session", autouse=True)
def global_cleanup() -> Generator[None, None, None]:
    """Purges the .temp directory used for testing"""
    yield None
    with contextlib.suppress(Exception):
        temp_dir = Path(__file__).parent / ".temp"

        if temp_dir.exists():
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)
