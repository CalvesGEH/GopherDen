import pytest
from datetime import timedelta

from tests.utils import randomword, random_chore

from repos.all_repositories import AllRepositories
from schema.chore import ChoreCreate


@pytest.fixture(scope="function")
def unique_chore() -> ChoreCreate:
    chore = random_chore()
    return ChoreCreate(
        name=chore["name"] + " " + randomword(8),
        description=chore["description"],
        total_time=chore["total_time_minutes"] + "m",
        frequency_days=timedelta(days=int(chore["frequency_days"])),
    )