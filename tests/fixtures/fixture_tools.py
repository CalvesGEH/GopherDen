import pytest

from tests.utils import randomword, random_tool

from backend.repos.all_repositories import AllRepositories
from backend.schema.tool import ToolCreate


@pytest.fixture(scope="function")
def unique_tool() -> ToolCreate:
    tool = random_tool()
    return ToolCreate(
        name=tool["name"] + " " + randomword(8),
        description=tool["description"]
    )