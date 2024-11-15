import pytest

from db.db_setup import SessionLocal
from repos.all_repositories import AllRepositories, get_repositories


@pytest.fixture(scope="session")
def database() -> AllRepositories:
    try:
        db = SessionLocal()
        yield get_repositories(db)

    finally:
        db.close()
